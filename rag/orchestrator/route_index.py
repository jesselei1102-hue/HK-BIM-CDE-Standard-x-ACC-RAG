"""Orchestrator 语义路由向量索引（track / capability 例句，不含答案正文）。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import chromadb
import ollama
from chromadb.errors import NotFoundError

from rag.config import AppConfig, get_config

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RouteExemplar:
    route_id: str
    text: str
    label_type: str  # capability | capability_null | track_signal | out_of_domain
    label: str
    hint_query: str = ""
    lang: str = "mixed"


@dataclass(frozen=True)
class RouteMatch:
    route_id: str
    text: str
    label_type: str
    label: str
    hint_query: str
    similarity: float


@dataclass(frozen=True)
class RouteIndexBuildResult:
    record_count: int
    collection_name: str
    chroma_dir: Path


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def build_route_exemplars(routes_path: Path) -> list[RouteExemplar]:
    """从 orchestrator_routes.jsonl 展开 canonical + aliases。"""
    records: list[RouteExemplar] = []
    seen: set[tuple[str, str]] = set()

    def add(
        *,
        route_id: str,
        text: str,
        label_type: str,
        label: str,
        hint_query: str = "",
        lang: str = "mixed",
    ) -> None:
        normalized = text.strip()
        if not normalized:
            return
        key = (label_type, label, normalized.casefold())
        if key in seen:
            return
        seen.add(key)
        records.append(
            RouteExemplar(
                route_id=route_id,
                text=normalized,
                label_type=label_type,
                label=label,
                hint_query=hint_query.strip(),
                lang=lang,
            )
        )

    for row in _read_jsonl(routes_path):
        route_id = row["route_id"]
        label_type = row["label_type"]
        label = row.get("label") or ""
        hint = row.get("hint_query") or ""
        lang = row.get("lang") or "mixed"
        add(
            route_id=route_id,
            text=row["text"],
            label_type=label_type,
            label=label,
            hint_query=hint,
            lang=lang,
        )
        for alias in row.get("aliases") or []:
            add(
                route_id=f"{route_id}__alias",
                text=alias,
                label_type=label_type,
                label=label,
                hint_query=hint,
                lang=lang,
            )
    return records


class OrchestratorRouteIndex:
    """本地 embedding + Chroma，仅用于 track/capability 路由。"""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or get_config()
        self.router_config = self.config.semantic_router
        self._chroma = chromadb.PersistentClient(
            path=str(self.config.storage.orchestrator_chroma_dir)
        )
        self._ollama = ollama.Client(
            host=self.config.models.ollama_host,
            timeout=self.config.models.request_timeout_seconds,
            trust_env=False,
        )
        self._collection = None
        self._try_load_collection()

    @property
    def available(self) -> bool:
        return self._collection is not None

    def _try_load_collection(self) -> None:
        try:
            self._collection = self._chroma.get_collection(
                self.config.storage.orchestrator_collection_name
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
        routes_path: Path | None = None,
        rebuild: bool = False,
    ) -> RouteIndexBuildResult:
        routes_path = routes_path or self.router_config.routes_path
        records = build_route_exemplars(routes_path)
        name = self.config.storage.orchestrator_collection_name
        chroma_dir = self.config.storage.orchestrator_chroma_dir

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
                    "purpose": "orchestrator_route_only",
                },
            )

        existing_ids = set(collection.get(include=[])["ids"])
        target_ids: set[str] = set()
        pending: list[RouteExemplar] = []
        for index, record in enumerate(records):
            record_key = f"{record.label_type}:{record.label}:{index}"
            target_ids.add(record_key)
            if record_key not in existing_ids:
                pending.append(
                    RouteExemplar(
                        route_id=record_key,
                        text=record.text,
                        label_type=record.label_type,
                        label=record.label,
                        hint_query=record.hint_query,
                        lang=record.lang,
                    )
                )

        stale_ids = list(existing_ids - target_ids)
        if stale_ids:
            collection.delete(ids=stale_ids)

        batch_size = self.config.models.embedding_batch_size
        for start in range(0, len(pending), batch_size):
            batch = pending[start : start + batch_size]
            embeddings = self._embed([item.text for item in batch])
            collection.upsert(
                ids=[item.route_id for item in batch],
                embeddings=embeddings,
                documents=[item.text for item in batch],
                metadatas=[
                    {
                        "label_type": item.label_type,
                        "label": item.label,
                        "hint_query": item.hint_query,
                        "lang": item.lang,
                        "source_text": item.text[:200],
                    }
                    for item in batch
                ],
            )

        self._collection = collection
        manifest = {
            "record_count": len(records),
            "collection_name": name,
            "embedding_model": self.config.models.embedding_model,
            "routes_path": str(routes_path),
        }
        manifest_path = self.config.storage.orchestrator_manifest_path
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return RouteIndexBuildResult(
            record_count=len(records),
            collection_name=name,
            chroma_dir=chroma_dir,
        )

    def search(self, query: str, top_k: int | None = None) -> list[RouteMatch]:
        if not self.available or not query.strip():
            return []

        limit = top_k or self.router_config.route_top_k
        embedding = self._embed([query])[0]
        result = self._collection.query(  # type: ignore[union-attr]
            query_embeddings=[embedding],
            n_results=min(limit * 4, 40),
            include=["documents", "distances", "metadatas"],
        )

        matches: list[RouteMatch] = []
        for doc, distance, meta in zip(
            result["documents"][0],
            result["distances"][0],
            result["metadatas"][0],
        ):
            similarity = 1.0 - float(distance)
            matches.append(
                RouteMatch(
                    route_id=meta.get("label_type", "") + ":" + meta.get("label", ""),
                    text=doc,
                    label_type=meta["label_type"],
                    label=meta["label"],
                    hint_query=meta.get("hint_query") or "",
                    similarity=similarity,
                )
            )
        matches.sort(key=lambda item: item.similarity, reverse=True)
        return matches[:limit]
