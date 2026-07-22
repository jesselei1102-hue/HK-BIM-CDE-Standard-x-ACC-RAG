"""解析 playbook Markdown：按 ## / ### 切段入库，便于检索。"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from rag.config import PROJECT_ROOT
from rag.ingestion import Document, IngestionReport, RejectedPage
from rag.playbook_acc_hk.paths import playbook_url

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
H2_RE = re.compile(r"(?m)^(## .+)$")
H3_RE = re.compile(r"(?m)^(### .+)$")
FENCE_RE = re.compile(r"(?m)^```")


@dataclass(frozen=True)
class PlaybookCorpusLoadConfig:
    source_dir: Path
    file_glob: str = "*.md"
    product: str = "playbook_acc_hk"


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    return meta, body


def _slugify(heading: str) -> str:
    text = heading.lstrip("#").strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text, flags=re.UNICODE)
    text = re.sub(r"_+", "_", text).strip("_")
    return text[:80] or "section"


def _protected_spans(text: str) -> list[tuple[int, int]]:
    """Return [start, end) spans that must not be split (fenced code)."""
    spans: list[tuple[int, int]] = []
    opens = list(FENCE_RE.finditer(text))
    i = 0
    while i + 1 < len(opens):
        start = opens[i].start()
        end = opens[i + 1].end()
        # include until end of closing fence line
        nl = text.find("\n", end)
        end = len(text) if nl < 0 else nl + 1
        spans.append((start, end))
        i += 2
    return spans


def _in_protected(pos: int, spans: list[tuple[int, int]]) -> bool:
    return any(start <= pos < end for start, end in spans)


def _heading_matches(body: str) -> list[re.Match[str]]:
    spans = _protected_spans(body)
    matches: list[re.Match[str]] = []
    for pattern in (H2_RE, H3_RE):
        for match in pattern.finditer(body):
            if not _in_protected(match.start(), spans):
                matches.append(match)
    matches.sort(key=lambda m: m.start())
    return matches


def _split_semantic_sections(body: str) -> list[tuple[str, str, str]]:
    """Return (section_title, breadcrumb, section_body) list.

    Prefer H3 units under an H2 breadcrumb; fall back to H2; then whole body.
    """
    matches = _heading_matches(body)
    if not matches:
        cleaned = body.strip()
        return [("body", "", cleaned)] if cleaned else []

    sections: list[tuple[str, str, str]] = []
    preamble = body[: matches[0].start()].strip()
    if len(preamble) >= 80:
        sections.append(("preamble", "", preamble))

    current_h2 = ""
    for index, match in enumerate(matches):
        raw_heading = match.group(1)
        level = 3 if raw_heading.startswith("###") else 2
        heading = raw_heading.lstrip("#").strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        if level == 2:
            current_h2 = heading
            # If the next match is an H3 under this H2, skip emitting the H2 shell
            # unless there is substantial intro text before the first H3.
            next_is_h3 = (
                index + 1 < len(matches)
                and matches[index + 1].group(1).startswith("###")
            )
            if next_is_h3:
                if len(content) >= 80:
                    breadcrumb = heading
                    block = f"## {heading}\n\n{content}"
                    sections.append((f"{heading} — intro", breadcrumb, block))
                continue
            if len(content) < 40:
                continue
            block = f"## {heading}\n\n{content}"
            sections.append((heading, heading, block))
            continue

        # H3
        if len(content) < 40:
            continue
        breadcrumb = f"{current_h2} > {heading}" if current_h2 else heading
        header = f"## {current_h2}\n\n### {heading}" if current_h2 else f"### {heading}"
        block = f"{header}\n\n{content}"
        sections.append((heading, breadcrumb, block))
    return sections


def load_playbook_corpus(config: PlaybookCorpusLoadConfig) -> IngestionReport:
    report = IngestionReport()
    paths = sorted(config.source_dir.glob(config.file_glob))
    page_counter = 0
    for path in paths:
        if not path.is_file():
            continue
        report.scanned_files += 1
        raw = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(raw)
        chapter_title = str(meta.get("title", path.stem))
        chapter_id = path.stem
        capability = str(meta.get("capability", chapter_id))
        domain = str(meta.get("domain", "mixed"))
        source_type = str(meta.get("source_type", "playbook_recommended"))
        precedence = meta.get("precedence_rank", 20)
        sections = _split_semantic_sections(body)
        if not sections:
            report.rejected.append(
                RejectedPage(
                    source_file=str(path),
                    page_index=0,
                    line_start=1,
                    title=chapter_title,
                    source_url=playbook_url(chapter_id),
                    reason="too_short",
                )
            )
            continue

        for section_title, breadcrumb, section_body in sections:
            page_counter += 1
            slug = _slugify(section_title)
            source_url = playbook_url(chapter_id, slug)
            title = (
                f"{chapter_title} — {breadcrumb}"
                if breadcrumb
                else f"{chapter_title} — {section_title}"
            )
            content_hash = hashlib.sha256(section_body.encode("utf-8")).hexdigest()
            # Inject routing tags into body so vectors carry domain/capability/precedence.
            tag_line = (
                f"[capability={capability}] [domain={domain}] "
                f"[source_type={source_type}] [precedence={precedence}] "
                f"[recommended_configuration]"
            )
            if breadcrumb:
                tag_line += f"\n[section={breadcrumb}]"
            augmented = f"{tag_line}\n\n{section_body}"
            report.documents.append(
                Document(
                    title=title,
                    source_url=source_url,
                    text=augmented,
                    source_file=str(path.relative_to(PROJECT_ROOT)),
                    page_index=page_counter,
                    line_start=1,
                    product=config.product,
                    content_hash=content_hash,
                )
            )
            report.accepted_pages += 1
            report.total_pages += 1

    return report
