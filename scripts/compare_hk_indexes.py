#!/usr/bin/env python3
"""Compare high vs substantive HK indexes on grounded eval suites."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _run(env: dict[str, str], argv: list[str]) -> dict:
    proc = subprocess.run(
        [sys.executable, *argv],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    return {
        "cmd": " ".join(argv),
        "exit_code": proc.returncode,
        "pass": proc.returncode == 0,
        "stdout": (proc.stdout or "").strip(),
        "stderr": (proc.stderr or "").strip(),
    }


def _parse_metrics(stdout: str) -> dict:
    metrics: dict[str, float] = {}
    for line in stdout.splitlines():
        if "SectionRecall@1:" in line:
            metrics["section_recall_at_1"] = float(line.split(":")[1].split("%")[0]) / 100
        if "SectionRecall@3:" in line:
            metrics["section_recall_at_3"] = float(line.split(":")[1].split("%")[0]) / 100
        if "industry route accuracy:" in line:
            metrics["route_accuracy"] = float(line.split(":")[1].split("%")[0]) / 100
        if "docs false positive" in line:
            metrics["docs_false_positive"] = float(line.split(":")[1].strip())
        if "source accuracy:" in line:
            metrics["source_accuracy"] = float(line.split(":")[1].split("%")[0]) / 100
        if "key-fact retention:" in line:
            metrics["key_fact_retention"] = float(line.split(":")[1].split("%")[0]) / 100
        if "authority confusion accuracy:" in line:
            metrics["authority_confusion_accuracy"] = (
                float(line.split(":")[1].split("%")[0]) / 100
            )
    return metrics


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="A/B compare HK indexes")
    parser.add_argument(
        "--substantive-dir",
        default=".rag_data/industry_hk_cde_substantive",
    )
    parser.add_argument(
        "--substantive-collection",
        default="industry_hk_cde_substantive",
    )
    args = parser.parse_args(argv)

    base_env = os.environ.copy()
    configs = {
        "high": {
            **base_env,
            "INDUSTRY_HK_DATA_DIR": str(PROJECT_ROOT / ".rag_data" / "industry_hk_cde"),
            "INDUSTRY_HK_COLLECTION": "industry_hk_cde",
        },
        "substantive": {
            **base_env,
            "INDUSTRY_HK_DATA_DIR": str(PROJECT_ROOT / args.substantive_dir),
            "INDUSTRY_HK_COLLECTION": args.substantive_collection,
        },
    }

    suites = [
        ("hk_cde", ["scripts/eval_hk_cde.py"]),
        ("hk_cde_coverage", ["scripts/eval_hk_cde_coverage.py"]),
        # Generation authority checks are slow/LLM-dependent; A/B compare uses
        # retrieval + route gates. Run without --skip-generation for full authority.
        ("hk_cde_requirements", ["scripts/eval_hk_requirements.py", "--skip-generation"]),
    ]

    out_dir = PROJECT_ROOT / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    summary: dict = {"modes": {}}

    for mode, env in configs.items():
        mode_report = {"suites": {}}
        for name, cmd in suites:
            result = _run(env, cmd)
            result["metrics"] = _parse_metrics(result["stdout"])
            mode_report["suites"][name] = result
            print(f"\n=== {mode}/{name} exit={result['exit_code']} ===")
            print(result["stdout"])
            if result["stderr"]:
                print(result["stderr"], file=sys.stderr)
        out_path = out_dir / f"hk_{mode}.json"
        out_path.write_text(
            json.dumps(mode_report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary["modes"][mode] = mode_report

    high = summary["modes"]["high"]["suites"]
    sub = summary["modes"]["substantive"]["suites"]
    high_cov = high["hk_cde_coverage"]["metrics"]
    sub_cov = sub["hk_cde_coverage"]["metrics"]
    high_base = high["hk_cde"]["metrics"]
    sub_base = sub["hk_cde"]["metrics"]
    sub_req = sub["hk_cde_requirements"]["metrics"]

    gates = {
        "baseline_recall_ok": sub_base.get("section_recall_at_1", 0) >= 0.95,
        "docs_fp_zero": sub_base.get("docs_false_positive", 1) == 0,
        "coverage_r3_ok": sub_cov.get("section_recall_at_3", 0) >= 0.90,
        "source_acc_ok": sub_req.get("source_accuracy", 0) >= 0.90,
        "no_major_regression": (
            sub_base.get("section_recall_at_1", 0)
            >= high_base.get("section_recall_at_1", 0) - 0.05
        ),
        "substantive_suite_pass": all(
            suite.get("pass") for suite in sub.values()
        ),
    }
    summary["gates"] = gates
    # Flat substantive swap is only a diagnostic green light; production still
    # prefers high + on-demand shadow routing for case_study/terminology/software.
    summary["promote_substantive"] = all(gates.values())
    summary["promote_expanded_high"] = (
        high_base.get("section_recall_at_1", 0) >= 0.95
        and high_base.get("docs_false_positive", 1) == 0
        and high_cov.get("section_recall_at_3", 0) >= 0.90
        and high["hk_cde_requirements"]["metrics"].get("source_accuracy", 0) >= 0.90
        and all(suite.get("pass") for suite in high.values())
    )
    summary["promote"] = (
        summary["promote_substantive"] or summary["promote_expanded_high"]
    )
    if summary["promote_expanded_high"]:
        summary["accepted_scope"] = "high_with_routed_shadow"
    elif summary["promote_substantive"]:
        summary["accepted_scope"] = "substantive"
    else:
        summary["accepted_scope"] = "none"

    md_lines = [
        "# HK Index Comparison",
        "",
        "Source-grounded engineering benchmark (not customer acceptance).",
        "",
        "## Gates (substantive promotion)",
        "",
    ]
    for key, value in gates.items():
        md_lines.append(f"- `{key}`: **{'PASS' if value else 'FAIL'}**")
    md_lines.extend(
        [
            "",
            f"- `promote_substantive`: **{'YES' if summary['promote_substantive'] else 'NO'}**",
            f"- `promote_expanded_high`: **{'YES' if summary['promote_expanded_high'] else 'NO'}**",
            f"- **Accepted scope: `{summary['accepted_scope']}`**",
            "",
            "## Metrics",
            "",
            "| Mode | Baseline R@1 | Coverage R@1 | Coverage R@3 | Source Acc |",
            "|------|--------------|--------------|--------------|------------|",
            "| high | {h1:.1%} | {hc1:.1%} | {hc3:.1%} | {hs:.1%} |".format(
                h1=high_base.get("section_recall_at_1", 0),
                hc1=high_cov.get("section_recall_at_1", 0),
                hc3=high_cov.get("section_recall_at_3", 0),
                hs=high["hk_cde_requirements"]["metrics"].get("source_accuracy", 0),
            ),
            "| substantive | {s1:.1%} | {sc1:.1%} | {sc3:.1%} | {ss:.1%} |".format(
                s1=sub_base.get("section_recall_at_1", 0),
                sc1=sub_cov.get("section_recall_at_1", 0),
                sc3=sub_cov.get("section_recall_at_3", 0),
                ss=sub_req.get("source_accuracy", 0),
            ),
            "",
            "## Decision notes",
            "",
            "- After retrieval hardening, keep production on **`high`** and merge case_study / terminology / software_guide hits from the substantive shadow on explicit family intent.",
            "- Flat promotion of `substantive` may be gate-green for diagnostics, but is not the preferred production swap while everyday CDE queries should stay on the curated high pool.",
            "- Software-specific statutory appendices remain deferred from `substantive` and available via `--scope all`.",
            "- This is a source-grounded engineering benchmark, not customer acceptance or legal interpretation validation.",
            "",
        ]
    )
    md_path = PROJECT_ROOT / "eval" / "HK_INDEX_COMPARISON.md"
    md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    summary_path = out_dir / "hk_index_comparison.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(md_path.read_text(encoding="utf-8"))
    return 0 if summary["promote"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
