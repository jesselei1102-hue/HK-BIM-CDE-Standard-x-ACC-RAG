"""香港 CDE 行业知识库配置。"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from rag.config import (
    ChunkConfig,
    ModelConfig,
    PROJECT_ROOT,
    RetrievalConfig,
    _env_bool,
    _env_float,
    _env_int,
    _env_path,
)

from .paths import (
    HK_CHROMA_DIR,
    HK_CHUNKS_PATH,
    HK_COLLECTION_NAME,
    HK_CORPUS_DIR,
    HK_KB_CHROMA_DIR,
    HK_KB_COLLECTION_NAME,
    HK_KB_MANIFEST_PATH,
    HK_MANIFEST_PATH,
    HK_QUERY_KB_PATH,
    HK_RAG_DATA_DIR,
)


@dataclass(frozen=True)
class IndustryCorpusConfig:
    source_dir: Path = HK_CORPUS_DIR
    file_glob: str = "**/*.md"
    product: str = "hk_cde"


@dataclass(frozen=True)
class IndustryQueryKBConfig:
    enabled: bool = True
    kb_path: Path = HK_QUERY_KB_PATH
    short_query_max_chars: int = 24
    trigger_sim: float = 0.52
    require_sim_improvement: bool = True
    target_url_boost: float = 0.25
    contains_max_length_delta: int = 6
    route_top_k: int = 5
    min_route_sim: float = 0.40


@dataclass(frozen=True)
class IndustryStorageConfig:
    data_dir: Path = HK_RAG_DATA_DIR
    collection_name: str = HK_COLLECTION_NAME

    @property
    def chroma_dir(self) -> Path:
        return HK_CHROMA_DIR

    @property
    def chunks_path(self) -> Path:
        return HK_CHUNKS_PATH

    @property
    def manifest_path(self) -> Path:
        return HK_MANIFEST_PATH

    @property
    def kb_chroma_dir(self) -> Path:
        return HK_KB_CHROMA_DIR

    @property
    def kb_collection_name(self) -> str:
        return HK_KB_COLLECTION_NAME

    @property
    def kb_manifest_path(self) -> Path:
        return HK_KB_MANIFEST_PATH


@dataclass(frozen=True)
class IndustryHKConfig:
    corpus: IndustryCorpusConfig = field(default_factory=IndustryCorpusConfig)
    models: ModelConfig = field(default_factory=ModelConfig)
    chunks: ChunkConfig = field(default_factory=ChunkConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    query_kb: IndustryQueryKBConfig = field(default_factory=IndustryQueryKBConfig)
    storage: IndustryStorageConfig = field(default_factory=IndustryStorageConfig)
    ingest_all_priorities: bool = False

    def validate(self) -> None:
        if not self.corpus.source_dir.is_dir():
            raise ValueError(f"行业语料目录不存在：{self.corpus.source_dir}")
        if self.chunks.target_tokens <= 0:
            raise ValueError("RAG_CHUNK_TOKENS 必须大于 0")
        if self.retrieval.top_k <= 0:
            raise ValueError("RAG_TOP_K 必须大于 0")


def get_industry_hk_config() -> IndustryHKConfig:
    return IndustryHKConfig(
        corpus=IndustryCorpusConfig(
            source_dir=_env_path(
                "INDUSTRY_HK_CORPUS_DIR",
                PROJECT_ROOT / "knowledge" / "industry" / "hk_cde" / "corpus",
            ),
            file_glob=os.getenv("INDUSTRY_HK_FILE_GLOB", "**/*.md"),
            product=os.getenv("INDUSTRY_HK_PRODUCT", "hk_cde"),
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
            nlp_coarse_enabled=_env_bool("RAG_NLP_COARSE", True),
            nlp_coarse_candidates=_env_int("RAG_NLP_COARSE_CANDIDATES", 80),
            nlp_rerank_enabled=_env_bool("RAG_NLP_RERANK", True),
            hybrid_prefetch=_env_int("RAG_HYBRID_PREFETCH", 12),
        ),
        query_kb=IndustryQueryKBConfig(
            enabled=os.getenv("INDUSTRY_KB_ENABLED", "true").lower()
            in {"1", "true", "yes"},
            kb_path=_env_path(
                "INDUSTRY_KB_PATH",
                PROJECT_ROOT / "knowledge" / "industry" / "hk_cde" / "query_kb.jsonl",
            ),
            short_query_max_chars=_env_int("INDUSTRY_KB_SHORT_QUERY_MAX_CHARS", 24),
            trigger_sim=_env_float("INDUSTRY_KB_TRIGGER_SIM", 0.52),
            require_sim_improvement=os.getenv(
                "INDUSTRY_KB_REQUIRE_SIM_IMPROVEMENT", "true"
            ).lower()
            in {"1", "true", "yes"},
            target_url_boost=_env_float("INDUSTRY_KB_TARGET_URL_BOOST", 0.25),
            contains_max_length_delta=_env_int(
                "INDUSTRY_KB_CONTAINS_MAX_LEN_DELTA", 6
            ),
            route_top_k=_env_int("INDUSTRY_KB_ROUTE_TOP_K", 5),
            min_route_sim=_env_float("INDUSTRY_KB_MIN_ROUTE_SIM", 0.40),
        ),
        storage=IndustryStorageConfig(
            data_dir=_env_path(
                "INDUSTRY_HK_DATA_DIR",
                PROJECT_ROOT / ".rag_data" / "industry_hk_cde",
            ),
            collection_name=os.getenv(
                "INDUSTRY_HK_COLLECTION", "industry_hk_cde"
            ),
        ),
        ingest_all_priorities=os.getenv("INDUSTRY_HK_INGEST_ALL", "false").lower()
        in {"1", "true", "yes"},
    )
