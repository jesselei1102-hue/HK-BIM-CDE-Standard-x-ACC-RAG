"""PDF 抽取与页账通用工具。"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pypdf import PdfReader
from pypdf.generic import Destination

DOTS_TOC_RE = re.compile(r"^(.+?)\s*\.{3,}\s*(\d+)\s*$", re.MULTILINE)
PRINTABLE_RE = re.compile(r"[\x20-\x7E\u00A0-\u024F\u3400-\u9FFF]")
REPLACEMENT_THRESHOLD = 0.08
GARBAGE_THRESHOLD = 0.35
MIN_OK_CHARS = 80


@dataclass(frozen=True)
class SectionSpec:
    section_id: str
    title: str
    page_start: int
    page_end: int
    level: int = 1
    priority: str = "normal"


@dataclass(frozen=True)
class PageRecord:
    doc_id: str
    page: int
    char_count: int
    status: str
    section_id: str | None
    skip_reason: str | None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def slugify(text: str, *, prefix: str = "") -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    text = re.sub(r"_+", "_", text)
    if prefix:
        text = f"{prefix}_{text}" if text else prefix
    return text[:80] or "section"


def classify_page_text(text: str) -> tuple[str, str | None]:
    stripped = (text or "").strip()
    char_count = len(stripped)
    if char_count == 0:
        return "empty", "no_extractable_text"
    printable = len(PRINTABLE_RE.findall(stripped))
    ratio = printable / max(char_count, 1)
    replacement = stripped.count("\ufffd") / max(char_count, 1)
    if ratio < GARBAGE_THRESHOLD or replacement > REPLACEMENT_THRESHOLD:
        if char_count < MIN_OK_CHARS:
            return "image_only", "low_printable_ratio"
        return "garbage", "low_printable_ratio"
    if char_count < MIN_OK_CHARS:
        return "empty", "too_short"
    return "ok", None


def extract_page_text(reader: PdfReader, page_index: int) -> str:
    try:
        return reader.pages[page_index].extract_text() or ""
    except Exception:
        return ""


def parse_dots_toc(text: str) -> list[tuple[int, str]]:
    entries: list[tuple[int, str]] = []
    for match in DOTS_TOC_RE.finditer(text):
        title = match.group(1).strip()
        page = int(match.group(2))
        if len(title) >= 3:
            entries.append((page, title))
    entries.sort(key=lambda item: (item[0], item[1]))
    deduped: list[tuple[int, str]] = []
    seen_pages: set[int] = set()
    for page, title in entries:
        if page in seen_pages:
            continue
        seen_pages.add(page)
        deduped.append((page, title))
    return deduped


def sections_from_page_starts(
    entries: list[tuple[int, str]],
    *,
    page_count: int,
    doc_id: str,
    min_level: int = 1,
) -> list[SectionSpec]:
    if not entries:
        return []
    specs: list[SectionSpec] = []
    for index, (page_start, title) in enumerate(entries):
        page_end = page_count
        for next_page, _ in entries[index + 1 :]:
            if next_page > page_start:
                page_end = next_page - 1
                break
        level = _heading_level(title)
        if level < min_level:
            continue
        section_id = slugify(title, prefix=f"{doc_id}")
        specs.append(
            SectionSpec(
                section_id=section_id,
                title=title,
                page_start=page_start,
                page_end=page_end,
                level=level,
            )
        )
    return specs


def _heading_level(title: str) -> int:
    match = re.match(r"^(\d+(?:\.\d+)*)", title.strip())
    if match:
        return match.group(1).count(".") + 1
    if title.strip().startswith("Appendix"):
        return 1
    return 1


def flatten_outline(
    reader: PdfReader,
    outline: Any,
    *,
    depth: int = 0,
) -> list[tuple[int, str, int]]:
    items: list[tuple[int, str, int]] = []
    if not outline:
        return items
    for entry in outline:
        if isinstance(entry, list):
            items.extend(flatten_outline(reader, entry, depth=depth + 1))
            continue
        if not isinstance(entry, Destination):
            continue
        title = str(getattr(entry, "title", "")).strip()
        try:
            page = reader.get_destination_page_number(entry) + 1
        except Exception:
            continue
        items.append((page, title, depth))
    return items


def devb_main_body_sections(reader: PdfReader, end_page: int) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for page_index in range(end_page):
        text = extract_page_text(reader, page_index)
        for line in text.splitlines():
            line = line.strip()
            if "FOR WORKS DEPARTMENTS" not in line.upper():
                continue
            rest = re.sub(
                r"(?i).*FOR WORKS DEPARTMENTS\s*",
                "",
                line,
            ).strip()
            if (
                not rest
                or len(rest) < 4
                or rest.upper() in {"P1", "P2"}
                or re.fullmatch(r"P\d+", rest, re.I)
            ):
                continue
            headings.append((page_index + 1, rest))
            break
    deduped: list[tuple[int, str]] = []
    prev_title = None
    for page, title in headings:
        if title != prev_title:
            deduped.append((page, title))
            prev_title = title
    return deduped


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def utc_now() -> str:
    return datetime.now(UTC).isoformat()
