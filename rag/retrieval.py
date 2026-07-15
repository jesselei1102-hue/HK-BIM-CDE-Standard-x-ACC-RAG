"""混合检索：Chroma 向量检索 + BM25 关键词检索 + RRF 融合。

低分短句走标题/术语路由索引（Top-K）→ 受控改写 → 正文 RAG；KB 不进生成上下文。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import chromadb
import ollama
from rank_bm25 import BM25Okapi

from .config import AppConfig, get_config
from .nlp_coarse import (
    analyze_query,
    coarse_candidate_ids,
    rerank_chunks,
    trim_chunks_by_token_budget,
)
from .query_kb import KBRouter, RouteCandidate, RouteDecision


TOKEN_RE = re.compile(r"[\w\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+", re.UNICODE)


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    title: str
    source_url: str
    source_file: str
    page_index: int
    line_start: int
    product: str
    chunk_index: int
    chunk_count: int
    token_count: int
    text: str
    score: float
    vector_similarity: float | None = None
    lexical_rank: int | None = None
    vector_rank: int | None = None


@dataclass
class RetrievalDebugInfo:
    original_query: str
    kb_hit: bool = False
    kb_id: str | None = None
    kb_matched_term: str | None = None
    kb_route_reason: str | None = None
    kb_candidates: list[dict[str, str | float]] | None = None
    rewritten_query: str | None = None
    original_top1_sim: float | None = None
    rewritten_top1_sim: float | None = None
    adopted_path: str = "original"  # original | kb_rewrite | kb_boost
    target_url_boosted: bool = False
    nlp_coarse_enabled: bool = False
    nlp_rerank_enabled: bool = False
    nlp_keywords: list[str] = field(default_factory=list)
    nlp_coarse_pool_size: int = 0
    context_token_estimate: int = 0


@dataclass
class RetrievalResult:
    chunks: list[RetrievedChunk]
    debug: RetrievalDebugInfo


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


def load_chunks(chunks_path: Path) -> list[dict[str, Any]]:
    if not chunks_path.is_file():
        raise FileNotFoundError(
            f"未找到 chunks 文件：{chunks_path}。请先运行 python ingest.py"
        )
    chunks: list[dict[str, Any]] = []
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    if not chunks:
        raise ValueError(f"chunks 文件为空：{chunks_path}")
    return chunks


class HybridRetriever:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or get_config()
        self.chunks = load_chunks(self.config.storage.chunks_path)
        self.chunks_by_id = {chunk["chunk_id"]: chunk for chunk in self.chunks}
        self.chunk_ids = [chunk["chunk_id"] for chunk in self.chunks]
        self._bm25 = BM25Okapi([tokenize(chunk["text"]) for chunk in self.chunks])
        self._chroma = chromadb.PersistentClient(
            path=str(self.config.storage.chroma_dir)
        )
        self._collection = self._chroma.get_collection(
            self.config.storage.collection_name
        )
        self._ollama = ollama.Client(
            host=self.config.models.ollama_host,
            timeout=self.config.models.request_timeout_seconds,
            trust_env=False,
        )
        self._kb_router = KBRouter(self.config)
        self.last_debug: RetrievalDebugInfo | None = None

    @staticmethod
    def _candidate_summary(candidates: list[RouteCandidate]) -> list[dict[str, str | float]]:
        return [
            {
                "title": item.target_title,
                "term": item.matched_term,
                "sim": round(item.similarity, 4),
                "source": item.source_type,
            }
            for item in candidates
        ]

    def _embed_query(self, query: str) -> list[float]:
        response = self._ollama.embed(
            model=self.config.models.embedding_model,
            input=[query],
        )
        return response.embeddings[0]

    def _vector_hits(
        self,
        query: str,
        *,
        n_results: int | None = None,
        allowed_ids: set[str] | None = None,
    ) -> list[tuple[str, float, int]]:
        fetch = n_results or self.config.retrieval.vector_candidates
        # 粗筛后在更大候选中过滤，避免被池外噪声占满 Top-N。
        if allowed_ids is not None:
            fetch = max(fetch, min(len(allowed_ids), fetch * 3))
        embedding = self._embed_query(query)
        result = self._collection.query(
            query_embeddings=[embedding],
            n_results=min(fetch, max(len(self.chunk_ids), 1)),
            include=["distances"],
        )
        ids = result["ids"][0]
        distances = result["distances"][0]
        hits: list[tuple[str, float, int]] = []
        for rank, (chunk_id, distance) in enumerate(zip(ids, distances), start=1):
            if allowed_ids is not None and chunk_id not in allowed_ids:
                continue
            similarity = 1.0 - float(distance)
            if similarity < self.config.retrieval.minimum_vector_similarity:
                continue
            hits.append((chunk_id, similarity, len(hits) + 1))
            if len(hits) >= (n_results or self.config.retrieval.vector_candidates):
                break
        return hits

    def _raw_top_vector_sim(self, query: str) -> float | None:
        embedding = self._embed_query(query)
        result = self._collection.query(
            query_embeddings=[embedding],
            n_results=1,
            include=["distances"],
        )
        if not result["ids"][0]:
            return None
        return 1.0 - float(result["distances"][0][0])

    def _lexical_hits(
        self,
        query: str,
        *,
        allowed_ids: set[str] | None = None,
        analysis_keywords: list[str] | None = None,
    ) -> list[tuple[str, float, int]]:
        terms = analysis_keywords or tokenize(query)
        scores = self._bm25.get_scores(terms)
        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )
        hits: list[tuple[str, float, int]] = []
        for index, score in ranked:
            if score <= 0:
                continue
            chunk_id = self.chunk_ids[index]
            if allowed_ids is not None and chunk_id not in allowed_ids:
                continue
            hits.append((chunk_id, float(score), len(hits) + 1))
            if len(hits) >= self.config.retrieval.lexical_candidates:
                break
        return hits

    def _retrieve_internal(
        self,
        query: str,
        top_k: int,
        *,
        boost_target_url: str | None = None,
        debug: RetrievalDebugInfo | None = None,
    ) -> list[RetrievedChunk]:
        analysis = analyze_query(query)
        cfg = self.config.retrieval
        allowed_ids: set[str] | None = None
        coarse_ids: list[str] = []

        if cfg.nlp_coarse_enabled:
            coarse_ids = coarse_candidate_ids(
                self._bm25,
                self.chunk_ids,
                analysis,
                top_n=cfg.nlp_coarse_candidates,
            )
            allowed_ids = set(coarse_ids) if coarse_ids else None

        if debug is not None:
            debug.nlp_coarse_enabled = cfg.nlp_coarse_enabled
            debug.nlp_rerank_enabled = cfg.nlp_rerank_enabled
            debug.nlp_keywords = list(analysis.keywords)
            debug.nlp_coarse_pool_size = len(coarse_ids)

        prefetch = max(top_k, cfg.hybrid_prefetch)
        vector_n = max(cfg.vector_candidates, prefetch)
        vector_hits = self._vector_hits(
            query,
            n_results=vector_n,
            allowed_ids=allowed_ids,
        )
        # 粗筛过严导致向量空时回退全库，避免漏召回。
        if not vector_hits and allowed_ids is not None:
            vector_hits = self._vector_hits(query, n_results=vector_n)
            if debug is not None:
                debug.nlp_coarse_pool_size = 0

        lexical_hits = self._lexical_hits(
            query,
            allowed_ids=allowed_ids,
            analysis_keywords=analysis.keywords or analysis.tokens,
        )

        rrf_scores: dict[str, float] = {}
        vector_meta: dict[str, tuple[float, int]] = {}
        lexical_meta: dict[str, int] = {}

        if analysis.is_cjk_heavy:
            vector_weight = 5.0
            lexical_weight = 1.0 if cfg.nlp_coarse_enabled else 0.0
        else:
            vector_weight = 2.0
            lexical_weight = 1.0

        for chunk_id, similarity, rank in vector_hits:
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + vector_weight / (
                cfg.rrf_k + rank
            )
            vector_meta[chunk_id] = (similarity, rank)

        for chunk_id, _score, rank in lexical_hits:
            rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + lexical_weight / (
                cfg.rrf_k + rank
            )
            lexical_meta[chunk_id] = rank

        if boost_target_url:
            boost = self.config.query_kb.target_url_boost
            pool_items = (
                ((cid, self.chunks_by_id[cid]) for cid in allowed_ids if cid in self.chunks_by_id)
                if allowed_ids is not None
                else self.chunks_by_id.items()
            )
            for chunk_id, chunk in pool_items:
                url = chunk["source_url"]
                if url == boost_target_url or url.startswith(
                    boost_target_url.rstrip("/") + "/"
                ):
                    rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + boost

        ordered = sorted(rrf_scores.items(), key=lambda item: item[1], reverse=True)
        selected: list[RetrievedChunk] = []
        used_pages: set[str] = set()

        for chunk_id, score in ordered:
            chunk = self.chunks_by_id[chunk_id]
            page_key = chunk["source_url"]
            if page_key in used_pages:
                continue

            vector_similarity, vector_rank = vector_meta.get(chunk_id, (None, None))
            selected.append(
                RetrievedChunk(
                    chunk_id=chunk_id,
                    title=chunk["title"],
                    source_url=chunk["source_url"],
                    source_file=chunk["source_file"],
                    page_index=int(chunk["page_index"]),
                    line_start=int(chunk["line_start"]),
                    product=chunk["product"],
                    chunk_index=int(chunk["chunk_index"]),
                    chunk_count=int(chunk["chunk_count"]),
                    token_count=int(chunk["token_count"]),
                    text=chunk["text"],
                    score=score,
                    vector_similarity=vector_similarity,
                    lexical_rank=lexical_meta.get(chunk_id),
                    vector_rank=vector_rank,
                )
            )
            used_pages.add(page_key)
            if len(selected) >= prefetch:
                break

        if cfg.nlp_rerank_enabled and selected:
            selected = rerank_chunks(selected, analysis)

        selected = trim_chunks_by_token_budget(
            selected,
            top_k=top_k,
            max_tokens=cfg.maximum_context_tokens,
        )
        if debug is not None:
            debug.context_token_estimate = sum(item.token_count for item in selected)
        return selected

    def retrieve_with_debug(
        self,
        query: str,
        top_k: int | None = None,
        *,
        boost_url_prefix: str | None = None,
    ) -> RetrievalResult:
        query = query.strip()
        if not query:
            raise ValueError("问题不能为空")

        limit = top_k or self.config.retrieval.top_k
        debug = RetrievalDebugInfo(original_query=query)

        original_chunks = self._retrieve_internal(
            query,
            limit,
            boost_target_url=boost_url_prefix,
            debug=debug,
        )
        original_sim = (
            original_chunks[0].vector_similarity if original_chunks else None
        )
        if original_sim is None:
            original_sim = self._raw_top_vector_sim(query)
        debug.original_top1_sim = original_sim

        kb = self._kb_router
        route_decision: RouteDecision | None = None
        kb_candidates: list[RouteCandidate] = []
        top1_url = original_chunks[0].source_url if original_chunks else None

        if kb.should_route(query, original_sim, top1_url):
            kb_candidates, route_decision = kb.route(query)

        if route_decision is None:
            debug.adopted_path = "original"
            if kb_candidates:
                debug.kb_candidates = self._candidate_summary(kb_candidates)
            self.last_debug = debug
            return RetrievalResult(chunks=original_chunks, debug=debug)

        debug.kb_hit = True
        debug.kb_id = route_decision.entry_id
        debug.kb_matched_term = route_decision.matched_term
        debug.kb_route_reason = route_decision.reason
        debug.kb_candidates = self._candidate_summary(kb_candidates)
        rewritten = route_decision.rewritten_query
        debug.rewritten_query = rewritten

        rewritten_chunks = self._retrieve_internal(rewritten, limit, debug=debug)
        rewritten_sim = (
            rewritten_chunks[0].vector_similarity if rewritten_chunks else None
        )
        if rewritten_sim is None:
            rewritten_sim = self._raw_top_vector_sim(rewritten)
        debug.rewritten_top1_sim = rewritten_sim

        threshold = self.config.query_kb.trigger_sim
        require_improvement = self.config.query_kb.require_sim_improvement
        target_url = route_decision.target_url

        adopt_rewrite = False
        if rewritten_chunks:
            if rewritten_sim is not None and rewritten_sim >= threshold:
                if not require_improvement:
                    adopt_rewrite = True
                elif original_sim is None or rewritten_sim > original_sim:
                    adopt_rewrite = True

        if adopt_rewrite and rewritten_chunks:
            if rewritten_chunks[0].source_url == target_url:
                debug.adopted_path = "kb_rewrite"
                debug.context_token_estimate = sum(
                    item.token_count for item in rewritten_chunks
                )
                self.last_debug = debug
                return RetrievalResult(chunks=rewritten_chunks, debug=debug)

        boosted_chunks = self._retrieve_internal(
            query,
            limit,
            boost_target_url=target_url,
            debug=debug,
        )
        if boosted_chunks:
            debug.adopted_path = "kb_boost"
            debug.target_url_boosted = True
            self.last_debug = debug
            return RetrievalResult(chunks=boosted_chunks, debug=debug)

        if adopt_rewrite and rewritten_chunks:
            debug.adopted_path = "kb_rewrite"
            self.last_debug = debug
            return RetrievalResult(chunks=rewritten_chunks, debug=debug)

        debug.adopted_path = "original"
        self.last_debug = debug
        return RetrievalResult(chunks=original_chunks, debug=debug)

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[RetrievedChunk]:
        return self.retrieve_with_debug(query, top_k=top_k).chunks


def format_context(chunks: list[RetrievedChunk]) -> str:
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        body = chunk.text
        if len(body) > 1800:
            body = body[:1800] + "\n..."
        blocks.append(
            f"[{index}] {chunk.title}\n"
            f"Source: {chunk.source_url}\n"
            f"{body}"
        )
    return "\n\n".join(blocks)


def format_retrieval_debug(debug: RetrievalDebugInfo) -> str:
    lines = [
        f"original_query: {debug.original_query}",
        f"kb_hit: {debug.kb_hit}",
        f"kb_id: {debug.kb_id or '-'}",
        f"kb_matched_term: {debug.kb_matched_term or '-'}",
        f"kb_route_reason: {debug.kb_route_reason or '-'}",
        f"rewritten_query: {debug.rewritten_query or '-'}",
        f"original_top1_sim: {debug.original_top1_sim}",
        f"rewritten_top1_sim: {debug.rewritten_top1_sim}",
        f"adopted_path: {debug.adopted_path}",
        f"target_url_boosted: {debug.target_url_boosted}",
        f"nlp_coarse: {debug.nlp_coarse_enabled} pool={debug.nlp_coarse_pool_size}",
        f"nlp_rerank: {debug.nlp_rerank_enabled}",
        f"nlp_keywords: {', '.join(debug.nlp_keywords) or '-'}",
        f"context_token_estimate: {debug.context_token_estimate}",
    ]
    if debug.kb_candidates:
        lines.append("kb_top_candidates:")
        for index, item in enumerate(debug.kb_candidates, start=1):
            lines.append(
                f"  [{index}] {item['title']} "
                f"(term={item['term']}, sim={item['sim']}, source={item['source']})"
            )
    lines.append("generation_context: docs_chunks_only")
    return "\n".join(lines)
