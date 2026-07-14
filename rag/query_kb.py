"""查询路由：标题/术语索引 Top-K → 受控改写 → 正文 RAG。

知识库不进入生成 prompt，仅占用磁盘索引与极小的候选元数据。
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from .config import AppConfig, QueryKBConfig, get_config
from .kb_index import KBRoutingIndex, RouteCandidate


_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


@dataclass(frozen=True)
class KBEntry:
    id: str
    topic: str
    aliases: tuple[str, ...]
    canonical_query_zh: str
    canonical_query_en: str
    target_title: str
    target_url: str
    target_guid: str
    entry_type: str
    evidence: str
    external_sources: tuple[str, ...]
    status: str


@dataclass(frozen=True)
class RouteDecision:
    """受控改写结果：只含路由元数据，无文档正文。"""

    entry_id: str
    target_title: str
    target_url: str
    target_guid: str
    rewritten_query: str
    matched_term: str
    source_type: str
    similarity: float
    reason: str  # exact_term | vector_top1 | alias_fallback


def normalize_query(text: str) -> str:
    text = unicodedata.normalize("NFKC", text.strip())
    text = re.sub(r"\s+", "", text)
    return text.lower()


def is_chinese_query(text: str) -> bool:
    return bool(_CJK_RE.search(text))


def load_kb_entries(path: Path) -> list[KBEntry]:
    if not path.is_file():
        return []
    entries: list[KBEntry] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("status") != "approved":
                continue
            entries.append(
                KBEntry(
                    id=row["id"],
                    topic=row["topic"],
                    aliases=tuple(row.get("aliases", [])),
                    canonical_query_zh=row.get("canonical_query_zh", ""),
                    canonical_query_en=row.get("canonical_query_en", ""),
                    target_title=row["target_title"],
                    target_url=row["target_url"],
                    target_guid=row["target_guid"],
                    entry_type=row.get("entry_type", "how_to"),
                    evidence=row.get("evidence", ""),
                    external_sources=tuple(row.get("external_sources", [])),
                    status=row["status"],
                )
            )
    return entries


def rewrite_from_candidate(query: str, candidate: RouteCandidate) -> str:
    if is_chinese_query(query) and candidate.rewrite_query_zh:
        return candidate.rewrite_query_zh
    if candidate.rewrite_query_en:
        return candidate.rewrite_query_en
    return candidate.rewrite_query_zh or candidate.target_title


class KBRouter:
    """短句召回路由器：索引检索 + 确定性改写，零生成 token。"""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or get_config()
        self.kb_config: QueryKBConfig = self.config.query_kb
        self.entries = load_kb_entries(self.kb_config.kb_path)
        self.entries_by_id = {entry.id: entry for entry in self.entries}
        self._alias_index: list[tuple[str, KBEntry, str]] = []
        for entry in self.entries:
            for alias in entry.aliases:
                normalized = normalize_query(alias)
                if normalized:
                    self._alias_index.append((normalized, entry, alias))
        self._alias_index.sort(key=lambda item: len(item[0]), reverse=True)
        self._index = KBRoutingIndex(self.config)

    @property
    def enabled(self) -> bool:
        return self.kb_config.enabled and (
            self._index.available or bool(self.entries)
        )

    def search_candidates(self, query: str) -> list[RouteCandidate]:
        if not self.enabled:
            return []
        if self._index.available:
            return self._index.search(query, top_k=self.kb_config.route_top_k)
        return self._alias_candidates(query)

    def _alias_candidates(self, query: str) -> list[RouteCandidate]:
        normalized = normalize_query(query)
        results: list[RouteCandidate] = []
        for alias_norm, entry, alias_raw in self._alias_index:
            if normalized == alias_norm or (
                len(normalized) <= self.kb_config.short_query_max_chars
                and alias_norm in normalized
            ):
                results.append(
                    RouteCandidate(
                        entry_id=entry.id,
                        target_title=entry.target_title,
                        target_url=entry.target_url,
                        target_guid=entry.target_guid,
                        matched_term=alias_raw,
                        source_type="kb_alias",
                        similarity=1.0 if normalized == alias_norm else 0.9,
                        rewrite_query_zh=entry.canonical_query_zh,
                        rewrite_query_en=entry.canonical_query_en,
                    )
                )
                break
        return results[: self.kb_config.route_top_k]

    def controlled_rewrite(
        self,
        query: str,
        candidates: list[RouteCandidate],
    ) -> RouteDecision | None:
        if not candidates:
            return None

        normalized = normalize_query(query)
        for candidate in candidates:
            if normalize_query(candidate.matched_term) == normalized:
                return RouteDecision(
                    entry_id=candidate.entry_id,
                    target_title=candidate.target_title,
                    target_url=candidate.target_url,
                    target_guid=candidate.target_guid,
                    rewritten_query=rewrite_from_candidate(query, candidate),
                    matched_term=candidate.matched_term,
                    source_type=candidate.source_type,
                    similarity=candidate.similarity,
                    reason="exact_term",
                )

        best = candidates[0]
        if best.similarity < self.kb_config.min_route_sim:
            return None

        return RouteDecision(
            entry_id=best.entry_id,
            target_title=best.target_title,
            target_url=best.target_url,
            target_guid=best.target_guid,
            rewritten_query=rewrite_from_candidate(query, best),
            matched_term=best.matched_term,
            source_type=best.source_type,
            similarity=best.similarity,
            reason="vector_top1",
        )

    def should_route(
        self,
        query: str,
        top1_sim: float | None,
        top1_url: str | None = None,
    ) -> bool:
        if not self.enabled:
            return False
        if len(normalize_query(query)) > self.kb_config.short_query_max_chars:
            return False

        normalized = normalize_query(query)
        question_prefixes = ("如何", "怎么", "怎样", "what", "how", "when", "where")
        if any(normalized.startswith(prefix) for prefix in question_prefixes):
            if len(query.strip()) > self.kb_config.short_query_max_chars:
                return False

        candidates = self.search_candidates(query)
        if not candidates:
            return False

        decision = self.controlled_rewrite(query, candidates)
        if decision is None:
            return False

        if top1_sim is not None and top1_sim >= self.kb_config.trigger_sim:
            if not top1_url or top1_url == decision.target_url:
                return False
        if top1_url and top1_url != decision.target_url:
            return True
        if top1_sim is not None and top1_sim < self.kb_config.trigger_sim:
            return True
        return False

    def route(self, query: str) -> tuple[list[RouteCandidate], RouteDecision | None]:
        candidates = self.search_candidates(query)
        decision = self.controlled_rewrite(query, candidates)
        return candidates, decision


# 兼容旧接口名
QueryKB = KBRouter

KBMatch = RouteDecision
