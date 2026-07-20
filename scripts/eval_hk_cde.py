#!/usr/bin/env python3
"""香港 CDE 行业知识库评测：路由触发、SectionRecall@1、产品轨误伤率。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.config import get_config  # noqa: E402
from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.intent import should_route_industry  # noqa: E402
from rag.industry_hk.retrieval import IndustryHybridRetriever  # noqa: E402
from rag.retrieval import HybridRetriever  # noqa: E402


def _load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="评测 HK CDE 行业 RAG")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hk_cde_cases.jsonl",
    )
    args = parser.parse_args(argv)

    cases = _load_cases(args.cases)
    industry_retriever = IndustryHybridRetriever(get_industry_hk_config())
    docs_retriever = HybridRetriever(get_config())

    recall_hits = 0
    recall_total = 0
    route_hits = 0
    route_total = 0
    docs_false_positive = 0

    for case in cases:
        query = case["query"]
        expect_track = case.get("expect_track", "industry")
        expect_fragment = case.get("expect_section_contains", "").lower()

        predicted_industry = should_route_industry(query)
        predicted_track = "industry" if predicted_industry else "docs"
        if expect_track == "industry":
            route_total += 1
            if predicted_track == "industry":
                route_hits += 1
        if expect_track == "docs" and predicted_track == "industry":
            docs_false_positive += 1

        if expect_track == "industry" and expect_fragment:
            recall_total += 1
            result = industry_retriever.retrieve_with_debug(query, top_k=1)
            if result.chunks:
                top = result.chunks[0]
                haystack = f"{top.source_url} {top.title} {top.source_file}".lower()
                if expect_fragment in haystack:
                    recall_hits += 1

    recall_at_1 = recall_hits / recall_total if recall_total else 0.0
    route_acc = route_hits / route_total if route_total else 0.0

    print("HK CDE Eval")
    print(f"  cases: {len(cases)}")
    print(f"  SectionRecall@1: {recall_at_1:.1%} ({recall_hits}/{recall_total})")
    print(f"  industry route accuracy: {route_acc:.1%} ({route_hits}/{route_total})")
    print(f"  docs false positive (industry steal): {docs_false_positive}")

    ok = recall_at_1 >= 0.95 and docs_false_positive == 0
    if not ok:
        print("FAIL: 未达基线（Recall@1>=95%, docs误伤=0）", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
