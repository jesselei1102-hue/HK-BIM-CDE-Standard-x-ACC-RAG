#!/usr/bin/env python3
"""Benchmark retrieve latency for hybrid / single-track asks (no generation)."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from time import perf_counter

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.orchestrator.pipeline import HybridOrchestrator  # noqa: E402

DEFAULT_QUERIES = [
    "What is WIP in Hong Kong CDE?",
    "How to configure ACC folder permissions for HK CDE",
    "DEVB Harmonisation v3: THE WAY FORWARD",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Benchmark ask() retrieve latency")
    parser.add_argument("--corpus", default="hybrid", choices=["auto", "hybrid", "hk_cde", "docs", "playbook"])
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument(
        "--out",
        type=Path,
        default=PROJECT_ROOT / "eval" / "results" / "latency.json",
    )
    args = parser.parse_args(argv)

    orch = HybridOrchestrator()
    force = None if args.corpus == "auto" else args.corpus
    # Warmup loads Chroma / BM25.
    for _ in range(max(args.warmup, 0)):
        orch.ask(DEFAULT_QUERIES[0], force_track=force, no_generate=True)

    samples: list[dict] = []
    for query in DEFAULT_QUERIES:
        times: list[float] = []
        retrieve_times: list[float] = []
        for _ in range(args.runs):
            t0 = perf_counter()
            result = orch.ask(query, force_track=force, no_generate=True)
            wall_ms = (perf_counter() - t0) * 1000.0
            times.append(wall_ms)
            retrieve_times.append(float((result.debug.latency_ms or {}).get("retrieve", wall_ms)))
        samples.append(
            {
                "query": query,
                "track": force or "auto",
                "wall_ms": times,
                "retrieve_ms": retrieve_times,
                "p50_wall_ms": statistics.median(times),
                "p50_retrieve_ms": statistics.median(retrieve_times),
            }
        )

    report = {
        "corpus": args.corpus,
        "runs": args.runs,
        "samples": samples,
        "p50_wall_ms": statistics.median([s["p50_wall_ms"] for s in samples]),
        "p50_retrieve_ms": statistics.median([s["p50_retrieve_ms"] for s in samples]),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
