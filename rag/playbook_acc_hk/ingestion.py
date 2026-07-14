"""解析 playbook Markdown：按 ## 切段入库，便于检索。"""

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


def _split_h2_sections(body: str) -> list[tuple[str, str]]:
    """返回 (section_title, section_body) 列表。"""
    matches = list(H2_RE.finditer(body))
    if not matches:
        cleaned = body.strip()
        return [("body", cleaned)] if cleaned else []

    sections: list[tuple[str, str]] = []
    # 前言（第一个 ## 之前）
    preamble = body[: matches[0].start()].strip()
    if len(preamble) >= 80:
        sections.append(("preamble", preamble))

    for index, match in enumerate(matches):
        heading = match.group(1).lstrip("#").strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        content = body[start:end].strip()
        if len(content) < 40:
            continue
        sections.append((heading, f"## {heading}\n\n{content}"))
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
        sections = _split_h2_sections(body)
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

        for section_title, section_body in sections:
            page_counter += 1
            slug = _slugify(section_title)
            source_url = playbook_url(chapter_id, slug)
            title = f"{chapter_title} — {section_title}"
            content_hash = hashlib.sha256(section_body.encode("utf-8")).hexdigest()
            # 把 capability / 推荐配置提示注入正文首行，便于向量命中且仍属 chunk 正文
            augmented = (
                f"[capability={capability}] [recommended_configuration]\n\n"
                f"{section_body}"
            )
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
