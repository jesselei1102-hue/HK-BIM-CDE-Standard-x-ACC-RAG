"""Playbook 混合检索（独立 collection）。"""

from __future__ import annotations

from rag.config import AppConfig, CorpusConfig, QueryKBConfig
from rag.playbook_acc_hk.config import PlaybookConfig, get_playbook_config
from rag.retrieval import HybridRetriever


class PlaybookStorageBridge:
    def __init__(self, storage) -> None:
        self._s = storage

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


def playbook_to_app_config(config: PlaybookConfig) -> AppConfig:
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
        storage=PlaybookStorageBridge(config.storage),  # type: ignore[arg-type]
    )


class PlaybookHybridRetriever(HybridRetriever):
    def __init__(self, config: PlaybookConfig | None = None) -> None:
        playbook = config or get_playbook_config()
        super().__init__(playbook_to_app_config(playbook))
        self.playbook_config = playbook
