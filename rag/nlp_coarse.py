"""NLP 粗筛与特征精排：压低进 LLM 的候选 token，提升排序精度。

阶段：
1. 查询分析：分词、去停用词、提取关键词
2. 粗筛：BM25 先从全库筛出候选池（不做向量全扫对比）
3. 精排：在混合检索结果上用关键词覆盖 / 标题命中 / 向量分重排
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Any, Protocol

TOKEN_RE = re.compile(r"[\w\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+", re.UNICODE)
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")

STOPWORDS = {
    # English
    "a",
    "an",
    "the",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "is",
    "are",
    "be",
    "how",
    "what",
    "which",
    "when",
    "where",
    "who",
    "why",
    "can",
    "do",
    "does",
    "please",
    "help",
    # Chinese
    "的",
    "了",
    "吗",
    "呢",
    "啊",
    "吧",
    "是",
    "在",
    "有",
    "和",
    "与",
    "及",
    "或",
    "被",
    "把",
    "对",
    "从",
    "到",
    "为",
    "以",
    "上",
    "下",
    "中",
    "个",
    "这",
    "那",
    "如何",
    "怎么",
    "怎样",
    "什么",
    "哪些",
    "请问",
    "一下",
    "可以",
    "能否",
    "需要",
    "进行",
    "以及",
    "关于",
}


@dataclass(frozen=True)
class QueryAnalysis:
    original: str
    tokens: list[str]
    keywords: list[str]
    is_cjk_heavy: bool
    intent_hints: tuple[str, ...]


class SupportsBM25(Protocol):
    def get_scores(self, query: list[str]) -> Any: ...


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]


DOMAIN_TERMS = (
    "文件夹",
    "权限",
    "审批",
    "工作流",
    "审阅",
    "文件",
    "格式",
    "命名",
    "容器",
    "设置",
    "workflow",
    "approval",
    "permission",
    "folder",
    "review",
    "gateway",
    "wip",
    "cde",
)

# 中文问英文 Docs 时，把领域词扩展成 BM25 可用的英文检索词。
ZH_EN_EXPAND: dict[str, tuple[str, ...]] = {
    "文件夹": ("folder", "folders"),
    "权限": ("permission", "permissions"),
    "审批": ("approval", "approve", "workflow"),
    "工作流": ("workflow",),
    "审阅": ("review", "reviews"),
    "文件": ("file", "files"),
    "格式": ("format", "formats", "supported"),
    "命名": ("naming", "name"),
    "设置": ("settings", "manage", "set"),
    "容器": ("container", "cde", "wip"),
}


def _find_domain_terms(query: str) -> list[str]:
    lowered = query.lower()
    hits = [
        term.lower() if term.isascii() else term
        for term in sorted(DOMAIN_TERMS, key=len, reverse=True)
        if term in lowered or term in query
    ]
    # 去重保序
    seen: set[str] = set()
    ordered: list[str] = []
    for term in hits:
        if term not in seen:
            seen.add(term)
            ordered.append(term)
    return ordered


def _cjk_bigrams_outside_domains(text: str, domain_terms: list[str]) -> list[str]:
    """仅在领域词覆盖之外生成 2-gram，避免 TF 膨胀。"""

    chars = CJK_RE.findall(text)
    if len(chars) < 2:
        return []

    covered = [False] * len(chars)
    for term in sorted(
        (item for item in domain_terms if not item.isascii()),
        key=len,
        reverse=True,
    ):
        term_chars = CJK_RE.findall(term)
        width = len(term_chars)
        if width == 0:
            continue
        for start in range(0, len(chars) - width + 1):
            if chars[start : start + width] == term_chars:
                for index in range(start, start + width):
                    covered[index] = True

    grams: list[str] = []
    for index in range(len(chars) - 1):
        # 领域词内部不拆；边界 2-gram 仍可保留作兜底。
        if covered[index] and covered[index + 1]:
            continue
        gram = chars[index] + chars[index + 1]
        if gram not in STOPWORDS:
            grams.append(gram)
    return grams


def analyze_query(query: str) -> QueryAnalysis:
    tokens = tokenize(query)
    domain_hits = _find_domain_terms(query)

    keywords: list[str] = []
    for token in tokens:
        if token in STOPWORDS or len(token) <= 1:
            continue
        # 无空格中文整句 token：已有领域词时丢弃，避免 BM25 巨词干扰。
        if len(CJK_RE.findall(token)) >= 8 and domain_hits:
            continue
        keywords.append(token)

    keywords.extend(domain_hits)
    keywords.extend(_cjk_bigrams_outside_domains(query, domain_hits))

    seen: set[str] = set()
    ordered: list[str] = []
    for item in keywords:
        if item in STOPWORDS or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
        for english in ZH_EN_EXPAND.get(item, ()):
            if english not in seen:
                seen.add(english)
                ordered.append(english)
    keywords = ordered
    if not keywords:
        keywords = [token for token in tokens if token not in STOPWORDS] or tokens[:]

    cjk_chars = len(CJK_RE.findall(query))
    is_cjk_heavy = cjk_chars / max(len(query), 1) >= 0.25

    hints: list[str] = []
    joined = " ".join(keywords)
    hint_map = (
        (("permission", "权限", "folder", "文件夹"), "permissions"),
        (("workflow", "approval", "审批", "审阅", "review", "工作流"), "reviews"),
        (("file", "format", "格式", "supported"), "files"),
        (("wip", "gateway", "cde", "iso"), "cde"),
        (("naming", "命名"), "naming"),
    )
    for terms, hint in hint_map:
        if any(term in joined or term in query.lower() for term in terms):
            hints.append(hint)

    return QueryAnalysis(
        original=query,
        tokens=tokens,
        keywords=keywords,
        is_cjk_heavy=is_cjk_heavy,
        intent_hints=tuple(hints),
    )


def coarse_candidate_ids(
    bm25: SupportsBM25,
    chunk_ids: list[str],
    analysis: QueryAnalysis,
    *,
    top_n: int,
) -> list[str]:
    """用 BM25 做全库粗筛，返回候选 chunk_id 列表。"""

    if top_n <= 0 or not chunk_ids:
        return []

    query_terms = analysis.keywords or analysis.tokens
    if not query_terms:
        return chunk_ids[:top_n]

    scores = bm25.get_scores(query_terms)
    ranked = sorted(
        enumerate(scores),
        key=lambda item: item[1],
        reverse=True,
    )[:top_n]
    return [chunk_ids[index] for index, score in ranked if score > 0]


def _keyword_coverage(text: str, keywords: list[str]) -> float:
    if not keywords:
        return 0.0
    lowered = text.lower()
    hits = sum(1 for keyword in keywords if keyword in lowered)
    return hits / len(keywords)


def _title_hit(title: str, keywords: list[str]) -> float:
    if not keywords:
        return 0.0
    lowered = title.lower()
    return 1.0 if any(keyword in lowered for keyword in keywords) else 0.0


def _minmax_normalize(values: list[float | None]) -> list[float]:
    present = [value for value in values if value is not None]
    if not present:
        return [0.0 for _ in values]
    min_sim = min(present)
    max_sim = max(present)
    spread = max_sim - min_sim
    if spread <= 1e-9:
        return [0.5 if value is not None else 0.0 for value in values]
    return [
        (value - min_sim) / (spread + 1e-5) if value is not None else 0.0
        for value in values
    ]


def feature_rerank_score(
    *,
    rrf_score: float,
    norm_similarity: float,
    title: str,
    text: str,
    analysis: QueryAnalysis,
    max_rrf: float,
) -> float:
    """融合 RRF、归一化向量相似度、关键词覆盖与标题命中。"""

    norm_rrf = (rrf_score / max_rrf) if max_rrf > 0 else 0.0
    coverage = _keyword_coverage(f"{title}\n{text}", analysis.keywords)
    title_score = _title_hit(title, analysis.keywords)

    # CJK 查询更依赖语义；英文查询提高关键词权重。
    if analysis.is_cjk_heavy:
        weights = (0.40, 0.35, 0.15, 0.10)
    else:
        weights = (0.35, 0.25, 0.25, 0.15)

    return (
        weights[0] * norm_rrf
        + weights[1] * max(0.0, min(1.0, norm_similarity))
        + weights[2] * coverage
        + weights[3] * title_score
    )


def rerank_chunks(
    chunks: list[Any],
    analysis: QueryAnalysis,
) -> list[Any]:
    """对 RetrievedChunk 列表做特征精排，写回 score。"""

    if len(chunks) <= 1:
        return chunks

    max_rrf = max(chunk.score for chunk in chunks) or 1.0
    norm_sims = _minmax_normalize(
        [chunk.vector_similarity for chunk in chunks]
    )
    rescored = []
    for chunk, norm_sim in zip(chunks, norm_sims):
        new_score = feature_rerank_score(
            rrf_score=chunk.score,
            norm_similarity=norm_sim,
            title=chunk.title,
            text=chunk.text,
            analysis=analysis,
            max_rrf=max_rrf,
        )
        rescored.append(replace(chunk, score=new_score))
    rescored.sort(key=lambda item: item.score, reverse=True)
    return rescored


def estimate_context_tokens(chunks: list[Any]) -> int:
    return sum(int(getattr(chunk, "token_count", 0)) for chunk in chunks)


def trim_chunks_by_token_budget(
    chunks: list[Any],
    *,
    top_k: int,
    max_tokens: int,
) -> list[Any]:
    selected: list[Any] = []
    used = 0
    for chunk in chunks:
        token_count = int(getattr(chunk, "token_count", 0))
        if selected and used + token_count > max_tokens:
            # 不继续捞排名更低的短碎片，避免 Lost-in-the-middle 噪声。
            break
        selected.append(chunk)
        used += token_count
        if len(selected) >= top_k:
            break
    return selected
