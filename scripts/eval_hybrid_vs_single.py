#!/usr/bin/env python3
"""Compare hybrid vs forced single-track coverage on hybrid expect cases.

For cross-domain questions (expect_track=hybrid), single-track corpora can only
cover one source family. Hybrid should retrieve Docs + HK CDE + Playbook.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.orchestrator.classify import classify_intent  # noqa: E402
from rag.orchestrator.pipeline import HybridOrchestrator  # noqa: E402


TRACKS = ("docs", "hk_cde", "playbook", "hybrid")


@dataclass
class ModeScore:
    mode: str
    cases: int
    dual_hits: int
    triple_hits: int
    docs_hits: int
    hk_hits: int
    playbook_hits: int

    @property
    def dual_rate(self) -> float:
        return self.dual_hits / self.cases if self.cases else 0.0

    @property
    def triple_rate(self) -> float:
        return self.triple_hits / self.cases if self.cases else 0.0


def _load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def _coverage(orchestrator: HybridOrchestrator, query: str, mode: str) -> tuple[bool, bool, bool]:
    if mode == "hybrid":
        decision = classify_intent(query)
        result = orchestrator.retrieve_hybrid(query, decision, top_k=None)
        return (
            len(result.chunks_docs) >= 1,
            len(result.chunks_industry) >= 1,
            len(result.chunks_playbook) >= 1,
        )

    result = orchestrator.ask(query, force_track=mode, top_k=3, no_generate=True)
    return (
        len(result.chunks_docs) >= 1,
        len(result.chunks_industry) >= 1,
        len(result.chunks_playbook) >= 1,
    )


def score_mode(
    orchestrator: HybridOrchestrator, cases: list[dict], mode: str
) -> tuple[ModeScore, list[dict]]:
    dual = triple = docs_h = hk_h = pb_h = 0
    details: list[dict] = []
    for case in cases:
        query = case["query"]
        has_docs, has_hk, has_pb = _coverage(orchestrator, query, mode)
        dual_ok = has_docs and has_hk
        triple_ok = dual_ok and has_pb
        if has_docs:
            docs_h += 1
        if has_hk:
            hk_h += 1
        if has_pb:
            pb_h += 1
        if dual_ok:
            dual += 1
        if triple_ok:
            triple += 1
        details.append(
            {
                "id": case.get("id"),
                "query": query,
                "mode": mode,
                "has_docs": has_docs,
                "has_hk_cde": has_hk,
                "has_playbook": has_pb,
                "dual": dual_ok,
                "triple": triple_ok,
            }
        )
    score = ModeScore(
        mode=mode,
        cases=len(cases),
        dual_hits=dual,
        triple_hits=triple,
        docs_hits=docs_h,
        hk_hits=hk_h,
        playbook_hits=pb_h,
    )
    return score, details


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Hybrid vs single-track coverage on hybrid cases"
    )
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hybrid_cases.jsonl",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Write JSON report path (default: eval/results/hybrid_vs_single.json)",
    )
    args = parser.parse_args(argv)

    all_cases = _load_cases(args.cases)
    hybrid_cases = [c for c in all_cases if c.get("expect_track") == "hybrid"]
    if not hybrid_cases:
        print("No hybrid expect cases found", file=sys.stderr)
        return 1

    orchestrator = HybridOrchestrator()
    scores: list[ModeScore] = []
    all_details: list[dict] = []
    for mode in TRACKS:
        score, details = score_mode(orchestrator, hybrid_cases, mode)
        scores.append(score)
        all_details.extend(details)

    print("Hybrid vs Single-Track Coverage")
    print(f"  hybrid expect cases: {len(hybrid_cases)}")
    print(
        f"  {'mode':<10} {'docs':>8} {'hk_cde':>8} {'playbook':>10} "
        f"{'DualRecall':>11} {'TripleRecall':>13}"
    )
    by_mode: dict[str, ModeScore] = {}
    for s in scores:
        by_mode[s.mode] = s
        n = s.cases
        print(
            f"  {s.mode:<10} "
            f"{s.docs_hits}/{n:>2} "
            f"{s.hk_hits}/{n:>2} "
            f"{s.playbook_hits}/{n:>4} "
            f"{s.dual_rate:>10.1%} "
            f"{s.triple_rate:>12.1%}"
        )

    hybrid = by_mode["hybrid"]
    singles = [by_mode[m] for m in ("docs", "hk_cde", "playbook")]
    best_single_triple = max(s.triple_rate for s in singles)
    best_single_dual = max(s.dual_rate for s in singles)

    print()
    print(
        f"  Verdict: hybrid TripleRecall {hybrid.triple_rate:.1%} "
        f"vs best single-track {best_single_triple:.1%}; "
        f"hybrid DualRecall {hybrid.dual_rate:.1%} "
        f"vs best single-track {best_single_dual:.1%}"
    )

    # Hybrid should dominate multi-source coverage.
    ok = (
        hybrid.triple_rate >= 0.80
        and hybrid.triple_rate > best_single_triple
        and hybrid.dual_rate >= 0.80
        and hybrid.dual_rate >= best_single_dual
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cases_file": str(args.cases.relative_to(PROJECT_ROOT)),
        "hybrid_case_count": len(hybrid_cases),
        "modes": {
            s.mode: {
                **asdict(s),
                "dual_rate": round(s.dual_rate, 4),
                "triple_rate": round(s.triple_rate, 4),
            }
            for s in scores
        },
        "verdict": {
            "hybrid_beats_best_single_on_triple": hybrid.triple_rate > best_single_triple,
            "hybrid_beats_or_ties_best_single_on_dual": hybrid.dual_rate
            >= best_single_dual,
            "pass": ok,
        },
        "details": all_details,
    }

    out = args.out or (PROJECT_ROOT / "eval" / "results" / "hybrid_vs_single.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  wrote {out.relative_to(PROJECT_ROOT)}")

    if not ok:
        print("FAIL", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
