#!/usr/bin/env python3
"""Playbook 单轨 + hybrid 含手册召回评测。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.orchestrator.classify import classify_intent  # noqa: E402
from rag.orchestrator.pipeline import HybridOrchestrator  # noqa: E402


def _load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="评测 playbook 轨")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "playbook_acc_hk_cases.jsonl",
    )
    args = parser.parse_args(argv)

    cases = _load_cases(args.cases)
    orchestrator = HybridOrchestrator()

    intent_hits = 0
    intent_total = 0
    recall_hits = 0
    recall_total = 0
    triple_hits = 0
    triple_total = 0

    for case in cases:
        query = case["query"]
        expect = case["expect_track"]
        decision = classify_intent(query)
        intent_total += 1
        if decision.track == expect:
            intent_hits += 1

        if expect == "playbook":
            recall_total += 1
            result = orchestrator.ask(
                query, force_track="playbook", top_k=3, no_generate=True
            )
            blob = " ".join(
                f"{c.title} {c.source_url} {c.text[:400]}"
                for c in result.chunks_playbook
            ).lower()
            needle = (case.get("expect_capability_contains") or "").lower()
            if result.chunks_playbook and (not needle or needle in blob):
                recall_hits += 1

        if expect == "hybrid":
            triple_total += 1
            result = orchestrator.retrieve_hybrid(query, decision, top_k=None)
            if (
                len(result.chunks_docs) >= 1
                and len(result.chunks_industry) >= 1
                and len(result.chunks_playbook) >= 1
            ):
                triple_hits += 1

    intent_acc = intent_hits / intent_total if intent_total else 0.0
    recall = recall_hits / recall_total if recall_total else 0.0
    triple = triple_hits / triple_total if triple_total else 0.0

    print("Playbook Eval")
    print(f"  cases: {len(cases)}")
    print(f"  intent accuracy: {intent_acc:.1%} ({intent_hits}/{intent_total})")
    print(f"  playbook recall: {recall:.1%} ({recall_hits}/{recall_total})")
    print(f"  hybrid triple recall: {triple:.1%} ({triple_hits}/{triple_total})")

    ok = intent_acc >= 0.75 and recall >= 0.80 and (triple_total == 0 or triple >= 0.80)
    if not ok:
        print("FAIL", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
