"""不依赖大模型：从已检索 chunk 规则拼装 hybrid 答案（capability 可扩展）。"""

from __future__ import annotations

import re

from rag.orchestrator.merge import MergedContexts, TrackedChunk

_FENCE_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)


def _idx(tracked: list[TrackedChunk], track: str) -> int | None:
    for item in tracked:
        if item.track == track:
            return item.display_index
    return None


def _docs_indices(tracked: list[TrackedChunk]) -> list[int]:
    return [item.display_index for item in tracked if item.track == "docs"]


def _extract_tree(text: str) -> str | None:
    match = _FENCE_RE.search(text)
    if not match:
        return None
    body = match.group(1).strip()
    return body if "01_WIP" in body else None


def compose_folder_hybrid(merged: MergedContexts) -> str | None:
    """folder capability：四段答案由资料抽取拼装，避免小 LLM 胡说「无法确认」。"""
    tracked = merged.tracked
    if not tracked:
        return None

    hk_idx = _idx(tracked, "hk_cde")
    pb_idx = _idx(tracked, "playbook")
    doc_idxs = _docs_indices(tracked)
    if hk_idx is None or pb_idx is None or not doc_idxs:
        return None

    hk = next(t.chunk for t in tracked if t.track == "hk_cde")
    pb = next(t.chunk for t in tracked if t.track == "playbook")
    docs = [t.chunk for t in tracked if t.track == "docs"]

    if "01_WIP" not in pb.text and "2_wip" not in pb.source_url:
        return None

    tree = _extract_tree(pb.text)
    doc_cite = doc_idxs[0] if len(doc_idxs) == 1 else doc_idxs
    doc_cite_str = (
        f"[{doc_cite}]"
        if isinstance(doc_cite, int)
        else "[" + "][".join(str(i) for i in doc_cite) + "]"
    )

    standards = f"""## 标准要求
- 项目数据应放在标准 CDE 文件夹结构中，遵循 ISO 19650 的 **WIP / Shared / Published / Archive(d)** 数据隔离原则 [{hk_idx}]
- 多栋/多区项目应在 CDE 内为各元素设子文件夹，保持 BIM 结构 [{hk_idx}]
- 本地缓存文件须有严格目录惯例，且最终须回到 CDE 管理 [{hk_idx}]"""

    impl_lines = [
        f"- 在 **Project Files** 下建四顶层夹：`01_WIP`、`02_Shared`、`03_Published`、`04_Archive`（手册推荐配置，写入 BEP 可调） [{pb_idx}]",
        f"- WIP 下按专业分子夹（ARC / STR / MEP / CIV / LAN / GEO / SUR），其下 Models、Drawings、Schedules 等 [{pb_idx}]",
        f"- **02_Shared / 03_Published** 启用 Naming Standard；**01_WIP** 可不强制命名，边界写在 BEP [{pb_idx}]",
    ]
    if tree:
        impl_lines.append(f"- 推荐目录树示例：\n```\n{tree}\n```")
    implementation = "## 实施建议\n" + "\n".join(impl_lines)

    product_bullets: list[str] = []
    for chunk in docs:
        low = chunk.text.lower()
        if "organize" in low or "folder" in low or "files" in chunk.title.lower():
            product_bullets.append(
                f"- **Docs → Files**：创建子文件夹组织项目数据；子夹可继承父夹权限并可单独调整 {doc_cite_str}"
            )
        if "template" in low or "naming" in low:
            product_bullets.append(
                f"- 可用 **Project Template** 预置文件夹；在 **Naming Standards** 对 Shared/Published 强制命名 {doc_cite_str}"
            )
        if "permission" in low:
            product_bullets.append(
                f"- 在文件夹 **Permissions** 按角色限制可见/上传，实现 WIP 专业隔离 {doc_cite_str}"
            )
    if not product_bullets:
        product_bullets.append(
            f"- 在 Docs **Files** 中手动创建与手册一致的文件夹层级，并配置权限与命名标准 {doc_cite_str}"
        )
    # 去重保序
    seen: set[str] = set()
    unique_product: list[str] = []
    for line in product_bullets:
        if line not in seen:
            seen.add(line)
            unique_product.append(line)
    product = "## 产品操作\n" + "\n".join(unique_product[:4])

    alignment = f"""## 对齐与缺口
- **对齐**：港标四容器 = 用文件夹位置 + 权限表达状态；手册用 `01_WIP`…`04_Archive` 命名映射 [{hk_idx}][{pb_idx}]
- **对齐**：Docs 提供建夹、权限、命名标准，可承载上述结构 {doc_cite_str}
- **缺口**：ACC **不会**在审批通过后自动把文件从 WIP 迁到 Shared；Status 属性也 **不会**随 Workflow 自动更新，需文控人工操作或 API [{pb_idx}]"""

    return "\n\n".join([standards, implementation, product, alignment])


def try_compose_structured_hybrid(
    merged: MergedContexts,
    capability: str | None,
    *,
    question: str = "",
    answer_lang: str = "auto",
) -> str | None:
    from rag.answer_language import localize_hybrid_section_headers, resolve_answer_language
    from rag.orchestrator.classify import is_folder_question

    text: str | None = None
    if capability == "folder" or is_folder_question(question, capability):
        text = compose_folder_hybrid(merged)
    if not text:
        return None
    lang = resolve_answer_language(question, answer_lang)
    return localize_hybrid_section_headers(text, lang)
