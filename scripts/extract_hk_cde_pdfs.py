#!/usr/bin/env python3
"""从香港 CDE 标准 PDF 按章节抽取英文原文到 Markdown 语料。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml
from pypdf import PdfReader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.extract_utils import (  # noqa: E402
    PageRecord,
    SectionSpec,
    append_jsonl,
    classify_page_text,
    devb_main_body_sections,
    extract_page_text,
    flatten_outline,
    parse_dots_toc,
    sections_from_page_starts,
    sha256_file,
    slugify,
    utc_now,
    write_json,
)
from rag.industry_hk.paths import (  # noqa: E402
    HK_CORPUS_DIR,
    HK_EXTRACT_REPORT_PATH,
    HK_OUTLINE_MAP_PATH,
    HK_PAGE_LEDGER_PATH,
    HK_PRIORITY_SECTIONS_PATH,
    HK_RESEARCH_DIR,
    HK_SECTIONS_INDEX_PATH,
    HK_SOURCES_MANIFEST_PATH,
    PDF_SOURCES,
    section_url,
)

HIGH_KEYWORDS = (
    "common data environment",
    "cde",
    "work in progress",
    "wip",
    "gateway",
    "shared",
    "published",
    "archive",
    "handover",
    "status code",
    "authorisation",
    "information container",
    "naming",
    "harmonisation",
    "oir",
    "air",
    "pir",
    "eir",
    "information requirement",
    "landsd",
    "federation",
    "responsibility",
    "iso 19650",
)


NOISE_TITLE_TOKENS = (
    "front matter",
    "foreword",
    "preface",
    "acknowledgement",
    "acknowledgment",
    "table of contents",
    "contents",
    "document revision",
    "disclaimer",
    "member list",
)


def _priority_for_section(doc_id: str, title: str, default_priority: str = "normal") -> str:
    lowered = title.lower().strip()
    if any(token in lowered for token in NOISE_TITLE_TOKENS):
        return "normal"
    if doc_id == "cic_beginner_cde":
        return "high"
    if doc_id == "cicbims_2024":
        if lowered.startswith("4.") or "common data environment" in lowered:
            return "high"
        if lowered.startswith("2.") and any(
            token in lowered
            for token in ("oir", "air", "pir", "eir", "information requirement")
        ):
            return "high"
        if lowered.startswith("1.") and "information management" in lowered:
            return "high"
    if doc_id == "devb_harmonisation_v3":
        if any(token in lowered for token in HIGH_KEYWORDS):
            return "high"
        if lowered.startswith("appendix") and any(
            token in lowered
            for token in (
                "terminolog",
                "responsibility",
                "naming",
                "information container",
                "landsd",
                "federation",
            )
        ):
            return "high"
    if doc_id in {
        "cic_mep_2021",
        "cic_uu_2021",
        "cic_object_guide_2021",
        "cic_statutory_plans_2020",
    }:
        if any(
            token in lowered
            for token in (
                "loin",
                "lod",
                "requirement",
                "responsibility",
                "submission",
                "model",
                "object",
                "naming",
                "information",
            )
        ):
            return "high"
        return default_priority
    if doc_id.startswith("cic_stat_") and doc_id.endswith("_2020"):
        return "normal"
    if doc_id in {"cic_dictionary_2024", "cic_amfm_case_2021", "cic_zcp_bimip_v15"}:
        return "normal"
    return default_priority


def _load_toc_override(doc_id: str) -> list[tuple[int, str]] | None:
    override_path = HK_RESEARCH_DIR / "toc_overrides" / f"{doc_id}.json"
    if not override_path.is_file():
        return None
    payload = json.loads(override_path.read_text(encoding="utf-8"))
    return [(int(item["page"]), str(item["title"])) for item in payload["sections"]]


def _build_sections(reader: PdfReader, spec: dict) -> list[SectionSpec]:
    doc_id = spec["doc_id"]
    page_count = len(reader.pages)
    strategy = spec["toc_strategy"]
    entries: list[tuple[int, str]] = []

    override = _load_toc_override(doc_id)
    if override:
        entries = override
    elif strategy == "dots":
        text = ""
        start, end = spec.get("toc_pages", (5, 9))
        for page_index in range(start, min(end, page_count)):
            text += extract_page_text(reader, page_index) + "\n"
        entries = parse_dots_toc(text)
        entries = [
            (page, title)
            for page, title in entries
            if not title.lower().startswith("bim standards contents")
        ]
    elif strategy == "outline":
        raw = flatten_outline(reader, reader.outline)
        entries = [(page, title) for page, title, _depth in raw]
    elif strategy == "devb_mixed":
        end_page = int(spec.get("main_body_end_page", 41))
        entries = devb_main_body_sections(reader, end_page)
        raw = flatten_outline(reader, reader.outline)
        appendix_entries = [
            (page, title)
            for page, title, _depth in raw
            if page > end_page or title.lower().startswith("appendix")
        ]
        entries.extend(appendix_entries)
        entries.sort(key=lambda item: (item[0], item[1]))
    else:
        raise ValueError(f"未知 toc_strategy: {strategy}")

    default_priority = str(spec.get("default_priority", "normal"))
    if not entries:
        # Fallback: whole-document section so intake never silently drops a PDF.
        return [
            SectionSpec(
                section_id=f"{doc_id}_full_document",
                title=spec.get("authority_prefix", doc_id),
                page_start=1,
                page_end=page_count,
                level=1,
                priority=default_priority,
            )
        ]

    sections = sections_from_page_starts(
        entries,
        page_count=page_count,
        doc_id=doc_id,
        min_level=1,
    )
    if sections and sections[0].page_start > 1:
        front = SectionSpec(
            section_id=f"{doc_id}_front_matter",
            title="Front Matter",
            page_start=1,
            page_end=sections[0].page_start - 1,
            level=0,
            priority="normal",
        )
        sections = [front, *sections]
    return [
        SectionSpec(
            section_id=section.section_id,
            title=section.title,
            page_start=section.page_start,
            page_end=section.page_end,
            level=section.level,
            priority=_priority_for_section(
                doc_id, section.title, default_priority=default_priority
            ),
        )
        for section in sections
    ]


def _page_to_section(
    page: int,
    sections: list[SectionSpec],
) -> str | None:
    matches = [
        section.section_id
        for section in sections
        if section.page_start <= page <= section.page_end
    ]
    if not matches:
        return None
    return matches[-1]


def _render_section_md(
    *,
    spec: dict,
    section: SectionSpec,
    body: str,
    source_file: str,
) -> str:
    doc_id = spec["doc_id"]
    frontmatter = {
        "source_file": source_file,
        "doc_id": doc_id,
        "section_id": section.section_id,
        "title": section.title,
        "page_start": section.page_start,
        "page_end": section.page_end,
        "authority": (
            f"{spec['authority_prefix']} §"
            f"{section.title.split()[0] if section.title else section.section_id}"
        ),
        "authority_type": spec.get("authority_type", "standard"),
        "normative_weight": spec.get("normative_weight", "recommended"),
        "discipline": spec.get("discipline", "general"),
        "lifecycle_stage": spec.get("lifecycle_stage", "project"),
        "publication_year": spec.get("publication_year"),
        "software": spec.get("software"),
        "priority": section.priority,
        "language": "en",
        "source_url": section_url(doc_id, section.section_id),
    }
    yaml_block = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        sort_keys=False,
    ).strip()
    return f"---\n{yaml_block}\n---\n\n# {section.title}\n\n{body.strip()}\n"


def extract_pdf(spec: dict) -> dict:
    path = Path(spec["path"])
    doc_id = spec["doc_id"]
    reader = PdfReader(str(path))
    page_count = len(reader.pages)
    sections = _build_sections(reader, spec)

    ledger_rows: list[dict] = []
    page_texts: dict[int, str] = {}
    for page in range(1, page_count + 1):
        text = extract_page_text(reader, page - 1)
        page_texts[page] = text
        status, skip_reason = classify_page_text(text)
        ledger_rows.append(
            {
                "doc_id": doc_id,
                "page": page,
                "char_count": len(text.strip()),
                "status": status,
                "section_id": _page_to_section(page, sections),
                "skip_reason": skip_reason,
            }
        )

    outline_map: list[dict] = []
    corpus_dir = HK_CORPUS_DIR / doc_id
    corpus_dir.mkdir(parents=True, exist_ok=True)
    sections_index_rows: list[dict] = []
    priority_rows: list[dict] = []

    for section in sections:
        parts: list[str] = []
        for page in range(section.page_start, section.page_end + 1):
            parts.append(page_texts.get(page, ""))
        body = "\n\n".join(part.strip() for part in parts if part.strip())
        md_path = corpus_dir / f"{section.section_id}.md"
        md_path.write_text(
            _render_section_md(
                spec=spec,
                section=section,
                body=body,
                source_file=str(path.relative_to(PROJECT_ROOT)),
            ),
            encoding="utf-8",
        )
        mapped = bool(body.strip())
        outline_map.append(
            {
                "title": section.title,
                "page_start": section.page_start,
                "page_end": section.page_end,
                "section_id": section.section_id,
                "mapped": mapped,
                "priority": section.priority,
            }
        )
        sections_index_rows.append(
            {
                "doc_id": doc_id,
                "section_id": section.section_id,
                "title": section.title,
                "source_url": section_url(doc_id, section.section_id),
                "source_path": str(md_path.relative_to(PROJECT_ROOT)),
                "page_start": section.page_start,
                "page_end": section.page_end,
                "char_count": len(body),
                "priority": section.priority,
            }
        )
        priority_rows.append(
            {
                "doc_id": doc_id,
                "section_id": section.section_id,
                "title": section.title,
                "authority": f"{spec['authority_prefix']} {section.title}",
                "authority_type": spec.get("authority_type", "standard"),
                "normative_weight": spec.get("normative_weight", "recommended"),
                "discipline": spec.get("discipline", "general"),
                "page_start": section.page_start,
                "page_end": section.page_end,
                "priority": section.priority,
                "source_path": str(md_path.relative_to(PROJECT_ROOT)),
            }
        )

    return {
        "doc_id": doc_id,
        "path": str(path.relative_to(PROJECT_ROOT)),
        "page_count": page_count,
        "section_count": len(sections),
        "ledger_rows": ledger_rows,
        "outline_map": outline_map,
        "sections_index_rows": sections_index_rows,
        "priority_rows": priority_rows,
    }


def _find_gaps(ledger_rows: list[dict], page_count: int, doc_id: str) -> list[int]:
    gaps: list[int] = []
    by_page = {row["page"]: row for row in ledger_rows if row["doc_id"] == doc_id}
    for page in range(1, page_count + 1):
        row = by_page.get(page)
        if row is None:
            gaps.append(page)
            continue
        if row["section_id"] is None:
            gaps.append(page)
    return gaps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="抽取香港 CDE PDF 章节语料")
    parser.add_argument(
        "--force",
        action="store_true",
        help="即使 manifest 哈希未变也重新抽取",
    )
    args = parser.parse_args(argv)

    HK_RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    HK_CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    if HK_PAGE_LEDGER_PATH.exists():
        HK_PAGE_LEDGER_PATH.unlink()
    if HK_SECTIONS_INDEX_PATH.exists():
        HK_SECTIONS_INDEX_PATH.unlink()

    manifest_sources: list[dict] = []
    all_ledger: list[dict] = []
    all_outline: list[dict] = []
    all_sections_index: list[dict] = []
    all_priority: list[dict] = []
    per_doc_reports: list[dict] = []

    for spec in PDF_SOURCES:
        path = Path(spec["path"])
        if not path.is_file():
            print(f"缺少源文件：{path}", file=sys.stderr)
            return 1

        file_hash = sha256_file(path)
        stat = path.stat()
        reader = PdfReader(str(path))
        page_count = len(reader.pages)

        manifest_sources.append(
            {
                "doc_id": spec["doc_id"],
                "path": str(path.relative_to(PROJECT_ROOT)),
                "sha256": file_hash,
                "byte_size": stat.st_size,
                "page_count": page_count,
                "mtime": stat.st_mtime,
                "kind": "pdf",
                "authority_type": spec.get("authority_type", "standard"),
                "normative_weight": spec.get("normative_weight", "recommended"),
                "discipline": spec.get("discipline", "general"),
                "lifecycle_stage": spec.get("lifecycle_stage", "project"),
                "publication_year": spec.get("publication_year"),
                "software": spec.get("software"),
            }
        )

        print(f"抽取 {spec['doc_id']} ({page_count} 页)...")
        result = extract_pdf(spec)
        all_ledger.extend(result["ledger_rows"])
        all_outline.extend(
            {**row, "doc_id": spec["doc_id"]} for row in result["outline_map"]
        )
        all_sections_index.extend(result["sections_index_rows"])
        all_priority.extend(result["priority_rows"])

        ok_pages = sum(1 for row in result["ledger_rows"] if row["status"] == "ok")
        empty_pages = sum(
            1 for row in result["ledger_rows"] if row["status"] == "empty"
        )
        garbage_pages = sum(
            1
            for row in result["ledger_rows"]
            if row["status"] in {"garbage", "image_only"}
        )
        gaps = _find_gaps(result["ledger_rows"], page_count, spec["doc_id"])
        per_doc_reports.append(
            {
                "doc_id": spec["doc_id"],
                "page_count": page_count,
                "section_count": result["section_count"],
                "ok_pages": ok_pages,
                "empty_pages": empty_pages,
                "garbage_pages": garbage_pages,
                "page_coverage_pct": round(ok_pages / page_count * 100, 2),
                "gaps": gaps,
            }
        )

    write_json(
        HK_SOURCES_MANIFEST_PATH,
        {
            "generated_at": utc_now(),
            "sources": manifest_sources,
        },
    )
    append_jsonl(HK_PAGE_LEDGER_PATH, all_ledger)
    write_json(HK_OUTLINE_MAP_PATH, {"sections": all_outline})
    append_jsonl(HK_SECTIONS_INDEX_PATH, all_sections_index)
    write_json(
        HK_PRIORITY_SECTIONS_PATH,
        {
            "generated_at": utc_now(),
            "sections": all_priority,
        },
    )

    total_pages = sum(item["page_count"] for item in per_doc_reports)
    total_ok = sum(item["ok_pages"] for item in per_doc_reports)
    all_gaps = [gap for item in per_doc_reports for gap in item["gaps"]]
    mapped = sum(1 for row in all_outline if row["mapped"])
    outline_mapped_pct = round(mapped / max(len(all_outline), 1) * 100, 2)

    report = {
        "generated_at": utc_now(),
        "documents": per_doc_reports,
        "page_coverage_pct": round(total_ok / max(total_pages, 1) * 100, 2),
        "outline_mapped_pct": outline_mapped_pct,
        "gaps": all_gaps,
        "acknowledged_quality_issues": False,
        "term_probes": {},
    }
    write_json(HK_EXTRACT_REPORT_PATH, report)

    print(f"页账写入：{HK_PAGE_LEDGER_PATH}")
    print(f"语料目录：{HK_CORPUS_DIR}")
    print(f"覆盖率：{report['page_coverage_pct']}% | gaps={len(all_gaps)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
