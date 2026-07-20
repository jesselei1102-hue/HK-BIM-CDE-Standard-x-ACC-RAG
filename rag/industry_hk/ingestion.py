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

NOISE_TITLE_RE = re.compile(
    r"(front\s*matter|foreword|preface|acknowledg|table\s*of\s*contents|"
    r"^contents$|document\s*revision|disclaimer|member\s*list|"
    r"enquiry\s*and\s*feedback)",
    re.I,
)

VALID_SCOPES = {"high", "substantive", "all"}


@dataclass(frozen=True)
class IndustryCorpusConfig:
    source_dir: Path
    file_glob: str = "**/*.md"
    product: str = "hk_cde"
    priority_filter: str | None = "high"
    ingest_scope: str = "high"


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    meta = yaml.safe_load(match.group(1)) or {}
    body = text[match.end() :]
    return meta, body


def is_noise_section(meta: dict) -> bool:
    title = str(meta.get("title", ""))
    section_id = str(meta.get("section_id", ""))
    haystack = f"{title} {section_id}"
    return bool(NOISE_TITLE_RE.search(haystack))


def should_accept_section(meta: dict, *, ingest_scope: str) -> tuple[bool, str | None]:
    scope = (ingest_scope or "high").lower()
    if scope not in VALID_SCOPES:
        raise ValueError(f"unsupported ingest_scope: {ingest_scope}")
    priority = str(meta.get("priority", "normal"))
    doc_id = str(meta.get("doc_id") or "")
    source_path = str(meta.get("source_path") or meta.get("source_file") or "")
    # Template field stubs are checklist aids — keep out of default high pool.
    if scope == "high" and (
        doc_id.startswith("template")
        or "/templates/" in source_path
        or str(meta.get("authority_type") or "") == "template"
    ):
        return False, "template_deferred_from_high"
    if scope == "all":
        return True, None
    if scope == "high":
        if priority != "high":
            return False, f"priority_{priority}_skipped"
        return True, None
    # substantive: keep useful high/normal, drop navigation/noise
    if is_noise_section(meta):
        return False, "noise_section_skipped"
    if priority not in {"high", "normal"}:
        return False, f"priority_{priority}_skipped"
    authority_type = str(meta.get("authority_type") or "")
    if authority_type == "software_guide":
        return False, "software_guide_deferred"
    return True, None


def collect_indexed_manifest(documents: list[Document]) -> dict[str, list[str]]:
    """Derive indexed provenance sets from accepted Document source_urls / text."""
    doc_ids: set[str] = set()
    authority_types: set[str] = set()
    normative_weights: set[str] = set()
    for doc in documents:
        url = doc.source_url or ""
        if url.startswith("hk_cde://"):
            doc_ids.add(url[len("hk_cde://") :].split("/", 1)[0])
        header = (doc.text or "")[:400]
        for match in re.finditer(r"authority_type:\s*([a-z_]+)", header, re.I):
            authority_types.add(match.group(1).lower())
        for match in re.finditer(r"normative_weight:\s*([a-z_]+)", header, re.I):
            normative_weights.add(match.group(1).lower())
        # Templates
        if "/templates/" in (doc.source_file or ""):
            authority_types.add("template")
    return {
        "indexed_doc_ids": sorted(doc_ids),
        "indexed_authority_types": sorted(authority_types),
        "indexed_normative_weights": sorted(normative_weights),
    }


def load_industry_corpus(config: IndustryCorpusConfig) -> IngestionReport:
    report = IngestionReport()
    paths = sorted(config.source_dir.glob(config.file_glob))
    scope = (config.ingest_scope or "high").lower()
    if config.priority_filter is None and scope == "high":
        # Legacy: priority_filter=None meant ingest all.
        scope = "all"

    for path in paths:
        if not path.is_file():
            continue
        report.scanned_files += 1
        raw = path.read_text(encoding="utf-8")
        meta, body = _parse_frontmatter(raw)
        title = str(meta.get("title", path.stem))
        accept, reason = should_accept_section(meta, ingest_scope=scope)
        if not accept:
            report.rejected.append(
                RejectedPage(
                    source_file=str(path),
                    page_index=0,
                    line_start=1,
                    title=title,
                    source_url=str(meta.get("source_url", "")),
                    reason=reason or "filtered",
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
        # Keep a short machine-readable authority header for grounding/eval, but
        # avoid long duplicated prefixes dominating embeddings.
        authority_bits = []
        for key in (
            "doc_id",
            "section_id",
            "authority_type",
            "normative_weight",
            "discipline",
            "authority",
        ):
            value = meta.get(key)
            if value:
                authority_bits.append(f"{key}: {value}")
        prefix = ""
        if authority_bits:
            prefix = "[" + "; ".join(authority_bits) + "]\n\n"

        # Breadcrumb for nested LOD / object sections improves title disambiguation.
        parent = str(meta.get("parent_title") or "").strip()
        title_for_doc = title
        if parent and parent.lower() not in title.lower():
            title_for_doc = f"{parent} > {title}"

        report.documents.append(
            Document(
                title=title_for_doc,
                source_url=str(
                    meta.get("source_url", f"hk_cde://{meta.get('doc_id','unknown')}")
                ),
                text=prefix + cleaned,
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
