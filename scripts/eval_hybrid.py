#!/usr/bin/env python3
"""双轨编排评测：意图、DualRecall、对齐段约束。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.orchestrator.classify import classify_intent  # noqa: E402
from rag.orchestrator.pipeline import HybridOrchestrator  # noqa: E402


SECTION_RE = re.compile(
    r"标准要求|實施建議|实施建议|產品操作|产品操作|对齐与缺口|對齊與缺口|"
    r"Standards?\s+Requirements?|Implementation\s+(?:Guidance|Advice)|"
    r"Product\s+(?:Steps|Operations|Guidance)|Alignment\s*(?:&|and)?\s*Gaps?",
    re.I,
)


def _load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="评测 V2 双轨编排")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hybrid_cases.jsonl",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="对 hybrid 用例调用生成以检查三段标题（较慢）",
    )
    args = parser.parse_args(argv)

    cases = _load_cases(args.cases)
    orchestrator = HybridOrchestrator()

    intent_hits = 0
    intent_total = 0
    capability_hits = 0
    capability_total = 0
    dual_hits = 0
    dual_total = 0
    false_hybrid = 0
    section_hits = 0
    section_total = 0
    playbook_hits = 0
    playbook_total = 0

    for case in cases:
        query = case["query"]
        expect = case["expect_track"]
        decision = classify_intent(query)
        intent_total += 1
        if decision.track == expect:
            intent_hits += 1
        elif expect in {"docs", "hk_cde", "playbook"} and decision.track == "hybrid":
            false_hybrid += 1

        if "expect_capability" in case:
            capability_total += 1
            expected_cap = case["expect_capability"]
            if decision.capability == expected_cap:
                capability_hits += 1
            else:
                print(
                    f"  capability miss [{case.get('id')}]: "
                    f"got={decision.capability!r} expect={expected_cap!r} "
                    f"query={query}",
                    file=sys.stderr,
                )

        if expect == "hybrid":
            dual_total += 1
            playbook_total += 1
            result = orchestrator.retrieve_hybrid(query, decision, top_k=None)
            docs_n = len(result.chunks_docs)
            ind_n = len(result.chunks_industry)
            pb_n = len(result.chunks_playbook)
            if docs_n >= 1 and ind_n >= 1:
                dual_hits += 1
            if docs_n >= 1 and ind_n >= 1 and pb_n >= 1:
                playbook_hits += 1

            if args.generate:
                section_total += 1
                full = orchestrator.ask(query, force_track="hybrid", top_k=None)
                answer = full.answer.answer if full.answer else ""
                if len(SECTION_RE.findall(answer)) >= 3:
                    section_hits += 1

    intent_acc = intent_hits / intent_total if intent_total else 0.0
    capability_acc = (
        capability_hits / capability_total if capability_total else 1.0
    )
    dual_recall = dual_hits / dual_total if dual_total else 0.0
    playbook_recall = playbook_hits / playbook_total if playbook_total else 0.0

    print("Hybrid Orchestrator Eval")
    print(f"  cases: {len(cases)}")
    print(f"  intent accuracy: {intent_acc:.1%} ({intent_hits}/{intent_total})")
    print(
        f"  capability accuracy: {capability_acc:.1%} "
        f"({capability_hits}/{capability_total})"
    )
    print(f"  DualRecall: {dual_recall:.1%} ({dual_hits}/{dual_total})")
    print(
        f"  TripleRecall(+playbook): {playbook_recall:.1%} "
        f"({playbook_hits}/{playbook_total})"
    )
    print(f"  false hybrid (pure-track stolen): {false_hybrid}")
    if args.generate:
        print(
            f"  section headings: "
            f"{section_hits}/{section_total}"
        )

    ok = (
        dual_recall >= 0.80
        and false_hybrid == 0
        and intent_acc >= 0.80
        and capability_acc >= 0.90
    )
    if playbook_total and playbook_recall < 0.80:
        ok = False
    if args.generate and section_total and section_hits < section_total:
        ok = False
    if not ok:
        print("FAIL", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
