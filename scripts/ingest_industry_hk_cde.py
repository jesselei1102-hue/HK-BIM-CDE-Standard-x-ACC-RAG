#!/usr/bin/env python3
"""构建香港 CDE 行业知识库向量索引（先过完整性门禁）。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.chunking import calculate_stats, chunk_documents  # noqa: E402
from rag.config import AppConfig, CorpusConfig, QueryKBConfig, StorageConfig  # noqa: E402
from rag.indexing import index_chunks  # noqa: E402
from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.ingestion import (  # noqa: E402
    IndustryCorpusConfig,
    collect_indexed_manifest,
    load_industry_corpus,
)
from rag.industry_hk.paths import (  # noqa: E402
    HK_EXTRACT_REPORT_PATH,
    HK_SOURCES_MANIFEST_PATH,
)
from rag.industry_hk.retrieval import IndustryStorageBridge  # noqa: E402

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _run_validation() -> None:
    script = PROJECT_ROOT / "scripts" / "validate_hk_extract_completeness.py"
    result = subprocess.run([sys.executable, str(script)], check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def _to_app_config(playbook_like) -> AppConfig:
    return AppConfig(
        corpus=CorpusConfig(
            source_dir=playbook_like.corpus.source_dir,
            file_glob=playbook_like.corpus.file_glob,
            product=playbook_like.corpus.product,
        ),
        models=playbook_like.models,
        chunks=playbook_like.chunks,
        retrieval=playbook_like.retrieval,
        query_kb=QueryKBConfig(
            enabled=playbook_like.query_kb.enabled,
            kb_path=playbook_like.query_kb.kb_path,
            short_query_max_chars=playbook_like.query_kb.short_query_max_chars,
            trigger_sim=playbook_like.query_kb.trigger_sim,
            require_sim_improvement=playbook_like.query_kb.require_sim_improvement,
            target_url_boost=playbook_like.query_kb.target_url_boost,
            contains_max_length_delta=playbook_like.query_kb.contains_max_length_delta,
            route_top_k=playbook_like.query_kb.route_top_k,
            min_route_sim=playbook_like.query_kb.min_route_sim,
        ),
        storage=IndustryStorageBridge(playbook_like.storage),  # type: ignore[arg-type]
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


def _parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def _coverage_from_documents(documents: list, source_dir: Path) -> dict:
    """Compute coverage keyed by (doc_id, page) to avoid cross-PDF collisions."""
    accepted_keys: set[tuple[str, int]] = set()
    accepted_sections = 0
    for doc in documents:
        source_file = Path(doc.source_file)
        abs_path = source_file if source_file.is_absolute() else PROJECT_ROOT / source_file
        meta: dict = {}
        if abs_path.is_file():
            meta = _parse_frontmatter(abs_path.read_text(encoding="utf-8"))
        doc_id = str(meta.get("doc_id") or abs_path.parent.name)
        page_start = int(meta.get("page_start") or doc.page_index or 1)
        page_end = int(meta.get("page_end") or page_start)
        accepted_sections += 1
        for page in range(page_start, page_end + 1):
            accepted_keys.add((doc_id, page))

    total_sections = 0
    all_keys: set[tuple[str, int]] = set()
    for path in sorted(source_dir.glob("**/*.md")):
        if not path.is_file() or path.parent.name == "templates":
            continue
        total_sections += 1
        meta = _parse_frontmatter(path.read_text(encoding="utf-8"))
        doc_id = str(meta.get("doc_id") or path.parent.name)
        page_start = int(meta.get("page_start") or 1)
        page_end = int(meta.get("page_end") or page_start)
        for page in range(page_start, page_end + 1):
            all_keys.add((doc_id, page))

    section_ingest_pct = round(accepted_sections / max(total_sections, 1) * 100, 2)
    page_range_ingest_pct = round(len(accepted_keys) / max(len(all_keys), 1) * 100, 2)
    return {
        "accepted_sections": accepted_sections,
        "total_sections": total_sections,
        "section_ingest_pct": section_ingest_pct,
        "accepted_page_keys": len(accepted_keys),
        "total_page_keys": len(all_keys),
        "page_range_ingest_pct": page_range_ingest_pct,
        # Back-compat alias using corrected page-key logic.
        "ingested_page_pct": page_range_ingest_pct,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ingest 香港 CDE 行业语料")
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument(
        "--scope",
        choices=("high", "substantive", "all"),
        default=None,
        help="high=curated; substantive=useful body; all=unfiltered",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="alias for --scope all (legacy)",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    args = parser.parse_args(argv)

    if not args.skip_validation:
        print("运行完整性门禁...")
        _run_validation()

    scope = args.scope or ("all" if args.all else "high")
    industry = get_industry_hk_config()
    industry = replace(
        industry,
        corpus=IndustryCorpusConfig(
            source_dir=industry.corpus.source_dir,
            file_glob=industry.corpus.file_glob,
            product=industry.corpus.product,
            priority_filter="high" if scope == "high" else None,
            ingest_scope=scope,
        ),
        ingest_all_priorities=scope == "all",
    )

    ingestion = load_industry_corpus(industry.corpus)
    app_config = _to_app_config(industry)
    chunks = chunk_documents(ingestion.documents, app_config.chunks)
    # Propagate authority header onto every chunk of a multi-chunk section so
    # later chunks retain authority_type / normative_weight for grounding.
    by_url: dict[str, str] = {}
    for chunk in chunks:
        text = chunk.text
        if "authority_type:" in text[:500]:
            header_end = text.find("]\n")
            if header_end > 0:
                # Capture "[doc_id: ... authority ...]\n\n" possibly after a title line.
                bracket = text.find("[doc_id:")
                if bracket < 0:
                    bracket = text.find("[authority_type:")
                if bracket >= 0:
                    end = text.find("]\n", bracket)
                    if end > bracket:
                        by_url[chunk.source_url] = text[bracket : end + 1]
    if by_url:
        stamped = []
        for chunk in chunks:
            header = by_url.get(chunk.source_url)
            if header and header not in chunk.text[:400]:
                from dataclasses import replace as dc_replace

                stamped.append(
                    dc_replace(chunk, text=f"{header}\n\n{chunk.text}")
                )
            else:
                stamped.append(chunk)
        chunks = stamped
    stats = calculate_stats(chunks)
    coverage = _coverage_from_documents(
        ingestion.documents, industry.corpus.source_dir
    )

    print("行业 HK CDE 索引准备")
    print(f"  scope：{scope}")
    print(f"  data_dir：{industry.storage.data_dir}")
    print(f"  collection：{industry.storage.collection_name}")
    print(f"  语料文件：{ingestion.scanned_files}")
    print(f"  入库章节：{ingestion.accepted_pages}")
    print(f"  跳过：{len(ingestion.rejected)}")
    print(f"  Chunks：{stats.chunks}")
    print(f"  page_coverage_pct：{_ingest_metrics()['page_coverage_pct']}%")
    print(
        f"  section_ingest_pct：{coverage['section_ingest_pct']}% "
        f"({coverage['accepted_sections']}/{coverage['total_sections']})"
    )
    print(
        f"  page_range_ingest_pct：{coverage['page_range_ingest_pct']}% "
        f"({coverage['accepted_page_keys']}/{coverage['total_page_keys']})"
    )

    if args.dry_run:
        return 0

    result = index_chunks(chunks, app_config, rebuild=args.rebuild)
    manifest_path = industry.storage.manifest_path
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    indexed = collect_indexed_manifest(ingestion.documents)
    manifest.update(
        {
            "corpus": "industry_hk_cde",
            "ingest_scope": scope,
            "ingested_at": datetime.now(UTC).isoformat(),
            **coverage,
            **_ingest_metrics(),
            **indexed,
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
