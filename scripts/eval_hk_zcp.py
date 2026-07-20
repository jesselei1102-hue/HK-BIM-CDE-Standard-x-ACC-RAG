#!/usr/bin/env python3
"""Eval ZCP BIMIP project-configuration retrieval (case-study reference)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.retrieval import IndustryHybridRetriever  # noqa: E402


def _load(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Eval ZCP project-config recall")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "hk_cde_zcp_cases.jsonl",
    )
    args = parser.parse_args(argv)

    # Prefer shadow substantive index if present.
    import os

    os.environ.setdefault(
        "INDUSTRY_HK_SHADOW_DATA_DIR", ".rag_data/industry_hk_cde_substantive"
    )
    # Also point primary config at substantive when available for ZCP-only eval.
    substantive = PROJECT_ROOT / ".rag_data" / "industry_hk_cde_substantive"
    if substantive.is_dir():
        os.environ["INDUSTRY_HK_DATA_DIR"] = str(substantive)
        os.environ["INDUSTRY_HK_COLLECTION"] = "industry_hk_cde_substantive"

    cases = _load(args.cases)
    retriever = IndustryHybridRetriever(get_industry_hk_config())
    hit3 = 0
    for case in cases:
        result = retriever.retrieve_with_debug(case["query"], top_k=3)
        needle = str(case.get("expected_section_contains") or "").lower()
        doc = str(case.get("expected_doc") or "").lower()
        ok = False
        for chunk in result.chunks:
            hay = f"{chunk.source_url} {chunk.title} {chunk.source_file}".lower()
            if doc and doc in hay and (not needle or needle in hay):
                ok = True
                break
            if needle and needle in hay:
                ok = True
                break
        if ok:
            hit3 += 1
        else:
            top = result.chunks[0].source_url if result.chunks else "(empty)"
            print(f"MISS {case['id']}: got {top}")

    recall = hit3 / max(len(cases), 1)
    print("HK ZCP Project-Config Eval")
    print(f"  cases: {len(cases)}")
    print(f"  SectionRecall@3: {recall:.1%} ({hit3}/{len(cases)})")
    if recall < 0.90:
        print("FAIL: ZCP R@3 < 90%", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
