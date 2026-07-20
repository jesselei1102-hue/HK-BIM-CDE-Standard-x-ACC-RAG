#!/usr/bin/env python3
"""Docs long-query retrieval eval (beyond short Query KB triggers)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.config import get_config  # noqa: E402
from rag.retrieval import HybridRetriever  # noqa: E402


DEFAULT_CASES = PROJECT_ROOT / "eval" / "docs_cases.jsonl"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Eval Docs long-query recall")
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--top-k", type=int, default=3)
    args = parser.parse_args(argv)

    if not args.cases.is_file():
        print(f"Missing cases file: {args.cases}", file=sys.stderr)
        return 1

    config = get_config()
    if not config.storage.chunks_path.is_file():
        print("Docs index missing; skip with PASS (optional track).", file=sys.stderr)
        print("PASS (skipped)")
        return 0

    retriever = HybridRetriever(config)
    cases = [
        json.loads(line)
        for line in args.cases.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    hits = 0
    for case in cases:
        result = retriever.retrieve_with_debug(case["query"], top_k=args.top_k)
        needle = str(case.get("expected_url_contains") or "").lower()
        ok = any(needle in (c.source_url or "").lower() for c in result.chunks)
        hits += int(ok)
        mark = "OK" if ok else "MISS"
        top = result.chunks[0].source_url if result.chunks else "-"
        print(f"[{mark}] {case.get('id', '?')} top1={top}")

    rate = hits / max(len(cases), 1)
    print(f"DocsRecall@{args.top_k}: {rate:.1%} ({hits}/{len(cases)})")
    if rate < 0.8:
        print("FAIL: DocsRecall < 80%", file=sys.stderr)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
