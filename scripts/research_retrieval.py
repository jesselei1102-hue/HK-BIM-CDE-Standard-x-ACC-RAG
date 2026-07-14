"""批量短句检索失败归因，输出 retrieval_gaps.jsonl。

用法：
    python scripts/research_retrieval.py
    python scripts/research_retrieval.py --queries eval/short_queries.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import time

from rag.config import get_config
from rag.retrieval import HybridRetriever

DEFAULT_SHORT_QUERIES = [
    "设置权限",
    "文件夹权限",
    "审批",
    "审阅",
    "附函",
    "传送件",
    "支持格式",
    "文件大小",
    "支持浏览器",
    "公开链接",
    "上传",
    "标记",
    "命名标准",
    "活动日志",
    "如何设置文件夹权限",
    "怎么创建 transmittal",
    "审批流程怎么配",
    "Autodesk Docs 请问如何设置文件夹权限",
    "Autodesk Docs 中单个文件最大可以多大？",
    "What browsers are supported for Autodesk Construction Cloud?",
]


def load_queries(path: Path | None) -> list[str]:
    if path is None:
        return DEFAULT_SHORT_QUERIES
    queries: list[str] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                queries.append(line)
    return queries


def top_vector_similarity(retriever: HybridRetriever, query: str) -> tuple[float | None, str, str]:
    vector_hits = retriever._vector_hits(query)
    if not vector_hits:
        return None, "", ""
    chunk_id, similarity, _rank = vector_hits[0]
    chunk = retriever.chunks_by_id[chunk_id]
    return similarity, chunk["title"], chunk["source_url"]


def analyze_query(retriever: HybridRetriever, query: str) -> dict:
    config = retriever.config
    threshold = config.retrieval.minimum_vector_similarity

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            raw_sim, raw_title, raw_url = top_vector_similarity(retriever, query)
            prefixed = f"Autodesk Docs {query}"
            prefix_sim, prefix_title, prefix_url = top_vector_similarity(
                retriever, prefixed
            )
            contexts = retriever.retrieve(query)
            break
        except Exception as exc:
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    else:
        raise last_error  # type: ignore[misc]
    top1 = contexts[0] if contexts else None

    gap_reasons: list[str] = []
    if not contexts:
        gap_reasons.append("empty_result")
    if raw_sim is not None and raw_sim < threshold:
        gap_reasons.append("below_threshold")
    if prefix_sim is not None and raw_sim is not None and prefix_sim > raw_sim + 0.02:
        if prefix_title != raw_title:
            gap_reasons.append("prefix_hurts_ranking")

    return {
        "query": query,
        "query_len": len(query),
        "top1_title": top1.title if top1 else raw_title,
        "top1_url": top1.source_url if top1 else raw_url,
        "top1_sim": top1.vector_similarity if top1 else raw_sim,
        "top1_score": top1.score if top1 else None,
        "raw_top1_sim": raw_sim,
        "raw_top1_title": raw_title,
        "raw_top1_url": raw_url,
        "prefixed_top1_sim": prefix_sim,
        "prefixed_top1_title": prefix_title,
        "prefixed_top1_url": prefix_url,
        "filtered_by_threshold": bool(raw_sim is not None and raw_sim < threshold),
        "result_count": len(contexts),
        "gap_reasons": gap_reasons,
        "needs_kb": bool(gap_reasons),
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="短句检索失败归因")
    parser.add_argument(
        "--queries",
        type=Path,
        help="每行一个测试短句的文本文件",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "knowledge" / "research" / "retrieval_gaps.jsonl",
    )
    args = parser.parse_args()

    queries = load_queries(args.queries)
    config = get_config()
    retriever = HybridRetriever(config)

    rows = [analyze_query(retriever, query) for query in queries]
    write_jsonl(args.output, rows)

    needs_kb = sum(1 for row in rows if row["needs_kb"])
    empty = sum(1 for row in rows if "empty_result" in row["gap_reasons"])
    below = sum(1 for row in rows if "below_threshold" in row["gap_reasons"])
    print(f"检索归因：{len(rows)} 条 → {args.output}")
    print(f"  需 KB 辅助：{needs_kb}")
    print(f"  空结果：{empty}")
    print(f"  低于阈值：{below}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
