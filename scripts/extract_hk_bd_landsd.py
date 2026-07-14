#!/usr/bin/env python3
"""抽取 BD ADM-19 / ADV-34 与 LandsD BIM-GIS 指南到 hk_cde corpus。

独立于 extract_hk_cde_pdfs.py，不改动既有 page_ledger 门禁；
产出 Markdown 可直接被 ingest_industry_hk_cde.py 收录（priority=high）。
"""

from __future__ import annotations

import argparse
import json
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
from rag.industry_hk.paths import HK_CORPUS_DIR, HK_RESEARCH_DIR, section_url  # noqa: E402

SOURCE_DIR = PROJECT_ROOT / "output" / "HK Standard" / "BD_LandsD"
SUPPLEMENT_MANIFEST = HK_RESEARCH_DIR / "bd_landsd_sources_manifest.json"

# page ranges are 1-based inclusive
DOCS: list[dict] = [
    {
        "doc_id": "bd_adm19",
        "path": SOURCE_DIR / "BD_BD_ADM019.pdf",
        "authority_prefix": "BD PNAP ADM-19",
        "title": "Buildings Department PNAP ADM-19 Building Approval Process",
        "sections": [
            ("Introduction & Conformity Among Plans", 1, 1, "high"),
            ("Processing of Plan Submissions", 2, 2, "high"),
            ("Staged Submission of Essential Information on GBP", 3, 3, "high"),
            ("Enquiry Service, Concept Drawings & Computer Calculations", 4, 4, "high"),
            ("Consent to Extraction of Information from BIM Model", 5, 5, "high"),
            ("Minor Amendments & Concurrent Approval-Consent", 6, 9, "high"),
            ("Appendix A — GBP Fundamental Check Items", 10, 11, "high"),
            ("Appendix B — Superstructure Plan Checks", 12, 14, "normal"),
            ("Appendix C — Drainage Plan Checks", 15, 16, "normal"),
            ("Appendix D — ELS Works", 17, 17, "normal"),
            ("Appendix E — Guidelines for Concept Drawings", 18, 18, "high"),
            ("Appendix F — Electronic Submission / CAD-BIM Presentation", 19, 27, "high"),
            ("Appendix G — Amendments Not Qualified as Minor", 28, 32, "normal"),
            ("Appendix H — Fast Track Processing Request", 33, 33, "normal"),
            ("Appendix I — Fast Track Examples", 34, 34, "normal"),
            ("Appendix J — Curtain Wall / Window Wall / Cladding Fast Track", 35, 35, "normal"),
        ],
    },
    {
        "doc_id": "bd_adv34",
        "path": SOURCE_DIR / "BD_BD_ADV034.pdf",
        "authority_prefix": "BD PNAP ADV-34",
        "title": "Buildings Department PNAP ADV-34 Building Information Modelling (BIM)",
        "sections": [
            ("BIM Submissions — General Guidelines", 1, 2, "high"),
            ("Appendix A — Examples of BIM Applications for Plan Submissions", 3, 4, "high"),
        ],
    },
    {
        "doc_id": "landsd_bim_gis",
        "path": SOURCE_DIR
        / "LandsD_LandsD_BIM_and_GIS_Data_Integration_Guidelines_Jun2023.pdf",
        "authority_prefix": "LandsD BIM-GIS Guidelines Jun 2023",
        "title": "LandsD BIM and GIS Data Integration Guidelines (June 2023)",
        "sections": [
            ("Front Matter & Revision History", 1, 2, "normal"),
            ("Table of Contents", 3, 3, "normal"),
            ("Chapter 1 — Introduction", 4, 6, "high"),
            ("Chapter 2 — High Level Requirements on BIM Modelling", 7, 10, "high"),
            ("Chapter 3 — High Level Requirements on Data Conversion", 11, 12, "high"),
            ("Enquiry and Feedback", 13, 14, "normal"),
        ],
    },
]


def _render_md(
    *,
    spec: dict,
    section_title: str,
    section_id: str,
    page_start: int,
    page_end: int,
    priority: str,
    body: str,
    source_file: str,
) -> str:
    doc_id = spec["doc_id"]
    frontmatter = {
        "source_file": source_file,
        "doc_id": doc_id,
        "section_id": section_id,
        "title": section_title,
        "page_start": page_start,
        "page_end": page_end,
        "authority": f"{spec['authority_prefix']} §{section_title}",
        "priority": priority,
        "language": "en",
        "source_url": section_url(doc_id, section_id),
    }
    yaml_block = yaml.safe_dump(
        frontmatter, allow_unicode=True, sort_keys=False
    ).strip()
    return f"---\n{yaml_block}\n---\n\n# {section_title}\n\n{body.strip()}\n"


def extract_one(spec: dict, *, dry_run: bool) -> dict:
    path = Path(spec["path"])
    if not path.is_file():
        raise FileNotFoundError(f"缺少 PDF：{path}")
    reader = PdfReader(str(path))
    page_count = len(reader.pages)
    rel = str(path.relative_to(PROJECT_ROOT))
    out_dir = HK_CORPUS_DIR / spec["doc_id"]
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    high = 0
    for title, start, end, priority in spec["sections"]:
        if end > page_count:
            raise ValueError(
                f"{spec['doc_id']} 节 {title!r} page_end={end} > pages={page_count}"
            )
        parts: list[str] = []
        for page in range(start, end + 1):
            text = extract_page_text(reader, page - 1).strip()
            if text:
                parts.append(f"<!-- page {page} -->\n{text}")
        body = "\n\n".join(parts)
        section_id = f"{spec['doc_id']}_{slugify(title)}"
        md = _render_md(
            spec=spec,
            section_title=title,
            section_id=section_id,
            page_start=start,
            page_end=end,
            priority=priority,
            body=body,
            source_file=rel,
        )
        out_path = out_dir / f"{section_id}.md"
        if not dry_run:
            out_path.write_text(md, encoding="utf-8")
        written += 1
        if priority == "high":
            high += 1
        print(f"  [{priority}] {out_path.name} p{start}-{end} chars={len(body)}")

    return {
        "doc_id": spec["doc_id"],
        "title": spec["title"],
        "path": rel,
        "sha256": sha256_file(path),
        "pages": page_count,
        "sections": written,
        "high_sections": high,
        "authority_prefix": spec["authority_prefix"],
        "extracted_at": utc_now(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="抽取 BD/LandsD 补充港标 PDF")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    print("BD / LandsD supplement extract")
    results: list[dict] = []
    for spec in DOCS:
        print(f"\n== {spec['doc_id']} ==")
        results.append(extract_one(spec, dry_run=args.dry_run))

    payload = {
        "generated_at": utc_now(),
        "note": (
            "Supplement to CIC/DEVB corpus; not part of extract_hk_cde_pdfs "
            "page_ledger gate. Source copies under output/HK Standard/BD_LandsD/."
        ),
        "sources": results,
    }
    if not args.dry_run:
        HK_RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
        SUPPLEMENT_MANIFEST.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\n写入 {SUPPLEMENT_MANIFEST}")
    print(f"完成：{len(results)} 份 PDF，合计 "
          f"{sum(item['sections'] for item in results)} 节")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
