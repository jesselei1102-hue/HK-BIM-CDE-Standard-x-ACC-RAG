"""Unit tests for multi-turn conversation rewrite and soft source hints."""

from __future__ import annotations

from rag.conversation import ConversationSession, ConversationTurn
from rag.orchestrator.followup import (
    looks_like_follow_up,
    rewrite_followup_query,
    turns_as_untrusted_context,
)
from rag.retrieval import apply_source_hint_soft_boost


def _session_with_permissions_turn() -> ConversationSession:
    session = ConversationSession()
    session.append(
        ConversationTurn(
            user_question="如何设置文件夹权限？",
            rewritten_query="如何设置文件夹权限？",
            answer="错误答案：最大文件只能 1MB。进入 Permissions settings 即可。",
            track="docs",
            source_urls=[
                "https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions"
            ],
            source_titles=["Manage Folder Permissions"],
        )
    )
    return session


def test_looks_like_follow_up():
    session = _session_with_permissions_turn()
    assert looks_like_follow_up("那子文件夹呢？", session)
    assert not looks_like_follow_up(
        "CIC BIM Standard 里 WIP Gateway 是什么？", session
    )
    assert not looks_like_follow_up("那子文件夹呢？", ConversationSession())


def test_conservative_followup_rewrite_does_not_copy_wrong_facts():
    session = _session_with_permissions_turn()
    standalone = rewrite_followup_query(
        "那子文件夹呢？",
        session,
        use_llm=False,
    )
    assert standalone.is_follow_up
    assert "子文件夹" in standalone.query or "权限" in standalone.query
    # Prior wrong numeric claim must not become retrieval premise.
    assert "1MB" not in standalone.query
    assert standalone.source_hints
    assert "Folder_Permissions" in standalone.source_hints[0]


def test_standalone_passthrough_skips_history_facts():
    session = _session_with_permissions_turn()
    standalone = rewrite_followup_query(
        "Autodesk Docs 中单个文件最大可以多大？",
        session,
        use_llm=False,
    )
    assert standalone.is_follow_up is False
    assert standalone.query == "Autodesk Docs 中单个文件最大可以多大？"
    assert "1MB" not in standalone.query


def test_untrusted_context_marked():
    session = _session_with_permissions_turn()
    blob = turns_as_untrusted_context(session.recent_turns())
    assert "<conversation_context_untrusted>" in blob
    assert "不可信" in blob or "不得作为事实" in blob


def test_source_hint_soft_boost_only_existing_candidates():
    scores = {
        "a": 1.0,
        "b": 0.8,
    }
    chunks = {
        "a": {
            "source_url": "https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions"
        },
        "b": {
            "source_url": "https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations"
        },
        "c": {
            "source_url": "https://help.autodesk.com/view/DOCS/ENU/?guid=Missing_Page"
        },
    }
    hits = apply_source_hint_soft_boost(
        scores,
        chunks,
        [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions",
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Missing_Page",
        ],
    )
    assert scores["a"] > 1.0
    assert scores["b"] == 0.8
    assert "c" not in scores  # never injected
    assert any("Folder_Permissions" in url for url in hits)
    assert not any("Missing_Page" in url for url in hits)
