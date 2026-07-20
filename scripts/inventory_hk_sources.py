#!/usr/bin/env python3
"""Inventory HK Standard sources: hash, dedupe, classify, report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.extract_utils import utc_now, write_json  # noqa: E402
from rag.industry_hk.paths import HK_SOURCE_INTAKE_REPORT_PATH  # noqa: E402
from rag.industry_hk.source_registry import inventory_sources  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inventory HK Standard source files")
    parser.add_argument(
        "--out",
        type=Path,
        default=HK_SOURCE_INTAKE_REPORT_PATH,
        help="Output JSON report path",
    )
    args = parser.parse_args(argv)

    report = inventory_sources()
    report["generated_at"] = utc_now()
    write_json(args.out, report)

    counts = report["counts"]
    print("HK source intake")
    print(f"  accepted: {counts['accepted']}")
    print(f"  extractable PDFs: {counts['extractable_pdfs']}")
    print(f"  image-heavy / non-extract: {counts['image_heavy']}")
    print(f"  missing: {counts['missing']}")
    print(f"  duplicates: {counts['duplicates']}")
    print(f"  wrote: {args.out}")
    if report["missing"]:
        for item in report["missing"]:
            print(f"MISSING {item['doc_id']}: {item['relative_path']}", file=sys.stderr)
        return 1
    if report["duplicates"]:
        for item in report["duplicates"]:
            print(
                f"DUPLICATE hash {item['sha256'][:12]} -> {item['doc_ids']}",
                file=sys.stderr,
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
