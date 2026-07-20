"""行业 HK CDE 混合检索（复用产品轨逻辑，独立 collection + 文档族重排）。"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from rag.config import AppConfig, CorpusConfig, QueryKBConfig
from rag.industry_hk.config import IndustryHKConfig, get_industry_hk_config
from rag.industry_hk.source_family import (
    doc_id_from_url,
    exact_title_bonus,
    extract_explicit_section_title,
    is_section_number_title,
    normalize_title,
    resolve_source_family,
)
from rag.orchestrator.industry_prefer import prefer_industry_chunks
from rag.retrieval import (
    HybridRetriever,
    RetrievedChunk,
    RetrievalDebugInfo,
    RetrievalResult,
)


class IndustryStorageBridge:
    """为 HybridRetriever / KBRoutingIndex 提供行业 storage 属性。"""

    def __init__(self, industry_storage) -> None:
        self._s = industry_storage

    @property
    def data_dir(self):
        return self._s.data_dir

    @property
    def collection_name(self) -> str:
        return self._s.collection_name

    @property
    def chroma_dir(self):
        return self._s.chroma_dir

    @property
    def chunks_path(self):
        return self._s.chunks_path

    @property
    def manifest_path(self):
        return self._s.manifest_path

    @property
    def kb_chroma_dir(self):
        return self._s.kb_chroma_dir

    @property
    def kb_collection_name(self) -> str:
        return self._s.kb_collection_name

    @property
    def kb_manifest_path(self):
        return self._s.kb_manifest_path


def industry_to_app_config(config: IndustryHKConfig) -> AppConfig:
    return AppConfig(
        corpus=CorpusConfig(
            source_dir=config.corpus.source_dir,
            file_glob=config.corpus.file_glob,
            product=config.corpus.product,
        ),
        models=config.models,
        chunks=config.chunks,
        retrieval=config.retrieval,
        query_kb=QueryKBConfig(
            enabled=config.query_kb.enabled,
            kb_path=config.query_kb.kb_path,
            short_query_max_chars=config.query_kb.short_query_max_chars,
            trigger_sim=config.query_kb.trigger_sim,
            require_sim_improvement=config.query_kb.require_sim_improvement,
            target_url_boost=config.query_kb.target_url_boost,
            contains_max_length_delta=config.query_kb.contains_max_length_delta,
            route_top_k=config.query_kb.route_top_k,
            min_route_sim=config.query_kb.min_route_sim,
        ),
        storage=IndustryStorageBridge(config.storage),  # type: ignore[arg-type]
    )


def _shadow_chunks_path() -> Path | None:
    raw = os.environ.get("INDUSTRY_HK_SHADOW_DATA_DIR", "").strip()
    if raw:
        path = Path(raw) / "chunks.jsonl"
        return path if path.is_file() else None
    candidate = Path(".rag_data/industry_hk_cde_substantive/chunks.jsonl")
    return candidate if candidate.is_file() else None


def _mentions_template(query: str) -> bool:
    return bool(
        re.search(r"\bD[1-9]\b|template\s*field|附录\s*D|Appendix\s*D", query or "", re.I)
    )


def _load_shadow_chunks_for_docs(
    chunks_path: Path, doc_ids: tuple[str, ...], query: str = "", limit: int = 12
) -> list[RetrievedChunk]:
    from rag.industry_hk.source_family import exact_title_bonus

    candidates: list[tuple[float, RetrievedChunk]] = []
    tokens = [t for t in re.split(r"[^\w]+", (query or "").lower()) if len(t) >= 3]
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            url = record.get("source_url", "")
            doc_id = doc_id_from_url(url)
            if doc_id not in doc_ids:
                continue
            hay = f"{record.get('title','')} {record.get('text','')[:800]}".lower()
            overlap = sum(1 for token in tokens if token in hay) if tokens else 0
            score = 0.55 + 0.15 * overlap
            score += exact_title_bonus(query, record.get("title") or "")
            # Prefer early chunks that usually carry authority headers / intros.
            score += max(0.0, 0.2 - 0.02 * int(record.get("chunk_index") or 0))
            # Prefer figure transcription / concrete folder trees for folder queries.
            qlow = (query or "").lower()
            if "folder" in qlow and (
                "01_revit model" in hay
                or "figures_transcription" in (record.get("source_url") or "").lower()
            ):
                score += 2.5
            candidates.append(
                (
                    score,
                    RetrievedChunk(
                        chunk_id=record["chunk_id"],
                        title=record["title"],
                        source_url=record["source_url"],
                        source_file=record["source_file"],
                        page_index=int(record["page_index"]),
                        line_start=int(record["line_start"]),
                        product=record["product"],
                        chunk_index=int(record["chunk_index"]),
                        chunk_count=int(record["chunk_count"]),
                        token_count=int(record["token_count"]),
                        text=record["text"],
                        score=score,
                        # Synthetic similarity so generation refuse gates treat
                        # shadow family hits as usable evidence.
                        vector_similarity=min(0.95, 0.55 + 0.08 * overlap),
                    ),
                )
            )
    candidates.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in candidates[:limit]]


def _record_to_chunk(record: dict, score: float) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=record["chunk_id"],
        title=record["title"],
        source_url=record["source_url"],
        source_file=record["source_file"],
        page_index=int(record["page_index"]),
        line_start=int(record["line_start"]),
        product=record["product"],
        chunk_index=int(record["chunk_index"]),
        chunk_count=int(record["chunk_count"]),
        token_count=int(record["token_count"]),
        text=record["text"],
        score=score,
        vector_similarity=min(0.99, 0.7 + 0.05 * score),
    )


def _load_explicit_title_pins(
    chunks_path: Path,
    query: str,
    *,
    doc_ids: tuple[str, ...] | None = None,
    limit: int = 6,
) -> list[RetrievedChunk]:
    """Inject exact section-title matches so they cannot fall out of top-k."""
    explicit = extract_explicit_section_title(query)
    if not explicit:
        return []
    explicit_n = normalize_title(explicit)
    explicit_core = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", explicit_n).strip()
    if len(explicit_core) < 4 and not re.match(r"^\d", explicit_n):
        return []

    hits: list[tuple[float, RetrievedChunk]] = []
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            url = record.get("source_url", "")
            doc_id = doc_id_from_url(url)
            if doc_ids and doc_id not in doc_ids:
                continue
            title = record.get("title") or ""
            title_n = normalize_title(title)
            title_core = re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", title_n).strip()
            score = exact_title_bonus(query, title)
            if score < 3.0 and title_n != explicit_n and title_core != explicit_core:
                continue
            if score < 1.5:
                continue
            # Prefer chunk 0 of the matching section page.
            score += max(0.0, 0.3 - 0.03 * int(record.get("chunk_index") or 0))
            hits.append((score, _record_to_chunk(record, score=max(score, 4.0))))
    hits.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in hits[:limit]]


def _load_keyword_section_pins(
    chunks_path: Path,
    query: str,
    *,
    doc_ids: tuple[str, ...] | None = None,
    limit: int = 4,
) -> list[RetrievedChunk]:
    """Pin canonical sections for common Chinese / keyword intents."""
    q = query or ""
    url_needles: list[str] = []
    if re.search(r"naming|命名|Information\s+Container|federation", q, re.I):
        url_needles.append("federation_and_bim_model_naming")
    if re.search(r"\bLOIN\b|level of information need|信息需求|資訊需求", q, re.I):
        url_needles.append("level_of_information_need")
    if re.search(r"level of documentation|\bDOC\b|文档等级|文檔等級", q, re.I):
        url_needles.append("level_of_documentation")
    if re.search(
        r"(?:ZCP|Zero\s*Carbon\s*Park).{0,40}folder|"
        r"folder.{0,40}(?:ZCP|Zero\s*Carbon\s*Park)|"
        r"ZCP\s*standardised\s*folder|"
        r"01_Revit\s*Model|"
        r"Figure\s*9.{0,20}ZCP|"
        r"ZCP.{0,20}Figure\s*9",
        q,
        re.I,
    ):
        url_needles.extend(
            [
                "cic_zcp_bimip_v15_figures_transcription",
                "cic_zcp_bimip_v15_2_19_handover_procedure",
            ]
        )
    if not url_needles:
        return []

    hits: list[tuple[float, RetrievedChunk]] = []
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            url = (record.get("source_url") or "").lower()
            doc_id = doc_id_from_url(record.get("source_url") or "")
            if doc_ids and doc_id not in doc_ids:
                continue
            if not any(needle in url for needle in url_needles):
                continue
            if "appendix_" in url:
                continue
            score = 5.0 + max(0.0, 0.2 - 0.02 * int(record.get("chunk_index") or 0))
            # Prefer chunks that already carry transcribed figure content.
            if "01_Revit Model" in (record.get("text") or ""):
                score += 1.0
            hits.append((score, _record_to_chunk(record, score=score)))
    hits.sort(key=lambda item: item[0], reverse=True)
    # One pin per section URL — keep the best chunk only.
    ordered: list[RetrievedChunk] = []
    seen_urls: set[str] = set()
    for _score, chunk in hits:
        url = chunk.source_url or chunk.chunk_id
        if url in seen_urls:
            continue
        seen_urls.add(url)
        ordered.append(chunk)
        if len(ordered) >= limit:
            break
    return ordered


def _dedupe_chunks(chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    """Collapse same source_url; keep the stronger / earlier chunk."""
    best_by_url: dict[str, RetrievedChunk] = {}
    order: list[str] = []
    orphans: list[RetrievedChunk] = []
    seen_ids: set[str] = set()

    def _better(new: RetrievedChunk, old: RetrievedChunk) -> bool:
        if (new.score or 0) != (old.score or 0):
            return (new.score or 0) > (old.score or 0)
        if (new.vector_similarity or 0) != (old.vector_similarity or 0):
            return (new.vector_similarity or 0) > (old.vector_similarity or 0)
        return int(new.chunk_index or 0) < int(old.chunk_index or 0)

    for chunk in chunks:
        if chunk.chunk_id in seen_ids:
            continue
        seen_ids.add(chunk.chunk_id)
        url = chunk.source_url or ""
        if not url:
            orphans.append(chunk)
            continue
        current = best_by_url.get(url)
        if current is None:
            best_by_url[url] = chunk
            order.append(url)
        elif _better(chunk, current):
            best_by_url[url] = chunk
    return [best_by_url[url] for url in order] + orphans


def _family_rerank(query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
    family = resolve_source_family(query)
    explicit = extract_explicit_section_title(query)
    explicit_n = normalize_title(explicit) if explicit else ""
    naming_intent = bool(
        re.search(r"naming|命名|Information\s+Container|federation", query or "", re.I)
    )
    scored: list[tuple[float, int, RetrievedChunk]] = []
    for index, chunk in enumerate(chunks):
        score = float(chunk.score or 0.0)
        score += exact_title_bonus(query, chunk.title)
        doc_id = doc_id_from_url(chunk.source_url) or ""
        url = (chunk.source_url or "").lower()
        if "/templates/" in (chunk.source_file or "") or doc_id.startswith("template"):
            if not _mentions_template(query):
                score -= 3.0
        # When a concrete section is named, demote overview / appendix fillers.
        if explicit_n:
            title_n = normalize_title(chunk.title)
            if title_n == explicit_n or explicit_n in title_n:
                score += 2.5
            if any(
                token in url
                for token in (
                    "executive_summary",
                    "table_of_contents",
                    "front_matter",
                    "acknowledgement",
                    "abbreviation",
                )
            ) and explicit_n not in title_n:
                score -= 2.0
            if "appendix_" in url and "appendix" not in explicit_n:
                score -= 1.25
        if naming_intent and doc_id == "devb_harmonisation_v3":
            if "federation_and_bim_model_naming" in url:
                score += 3.0
            elif "appendix_ix" in url or "appendix_xiv" in url:
                score -= 1.5
            elif "executive_summary" in url:
                score -= 1.0
        loin_intent = bool(
            re.search(
                r"\bLOIN\b|level of information need|信息需求|資訊需求",
                query or "",
                re.I,
            )
        )
        if loin_intent and "level_of_information_need" in url:
            score += 3.0
        if loin_intent and "appendix_" in url:
            score -= 1.0
        if family:
            if doc_id in family.doc_ids:
                score += 3.5 if family.prefer_shadow else 1.8
            elif family.prefer_shadow:
                score -= 1.5
            if family.doc_ids and doc_id and doc_id not in family.doc_ids:
                lowered = query.lower()
                if any(
                    token in lowered
                    for token in (
                        "lod",
                        "loin",
                        "field verification",
                        "appearance",
                        "document structure",
                        "responsibility matrix",
                    )
                ):
                    score -= 0.75
        scored.append((score, index, chunk))
    scored.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in scored]


class IndustryHybridRetriever(HybridRetriever):
    def __init__(self, config: IndustryHKConfig | None = None) -> None:
        industry = config or get_industry_hk_config()
        super().__init__(industry_to_app_config(industry))
        self.industry_config = industry

    def retrieve_with_debug(
        self,
        query: str,
        top_k: int | None = None,
        *,
        boost_url_prefix: str | None = None,
        source_hint_urls: list[str] | None = None,
    ) -> RetrievalResult:
        limit = top_k or self.config.retrieval.top_k

        # Section-number titles: skip fuzzy page_title KB to avoid cross-doc homonyms.
        if is_section_number_title(query):
            debug = RetrievalDebugInfo(original_query=query)
            chunks = self._retrieve_internal(
                query,
                limit,
                boost_target_url=boost_url_prefix,
                source_hint_urls=source_hint_urls,
                debug=debug,
            )
            debug.adopted_path = "original"
            result = RetrievalResult(chunks=chunks, debug=debug)
        else:
            result = super().retrieve_with_debug(
                query,
                top_k,
                boost_url_prefix=boost_url_prefix,
                source_hint_urls=source_hint_urls,
            )

        chunks = list(result.chunks)
        family = resolve_source_family(query)
        if family and family.prefer_shadow:
            shadow = _shadow_chunks_path()
            if shadow is not None:
                extra = _load_shadow_chunks_for_docs(
                    shadow, family.doc_ids, query=query
                )
                seen = {c.chunk_id for c in chunks}
                for item in extra:
                    if item.chunk_id not in seen:
                        chunks.append(item)
                        seen.add(item.chunk_id)

        # Exact section-title pins from the production chunks file.
        pin_docs = family.doc_ids if family else None
        title_pins = _load_explicit_title_pins(
            self.industry_config.storage.chunks_path,
            query,
            doc_ids=pin_docs,
        )
        keyword_pins = _load_keyword_section_pins(
            self.industry_config.storage.chunks_path,
            query,
            doc_ids=pin_docs,
        )
        seen = {c.chunk_id for c in chunks}
        for item in [*title_pins, *keyword_pins]:
            if item.chunk_id in seen:
                # Upgrade score / keep richer pin when already present.
                for index, existing in enumerate(chunks):
                    if existing.chunk_id == item.chunk_id and (item.score or 0) > (
                        existing.score or 0
                    ):
                        chunks[index] = item
                        break
                continue
            url = item.source_url or ""
            replaced = False
            if url:
                for index, existing in enumerate(chunks):
                    if existing.source_url == url and (item.score or 0) >= (
                        existing.score or 0
                    ):
                        chunks[index] = item
                        seen.add(item.chunk_id)
                        replaced = True
                        break
            if replaced:
                continue
            chunks.append(item)
            seen.add(item.chunk_id)

        chunks = _dedupe_chunks(_family_rerank(query, chunks))
        # Do not let overview pins steal explicit case-study / terminology /
        # software-guide family queries.
        if family and family.prefer_shadow:
            capped = chunks[:limit]
            return RetrievalResult(chunks=capped, debug=result.debug)

        preferred = prefer_industry_chunks(
            query,
            chunks,
            chunks_path=self.industry_config.storage.chunks_path,
            limit=limit,
        )
        capped = _dedupe_chunks(preferred)[:limit]
        if capped == result.chunks:
            return result
        return RetrievalResult(chunks=capped, debug=result.debug)
