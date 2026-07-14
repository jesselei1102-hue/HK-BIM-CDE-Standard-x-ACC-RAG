#!/usr/bin/env python3
"""构建香港 CDE 行业知识库向量索引（先过完整性门禁）。"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import UTC, datetime
from dataclasses import replace
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.chunking import calculate_stats, chunk_documents  # noqa: E402
from rag.config import AppConfig, CorpusConfig, QueryKBConfig, StorageConfig  # noqa: E402
from rag.indexing import index_chunks  # noqa: E402
from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.ingestion import IndustryCorpusConfig, load_industry_corpus  # noqa: E402
from rag.industry_hk.paths import HK_EXTRACT_REPORT_PATH, HK_SOURCES_MANIFEST_PATH  # noqa: E402


def _run_validation() -> None:
    script = PROJECT_ROOT / "scripts" / "validate_hk_extract_completeness.py"
    result = subprocess.run([sys.executable, str(script)], check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def _to_app_config(industry_config) -> AppConfig:
    return AppConfig(
        corpus=CorpusConfig(
            source_dir=industry_config.corpus.source_dir,
            file_glob=industry_config.corpus.file_glob,
            product=industry_config.corpus.product,
        ),
        models=industry_config.models,
        chunks=industry_config.chunks,
        retrieval=industry_config.retrieval,
        query_kb=QueryKBConfig(
            enabled=industry_config.query_kb.enabled,
            kb_path=industry_config.query_kb.kb_path,
            short_query_max_chars=industry_config.query_kb.short_query_max_chars,
            trigger_sim=industry_config.query_kb.trigger_sim,
            require_sim_improvement=industry_config.query_kb.require_sim_improvement,
            target_url_boost=industry_config.query_kb.target_url_boost,
            contains_max_length_delta=industry_config.query_kb.contains_max_length_delta,
            route_top_k=industry_config.query_kb.route_top_k,
            min_route_sim=industry_config.query_kb.min_route_sim,
        ),
        storage=StorageConfig(
            data_dir=industry_config.storage.data_dir,
            collection_name=industry_config.storage.collection_name,
        ),
    )


def _ingest_metrics() -> dict:
    report = json.loads(HK_EXTRACT_REPORT_PATH.read_text(encoding="utf-8"))
    manifest = json.loads(HK_SOURCES_MANIFEST_PATH.read_text(encoding="utf-8"))
    source_hashes = {
        item["doc_id"]: item.get("sha256", "")
        for item in manifest.get("sources", [])
    }
    gaps_hash = hashlib.sha256(
        json.dumps(report.get("gaps", []), sort_keys=True).encode()
    ).hexdigest()[:16]
    return {
        "page_coverage_pct": report.get("page_coverage_pct"),
        "gaps_hash": gaps_hash,
        "source_sha256": source_hashes,
        "deferred_pages": report.get("deferred_pages", []),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ingest 香港 CDE 行业语料")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--all", action="store_true", help="ingest 全部 priority（默认仅 high）")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    args = parser.parse_args(argv)

    if not args.skip_validation:
        print("运行完整性门禁...")
        _run_validation()

    industry = get_industry_hk_config()
    priority_filter = None if args.all else "high"
    industry = replace(
        industry,
        corpus=IndustryCorpusConfig(
            source_dir=industry.corpus.source_dir,
            file_glob=industry.corpus.file_glob,
            product=industry.corpus.product,
            priority_filter=priority_filter,
        ),
        ingest_all_priorities=args.all,
    )

    ingestion = load_industry_corpus(industry.corpus)
    app_config = _to_app_config(industry)
    chunks = chunk_documents(ingestion.documents, app_config.chunks)
    stats = calculate_stats(chunks)

    total_pages = sum(
        item.get("page_count", 0)
        for item in json.loads(HK_SOURCES_MANIFEST_PATH.read_text()).get("sources", [])
        if item.get("kind") == "pdf"
    )
    ingested_pages = len({doc.page_index for doc in ingestion.documents})
    ingested_page_pct = round(ingested_pages / max(total_pages, 1) * 100, 2)

    print("行业 HK CDE 索引准备")
    print(f"  语料文件：{ingestion.scanned_files}")
    print(f"  入库章节：{ingestion.accepted_pages}")
    print(f"  跳过：{len(ingestion.rejected)}")
    print(f"  Chunks：{stats.chunks}")
    print(f"  page_coverage_pct：{_ingest_metrics()['page_coverage_pct']}%")
    print(f"  ingested_page_pct：{ingested_page_pct}%")

    if args.dry_run:
        return 0

    result = index_chunks(chunks, app_config, rebuild=args.rebuild)
    manifest_path = industry.storage.manifest_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "corpus": "industry_hk_cde",
            "ingested_at": datetime.now(UTC).isoformat(),
            "ingested_page_pct": ingested_page_pct,
            **_ingest_metrics(),
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
