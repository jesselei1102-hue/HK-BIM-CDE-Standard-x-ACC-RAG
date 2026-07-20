#!/usr/bin/env python3
"""Bounded HK MVP optimization loop runner (shadow-only, no production overwrite).

Records each iteration's metrics under eval/results/hk_mvp_loop/<n>/.
Does not auto-promote or auto-commit.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

HARD_GATES = {
    "docs_false_positive": 0,
    "classic_section_recall_at_1": 0.95,
    "query_kb_recall": 1.0,
}


def _run(cmd: list[str], env: dict | None = None) -> tuple[int, str]:
    merged = None
    if env:
        import os

        merged = {**os.environ, **env}
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=merged,
        check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode, output


def _parse_classic(output: str) -> dict:
    metrics: dict[str, float | int] = {}
    for line in output.splitlines():
        if "SectionRecall@1:" in line:
            # e.g. SectionRecall@1: 82.6% (19/23)
            pct = line.split("SectionRecall@1:", 1)[1].strip().split("%", 1)[0]
            metrics["classic_section_recall_at_1"] = float(pct) / 100.0
        if "docs false positive" in line:
            metrics["docs_false_positive"] = int(line.rsplit(":", 1)[-1].strip())
    return metrics


def _parse_query_kb(output: str) -> dict:
    metrics: dict[str, float] = {}
    for line in output.splitlines():
        if line.startswith("ShortQueryRecall@1:"):
            # ShortQueryRecall@1: 18/20 (90.0%)
            if "(" in line and "%" in line:
                pct = line.rsplit("(", 1)[-1].split("%", 1)[0]
                metrics["query_kb_recall"] = float(pct) / 100.0
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HK MVP bounded eval loop")
    parser.add_argument("--iteration", type=int, default=1)
    parser.add_argument("--note", type=str, default="")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=PROJECT_ROOT / "eval" / "results" / "hk_mvp_loop",
    )
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Skip authority generation checks in requirements eval",
    )
    args = parser.parse_args(argv)

    out = args.out_dir / f"{args.iteration:02d}"
    out.mkdir(parents=True, exist_ok=True)

    report: dict = {
        "iteration": args.iteration,
        "note": args.note,
        "started_at": datetime.now(UTC).isoformat(),
        "suites": {},
        "hard_gates": HARD_GATES,
    }

    suites = [
        ("hk_cde", [sys.executable, "scripts/eval_hk_cde.py"]),
        ("hk_cde_coverage", [sys.executable, "scripts/eval_hk_cde_coverage.py"]),
        (
            "hk_cde_requirements",
            [sys.executable, "scripts/eval_hk_requirements.py"]
            + (["--skip-generation"] if args.skip_generation else []),
        ),
        ("query_kb", [sys.executable, "scripts/eval_query_kb.py"]),
        ("hk_zcp", [sys.executable, "scripts/eval_hk_zcp.py"]),
    ]

    metrics: dict[str, float | int] = {}
    all_pass = True
    for name, cmd in suites:
        code, output = _run(cmd)
        (out / f"{name}.log").write_text(output, encoding="utf-8")
        report["suites"][name] = {"exit_code": code, "pass": code == 0}
        all_pass = all_pass and code == 0
        if name == "hk_cde":
            metrics.update(_parse_classic(output))
        if name == "query_kb":
            metrics.update(_parse_query_kb(output))

    report["metrics"] = metrics
    report["finished_at"] = datetime.now(UTC).isoformat()
    report["all_suites_pass"] = all_pass
    report["hard_gates_pass"] = all(
        float(metrics.get(key, -1)) >= float(threshold)
        if key != "docs_false_positive"
        else int(metrics.get(key, 99)) <= int(threshold)
        for key, threshold in HARD_GATES.items()
        if key in metrics
    )
    report["promote_candidate"] = bool(
        report["all_suites_pass"] and report["hard_gates_pass"]
    )
    report["stop_reason"] = None
    if report["promote_candidate"]:
        report["stop_reason"] = "mvp_gates_passed"
    elif args.iteration >= 8:
        report["stop_reason"] = "max_iterations"

    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["promote_candidate"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
