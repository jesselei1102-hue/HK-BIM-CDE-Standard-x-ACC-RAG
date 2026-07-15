"""不依赖大模型：从已检索 chunk 规则拼装 hybrid 答案（capability 可扩展）。"""

from __future__ import annotations

import re

from rag.answer_language import AnswerLanguage, hybrid_section_headers, resolve_answer_language
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


def _compose_folder_hybrid_en(
    *,
    headers: tuple[str, str, str, str],
    hk_idx: int,
    pb_idx: int,
    doc_cite_str: str,
    tree: str | None,
    docs: list,
) -> str:
    h0, h1, h2, h3 = headers
    standards = f"""## {h0}
- Keep project data in a standard CDE folder structure under ISO 19650 **WIP / Shared / Published / Archive(d)** isolation [{hk_idx}]
- For multi-building / multi-zone projects, create element subfolders inside the CDE to preserve BIM structure [{hk_idx}]
- Local cache files must follow a strict directory convention and ultimately return to CDE control [{hk_idx}]"""

    impl_lines = [
        f"- Under **Project Files**, create four top-level folders: `01_WIP`, `02_Shared`, `03_Published`, `04_Archive` (playbook defaults; adjustable in the BEP) [{pb_idx}]",
        f"- Under WIP, add discipline subfolders (ARC / STR / MEP / CIV / LAN / GEO / SUR), then Models, Drawings, Schedules, etc. [{pb_idx}]",
        f"- Enforce **Naming Standard** on **02_Shared / 03_Published**; **01_WIP** may stay flexible — document the boundary in the BEP [{pb_idx}]",
    ]
    if tree:
        impl_lines.append(f"- Recommended folder tree:\n```\n{tree}\n```")
    implementation = f"## {h1}\n" + "\n".join(impl_lines)

    product_bullets: list[str] = []
    for chunk in docs:
        low = chunk.text.lower()
        if "organize" in low or "folder" in low or "files" in chunk.title.lower():
            product_bullets.append(
                f"- **Docs → Files**: create subfolders to organize project data; children inherit parent permissions and can be adjusted {doc_cite_str}"
            )
        if "template" in low or "naming" in low:
            product_bullets.append(
                f"- Use a **Project Template** to pre-seed folders; apply **Naming Standards** on Shared/Published {doc_cite_str}"
            )
        if "permission" in low:
            product_bullets.append(
                f"- Set folder **Permissions** by role for visibility/upload control (WIP discipline isolation) {doc_cite_str}"
            )
    if not product_bullets:
        product_bullets.append(
            f"- In Docs **Files**, create the playbook folder hierarchy manually, then configure permissions and naming standards {doc_cite_str}"
        )
    seen: set[str] = set()
    unique_product: list[str] = []
    for line in product_bullets:
        if line not in seen:
            seen.add(line)
            unique_product.append(line)
    product = f"## {h2}\n" + "\n".join(unique_product[:4])

    alignment = f"""## {h3}
- **Aligned**: HK four containers map to folder location + permissions; the playbook uses `01_WIP`…`04_Archive` naming [{hk_idx}][{pb_idx}]
- **Aligned**: Docs supports folders, permissions, and naming standards to host that structure {doc_cite_str}
- **Gap**: ACC does **not** auto-move files from WIP to Shared after approval; Status also does **not** auto-update with Workflow — needs document control or API [{pb_idx}]"""

    return "\n\n".join([standards, implementation, product, alignment])


def _compose_folder_hybrid_zh(
    *,
    lang: AnswerLanguage,
    headers: tuple[str, str, str, str],
    hk_idx: int,
    pb_idx: int,
    doc_cite_str: str,
    tree: str | None,
    docs: list,
) -> str:
    h0, h1, h2, h3 = headers
    if lang == "zh-Hant":
        standards = f"""## {h0}
- 項目資料應放在標準 CDE 資料夾結構中，遵循 ISO 19650 的 **WIP / Shared / Published / Archive(d)** 資料隔離原則 [{hk_idx}]
- 多棟/多區項目應在 CDE 內為各元素設子資料夾，保持 BIM 結構 [{hk_idx}]
- 本地快取檔案須有嚴格目錄慣例，且最終須回到 CDE 管理 [{hk_idx}]"""
        impl_lines = [
            f"- 在 **Project Files** 下建四頂層夾：`01_WIP`、`02_Shared`、`03_Published`、`04_Archive`（手冊推薦配置，寫入 BEP 可調） [{pb_idx}]",
            f"- WIP 下按專業分子夾（ARC / STR / MEP / CIV / LAN / GEO / SUR），其下 Models、Drawings、Schedules 等 [{pb_idx}]",
            f"- **02_Shared / 03_Published** 啟用 Naming Standard；**01_WIP** 可不強制命名，邊界寫在 BEP [{pb_idx}]",
        ]
        if tree:
            impl_lines.append(f"- 推薦目錄樹示例：\n```\n{tree}\n```")
        product_templates = {
            "organize": f"- **Docs → Files**：建立子資料夾組織項目資料；子夾可繼承父夾權限並可單獨調整 {doc_cite_str}",
            "template": f"- 可用 **Project Template** 預置資料夾；在 **Naming Standards** 對 Shared/Published 強制命名 {doc_cite_str}",
            "permission": f"- 在資料夾 **Permissions** 按角色限制可見/上傳，實現 WIP 專業隔離 {doc_cite_str}",
            "fallback": f"- 在 Docs **Files** 中手動建立與手冊一致的資料夾層級，並配置權限與命名標準 {doc_cite_str}",
        }
        alignment = f"""## {h3}
- **對齊**：港標四容器 = 用資料夾位置 + 權限表達狀態；手冊用 `01_WIP`…`04_Archive` 命名映射 [{hk_idx}][{pb_idx}]
- **對齊**：Docs 提供建夾、權限、命名標準，可承載上述結構 {doc_cite_str}
- **缺口**：ACC **不會**在審批通過後自動把檔案從 WIP 遷到 Shared；Status 屬性也 **不會**隨 Workflow 自動更新，需文控人工操作或 API [{pb_idx}]"""
    else:
        standards = f"""## {h0}
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
        product_templates = {
            "organize": f"- **Docs → Files**：创建子文件夹组织项目数据；子夹可继承父夹权限并可单独调整 {doc_cite_str}",
            "template": f"- 可用 **Project Template** 预置文件夹；在 **Naming Standards** 对 Shared/Published 强制命名 {doc_cite_str}",
            "permission": f"- 在文件夹 **Permissions** 按角色限制可见/上传，实现 WIP 专业隔离 {doc_cite_str}",
            "fallback": f"- 在 Docs **Files** 中手动创建与手册一致的文件夹层级，并配置权限与命名标准 {doc_cite_str}",
        }
        alignment = f"""## {h3}
- **对齐**：港标四容器 = 用文件夹位置 + 权限表达状态；手册用 `01_WIP`…`04_Archive` 命名映射 [{hk_idx}][{pb_idx}]
- **对齐**：Docs 提供建夹、权限、命名标准，可承载上述结构 {doc_cite_str}
- **缺口**：ACC **不会**在审批通过后自动把文件从 WIP 迁到 Shared；Status 属性也 **不会**随 Workflow 自动更新，需文控人工操作或 API [{pb_idx}]"""

    implementation = f"## {h1}\n" + "\n".join(impl_lines)

    product_bullets: list[str] = []
    for chunk in docs:
        low = chunk.text.lower()
        if "organize" in low or "folder" in low or "files" in chunk.title.lower():
            product_bullets.append(product_templates["organize"])
        if "template" in low or "naming" in low:
            product_bullets.append(product_templates["template"])
        if "permission" in low:
            product_bullets.append(product_templates["permission"])
    if not product_bullets:
        product_bullets.append(product_templates["fallback"])
    seen: set[str] = set()
    unique_product: list[str] = []
    for line in product_bullets:
        if line not in seen:
            seen.add(line)
            unique_product.append(line)
    product = f"## {h2}\n" + "\n".join(unique_product[:4])

    return "\n\n".join([standards, implementation, product, alignment])


def compose_folder_hybrid(
    merged: MergedContexts,
    *,
    lang: AnswerLanguage = "zh-Hans",
) -> str | None:
    """folder capability：四段答案由资料抽取拼装，避免小 LLM 胡说「无法确认」。"""
    tracked = merged.tracked
    if not tracked:
        return None

    hk_idx = _idx(tracked, "hk_cde")
    pb_idx = _idx(tracked, "playbook")
    doc_idxs = _docs_indices(tracked)
    if hk_idx is None or pb_idx is None or not doc_idxs:
        return None

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
    headers = hybrid_section_headers(lang)
    kwargs = {
        "headers": headers,
        "hk_idx": hk_idx,
        "pb_idx": pb_idx,
        "doc_cite_str": doc_cite_str,
        "tree": tree,
        "docs": docs,
    }
    if lang == "en":
        return _compose_folder_hybrid_en(**kwargs)
    return _compose_folder_hybrid_zh(lang=lang, **kwargs)


def try_compose_structured_hybrid(
    merged: MergedContexts,
    capability: str | None,
    *,
    question: str = "",
    answer_lang: str = "auto",
) -> str | None:
    if capability != "folder":
        return None
    lang = resolve_answer_language(question, answer_lang)
    return compose_folder_hybrid(merged, lang=lang)
