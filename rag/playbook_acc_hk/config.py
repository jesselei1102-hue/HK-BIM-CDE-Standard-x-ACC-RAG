"""Playbook 配置。"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from rag.config import (
    ChunkConfig,
    ModelConfig,
    PROJECT_ROOT,
    RetrievalConfig,
    _env_float,
    _env_int,
    _env_path,
)

from .paths import (
    PLAYBOOK_CHROMA_DIR,
    PLAYBOOK_CHUNKS_PATH,
    PLAYBOOK_COLLECTION_NAME,
    PLAYBOOK_CORPUS_DIR,
    PLAYBOOK_KB_CHROMA_DIR,
    PLAYBOOK_KB_COLLECTION_NAME,
    PLAYBOOK_KB_MANIFEST_PATH,
    PLAYBOOK_MANIFEST_PATH,
    PLAYBOOK_QUERY_KB_PATH,
    PLAYBOOK_RAG_DATA_DIR,
)


@dataclass(frozen=True)
class PlaybookCorpusConfig:
    source_dir: Path = PLAYBOOK_CORPUS_DIR
    file_glob: str = "*.md"
    product: str = "playbook_acc_hk"


@dataclass(frozen=True)
class PlaybookQueryKBConfig:
    enabled: bool = True
    kb_path: Path = PLAYBOOK_QUERY_KB_PATH
    short_query_max_chars: int = 24
    trigger_sim: float = 0.52
    require_sim_improvement: bool = True
    target_url_boost: float = 0.25
    contains_max_length_delta: int = 6
    route_top_k: int = 5
    min_route_sim: float = 0.40


@dataclass(frozen=True)
class PlaybookStorageConfig:
    data_dir: Path = PLAYBOOK_RAG_DATA_DIR
    collection_name: str = PLAYBOOK_COLLECTION_NAME

    @property
    def chroma_dir(self) -> Path:
        return PLAYBOOK_CHROMA_DIR

    @property
    def chunks_path(self) -> Path:
        return PLAYBOOK_CHUNKS_PATH

    @property
    def manifest_path(self) -> Path:
        return PLAYBOOK_MANIFEST_PATH

    @property
    def kb_chroma_dir(self) -> Path:
        return PLAYBOOK_KB_CHROMA_DIR

    @property
    def kb_collection_name(self) -> str:
        return PLAYBOOK_KB_COLLECTION_NAME

    @property
    def kb_manifest_path(self) -> Path:
        return PLAYBOOK_KB_MANIFEST_PATH


@dataclass(frozen=True)
class PlaybookConfig:
    corpus: PlaybookCorpusConfig = field(default_factory=PlaybookCorpusConfig)
    models: ModelConfig = field(default_factory=ModelConfig)
    chunks: ChunkConfig = field(default_factory=ChunkConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    query_kb: PlaybookQueryKBConfig = field(default_factory=PlaybookQueryKBConfig)
    storage: PlaybookStorageConfig = field(default_factory=PlaybookStorageConfig)

    def validate(self) -> None:
        if not self.corpus.source_dir.is_dir():
            raise ValueError(f"Playbook 语料目录不存在：{self.corpus.source_dir}")
        if self.chunks.target_tokens <= 0:
            raise ValueError("RAG_CHUNK_TOKENS 必须大于 0")
        if self.retrieval.top_k <= 0:
            raise ValueError("RAG_TOP_K 必须大于 0")


def get_playbook_config() -> PlaybookConfig:
    return PlaybookConfig(
        corpus=PlaybookCorpusConfig(
            source_dir=_env_path(
                "PLAYBOOK_CORPUS_DIR",
                PROJECT_ROOT / "knowledge" / "playbook" / "acc_hk_bim" / "corpus",
            ),
            file_glob=os.getenv("PLAYBOOK_FILE_GLOB", "*.md"),
            product=os.getenv("PLAYBOOK_PRODUCT", "playbook_acc_hk"),
        ),
        models=ModelConfig(
            ollama_host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"),
            embedding_model=os.getenv(
                "RAG_EMBEDDING_MODEL", "qwen3-embedding:0.6b"
            ),
            generation_model=os.getenv("RAG_LLM_MODEL", "qwen3.5:4b"),
            embedding_batch_size=_env_int("RAG_EMBEDDING_BATCH_SIZE", 32),
            request_timeout_seconds=_env_float("RAG_REQUEST_TIMEOUT", 120.0),
        ),
        chunks=ChunkConfig(
            target_tokens=_env_int("RAG_CHUNK_TOKENS", 600),
            overlap_tokens=_env_int("RAG_CHUNK_OVERLAP", 100),
            minimum_tokens=_env_int("RAG_MIN_CHUNK_TOKENS", 40),
        ),
        retrieval=RetrievalConfig(
            vector_candidates=_env_int("RAG_VECTOR_CANDIDATES", 12),
            lexical_candidates=_env_int("RAG_LEXICAL_CANDIDATES", 12),
            top_k=_env_int("RAG_TOP_K", 3),
            rrf_k=_env_int("RAG_RRF_K", 60),
            maximum_context_tokens=_env_int("RAG_MAX_CONTEXT_TOKENS", 2_000),
            minimum_vector_similarity=_env_float("RAG_MIN_SIMILARITY", 0.50),
        ),
        query_kb=PlaybookQueryKBConfig(
            enabled=os.getenv("PLAYBOOK_KB_ENABLED", "true").lower()
            in {"1", "true", "yes"},
            kb_path=_env_path(
                "PLAYBOOK_KB_PATH",
                PROJECT_ROOT
                / "knowledge"
                / "playbook"
                / "acc_hk_bim"
                / "query_kb.jsonl",
            ),
            short_query_max_chars=_env_int("PLAYBOOK_KB_SHORT_QUERY_MAX_CHARS", 24),
            trigger_sim=_env_float("PLAYBOOK_KB_TRIGGER_SIM", 0.52),
            require_sim_improvement=os.getenv(
                "PLAYBOOK_KB_REQUIRE_SIM_IMPROVEMENT", "true"
            ).lower()
            in {"1", "true", "yes"},
            target_url_boost=_env_float("PLAYBOOK_KB_TARGET_URL_BOOST", 0.25),
            contains_max_length_delta=_env_int(
                "PLAYBOOK_KB_CONTAINS_MAX_LEN_DELTA", 6
            ),
            route_top_k=_env_int("PLAYBOOK_KB_ROUTE_TOP_K", 5),
            min_route_sim=_env_float("PLAYBOOK_KB_MIN_ROUTE_SIM", 0.40),
        ),
        storage=PlaybookStorageConfig(
            data_dir=_env_path(
                "PLAYBOOK_DATA_DIR",
                PROJECT_ROOT / ".rag_data" / "playbook_acc_hk",
            ),
            collection_name=os.getenv("PLAYBOOK_COLLECTION", "playbook_acc_hk"),
        ),
    )
