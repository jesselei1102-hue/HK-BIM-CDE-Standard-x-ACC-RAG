from dataclasses import dataclass

from rag.nlp_coarse import (
    _minmax_normalize,
    analyze_query,
    coarse_candidate_ids,
    feature_rerank_score,
    rerank_chunks,
    trim_chunks_by_token_budget,
)


class FakeBM25:
    def __init__(self, scores: list[float]) -> None:
        self._scores = scores

    def get_scores(self, query: list[str]) -> list[float]:
        return self._scores


@dataclass(frozen=True)
class FakeChunk:
    title: str
    text: str
    score: float
    vector_similarity: float | None
    token_count: int = 100


def test_analyze_query_strips_stopwords_and_detects_intent() -> None:
    analysis = analyze_query("请问如何设置文件夹权限？")
    assert "请问" not in analysis.keywords
    assert "权限" in analysis.keywords
    assert "文件夹" in analysis.keywords
    assert analysis.is_cjk_heavy
    assert "permissions" in analysis.intent_hints


def test_analyze_query_avoids_noisy_ngrams_inside_domain_terms() -> None:
    analysis = analyze_query("请问如何设置文件夹权限？")
    # 领域词内部交叉拆解应被抑制；兜底 2-gram 也不该刷爆关键词。
    assert "夹权" not in analysis.keywords
    assert "件夹" not in analysis.keywords
    assert "文件夹" in analysis.keywords
    assert "permission" in analysis.keywords
    assert len(analysis.keywords) < 25


def test_coarse_candidate_ids_keeps_positive_scores() -> None:
    bm25 = FakeBM25([0.0, 3.0, 1.0, 0.0])
    ids = coarse_candidate_ids(
        bm25,
        ["a", "b", "c", "d"],
        analyze_query("folder permissions"),
        top_n=2,
    )
    assert ids == ["b", "c"]


def test_feature_rerank_prefers_keyword_and_title_hits() -> None:
    analysis = analyze_query("folder permissions")
    weak = feature_rerank_score(
        rrf_score=0.02,
        norm_similarity=0.5,
        title="Welcome",
        text="general product overview",
        analysis=analysis,
        max_rrf=0.05,
    )
    strong = feature_rerank_score(
        rrf_score=0.02,
        norm_similarity=0.5,
        title="Manage Folder Permissions",
        text="How to add folder permissions for members",
        analysis=analysis,
        max_rrf=0.05,
    )
    assert strong > weak


def test_minmax_spreads_narrow_similarity_band() -> None:
    norms = _minmax_normalize([0.572, 0.570, 0.559])
    assert norms[0] == max(norms)
    assert norms[-1] == min(norms)
    assert norms[0] - norms[-1] > 0.9


def test_rerank_uses_local_sim_normalization() -> None:
    analysis = analyze_query("approval workflow")
    chunks = [
        FakeChunk("Welcome", "hello", 0.03, 0.551, 400),
        FakeChunk(
            "Create Approval Workflow",
            "create approval workflow steps",
            0.02,
            0.560,
            300,
        ),
        FakeChunk("Other", "unrelated text", 0.025, 0.552, 500),
    ]
    ranked = rerank_chunks(chunks, analysis)
    assert ranked[0].title == "Create Approval Workflow"


def test_trim_breaks_instead_of_packing_tail_fragments() -> None:
    chunks = [
        FakeChunk("A", "a", 0.9, 0.9, 600),
        FakeChunk("B", "b", 0.8, 0.8, 500),
        FakeChunk("Tiny", "c", 0.1, 0.1, 40),
    ]
    trimmed = trim_chunks_by_token_budget(chunks, top_k=3, max_tokens=650)
    assert [item.title for item in trimmed] == ["A"]
    assert "Tiny" not in {item.title for item in trimmed}
