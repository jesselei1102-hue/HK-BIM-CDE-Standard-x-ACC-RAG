"""Query KB / 路由单元测试（不依赖 Ollama）。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from dataclasses import replace

from rag.config import AppConfig, QueryKBConfig, get_config
from rag.kb_index import RouteCandidate, build_route_records
from rag.query_kb import KBRouter, normalize_query, rewrite_from_candidate


@pytest.fixture()
def kb_path(tmp_path: Path) -> Path:
    path = tmp_path / "query_kb.jsonl"
    entries = [
        {
            "id": "folder_permissions_set",
            "topic": "permissions",
            "aliases": ["文件夹权限", "设置权限", "权限设置"],
            "canonical_query_zh": "如何设置文件夹权限",
            "canonical_query_en": "How do I set folder permissions",
            "target_title": "Manage Folder Permissions",
            "target_url": "https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions",
            "target_guid": "Folder_Permissions",
            "entry_type": "how_to",
            "evidence": "DOCS_help_002.md:7179",
            "external_sources": [],
            "status": "approved",
        },
        {
            "id": "approval_workflow",
            "topic": "reviews",
            "aliases": ["审批", "审阅"],
            "canonical_query_zh": "如何创建审批工作流",
            "canonical_query_en": "How do I create approval workflows",
            "target_title": "Create and Edit Approval Workflows",
            "target_url": "https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit",
            "target_guid": "Reviews_Create_Edit",
            "entry_type": "how_to",
            "evidence": "DOCS_help_003.md:8593",
            "external_sources": [],
            "status": "candidate",
        },
    ]
    with path.open("w", encoding="utf-8") as handle:
        for entry in entries:
            handle.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def test_normalize_query_fullwidth():
    assert normalize_query("设置权限") == normalize_query("设 置 权 限")


def test_build_route_records_from_kb(kb_path: Path):
    records = build_route_records(kb_path)
    texts = {record.text for record in records}
    assert "设置权限" in texts
    assert "Manage Folder Permissions" in texts
    assert "如何设置文件夹权限" in texts


def _router(kb_path: Path, **kb_overrides) -> KBRouter:
    base = get_config()
    kb_config = replace(base.query_kb, kb_path=kb_path, enabled=True, **kb_overrides)
    return KBRouter(replace(base, query_kb=kb_config))


def test_controlled_rewrite_exact_term(kb_path: Path):
    router = _router(kb_path)
    candidates = router._alias_candidates("设置权限")
    decision = router.controlled_rewrite("设置权限", candidates)
    assert decision is not None
    assert decision.entry_id == "folder_permissions_set"
    assert decision.reason == "exact_term"
    assert decision.rewritten_query == "如何设置文件夹权限"


def test_controlled_rewrite_vector_top1(kb_path: Path):
    router = _router(kb_path, min_route_sim=0.4)
    candidates = [
        RouteCandidate(
            entry_id="folder_permissions_set",
            target_title="Manage Folder Permissions",
            target_url="https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions",
            target_guid="Folder_Permissions",
            matched_term="folder permissions",
            source_type="kb_alias",
            similarity=0.72,
            rewrite_query_zh="如何设置文件夹权限",
            rewrite_query_en="How do I set folder permissions",
        )
    ]
    decision = router.controlled_rewrite("权限", candidates)
    assert decision is not None
    assert decision.reason == "vector_top1"


def test_should_route_short_query_only(kb_path: Path):
    router = _router(kb_path, short_query_max_chars=16)
    assert router.should_route("设置权限", 0.40) is True
    assert router.should_route("设置权限", 0.80) is False
    long_query = "请详细说明如何设置文件夹权限给团队成员"
    assert router.should_route(long_query, 0.40) is False


def test_rewrite_from_candidate_zh():
    candidate = RouteCandidate(
        entry_id="x",
        target_title="T",
        target_url="u",
        target_guid="g",
        matched_term="设置权限",
        source_type="kb_alias",
        similarity=1.0,
        rewrite_query_zh="如何设置文件夹权限",
        rewrite_query_en="How do I set folder permissions",
    )
    assert rewrite_from_candidate("设置权限", candidate) == "如何设置文件夹权限"
