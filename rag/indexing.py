"""使用 Ollama embedding 将 chunks 增量写入本地 Chroma。"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import chromadb
import ollama
from chromadb.errors import NotFoundError

from .chunking import Chunk, export_chunks
from .config import AppConfig


@dataclass(frozen=True)
class IndexingResult:
    total_chunks: int
    embedded_chunks: int
    unchanged_chunks: int
    deleted_chunks: int
    vector_dimension: int


def _batches(items: list[Any], size: int) -> list[list[Any]]:
    return [items[start : start + size] for start in range(0, len(items), size)]


def _metadata(chunk: Chunk) -> dict[str, str | int]:
    return {
        "title": chunk.title,
        "source_url": chunk.source_url,
        "source_file": chunk.source_file,
        "page_index": chunk.page_index,
        "line_start": chunk.line_start,
        "product": chunk.product,
        "document_hash": chunk.document_hash,
        "chunk_index": chunk.chunk_index,
        "chunk_count": chunk.chunk_count,
        "token_count": chunk.token_count,
    }


def _get_collection(
    client: chromadb.PersistentClient,
    config: AppConfig,
    rebuild: bool,
) -> Any:
    name = config.storage.collection_name
    try:
        collection = client.get_collection(name)
        exists = True
    except NotFoundError:
        collection = None
        exists = False

    if exists and rebuild:
        client.delete_collection(name)
        collection = None
        exists = False

    if not exists:
        return client.create_collection(
            name=name,
            metadata={
                "embedding_model": config.models.embedding_model,
                "hnsw:space": "cosine",
            },
        )

    indexed_model = (collection.metadata or {}).get("embedding_model")
    if indexed_model != config.models.embedding_model:
        raise ValueError(
            "Chroma collection 使用的 embedding 模型为 "
            f"{indexed_model!r}，当前配置为 {config.models.embedding_model!r}；"
            "请使用 --rebuild 重建索引"
        )
    return collection


def _write_artifacts(
    chunks: list[Chunk],
    config: AppConfig,
    result: IndexingResult,
) -> None:
    config.storage.data_dir.mkdir(parents=True, exist_ok=True)

    chunks_temp = config.storage.chunks_path.with_suffix(".jsonl.tmp")
    export_chunks(chunks, chunks_temp)
    chunks_temp.replace(config.storage.chunks_path)

    manifest = {
        "version": 1,
        "created_at": datetime.now(UTC).isoformat(),
        "source_dir": str(config.corpus.source_dir),
        "file_glob": config.corpus.file_glob,
        "embedding_model": config.models.embedding_model,
        "collection_name": config.storage.collection_name,
        "chunk_config": asdict(config.chunks),
        "result": asdict(result),
    }
    manifest_temp = config.storage.manifest_path.with_suffix(".json.tmp")
    manifest_temp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    manifest_temp.replace(config.storage.manifest_path)


def index_chunks(
    chunks: list[Chunk],
    config: AppConfig,
    rebuild: bool = False,
) -> IndexingResult:
    if not chunks:
        raise ValueError("没有可索引的 chunks")

    config.storage.chroma_dir.mkdir(parents=True, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=str(config.storage.chroma_dir))
    collection = _get_collection(chroma_client, config, rebuild)
    ollama_client = ollama.Client(
        host=config.models.ollama_host,
        timeout=config.models.request_timeout_seconds,
        trust_env=False,
    )

    existing_ids = set(collection.get(include=[])["ids"])
    chunks_by_id = {chunk.chunk_id: chunk for chunk in chunks}
    desired_ids = set(chunks_by_id)
    stale_ids = sorted(existing_ids - desired_ids)
    unchanged_ids = sorted(existing_ids & desired_ids)
    new_chunks = [chunk for chunk in chunks if chunk.chunk_id not in existing_ids]

    for batch in _batches(stale_ids, 500):
        collection.delete(ids=batch)

    # 内容相同时无需重新 embedding，但刷新行号等可能变化的元数据。
    for batch_ids in _batches(unchanged_ids, 500):
        batch_chunks = [chunks_by_id[chunk_id] for chunk_id in batch_ids]
        collection.update(
            ids=batch_ids,
            metadatas=[_metadata(chunk) for chunk in batch_chunks],
        )

    vector_dimension = 0
    embedded = 0
    embedding_batches = _batches(
        new_chunks,
        config.models.embedding_batch_size,
    )
    for batch_number, batch in enumerate(embedding_batches, start=1):
        response = ollama_client.embed(
            model=config.models.embedding_model,
            input=[chunk.text for chunk in batch],
        )
        embeddings = response.embeddings
        if len(embeddings) != len(batch):
            raise RuntimeError(
                f"Ollama 返回 {len(embeddings)} 个向量，但请求了 {len(batch)} 个"
            )
        dimensions = {len(vector) for vector in embeddings}
        if len(dimensions) != 1:
            raise RuntimeError("同一 embedding 批次返回了不同向量维度")
        vector_dimension = dimensions.pop()
        collection.upsert(
            ids=[chunk.chunk_id for chunk in batch],
            embeddings=embeddings,
            documents=[chunk.text for chunk in batch],
            metadatas=[_metadata(chunk) for chunk in batch],
        )
        embedded += len(batch)
        print(
            f"  Embedding 批次 {batch_number}/{len(embedding_batches)}："
            f"{embedded}/{len(new_chunks)}"
        )

    if not new_chunks and chunks:
        sample = collection.get(ids=[chunks[0].chunk_id], include=["embeddings"])
        stored_embeddings = sample.get("embeddings")
        if stored_embeddings is not None and len(stored_embeddings):
            vector_dimension = len(stored_embeddings[0])

    indexed_count = collection.count()
    if indexed_count != len(chunks):
        raise RuntimeError(
            f"Chroma 校验失败：预期 {len(chunks)}，实际 {indexed_count}"
        )

    result = IndexingResult(
        total_chunks=len(chunks),
        embedded_chunks=len(new_chunks),
        unchanged_chunks=len(unchanged_ids),
        deleted_chunks=len(stale_ids),
        vector_dimension=vector_dimension,
    )
    _write_artifacts(chunks, config, result)
    return result
