"""港标检索后处理：总览问句优先 CICBIMS/DEVB 正文，降低前言致谢噪声。"""

from __future__ import annotations

import re
from pathlib import Path

from rag.orchestrator.chunk_pin import load_chunk_by_url_part
from rag.orchestrator.classify import rewrite_industry_overview_query
from rag.retrieval import RetrievedChunk

_NOISE_URL_RE = re.compile(
    r"(acknowledgement|front_matter|"
    r"cic_beginner_cde_[^/]*_(preface|introduction|5_reference)|"
    r"cicbims_2024_preface|"
    r"cicbims_2024_12_acknowledgement|"
    r"cicbims_2024_9_reference|"
    r"appendix_i_iso_19650|"
    r"appendix_xiv)",
    re.I,
)

_CICBIMS_URL = "cicbims_2024"
_DEVB_URL = "devb_harmonisation_v3"
_BEGINNER_URL = "cic_beginner_cde"

CICBIMS_OVERVIEW_URL_PARTS = (
    "cicbims_2024/cicbims_2024_introduction",
    "cicbims_2024/cicbims_2024_1_digitalisation",
    "cicbims_2024/cicbims_2024_1_information_management_aligned_with_iso_19650",
)
DEVB_OVERVIEW_URL_PARTS = (
    "devb_harmonisation_v3/devb_harmonisation_v3_executive_summary",
    "devb_harmonisation_v3/devb_harmonisation_v3_table_of_contents",
    "devb_harmonisation_v3/devb_harmonisation_v3_federation_and_bim_model_naming",
)


def _want_devb(query: str) -> bool:
    text = query or ""
    rewritten = rewrite_industry_overview_query(text) or text
    return bool(
        re.search(r"harmonisation|harmonization|DEVB BIM", rewritten, re.I)
    )


def _want_cic(query: str) -> bool:
    if not rewrite_industry_overview_query(query or ""):
        return False
    return not _want_devb(query)


def load_industry_overview_pins(
    chunks_path: Path, query: str, limit: int = 2
) -> list[RetrievedChunk]:
    parts = (
        DEVB_OVERVIEW_URL_PARTS if _want_devb(query) else CICBIMS_OVERVIEW_URL_PARTS
    )
    if not rewrite_industry_overview_query(query):
        return []
    found: list[RetrievedChunk] = []
    seen: set[str] = set()
    for part in parts:
        chunk = load_chunk_by_url_part(chunks_path, part)
        if chunk and chunk.chunk_id not in seen:
            found.append(chunk)
            seen.add(chunk.chunk_id)
        if len(found) >= limit:
            break
    return found


def _score_chunk(query: str, chunk: RetrievedChunk, index: int) -> tuple[int, int]:
    url = chunk.source_url or ""
    want_devb = _want_devb(query)
    want_cic = _want_cic(query)

    if _NOISE_URL_RE.search(url):
        tier = 40
    elif want_devb and _DEVB_URL in url and "appendix_" not in url.lower():
        tier = 0
    elif want_devb and _DEVB_URL in url:
        tier = 8
    elif want_cic and _CICBIMS_URL in url and "introduction" in url:
        tier = 0
    elif want_cic and _CICBIMS_URL in url:
        tier = 1
    elif want_cic and _BEGINNER_URL in url:
        tier = 25
    elif want_cic or want_devb:
        tier = 15
    else:
        tier = 10
    return (tier, index)


def prefer_industry_chunks(
    query: str,
    chunks: list[RetrievedChunk],
    *,
    chunks_path: Path | None = None,
    limit: int | None = None,
) -> list[RetrievedChunk]:
    if not chunks and chunks_path is None:
        return chunks
    if not rewrite_industry_overview_query(query):
        return chunks

    pinned: list[RetrievedChunk] = []
    if chunks_path is not None:
        pinned = load_industry_overview_pins(
            chunks_path, query, limit=limit or max(len(chunks), 2) or 2
        )

    capped = limit or len(chunks) or 3
    merged: list[RetrievedChunk] = []
    seen: set[str] = set()
    for chunk in pinned + chunks:
        if chunk.chunk_id in seen:
            continue
        merged.append(chunk)
        seen.add(chunk.chunk_id)

    ranked = sorted(
        enumerate(merged),
        key=lambda item: _score_chunk(query, item[1], item[0]),
    )
    return [chunk for _, chunk in ranked][:capped]
