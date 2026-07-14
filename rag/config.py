"""本地 RAG 的集中配置。

默认值针对 ``output/DOCS`` 语料设计。常用参数可通过环境变量覆盖，
无需修改代码；路径型环境变量既支持绝对路径，也支持项目根目录下的
相对路径。
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(f"{name} 必须是整数，当前值为 {value!r}") from exc


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise ValueError(f"{name} 必须是数字，当前值为 {value!r}") from exc


def _env_path(name: str, default: Path) -> Path:
    value = os.getenv(name)
    if value is None:
        return default
    path = Path(value).expanduser()
    return path if path.is_absolute() else PROJECT_ROOT / path


@dataclass(frozen=True)
class CorpusConfig:
    source_dir: Path = PROJECT_ROOT / "output" / "DOCS"
    file_glob: str = "DOCS_help_*.md"
    product: str = "DOCS"


@dataclass(frozen=True)
class ModelConfig:
    ollama_host: str = "http://127.0.0.1:11434"
    embedding_model: str = "qwen3-embedding:0.6b"
    generation_model: str = "qwen3.5:4b"
    embedding_batch_size: int = 32
    request_timeout_seconds: float = 120.0


@dataclass(frozen=True)
class ChunkConfig:
    target_tokens: int = 600
    overlap_tokens: int = 100
    minimum_tokens: int = 40


@dataclass(frozen=True)
class RetrievalConfig:
    vector_candidates: int = 12
    lexical_candidates: int = 12
    top_k: int = 3
    rrf_k: int = 60
    maximum_context_tokens: int = 2_000
    minimum_vector_similarity: float = 0.55


@dataclass(frozen=True)
class QueryKBConfig:
    enabled: bool = True
    kb_path: Path = PROJECT_ROOT / "knowledge" / "query_kb.jsonl"
    short_query_max_chars: int = 16
    trigger_sim: float = 0.55
    require_sim_improvement: bool = True
    target_url_boost: float = 0.25
    contains_max_length_delta: int = 4
    route_top_k: int = 5
    min_route_sim: float = 0.42


@dataclass(frozen=True)
class StorageConfig:
    data_dir: Path = PROJECT_ROOT / ".rag_data"
    collection_name: str = "autodesk_docs"

    @property
    def chroma_dir(self) -> Path:
        return self.data_dir / "chroma"

    @property
    def chunks_path(self) -> Path:
        return self.data_dir / "chunks.jsonl"

    @property
    def manifest_path(self) -> Path:
        return self.data_dir / "manifest.json"

    @property
    def kb_chroma_dir(self) -> Path:
        return self.data_dir / "kb_chroma"

    @property
    def kb_collection_name(self) -> str:
        return "autodesk_docs_kb_route"

    @property
    def kb_manifest_path(self) -> Path:
        return self.data_dir / "kb_route_manifest.json"


@dataclass(frozen=True)
class AppConfig:
    corpus: CorpusConfig = field(default_factory=CorpusConfig)
    models: ModelConfig = field(default_factory=ModelConfig)
    chunks: ChunkConfig = field(default_factory=ChunkConfig)
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)
    query_kb: QueryKBConfig = field(default_factory=QueryKBConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)

    def validate(self) -> None:
        if not self.corpus.source_dir.is_dir():
            raise ValueError(f"语料目录不存在：{self.corpus.source_dir}")
        if self.chunks.target_tokens <= 0:
            raise ValueError("RAG_CHUNK_TOKENS 必须大于 0")
        if not 0 <= self.chunks.overlap_tokens < self.chunks.target_tokens:
            raise ValueError("RAG_CHUNK_OVERLAP 必须大于等于 0 且小于 chunk 大小")
        if self.chunks.minimum_tokens <= 0:
            raise ValueError("RAG_MIN_CHUNK_TOKENS 必须大于 0")
        if self.retrieval.top_k <= 0:
            raise ValueError("RAG_TOP_K 必须大于 0")
        if self.retrieval.maximum_context_tokens <= 0:
            raise ValueError("RAG_MAX_CONTEXT_TOKENS 必须大于 0")
        if not 0 <= self.retrieval.minimum_vector_similarity <= 1:
            raise ValueError("RAG_MIN_SIMILARITY 必须位于 0 到 1 之间")
        if self.query_kb.short_query_max_chars <= 0:
            raise ValueError("KB_SHORT_QUERY_MAX_CHARS 必须大于 0")
        if not 0 <= self.query_kb.trigger_sim <= 1:
            raise ValueError("KB_TRIGGER_SIM 必须位于 0 到 1 之间")


def get_config() -> AppConfig:
    """从默认值和环境变量构建并验证配置。"""

    config = AppConfig(
        corpus=CorpusConfig(
            source_dir=_env_path(
                "RAG_SOURCE_DIR", PROJECT_ROOT / "output" / "DOCS"
            ),
            file_glob=os.getenv("RAG_FILE_GLOB", "DOCS_help_*.md"),
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
            minimum_vector_similarity=_env_float("RAG_MIN_SIMILARITY", 0.55),
        ),
        query_kb=QueryKBConfig(
            enabled=os.getenv("KB_ENABLED", "true").lower() in {"1", "true", "yes"},
            kb_path=_env_path(
                "KB_PATH", PROJECT_ROOT / "knowledge" / "query_kb.jsonl"
            ),
            short_query_max_chars=_env_int("KB_SHORT_QUERY_MAX_CHARS", 16),
            trigger_sim=_env_float("KB_TRIGGER_SIM", 0.55),
            require_sim_improvement=os.getenv(
                "KB_REQUIRE_SIM_IMPROVEMENT", "true"
            ).lower()
            in {"1", "true", "yes"},
            target_url_boost=_env_float("KB_TARGET_URL_BOOST", 0.25),
            contains_max_length_delta=_env_int("KB_CONTAINS_MAX_LEN_DELTA", 4),
            route_top_k=_env_int("KB_ROUTE_TOP_K", 5),
            min_route_sim=_env_float("KB_MIN_ROUTE_SIM", 0.42),
        ),
        storage=StorageConfig(
            data_dir=_env_path("RAG_DATA_DIR", PROJECT_ROOT / ".rag_data"),
            collection_name=os.getenv("RAG_COLLECTION", "autodesk_docs"),
        ),
    )
    config.validate()
    return config
