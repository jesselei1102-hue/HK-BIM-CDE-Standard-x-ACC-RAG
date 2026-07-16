"""行业 HK CDE 混合检索（复用产品轨逻辑，独立 collection）。"""

from __future__ import annotations

from rag.config import AppConfig, CorpusConfig, QueryKBConfig
from rag.industry_hk.config import IndustryHKConfig, get_industry_hk_config
from rag.orchestrator.industry_prefer import prefer_industry_chunks
from rag.retrieval import HybridRetriever, RetrievalResult


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
    ) -> RetrievalResult:
        result = super().retrieve_with_debug(
            query, top_k, boost_url_prefix=boost_url_prefix
        )
        preferred = prefer_industry_chunks(
            query,
            list(result.chunks),
            chunks_path=self.industry_config.storage.chunks_path,
            limit=top_k or len(result.chunks) or 3,
        )
        if preferred == result.chunks:
            return result
        return RetrievalResult(chunks=preferred, debug=result.debug)
