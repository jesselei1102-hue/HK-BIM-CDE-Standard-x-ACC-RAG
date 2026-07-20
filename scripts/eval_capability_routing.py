#!/usr/bin/env python3
"""语义路由 A/B 评测：semantic vs legacy track/capability 准确率、分歧与延迟。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from statistics import mean

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.config import get_config  # noqa: E402
from rag.orchestrator.classify import classify_intent, classify_intent_legacy  # noqa: E402
from rag.orchestrator.semantic_router import get_semantic_router  # noqa: E402


def _load_cases(path: Path) -> list[dict]:
    cases: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                cases.append(json.loads(line))
    return cases


def _eval_mode(cases: list[dict], mode: str) -> dict:
    track_hits = 0
    cap_hits = 0
    cap_total = 0
    false_hybrid = 0
    conflict_total = 0
    conflict_hits = 0
    false_folder = 0
    latencies: list[float] = []
    disagreements: list[dict] = []

    import rag.orchestrator.semantic_router as sem_module

    prev_mode = os.environ.get("RAG_SEMANTIC_ROUTER")
    if mode in {"semantic", "on", "shadow"}:
        os.environ["RAG_SEMANTIC_ROUTER"] = "on" if mode == "semantic" else mode
    try:
        sem_module._router = None
        router = get_semantic_router(get_config())

        for case in cases:
            query = case["query"]
            expect_track = case["expect_track"]
            expect_cap = case.get("expect_capability")

            sem = router.route(query) if mode != "legacy" else None
            if sem is not None:
                latencies.append(sem.latency_ms)

            if mode == "legacy":
                decision = classify_intent_legacy(query)
            elif mode == "semantic":
                decision = classify_intent(query, mode="on")
            else:
                decision = classify_intent(query, mode=mode)

            if decision.track == expect_track:
                track_hits += 1
            elif expect_track in {"docs", "hk_cde", "playbook"} and decision.track == "hybrid":
                false_hybrid += 1

            if "expect_capability" in case:
                cap_total += 1
                if decision.capability == expect_cap:
                    cap_hits += 1

            if case.get("conflict"):
                conflict_total += 1
                if decision.capability == expect_cap:
                    conflict_hits += 1

            tags = case.get("tags") or []
            if "negative" in tags and expect_cap is None and decision.capability == "folder":
                false_folder += 1

            legacy = classify_intent_legacy(query)
            if mode != "legacy" and (
                legacy.track != decision.track or legacy.capability != decision.capability
            ):
                disagreements.append(
                    {
                        "id": case.get("id"),
                        "query": query,
                        "legacy_track": legacy.track,
                        "legacy_capability": legacy.capability,
                        "semantic_track": decision.track,
                        "semantic_capability": decision.capability,
                        "semantic_latency_ms": sem.latency_ms if sem else None,
                    }
                )
    finally:
        if prev_mode is None:
            os.environ.pop("RAG_SEMANTIC_ROUTER", None)
        else:
            os.environ["RAG_SEMANTIC_ROUTER"] = prev_mode

    total = len(cases)
    return {
        "mode": mode,
        "total": total,
        "track_accuracy": track_hits / total if total else 0.0,
        "track_hits": track_hits,
        "capability_accuracy": cap_hits / cap_total if cap_total else 0.0,
        "capability_hits": cap_hits,
        "capability_total": cap_total,
        "false_hybrid": false_hybrid,
        "false_folder": false_folder,
        "conflict_accuracy": conflict_hits / conflict_total if conflict_total else 1.0,
        "conflict_hits": conflict_hits,
        "conflict_total": conflict_total,
        "latency_p50_ms": sorted(latencies)[len(latencies) // 2] if latencies else None,
        "latency_mean_ms": mean(latencies) if latencies else None,
        "disagreements": disagreements[:20],
        "disagreement_count": len(disagreements),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate semantic orchestrator routing")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "capability_routing_cases.jsonl",
    )
    parser.add_argument(
        "--min-track-acc",
        type=float,
        default=0.95,
        help="Minimum track accuracy for semantic-on mode",
    )
    parser.add_argument(
        "--min-cap-acc",
        type=float,
        default=0.95,
        help="Minimum capability accuracy for semantic-on mode",
    )
    parser.add_argument(
        "--max-latency-ms",
        type=float,
        default=150.0,
        help="p50 latency gate for semantic routing",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=PROJECT_ROOT / "eval" / "results" / "capability_routing.json",
    )
    args = parser.parse_args(argv)

    cases = _load_cases(args.cases)
    legacy_report = _eval_mode(cases, "legacy")
    semantic_report = _eval_mode(cases, "semantic")

    report = {
        "cases_file": str(args.cases),
        "case_count": len(cases),
        "legacy": legacy_report,
        "semantic_on": semantic_report,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Cases: {len(cases)}")
    print(
        f"Legacy  TrackAcc={legacy_report['track_accuracy']:.1%} "
        f"CapAcc={legacy_report['capability_accuracy']:.1%} "
        f"FalseHybrid={legacy_report['false_hybrid']} FalseFolder={legacy_report['false_folder']}"
    )
    print(
        f"Semantic TrackAcc={semantic_report['track_accuracy']:.1%} "
        f"CapAcc={semantic_report['capability_accuracy']:.1%} "
        f"FalseHybrid={semantic_report['false_hybrid']} FalseFolder={semantic_report['false_folder']} "
        f"p50={semantic_report['latency_p50_ms']}ms disagreements={semantic_report['disagreement_count']}"
    )

    ok = True
    if semantic_report["track_accuracy"] < args.min_track_acc:
        print(f"FAIL: semantic track accuracy < {args.min_track_acc:.0%}", file=sys.stderr)
        ok = False
    if semantic_report["capability_accuracy"] < args.min_cap_acc:
        print(f"FAIL: semantic capability accuracy < {args.min_cap_acc:.0%}", file=sys.stderr)
        ok = False
    if semantic_report["false_hybrid"] > 0:
        print("FAIL: semantic false hybrid > 0", file=sys.stderr)
        ok = False
    if semantic_report["false_folder"] > 0:
        print("FAIL: bare WIP false folder > 0", file=sys.stderr)
        ok = False
    if semantic_report["conflict_total"] and semantic_report["conflict_accuracy"] < 1.0:
        print("FAIL: conflict subset accuracy < 100%", file=sys.stderr)
        ok = False
    if (
        semantic_report["latency_p50_ms"] is not None
        and semantic_report["latency_p50_ms"] > args.max_latency_ms
    ):
        print(f"FAIL: p50 latency {semantic_report['latency_p50_ms']:.1f}ms > {args.max_latency_ms}ms", file=sys.stderr)
        ok = False
    if semantic_report["track_accuracy"] < legacy_report["track_accuracy"]:
        print("FAIL: semantic track accuracy below legacy", file=sys.stderr)
        ok = False
    if semantic_report["capability_accuracy"] < legacy_report["capability_accuracy"]:
        print("FAIL: semantic capability accuracy below legacy", file=sys.stderr)
        ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
