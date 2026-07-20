"""Answer guidance soft-check unit tests."""

from rag.orchestrator.validate import (
    check_answer_guidance,
    has_actionable_guidance,
    looks_like_howto_question,
)


def test_howto_detection():
    assert looks_like_howto_question("怎么设置文件夹权限")
    assert looks_like_howto_question("How to configure WIP folders in ACC")
    assert not looks_like_howto_question("Autodesk Docs 中单个文件最大可以多大？")


def test_actionable_guidance_detects_steps():
    assert has_actionable_guidance(
        "结论：需要设置权限。\n1. 打开 Docs → Files\n2. 选择文件夹并设置权限\n3. 确认成员可见"
    )
    assert not has_actionable_guidance("需要设置权限。")


def test_check_answer_guidance_soft_issue():
    issue = check_answer_guidance("如何配置文件夹权限", "需要设置权限。")
    assert issue is not None
    assert issue.code == "insufficient_guidance"
    assert issue.severity == "soft"

    ok = check_answer_guidance(
        "如何配置文件夹权限",
        "结论：在 Docs 设置权限。\n1. Docs → Files\n2. 选择文件夹权限\n3. 验证成员可见",
    )
    assert ok is None

    fact = check_answer_guidance("单个文件最大可以多大？", "最大 5TB。[1]")
    assert fact is None
