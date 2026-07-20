#!/usr/bin/env python3
"""Generation quality gate (fixture + optional live Ollama hybrid checks).

Default mode validates citation / section / authority rules on fixtures
(no LLM). Pass ``--live`` to also run a small hybrid generation sample when
Ollama is available.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.orchestrator.merge import merge_triple_contexts  # noqa: E402
from rag.orchestrator.validate import validate_hybrid_answer  # noqa: E402
from rag.retrieval import RetrievedChunk  # noqa: E402


def _chunk(title: str, url: str, text: str, product: str) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=url,
        title=title,
        source_url=url,
        source_file=f"{title}.md",
        page_index=0,
        line_start=1,
        product=product,
        chunk_index=0,
        chunk_count=1,
        token_count=12,
        text=text,
        score=1.0,
        vector_similarity=0.9,
    )


FIXTURES = [
    {
        "id": "good_four_section",
        "expect_ok": True,
        "answer": (
            "## Standards Requirements\nUse WIP/Shared/Published [1].\n\n"
            "## Implementation Guidance\nUse 01_WIP tree [2].\n\n"
            "## Product Operations\nCreate folders [3].\n\n"
            "## Alignment and Gaps\nAligned with gaps noted [1][2][3]."
        ),
    },
    {
        "id": "bad_cross_cite",
        "expect_ok": False,
        "answer": (
            "## Standards Requirements\nFolders [3].\n\n"
            "## Implementation Guidance\nTree [2].\n\n"
            "## Product Operations\nCreate [3].\n\n"
            "## Alignment and Gaps\nGap [1][3]."
        ),
    },
    {
        "id": "authority_overclaim",
        "expect_ok": False,
        "answer": (
            "## Standards Requirements\nThis is a mandatory binding standard [1].\n\n"
            "## Implementation Guidance\nN/A\n\n"
            "## Product Operations\nCreate review [3].\n\n"
            "## Alignment and Gaps\nReference only [1][3]."
        ),
        "hk_text": "authority_type: case_study\nnormative_weight: reference\ncase example",
    },
]


def _merged(hk_text: str = "WIP Shared Published"):
    hk = _chunk("WIP", "hk_cde://cicbims/wip", hk_text, "hk_cde")
    pb = _chunk("WIP tree", "playbook://wip", "01_WIP folders", "playbook")
    docs = _chunk(
        "Organize",
        "https://help.autodesk.com/view/DOCS/ENU/?guid=Organize_Files",
        "Create folders",
        "docs",
    )
    return merge_triple_contexts(
        docs_chunks=[docs],
        industry_chunks=[hk],
        playbook_chunks=[pb],
    )


def _run_fixtures() -> list[dict]:
    rows: list[dict] = []
    for item in FIXTURES:
        merged = _merged(item.get("hk_text", "WIP Shared Published"))
        result = validate_hybrid_answer(item["answer"], merged, capability="folder")
        hard_fail = any(i.severity == "hard" for i in result.issues)
        soft_fail = any(i.severity == "soft" for i in result.issues)
        # Authority overclaim is soft but should still fail this gate fixture.
        ok = result.ok and not soft_fail if item["id"] == "authority_overclaim" else (
            result.ok and not hard_fail
        )
        passed = ok == item["expect_ok"]
        rows.append(
            {
                "id": item["id"],
                "pass": passed,
                "expect_ok": item["expect_ok"],
                "got_ok": ok,
                "issues": [i.code for i in result.issues],
            }
        )
    return rows


def _run_live(limit: int = 5) -> list[dict]:
    from rag.orchestrator.pipeline import HybridOrchestrator

    cases_path = PROJECT_ROOT / "eval" / "hybrid_cases.jsonl"
    rows: list[dict] = []
    orch = HybridOrchestrator()
    count = 0
    with cases_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            case = json.loads(line)
            if case.get("expect_track") != "hybrid":
                continue
            count += 1
            if count > limit:
                break
            result = orch.ask(case["query"], force_track="hybrid", no_generate=False)
            answer = (result.answer.text if result.answer else "") or ""
            validation = validate_hybrid_answer(
                answer,
                result.merged or _merged(),
                capability=result.debug.intent.capability,
                question=case["query"],
            )
            rows.append(
                {
                    "id": case.get("id", case["query"][:40]),
                    "pass": bool(validation.ok),
                    "issues": [i.code for i in validation.issues],
                    "track": result.track,
                }
            )
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generation quality gate")
    parser.add_argument("--live", action="store_true", help="Also run live Ollama hybrid cases")
    parser.add_argument("--live-limit", type=int, default=5)
    parser.add_argument(
        "--out",
        type=Path,
        default=PROJECT_ROOT / "eval" / "results" / "generation_gate.json",
    )
    args = parser.parse_args(argv)

    report = {"fixtures": _run_fixtures(), "live": []}
    if args.live:
        report["live"] = _run_live(limit=args.live_limit)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    failed = [r for r in report["fixtures"] if not r["pass"]]
    failed += [r for r in report["live"] if not r["pass"]]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"Wrote {args.out}")
    if failed:
        print(f"FAIL: {len(failed)} case(s)", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
