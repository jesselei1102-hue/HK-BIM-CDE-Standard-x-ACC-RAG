"""capability 分类、冲突优先级、folder 误触发防护。"""

from __future__ import annotations

from rag.orchestrator.classify import (
    classify_intent,
    classify_intent_legacy,
    detect_capability,
    is_folder_question,
)


def test_wip_glossary_is_not_folder_question() -> None:
    q = "WIP 是什么"
    decision = classify_intent(q)
    assert decision.track == "hk_cde"
    assert decision.capability is None
    assert not is_folder_question(q, decision.capability)


def test_permissions_capability() -> None:
    q = "设置权限"
    cap = detect_capability(q)
    assert cap is not None
    assert cap.key == "permissions"
    decision = classify_intent(q)
    assert decision.track == "docs"
    assert decision.capability == "permissions"
    assert "Folder Permissions" in (decision.product_query or "")


def test_folder_permissions_prefers_permissions_over_folder() -> None:
    cap = detect_capability("如何设置文件夹权限")
    assert cap is not None
    assert cap.key == "permissions"


def test_industry_overview_rewrite_cic() -> None:
    from rag.orchestrator.classify import (
        classify_intent,
        rewrite_industry_overview_query,
    )

    q = "I want to know more about CIC Standard, can you tell me"
    rewritten = rewrite_industry_overview_query(q)
    assert rewritten is not None
    assert "CICBIMS" in rewritten
    decision = classify_intent(q)
    assert decision.track == "hk_cde"
    assert decision.industry_query and "CICBIMS" in decision.industry_query


def test_industry_overview_rewrite_harmonisation() -> None:
    from rag.orchestrator.classify import rewrite_industry_overview_query

    q = "I want to know BIM harmonization guide"
    rewritten = rewrite_industry_overview_query(q)
    assert rewritten is not None
    assert "Harmonisation" in rewritten or "harmonisation" in rewritten.lower()


def test_industry_overview_skips_specific_devb_section() -> None:
    from rag.orchestrator.classify import rewrite_industry_overview_query

    q = "DEVB Harmonisation v3: THE WAY FORWARD"
    assert rewrite_industry_overview_query(q) is None


def test_exact_title_bonus_prefers_full_section() -> None:
    from rag.industry_hk.source_family import exact_title_bonus

    q = "CIC CDE Beginner Guide: 2.3.1. Subscription/Perpetual"
    full = exact_title_bonus(q, "2.3.1. Subscription/Perpetual")
    frag = exact_title_bonus(q, "Perpetual")
    assert full > frag
    assert full >= 3.0

def test_folder_naming_prefers_naming_over_folder() -> None:
    cap = detect_capability("文件夹命名标准怎么配")
    assert cap is not None
    assert cap.key == "naming"


def test_project_template_beats_folder() -> None:
    cap = detect_capability("ACC项目模板的文件夹结构怎么配")
    assert cap is not None
    assert cap.key == "project_template"


def test_gateway_workflow_on_industry_track() -> None:
    decision = classify_intent("Authorisation Gateway")
    assert decision.track == "hk_cde"
    assert decision.capability == "workflow"
    assert "authorisation gateway" in (decision.industry_query or "").lower()


def test_docs_create_project_uses_template_query() -> None:
    decision = classify_intent("如何在ACC创建项目")
    assert decision.track == "docs"
    assert decision.capability == "project_create"
    assert "create and manage projects" in (decision.product_query or "").lower()


def test_playbook_only_uses_capability_query() -> None:
    decision = classify_intent("项目模板怎么配置")
    assert decision.track == "playbook"
    assert decision.capability == "project_template"
    assert "project template" in (decision.playbook_query or "").lower()


def test_hybrid_folder_capability() -> None:
    decision = classify_intent(
        "How do I set up ACC Docs folder structure to align with HK standard"
    )
    assert decision.track == "hybrid"
    assert decision.capability == "folder"
    assert is_folder_question(decision.product_query or "", decision.capability)


def test_wip_folder_tree_triggers_folder_capability() -> None:
    q = "Show a real WIP discipline folder tree example for HK CDE in ACC"
    cap = detect_capability(q)
    assert cap is not None
    assert cap.key == "folder"
    decision = classify_intent(q)
    assert decision.track == "hybrid"
    assert decision.capability == "folder"
    assert "2_wip" in (decision.playbook_query or "").lower() or "01_WIP" in (
        decision.playbook_query or ""
    )


def test_bare_wip_glossary_still_not_folder() -> None:
    q = "What is WIP in Hong Kong CDE?"
    assert detect_capability(q) is None
    decision = classify_intent(q)
    assert decision.capability is None
    assert not is_folder_question(q, decision.capability)

def test_bim_manager_roles_routes_hybrid() -> None:
    q = "BIM Manager的责任是什么？在ACC上他需要使用哪些功能"
    cap = detect_capability(q)
    assert cap is not None
    assert cap.key == "roles"
    decision = classify_intent_legacy(q)
    assert decision.track == "hybrid"
    assert decision.capability == "roles"
    assert decision.has_industry_signal
    assert "BIM Manager" in (decision.industry_query or "")
    assert "Project Admin" in (decision.product_query or "") or "ACC" in (
        decision.product_query or ""
    )


def test_explicit_folder_words_without_capability() -> None:
    assert is_folder_question("请说明四容器目录结构", capability=None)
    assert not is_folder_question("WIP 区和 Shared 是什么", capability=None)
