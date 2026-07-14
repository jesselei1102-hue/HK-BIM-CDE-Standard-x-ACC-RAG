"""KB 路由索引：标题/术语的独立向量库，仅用于召回路由，不进入生成上下文。"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb
import ollama
from chromadb.errors import NotFoundError

from .config import PROJECT_ROOT, AppConfig, QueryKBConfig, get_config

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def _normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text.strip())
    text = re.sub(r"\s+", "", text)
    return text.lower()


def _is_chinese(text: str) -> bool:
    return bool(_CJK_RE.search(text))


@dataclass(frozen=True)
class RouteRecord:
    record_id: str
    text: str
    source_type: str  # kb_alias | kb_title | kb_canonical | page_title
    entry_id: str
    target_title: str
    target_url: str
    target_guid: str
    rewrite_query_zh: str
    rewrite_query_en: str


@dataclass(frozen=True)
class RouteCandidate:
    entry_id: str
    target_title: str
    target_url: str
    target_guid: str
    matched_term: str
    source_type: str
    similarity: float
    rewrite_query_zh: str
    rewrite_query_en: str


def _record_id(entry_id: str, source_type: str, text: str) -> str:
    digest = hashlib.sha256(f"{entry_id}:{source_type}:{text}".encode()).hexdigest()[:16]
    return f"{entry_id}:{source_type}:{digest}"


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_route_records(
    kb_path: Path,
    pages_index_path: Path | None = None,
) -> list[RouteRecord]:
    """从 query_kb 与 pages_index 生成路由索引记录（仅标题/术语，无正文）。"""

    records: list[RouteRecord] = []
    seen: set[str] = set()

    def add(
        *,
        text: str,
        source_type: str,
        entry_id: str,
        target_title: str,
        target_url: str,
        target_guid: str,
        rewrite_query_zh: str,
        rewrite_query_en: str,
    ) -> None:
        text = text.strip()
        if not text:
            return
        key = _normalize_text(text)
        if key in seen:
            return
        seen.add(key)
        records.append(
            RouteRecord(
                record_id=_record_id(entry_id, source_type, text),
                text=text,
                source_type=source_type,
                entry_id=entry_id,
                target_title=target_title,
                target_url=target_url,
                target_guid=target_guid,
                rewrite_query_zh=rewrite_query_zh,
                rewrite_query_en=rewrite_query_en,
            )
        )

    for row in _read_jsonl(kb_path):
        if row.get("status") != "approved":
            continue
        entry_id = row["id"]
        target_title = row["target_title"]
        target_url = row["target_url"]
        target_guid = row["target_guid"]
        rewrite_zh = row.get("canonical_query_zh", "")
        rewrite_en = row.get("canonical_query_en", "")

        add(
            text=target_title,
            source_type="kb_title",
            entry_id=entry_id,
            target_title=target_title,
            target_url=target_url,
            target_guid=target_guid,
            rewrite_query_zh=rewrite_zh or target_title,
            rewrite_query_en=rewrite_en or target_title,
        )
        if rewrite_zh:
            add(
                text=rewrite_zh,
                source_type="kb_canonical",
                entry_id=entry_id,
                target_title=target_title,
                target_url=target_url,
                target_guid=target_guid,
                rewrite_query_zh=rewrite_zh,
                rewrite_query_en=rewrite_en or rewrite_zh,
            )
        if rewrite_en:
            add(
                text=rewrite_en,
                source_type="kb_canonical",
                entry_id=entry_id,
                target_title=target_title,
                target_url=target_url,
                target_guid=target_guid,
                rewrite_query_zh=rewrite_zh or rewrite_en,
                rewrite_query_en=rewrite_en,
            )
        for alias in row.get("aliases", []):
            add(
                text=alias,
                source_type="kb_alias",
                entry_id=entry_id,
                target_title=target_title,
                target_url=target_url,
                target_guid=target_guid,
                rewrite_query_zh=rewrite_zh or alias,
                rewrite_query_en=rewrite_en or alias,
            )

    if pages_index_path and pages_index_path.is_file():
        for page in _read_jsonl(pages_index_path):
            guid = page.get("guid") or page.get("section_id") or page.get("source_url", "")
            title = page["title"]
            target_url = page.get("source_url", "")
            if not guid or not title:
                continue
            entry_id = f"page:{guid}"
            rewrite_zh = title if _is_chinese(title) else f"{title} 怎么操作"
            rewrite_en = title if not _is_chinese(title) else f"How do I use {title}"
            add(
                text=title,
                source_type="page_title",
                entry_id=entry_id,
                target_title=title,
                target_url=target_url,
                target_guid=guid,
                rewrite_query_zh=rewrite_zh,
                rewrite_query_en=rewrite_en,
            )

    return records


@dataclass(frozen=True)
class IndexBuildResult:
    record_count: int
    collection_name: str
    chroma_dir: Path


class KBRoutingIndex:
    """磁盘上的标题/术语向量索引；查询只返回 Top-K 候选元数据，不含文档正文。"""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or get_config()
        self.kb_config: QueryKBConfig = self.config.query_kb
        self._chroma = chromadb.PersistentClient(
            path=str(self.config.storage.kb_chroma_dir)
        )
        self._ollama = ollama.Client(
            host=self.config.models.ollama_host,
            timeout=self.config.models.request_timeout_seconds,
            trust_env=False,
        )
        self._collection = None
        self._records_by_id: dict[str, RouteRecord] = {}
        self._try_load_collection()

    @property
    def available(self) -> bool:
        return self._collection is not None

    def _try_load_collection(self) -> None:
        try:
            self._collection = self._chroma.get_collection(
                self.config.storage.kb_collection_name
            )
        except NotFoundError:
            self._collection = None

    def _embed(self, texts: list[str]) -> list[list[float]]:
        response = self._ollama.embed(
            model=self.config.models.embedding_model,
            input=texts,
        )
        return response.embeddings

    def build(
        self,
        *,
        kb_path: Path | None = None,
        pages_index_path: Path | None = None,
        rebuild: bool = False,
    ) -> IndexBuildResult:
        kb_path = kb_path or self.kb_config.kb_path
        pages_index_path = pages_index_path or (
            PROJECT_ROOT / "knowledge" / "research" / "pages_index.jsonl"
        )

        records = build_route_records(kb_path, pages_index_path)
        self._records_by_id = {record.record_id: record for record in records}

        name = self.config.storage.kb_collection_name
        if rebuild:
            try:
                self._chroma.delete_collection(name)
            except (NotFoundError, ValueError):
                pass

        try:
            collection = self._chroma.get_collection(name)
            if rebuild:
                raise NotFoundError()
        except NotFoundError:
            collection = self._chroma.create_collection(
                name=name,
                metadata={
                    "embedding_model": self.config.models.embedding_model,
                    "hnsw:space": "cosine",
                    "purpose": "kb_route_only",
                },
            )

        existing_ids = set(collection.get(include=[])["ids"])
        target_ids = {record.record_id for record in records}
        stale_ids = list(existing_ids - target_ids)
        if stale_ids:
            collection.delete(ids=stale_ids)

        pending = [record for record in records if record.record_id not in existing_ids]
        batch_size = self.config.models.embedding_batch_size
        for start in range(0, len(pending), batch_size):
            batch = pending[start : start + batch_size]
            embeddings = self._embed([item.text for item in batch])
            collection.upsert(
                ids=[item.record_id for item in batch],
                embeddings=embeddings,
                documents=[item.text for item in batch],
                metadatas=[
                    {
                        "source_type": item.source_type,
                        "entry_id": item.entry_id,
                        "target_title": item.target_title,
                        "target_url": item.target_url,
                        "target_guid": item.target_guid,
                        "rewrite_query_zh": item.rewrite_query_zh,
                        "rewrite_query_en": item.rewrite_query_en,
                    }
                    for item in batch
                ],
            )

        self._collection = collection
        manifest = {
            "record_count": len(records),
            "collection_name": name,
            "embedding_model": self.config.models.embedding_model,
        }
        manifest_path = self.config.storage.kb_manifest_path
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

        return IndexBuildResult(
            record_count=len(records),
            collection_name=name,
            chroma_dir=self.config.storage.kb_chroma_dir,
        )

    def search(self, query: str, top_k: int | None = None) -> list[RouteCandidate]:
        if not self.available or not query.strip():
            return []

        limit = top_k or self.kb_config.route_top_k
        embedding = self._embed([query])[0]
        result = self._collection.query(  # type: ignore[union-attr]
            query_embeddings=[embedding],
            n_results=min(limit * 3, 20),
            include=["documents", "distances", "metadatas"],
        )

        best_by_entry: dict[str, RouteCandidate] = {}
        for doc, distance, meta in zip(
            result["documents"][0],
            result["distances"][0],
            result["metadatas"][0],
        ):
            similarity = 1.0 - float(distance)
            entry_id = meta["entry_id"]
            candidate = RouteCandidate(
                entry_id=entry_id,
                target_title=meta["target_title"],
                target_url=meta["target_url"],
                target_guid=meta["target_guid"],
                matched_term=doc,
                source_type=meta["source_type"],
                similarity=similarity,
                rewrite_query_zh=meta["rewrite_query_zh"],
                rewrite_query_en=meta["rewrite_query_en"],
            )
            current = best_by_entry.get(entry_id)
            if current is None or candidate.similarity > current.similarity:
                best_by_entry[entry_id] = candidate

        ranked = sorted(
            best_by_entry.values(),
            key=lambda item: item.similarity,
            reverse=True,
        )
        return ranked[:limit]
