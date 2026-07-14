"""解析香港 CDE 行业语料 Markdown（YAML frontmatter + 正文）。"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from rag.config import PROJECT_ROOT
from rag.ingestion import Document, IngestionReport, RejectedPage

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


@dataclass(frozen=True)
class IndustryCorpusConfig:
    source_dir: Path
    file_glob: str = "**/*.md"
    product: str = "hk_cde"
    priority_filter: str | None = "high"


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    return meta, body


def load_industry_corpus(config: IndustryCorpusConfig) -> IngestionReport:
    report = IngestionReport()
    paths = sorted(config.source_dir.glob(config.file_glob))
    for path in paths:
        if not path.is_file():
            continue
        report.scanned_files += 1
        raw = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(raw)
        title = str(meta.get("title", path.stem))
        priority = str(meta.get("priority", "normal"))
        if config.priority_filter and priority != config.priority_filter:
            report.rejected.append(
                RejectedPage(
                    source_file=str(path),
                    page_index=0,
                    line_start=1,
                    title=title,
                    source_url=str(meta.get("source_url", "")),
                    reason=f"priority_{priority}_skipped",
                )
            )
            continue

        cleaned = body.strip()
        if len(cleaned) < 80:
            report.rejected.append(
                RejectedPage(
                    source_file=str(path),
                    page_index=int(meta.get("page_start", 0)),
                    line_start=1,
                    title=title,
                    source_url=str(meta.get("source_url", "")),
                    reason="too_short",
                )
            )
            continue

        content_hash = hashlib.sha256(cleaned.encode("utf-8")).hexdigest()
        report.documents.append(
            Document(
                title=title,
                source_url=str(
                    meta.get("source_url", f"hk_cde://{meta.get('doc_id','unknown')}")
                ),
                text=cleaned,
                source_file=str(path.relative_to(PROJECT_ROOT)),
                page_index=int(meta.get("page_start", 1)),
                line_start=1,
                product=config.product,
                content_hash=content_hash,
            )
        )
        report.accepted_pages += 1
        report.total_pages += 1

    return report
