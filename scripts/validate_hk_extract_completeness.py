#!/usr/bin/env python3
"""香港 CDE 抽取完整性门禁：ingest 前必须 exit 0。"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.extract_utils import sha256_file  # noqa: E402
from rag.industry_hk.paths import (  # noqa: E402
    HK_CORPUS_DIR,
    HK_EXTRACT_REPORT_PATH,
    HK_OUTLINE_MAP_PATH,
    HK_PAGE_LEDGER_PATH,
    HK_PRIORITY_SECTIONS_PATH,
    HK_SOURCES_MANIFEST_PATH,
    HK_TEMPLATES_DIR,
    PDF_SOURCES,
    TEMPLATE_SOURCES,
)

TERM_PROBES = ("WIP", "Gateway", "Information Container", "PIR")
HIGH_MIN_CHARS = 200
QUALITY_THRESHOLD = 0.15


def _fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校验香港 CDE 抽取完整性")
    parser.add_argument(
        "--acknowledge-quality",
        action="store_true",
        help="确认已人工审核质量问题（empty/garbage 超阈值）",
    )
    args = parser.parse_args(argv)

    required = (
        HK_SOURCES_MANIFEST_PATH,
        HK_PAGE_LEDGER_PATH,
        HK_OUTLINE_MAP_PATH,
        HK_EXTRACT_REPORT_PATH,
        HK_PRIORITY_SECTIONS_PATH,
    )
    for path in required:
        if not path.is_file():
            return _fail(f"缺少产物：{path}")

    manifest = _read_json(HK_SOURCES_MANIFEST_PATH)
    ledger = _read_jsonl(HK_PAGE_LEDGER_PATH)
    outline = _read_json(HK_OUTLINE_MAP_PATH)
    report = _read_json(HK_EXTRACT_REPORT_PATH)
    priority = _read_json(HK_PRIORITY_SECTIONS_PATH)

    manifest_by_id = {item["doc_id"]: item for item in manifest.get("sources", [])}

    for spec in PDF_SOURCES:
        doc_id = spec["doc_id"]
        path = Path(spec["path"])
        if not path.is_file():
            return _fail(f"缺少 PDF：{path}")
        entry = manifest_by_id.get(doc_id)
        if entry is None:
            return _fail(f"manifest 未登记 PDF：{doc_id}")
        current_hash = sha256_file(path)
        if entry.get("sha256") != current_hash:
            return _fail(f"{doc_id} sha256 与 manifest 不一致，请重新抽取")

    for spec in TEMPLATE_SOURCES:
        path = Path(spec["path"])
        if not path.is_file():
            return _fail(f"缺少模板：{path}")

    for spec in PDF_SOURCES:
        doc_id = spec["doc_id"]
        page_count = manifest_by_id[doc_id]["page_count"]
        doc_ledger = [row for row in ledger if row["doc_id"] == doc_id]
        if len(doc_ledger) != page_count:
            return _fail(
                f"{doc_id} 页账行数 {len(doc_ledger)} != page_count {page_count}"
            )

    gaps = report.get("gaps", [])
    if gaps:
        return _fail(f"存在未映射页：{gaps}")

    for spec in PDF_SOURCES:
        doc_id = spec["doc_id"]
        page_count = manifest_by_id[doc_id]["page_count"]
        doc_ledger = [row for row in ledger if row["doc_id"] == doc_id]
        bad = sum(
            1
            for row in doc_ledger
            if row["status"] in {"empty", "garbage", "image_only"}
        )
        ratio = bad / max(page_count, 1)
        if ratio > QUALITY_THRESHOLD and not (
            args.acknowledge_quality or report.get("acknowledged_quality_issues")
        ):
            return _fail(
                f"{doc_id} empty/garbage/image_only 占比 {ratio:.1%} 超过 "
                f"{QUALITY_THRESHOLD:.0%}，需 --acknowledge-quality"
            )

    high_sections = [
        item for item in priority.get("sections", []) if item.get("priority") == "high"
    ]
    for item in high_sections:
        rel_path = item.get("source_path", "")
        md_path = PROJECT_ROOT / rel_path
        if not md_path.is_file():
            return _fail(f"high 章节缺失语料：{rel_path}")
        body = md_path.read_text(encoding="utf-8")
        if len(body) < HIGH_MIN_CHARS:
            return _fail(
                f"high 章节过短（<{HIGH_MIN_CHARS} chars）：{item['section_id']}"
            )
        doc_id = item["doc_id"]
        section_pages = [
            row
            for row in ledger
            if row["doc_id"] == doc_id
            and row.get("section_id") == item["section_id"]
            and item["page_start"] <= row["page"] <= item["page_end"]
        ]
        for row in section_pages:
            if row["status"] == "deferred":
                return _fail(f"high 页不得 deferred：{doc_id} p{row['page']}")

    unmapped_high = [
        row
        for row in outline.get("sections", [])
        if row.get("priority") == "high" and not row.get("mapped")
    ]
    if unmapped_high:
        return _fail(f"high 优先级 outline 未映射：{len(unmapped_high)} 条")

    for spec in TEMPLATE_SOURCES:
        num = spec["template_num"]
        template_md = HK_TEMPLATES_DIR / f"D{num}_fields.md"
        if not template_md.is_file():
            return _fail(f"缺少模板字段 MD：{template_md}")
        text = template_md.read_text(encoding="utf-8")
        field_lines = [
            line
            for line in text.splitlines()
            if line.startswith("- ") or line.startswith("|")
        ]
        if len(field_lines) < 1:
            return _fail(f"D{num} 字段数不足")

    corpus_text = ""
    for md_path in HK_CORPUS_DIR.rglob("*.md"):
        if md_path.parent.name == "templates":
            continue
        corpus_text += md_path.read_text(encoding="utf-8") + "\n"
    for term in TERM_PROBES:
        if term.lower() not in corpus_text.lower():
            return _fail(f"关键术语探针未命中 corpus：{term}")

    print("PASS: 完整性校验通过")
    print(
        f"  page_coverage_pct={report.get('page_coverage_pct')}% "
        f"outline_mapped_pct={report.get('outline_mapped_pct')}% "
        f"high_sections={len(high_sections)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
