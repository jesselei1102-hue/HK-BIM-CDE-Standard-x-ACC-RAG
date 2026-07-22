#!/usr/bin/env python3
"""抽取 BD BIM GBP Submission 指南到 output/HK Standard/HK GBP/。

源文件：Guidelines for using Building Information Modelling in
General Building Plans Submission（BIMGBPS_e.pdf）。
独立于 hk_cde 主语料门禁，仅产出本地 Markdown + manifest。
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.extract_utils import (  # noqa: E402
    extract_page_text,
    sha256_file,
    slugify,
    utc_now,
)

OUT_DIR = PROJECT_ROOT / "output" / "HK Standard" / "HK GBP"
CORPUS_DIR = OUT_DIR / "corpus"
DEFAULT_SOURCE = Path("/Users/jiaxi/Documents/HK GBP Submission/BIMGBPS_e.pdf")
LOCAL_SOURCE = OUT_DIR / "BIMGBPS_e.pdf"
MANIFEST_PATH = OUT_DIR / "extract_manifest.json"

DOC = {
    "doc_id": "bd_bimgbps_2019",
    "authority_prefix": "BD BIM GBP Submission Guidelines 2019",
    "title": (
        "Guidelines for Using Building Information Modelling "
        "in General Building Plans Submission (2019)"
    ),
    # page ranges are 1-based inclusive PDF page numbers
    "sections": [
        ("Front Matter & Contents", 1, 5, "normal"),
        ("1-2. Background & Objectives", 6, 6, "high"),
        ("3. Scope", 7, 7, "high"),
        ("4. BIM File Submission Requirements", 8, 10, "high"),
        ("5.1 Technical Requirements", 11, 13, "high"),
        (
            "5.2 Essential Views for Composing the Prescribed Plans",
            14,
            32,
            "high",
        ),
        (
            "5.3 Essential Schedules for Composing the Prescribed Plans",
            33,
            47,
            "high",
        ),
        (
            "5.4 Amendment Plans and Alterations & Additions Plans",
            48,
            49,
            "high",
        ),
        (
            "5.5 Other Essential Information on Prescribed Plans or BIM Files for BD",
            50,
            52,
            "high",
        ),
        (
            "5.6 Other Information on Prescribed Plans or BIM Files for Other Departments",
            53,
            55,
            "high",
        ),
        ("6. File Structure and File Naming Convention", 56, 59, "high"),
        ("7. Review", 60, 60, "normal"),
        ("Appendix 1: Legends", 61, 64, "normal"),
        ("Appendix 2: Abbreviations", 65, 71, "normal"),
        ("Appendix 3: FS Notes", 72, 75, "normal"),
        (
            "Appendix 4: Planning Department Building Plan Vetting Form",
            76,
            80,
            "normal",
        ),
    ],
}


def _open_reader(path: Path) -> PdfReader:
    reader = PdfReader(str(path))
    if getattr(reader, "is_encrypted", False):
        result = reader.decrypt("")
        if result == 0:
            raise RuntimeError(f"无法解密 PDF（空密码失败）：{path}")
    return reader


def _render_md(
    *,
    section_title: str,
    section_id: str,
    page_start: int,
    page_end: int,
    priority: str,
    body: str,
    source_file: str,
) -> str:
    frontmatter = {
        "source_file": source_file,
        "doc_id": DOC["doc_id"],
        "section_id": section_id,
        "title": section_title,
        "page_start": page_start,
        "page_end": page_end,
        "authority": f"{DOC['authority_prefix']} §{section_title}",
        "authority_type": "statutory",
        "normative_weight": "guidance",
        "discipline": "statutory_submission",
        "lifecycle_stage": "statutory",
        "priority": priority,
        "language": "en",
        "source_url": (
            f"hkstd://{DOC['doc_id']}/{section_id}"
        ),
    }
    yaml_block = yaml.safe_dump(
        frontmatter, allow_unicode=True, sort_keys=False
    ).strip()
    return f"---\n{yaml_block}\n---\n\n# {section_title}\n\n{body.strip()}\n"


def extract(*, source: Path, dry_run: bool) -> dict:
    if not source.is_file():
        raise FileNotFoundError(f"缺少 PDF：{source}")

    if not dry_run:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        CORPUS_DIR.mkdir(parents=True, exist_ok=True)
        if source.resolve() != LOCAL_SOURCE.resolve():
            shutil.copy2(source, LOCAL_SOURCE)

    pdf_path = LOCAL_SOURCE if LOCAL_SOURCE.is_file() else source
    reader = _open_reader(pdf_path)
    page_count = len(reader.pages)
    rel = str(pdf_path.relative_to(PROJECT_ROOT))

    written = 0
    high = 0
    empty_pages = 0
    section_rows: list[dict] = []

    for title, start, end, priority in DOC["sections"]:
        if end > page_count:
            raise ValueError(
                f"节 {title!r} page_end={end} > pages={page_count}"
            )
        parts: list[str] = []
        for page in range(start, end + 1):
            text = extract_page_text(reader, page - 1).strip()
            if text:
                parts.append(f"<!-- page {page} -->\n{text}")
            else:
                empty_pages += 1
                parts.append(f"<!-- page {page}: empty/image-only -->")
        body = "\n\n".join(parts)
        section_id = f"{DOC['doc_id']}_{slugify(title)}"
        md = _render_md(
            section_title=title,
            section_id=section_id,
            page_start=start,
            page_end=end,
            priority=priority,
            body=body,
            source_file=rel,
        )
        out_path = CORPUS_DIR / f"{section_id}.md"
        if not dry_run:
            out_path.write_text(md, encoding="utf-8")
        written += 1
        if priority == "high":
            high += 1
        section_rows.append(
            {
                "section_id": section_id,
                "title": title,
                "page_start": start,
                "page_end": end,
                "priority": priority,
                "chars": len(body),
                "path": str(out_path.relative_to(PROJECT_ROOT)),
            }
        )
        print(f"  [{priority}] {out_path.name} p{start}-{end} chars={len(body)}")

    return {
        "doc_id": DOC["doc_id"],
        "title": DOC["title"],
        "path": rel,
        "sha256": sha256_file(pdf_path),
        "pages": page_count,
        "sections": written,
        "high_sections": high,
        "empty_or_image_pages": empty_pages,
        "authority_prefix": DOC["authority_prefix"],
        "extracted_at": utc_now(),
        "section_index": section_rows,
    }


def _write_readme(result: dict) -> None:
    lines = [
        "# HK GBP — BD BIM General Building Plans Submission Guidelines",
        "",
        "Buildings Department《Guidelines for Using Building Information Modelling "
        "in General Building Plans Submission》(2019)。",
        "",
        "## 来源",
        "",
        f"- 本地副本：`{result['path']}`",
        f"- 页数：{result['pages']}",
        f"- SHA256：`{result['sha256']}`",
        "",
        "## 抽取结果",
        "",
        f"- Markdown 目录：`corpus/`",
        f"- 章节数：{result['sections']}（high={result['high_sections']}）",
        f"- 空页/纯图页（按页计）：{result['empty_or_image_pages']}",
        "",
        "| 文件 | 页码 | 优先级 |",
        "|------|------|--------|",
    ]
    for row in result["section_index"]:
        lines.append(
            f"| `{Path(row['path']).name}` | "
            f"p{row['page_start']}-{row['page_end']} | {row['priority']} |"
        )
    lines.extend(
        [
            "",
            "## 重建",
            "",
            "```bash",
            "python scripts/extract_hk_gbp.py",
            "```",
            "",
            "说明：本目录目前独立存放，未自动并入 `knowledge/industry/hk_cde` 向量库。",
            "",
        ]
    )
    (OUT_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="抽取 BD BIM GBP 指南 PDF")
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE if DEFAULT_SOURCE.is_file() else LOCAL_SOURCE,
        help="源 PDF 路径",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    print("HK GBP / BD BIMGBPS extract")
    print(f"source: {args.source}")
    result = extract(source=args.source, dry_run=args.dry_run)
    payload = {
        "generated_at": utc_now(),
        "note": (
            "Standalone extract under output/HK Standard/HK GBP/. "
            "Not part of hk_cde page_ledger gate."
        ),
        "source": result,
    }
    if not args.dry_run:
        MANIFEST_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        _write_readme(result)
        print(f"\n写入 {MANIFEST_PATH}")
        print(f"写入 {OUT_DIR / 'README.md'}")
    print(
        f"完成：{result['sections']} 节 / {result['pages']} 页 "
        f"(high={result['high_sections']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
