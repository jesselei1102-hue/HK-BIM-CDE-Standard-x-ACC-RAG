"""Query KB 专项评测：ShortQueryRecall@1 与 KB 触发准确率。

用法：
    python scripts/eval_query_kb.py
    python scripts/eval_query_kb.py --cases eval/query_kb_cases.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.config import get_config
from rag.retrieval import HybridRetriever


def load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description="Query KB 评测")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "query_kb_cases.jsonl",
    )
    args = parser.parse_args()

    cases = load_cases(args.cases)
    config = get_config()
    retriever = HybridRetriever(config)

    recall_hits = 0
    kb_trigger_correct = 0
    false_rewrite = 0

    print(f"评测用例：{len(cases)} 条")
    print("-" * 72)

    for case in cases:
        query = case["short_query"]
        expected_url = case["expected_url"]
        should_trigger = case["should_trigger_kb"]

        result = retriever.retrieve_with_debug(query)
        top_url = result.chunks[0].source_url if result.chunks else ""
        expected_urls = [case["expected_url"], *case.get("acceptable_urls", [])]
        recall_ok = top_url in expected_urls
        if recall_ok:
            recall_hits += 1

        kb_triggered = result.debug.adopted_path in {"kb_rewrite", "kb_boost"}
        trigger_ok = kb_triggered == should_trigger
        if trigger_ok:
            kb_trigger_correct += 1

        if not should_trigger and kb_triggered:
            false_rewrite += 1

        status = "OK" if recall_ok else "MISS"
        kb_status = "KB✓" if trigger_ok else "KB✗"
        print(
            f"[{status}] [{kb_status}] {query}\n"
            f"       expected: {expected_url}\n"
            f"       got:      {top_url or '(empty)'}\n"
            f"       path:     {result.debug.adopted_path} "
            f"sim={result.debug.original_top1_sim} "
            f"kb={result.debug.kb_id or '-'}"
        )

    n = len(cases)
    print("-" * 72)
    print(f"ShortQueryRecall@1: {recall_hits}/{n} ({100 * recall_hits / n:.1f}%)")
    print(f"KB触发准确率:       {kb_trigger_correct}/{n} ({100 * kb_trigger_correct / n:.1f}%)")
    print(f"无KB误改写率:       {false_rewrite}/{n} ({100 * false_rewrite / n:.1f}%)")
    return 0 if recall_hits == n and false_rewrite == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
