"""语义路由器与 classify 集成测试。"""

from __future__ import annotations

from pathlib import Path

import pytest

from rag.config import AppConfig, SemanticRouterConfig, StorageConfig
from rag.orchestrator.classify import (
    classify_intent,
    classify_intent_legacy,
    is_folder_question,
)
from rag.orchestrator.route_index import build_route_exemplars
from rag.orchestrator.semantic_router import SemanticRouter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = PROJECT_ROOT / "knowledge" / "orchestrator_routes.jsonl"


def test_orchestrator_routes_file_exists() -> None:
    assert ROUTES_PATH.is_file()
    rows = build_route_exemplars(ROUTES_PATH)
    assert len(rows) >= 60


def test_classify_shadow_matches_legacy() -> None:
    q = "设置权限"
    legacy = classify_intent_legacy(q)
    shadow = classify_intent(q, mode="shadow")
    assert shadow.track == legacy.track
    assert shadow.capability == legacy.capability
    assert shadow.routing_source == "shadow"


def test_bare_wip_not_folder_capability_legacy() -> None:
    q = "WIP 是什么"
    decision = classify_intent_legacy(q)
    assert decision.capability is None
    assert not is_folder_question(q, decision.capability)


@pytest.mark.skipif(
    not (PROJECT_ROOT / ".rag_data" / "orchestrator_route_manifest.json").is_file(),
    reason="orchestrator route index not built",
)
def test_semantic_on_wip_folder_tree() -> None:
    q = "Show a real WIP discipline folder tree example for HK CDE in ACC"
    decision = classify_intent(q, mode="on")
    assert decision.capability == "folder"
    assert decision.track == "hybrid"


@pytest.mark.skipif(
    not (PROJECT_ROOT / ".rag_data" / "orchestrator_route_manifest.json").is_file(),
    reason="orchestrator route index not built",
)
def test_semantic_on_bare_wip_null() -> None:
    q = "What is WIP in Hong Kong CDE?"
    decision = classify_intent(q, mode="on")
    assert decision.capability is None


def test_semantic_router_index_missing_fallback() -> None:
    cfg = AppConfig(
        semantic_router=SemanticRouterConfig(mode="on"),
        storage=StorageConfig(data_dir=PROJECT_ROOT / ".rag_data_missing_test"),
    )
    router = SemanticRouter(cfg)
    result = router.route("设置权限")
    assert not result.index_available
    assert result.fallback_reason == "index_missing"
