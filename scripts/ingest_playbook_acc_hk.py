#!/usr/bin/env python3
"""构建 ACC × 港标 playbook 向量索引。"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.chunking import calculate_stats, chunk_documents  # noqa: E402
from rag.config import AppConfig, CorpusConfig, QueryKBConfig, StorageConfig  # noqa: E402
from rag.indexing import index_chunks  # noqa: E402
from rag.playbook_acc_hk.config import get_playbook_config  # noqa: E402
from rag.playbook_acc_hk.ingestion import (  # noqa: E402
    PlaybookCorpusLoadConfig,
    load_playbook_corpus,
)


def _to_app_config(playbook_config) -> AppConfig:
    return AppConfig(
        corpus=CorpusConfig(
            source_dir=playbook_config.corpus.source_dir,
            file_glob=playbook_config.corpus.file_glob,
            product=playbook_config.corpus.product,
        ),
        models=playbook_config.models,
        chunks=playbook_config.chunks,
        retrieval=playbook_config.retrieval,
        query_kb=QueryKBConfig(
            enabled=playbook_config.query_kb.enabled,
            kb_path=playbook_config.query_kb.kb_path,
            short_query_max_chars=playbook_config.query_kb.short_query_max_chars,
            trigger_sim=playbook_config.query_kb.trigger_sim,
            require_sim_improvement=playbook_config.query_kb.require_sim_improvement,
            target_url_boost=playbook_config.query_kb.target_url_boost,
            contains_max_length_delta=playbook_config.query_kb.contains_max_length_delta,
            route_top_k=playbook_config.query_kb.route_top_k,
            min_route_sim=playbook_config.query_kb.min_route_sim,
        ),
        storage=StorageConfig(
            data_dir=playbook_config.storage.data_dir,
            collection_name=playbook_config.storage.collection_name,
        ),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ingest ACC × 港标 playbook 语料")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    playbook = get_playbook_config()
    playbook.validate()
    load_cfg = PlaybookCorpusLoadConfig(
        source_dir=playbook.corpus.source_dir,
        file_glob=playbook.corpus.file_glob,
        product=playbook.corpus.product,
    )
    ingestion = load_playbook_corpus(load_cfg)
    app_config = _to_app_config(playbook)
    chunks = chunk_documents(ingestion.documents, app_config.chunks)
    stats = calculate_stats(chunks)

    print("Playbook ACC×港标 索引准备")
    print(f"  语料文件：{ingestion.scanned_files}")
    print(f"  入库段落：{ingestion.accepted_pages}")
    print(f"  跳过：{len(ingestion.rejected)}")
    print(f"  Chunks：{stats.chunks}")

    if args.dry_run:
        return 0

    result = index_chunks(chunks, app_config, rebuild=args.rebuild)
    manifest_path = playbook.storage.manifest_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "corpus": "playbook_acc_hk",
            "ingested_at": datetime.now(UTC).isoformat(),
            "source_files": ingestion.scanned_files,
            "sections": ingestion.accepted_pages,
        }
    )
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print("\n索引完成")
    print(f"  总 Chunks：{result.total_chunks}")
    print(f"  向量维度：{result.vector_dimension}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
