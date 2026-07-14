#!/usr/bin/env python3
"""Run the full eval suite and write a dated summary under eval/RESULTS.md."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SUITE = [
    ("query_kb", ["scripts/eval_query_kb.py"]),
    ("hk_cde", ["scripts/eval_hk_cde.py"]),
    ("playbook", ["scripts/eval_playbook_acc_hk.py"]),
    ("hybrid", ["scripts/eval_hybrid.py"]),
    ("hybrid_vs_single", ["scripts/eval_hybrid_vs_single.py"]),
]


def _run(label: str, argv: list[str]) -> dict:
    cmd = [sys.executable, *argv]
    proc = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return {
        "name": label,
        "cmd": " ".join(argv),
        "exit_code": proc.returncode,
        "pass": proc.returncode == 0,
        "stdout": proc.stdout.strip(),
        "stderr": (proc.stderr or "").strip(),
        "output": out.strip(),
    }


def _markdown(results: list[dict], generated_at: str) -> str:
    lines = [
        "# Eval Results",
        "",
        f"Generated: `{generated_at}`",
        "",
        "Baseline proof that **hybrid** covers Docs + HK CDE + Playbook on "
        "cross-domain cases, while forced single-track modes cannot.",
        "",
        "## Suite summary",
        "",
        "| Suite | Result | Exit |",
        "|-------|--------|------|",
    ]
    for item in results:
        badge = "PASS" if item["pass"] else "FAIL"
        lines.append(f"| `{item['name']}` | **{badge}** | {item['exit_code']} |")

    vs_path = PROJECT_ROOT / "eval" / "results" / "hybrid_vs_single.json"
    if vs_path.exists():
        report = json.loads(vs_path.read_text(encoding="utf-8"))
        modes = report.get("modes", {})
        lines.extend(
            [
                "",
                "## Hybrid vs single-track (hybrid expect cases)",
                "",
                f"Cases: **{report.get('hybrid_case_count', 0)}** "
                f"(`{report.get('cases_file', 'eval/hybrid_cases.jsonl')}`)",
                "",
                "| Mode | Docs hit | HK CDE hit | Playbook hit | DualRecall | TripleRecall |",
                "|------|----------|------------|--------------|------------|--------------|",
            ]
        )
        for mode in ("docs", "hk_cde", "playbook", "hybrid"):
            m = modes.get(mode, {})
            n = m.get("cases", 0) or 1
            lines.append(
                "| `{mode}` | {d}/{n} | {h}/{n} | {p}/{n} | {dual:.1%} | {triple:.1%} |".format(
                    mode=mode,
                    d=m.get("docs_hits", 0),
                    h=m.get("hk_hits", 0),
                    p=m.get("playbook_hits", 0),
                    n=n,
                    dual=m.get("dual_rate", 0.0),
                    triple=m.get("triple_rate", 0.0),
                )
            )
        verdict = report.get("verdict", {})
        lines.extend(
            [
                "",
                "### Verdict",
                "",
                f"- Hybrid beats best single-track on TripleRecall: "
                f"**{verdict.get('hybrid_beats_best_single_on_triple')}**",
                f"- Hybrid ≥ best single-track on DualRecall: "
                f"**{verdict.get('hybrid_beats_or_ties_best_single_on_dual')}**",
                f"- Gate: **{'PASS' if verdict.get('pass') else 'FAIL'}**",
            ]
        )

    lines.extend(["", "## Raw outputs", ""])
    for item in results:
        lines.append(f"### `{item['name']}`")
        lines.append("")
        lines.append("```")
        lines.append(item["output"] or "(empty)")
        lines.append("```")
        lines.append("")

    lines.extend(
        [
            "## How to re-run",
            "",
            "```bash",
            "source .venv/bin/activate",
            "python scripts/run_eval_suite.py",
            "# optional: also check generated section headers (slow)",
            "python scripts/eval_hybrid.py --generate",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run all RAG evals and write RESULTS.md")
    parser.add_argument(
        "--skip-vs",
        action="store_true",
        help="Skip hybrid-vs-single comparison",
    )
    args = parser.parse_args(argv)

    suite = list(SUITE)
    if args.skip_vs:
        suite = [item for item in suite if item[0] != "hybrid_vs_single"]

    generated_at = datetime.now(timezone.utc).isoformat()
    results = [_run(label, cmd) for label, cmd in suite]

    out_dir = PROJECT_ROOT / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    latest = {
        "generated_at": generated_at,
        "results": [
            {
                "name": r["name"],
                "cmd": r["cmd"],
                "exit_code": r["exit_code"],
                "pass": r["pass"],
                "stdout": r["stdout"],
                "stderr": r["stderr"],
            }
            for r in results
        ],
    }
    latest_path = out_dir / "latest.json"
    latest_path.write_text(
        json.dumps(latest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    md = _markdown(results, generated_at)
    md_path = PROJECT_ROOT / "eval" / "RESULTS.md"
    md_path.write_text(md, encoding="utf-8")

    print(md)
    print(f"\nWrote {md_path.relative_to(PROJECT_ROOT)}")
    print(f"Wrote {latest_path.relative_to(PROJECT_ROOT)}")

    if any(not r["pass"] for r in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
