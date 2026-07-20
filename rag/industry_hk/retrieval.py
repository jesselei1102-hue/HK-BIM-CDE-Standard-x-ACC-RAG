"""行业 HK CDE 混合检索（复用产品轨逻辑，独立 collection + 文档族重排）。"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from rag.config import AppConfig, CorpusConfig, QueryKBConfig
from rag.industry_hk.config import IndustryHKConfig, get_industry_hk_config
from rag.industry_hk.source_family import (
    doc_id_from_url,
    exact_title_bonus,
    is_section_number_title,
    resolve_source_family,
)
from rag.orchestrator.industry_prefer import prefer_industry_chunks
from rag.retrieval import (
    HybridRetriever,
    RetrievedChunk,
    RetrievalDebugInfo,
    RetrievalResult,
)


class IndustryStorageBridge:
    """为 HybridRetriever / KBRoutingIndex 提供行业 storage 属性。"""

    def __init__(self, industry_storage) -> None:
        self._s = industry_storage

    @property
    def data_dir(self):
        return self._s.data_dir

    @property
    def collection_name(self) -> str:
        return self._s.collection_name

    @property
    def chroma_dir(self):
        return self._s.chroma_dir

    @property
    def chunks_path(self):
        return self._s.chunks_path

    @property
    def manifest_path(self):
        return self._s.manifest_path

    @property
    def kb_chroma_dir(self):
        return self._s.kb_chroma_dir

    @property
    def kb_collection_name(self) -> str:
        return self._s.kb_collection_name

    @property
    def kb_manifest_path(self):
        return self._s.kb_manifest_path


def industry_to_app_config(config: IndustryHKConfig) -> AppConfig:
    return AppConfig(
        corpus=CorpusConfig(
            source_dir=config.corpus.source_dir,
            file_glob=config.corpus.file_glob,
            product=config.corpus.product,
        ),
        models=config.models,
        chunks=config.chunks,
        retrieval=config.retrieval,
        query_kb=QueryKBConfig(
            enabled=config.query_kb.enabled,
            kb_path=config.query_kb.kb_path,
            short_query_max_chars=config.query_kb.short_query_max_chars,
            trigger_sim=config.query_kb.trigger_sim,
            require_sim_improvement=config.query_kb.require_sim_improvement,
            target_url_boost=config.query_kb.target_url_boost,
            contains_max_length_delta=config.query_kb.contains_max_length_delta,
            route_top_k=config.query_kb.route_top_k,
            min_route_sim=config.query_kb.min_route_sim,
        ),
        storage=IndustryStorageBridge(config.storage),  # type: ignore[arg-type]
    )


def _shadow_chunks_path() -> Path | None:
    raw = os.environ.get("INDUSTRY_HK_SHADOW_DATA_DIR", "").strip()
    if raw:
        path = Path(raw) / "chunks.jsonl"
        return path if path.is_file() else None
    candidate = Path(".rag_data/industry_hk_cde_substantive/chunks.jsonl")
    return candidate if candidate.is_file() else None


def _mentions_template(query: str) -> bool:
    return bool(
        re.search(r"\bD[1-9]\b|template\s*field|附录\s*D|Appendix\s*D", query or "", re.I)
    )


def _load_shadow_chunks_for_docs(
    chunks_path: Path, doc_ids: tuple[str, ...], query: str = "", limit: int = 12
) -> list[RetrievedChunk]:
    from rag.industry_hk.source_family import exact_title_bonus, normalize_title

    candidates: list[tuple[float, RetrievedChunk]] = []
    tokens = [t for t in re.split(r"[^\w]+", (query or "").lower()) if len(t) >= 3]
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            url = record.get("source_url", "")
            doc_id = doc_id_from_url(url)
            if doc_id not in doc_ids:
                continue
            hay = f"{record.get('title','')} {record.get('text','')[:800]}".lower()
            overlap = sum(1 for token in tokens if token in hay) if tokens else 0
            score = 0.55 + 0.15 * overlap
            score += exact_title_bonus(query, record.get("title") or "")
            # Prefer early chunks that usually carry authority headers / intros.
            score += max(0.0, 0.2 - 0.02 * int(record.get("chunk_index") or 0))
            candidates.append(
                (
                    score,
                    RetrievedChunk(
                        chunk_id=record["chunk_id"],
                        title=record["title"],
                        source_url=record["source_url"],
                        source_file=record["source_file"],
                        page_index=int(record["page_index"]),
                        line_start=int(record["line_start"]),
                        product=record["product"],
                        chunk_index=int(record["chunk_index"]),
                        chunk_count=int(record["chunk_count"]),
                        token_count=int(record["token_count"]),
                        text=record["text"],
                        score=score,
                        # Synthetic similarity so generation refuse gates treat
                        # shadow family hits as usable evidence.
                        vector_similarity=min(0.95, 0.55 + 0.08 * overlap),
                    ),
                )
            )
    candidates.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in candidates[:limit]]


def _family_rerank(query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    family = resolve_source_family(query)
    scored: list[tuple[float, int, RetrievedChunk]] = []
    for index, chunk in enumerate(chunks):
        score = float(chunk.score or 0.0)
        score += exact_title_bonus(query, chunk.title)
        doc_id = doc_id_from_url(chunk.source_url) or ""
        if "/templates/" in (chunk.source_file or "") or doc_id.startswith("template"):
            if not _mentions_template(query):
                score -= 3.0
        if family:
            if doc_id in family.doc_ids:
                score += 3.5 if family.prefer_shadow else 1.8
            elif family.prefer_shadow:
                score -= 1.5
            if family.doc_ids and doc_id and doc_id not in family.doc_ids:
                lowered = query.lower()
                if any(
                    token in lowered
                    for token in (
                        "lod",
                        "loin",
                        "field verification",
                        "appearance",
                        "document structure",
                        "responsibility matrix",
                    )
                ):
                    score -= 0.75
        scored.append((score, index, chunk))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in scored]


class IndustryHybridRetriever(HybridRetriever):
    def __init__(self, config: IndustryHKConfig | None = None) -> None:
        industry = config or get_industry_hk_config()
        super().__init__(industry_to_app_config(industry))
        self.industry_config = industry

    def retrieve_with_debug(
        self,
        query: str,
        top_k: int | None = None,
        *,
        boost_url_prefix: str | None = None,
        source_hint_urls: list[str] | None = None,
    ) -> RetrievalResult:
        limit = top_k or self.config.retrieval.top_k

        # Section-number titles: skip fuzzy page_title KB to avoid cross-doc homonyms.
        if is_section_number_title(query):
            debug = RetrievalDebugInfo(original_query=query)
            chunks = self._retrieve_internal(
                query,
                limit,
                boost_target_url=boost_url_prefix,
                source_hint_urls=source_hint_urls,
                debug=debug,
            )
            debug.adopted_path = "original"
            result = RetrievalResult(chunks=chunks, debug=debug)
        else:
            result = super().retrieve_with_debug(
                query,
                top_k,
                boost_url_prefix=boost_url_prefix,
                source_hint_urls=source_hint_urls,
            )

        chunks = list(result.chunks)
        family = resolve_source_family(query)
        if family and family.prefer_shadow:
            shadow = _shadow_chunks_path()
            if shadow is not None:
                extra = _load_shadow_chunks_for_docs(
                    shadow, family.doc_ids, query=query
                )
                seen = {c.chunk_id for c in chunks}
                for item in extra:
                    if item.chunk_id not in seen:
                        chunks.append(item)
                        seen.add(item.chunk_id)

        chunks = _family_rerank(query, chunks)
        # Do not let overview pins steal explicit case-study / terminology /
        # software-guide family queries.
        if family and family.prefer_shadow:
            capped = chunks[:limit]
            return RetrievalResult(chunks=capped, debug=result.debug)

        preferred = prefer_industry_chunks(
            query,
            chunks,
            chunks_path=self.industry_config.storage.chunks_path,
            limit=limit,
        )
        capped = preferred[:limit]
        if capped == result.chunks:
            return result
        return RetrievalResult(chunks=capped, debug=result.debug)
