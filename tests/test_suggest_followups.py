"""追问建议生成测试。"""

from __future__ import annotations

from rag.orchestrator.suggest_followups import suggest_followups
from rag.retrieval import RetrievedChunk


def _chunk(title: str, url: str, text: str) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id="c1",
        title=title,
        source_url=url,
        source_file="x.md",
        page_index=0,
        line_start=1,
        product="hk_cde",
        chunk_index=0,
        chunk_count=1,
        token_count=10,
        text=text,
        score=1.0,
        vector_similarity=0.9,
    )


def test_english_question_gets_english_followups() -> None:
    result = suggest_followups(
        question="What is WIP?",
        track="hk_cde",
        chunks_industry=[
            _chunk(
                "WIP",
                "hk_cde://cicbims_2024/cicbims_2024_4_2_1_work_in_progress_wip",
                "Work in Progress WIP Gateway",
            )
        ],
        limit=3,
    )
    assert result.lang == "en"
    assert len(result.questions) == 3
    assert all(not any("\u4e00" <= ch <= "\u9fff" for ch in q) for q in result.questions)


def test_chinese_question_gets_chinese_followups() -> None:
    result = suggest_followups(
        question="WIP 是什么",
        track="hk_cde",
        chunks_industry=[
            _chunk(
                "WIP",
                "hk_cde://cicbims_2024/cicbims_2024_4_2_1_work_in_progress_wip",
                "Work in Progress",
            )
        ],
        limit=3,
    )
    assert result.lang.startswith("zh")
    assert any(any("\u4e00" <= ch <= "\u9fff" for ch in q) for q in result.questions)


def test_forced_answer_lang_does_not_override_question_language() -> None:
    result = suggest_followups(
        question="What is WIP?",
        track="hk_cde",
        answer_lang="zh-Hans",
        limit=3,
    )
    assert result.lang == "en"
    assert all(not any("\u4e00" <= ch <= "\u9fff" for ch in q) for q in result.questions)


def test_zcp_source_suggestions_en() -> None:
    result = suggest_followups(
        question="What is the ZCP BIMIP standardised folder structure?",
        track="hk_cde",
        chunks_industry=[
            _chunk(
                "ZCP figures",
                "hk_cde://cic_zcp_bimip_v15/cic_zcp_bimip_v15_figures_transcription",
                "01_Revit Model 02_Forge Model",
            )
        ],
        limit=3,
    )
    joined = " ".join(result.questions)
    assert "ZCP" in joined
    assert result.lang == "en"
