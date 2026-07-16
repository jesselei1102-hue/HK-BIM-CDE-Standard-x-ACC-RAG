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
- **Gap**: Workflow **Action Upon Completion** can **copy** approved files and **update attributes**, but it is copy≠move (source remains) and the target must be under the same top-level folder — document source cleanup in the BEP [{pb_idx}]"""

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
- **缺口**：Workflow **Action Upon Completion** 可 **複製**已批准檔並 **更新屬性**，但是 copy≠move（源檔仍在），且目標須同 top-level；源夾清理寫入 BEP [{pb_idx}]"""
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
- **缺口**：Workflow **Action Upon Completion** 可 **复制**已批准文件并 **更新属性**，但是 copy≠move（源文件仍在），且目标须同 top-level；源夹清理写入 BEP [{pb_idx}]"""

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


def _doc_cite_str(tracked: list[TrackedChunk]) -> str | None:
    doc_idxs = _docs_indices(tracked)
    if not doc_idxs:
        return None
    if len(doc_idxs) == 1:
        return f"[{doc_idxs[0]}]"
    return "[" + "][".join(str(i) for i in doc_idxs) + "]"


def compose_workflow_hybrid(
    merged: MergedContexts,
    *,
    lang: AnswerLanguage = "zh-Hans",
) -> str | None:
    """workflow capability：固定拼装 Action Upon Completion，避免小模型写回「不能自动迁夹」。"""
    tracked = merged.tracked
    if not tracked:
        return None
    hk_idx = _idx(tracked, "hk_cde")
    pb_idx = _idx(tracked, "playbook")
    doc_cite_str = _doc_cite_str(tracked)
    if hk_idx is None or pb_idx is None or doc_cite_str is None:
        return None

    h0, h1, h2, h3 = hybrid_section_headers(lang)
    if lang == "en":
        return "\n\n".join(
            [
                f"""## {h0}
- HK / ISO-aligned CDE needs a formal check → review → approve gate before information moves container state [{hk_idx}]
- Status / suitability codes must show whether further authorisation or client acceptance is required [{hk_idx}]
- An Information Gateway is the audited transition between WIP / Shared / Published / Archive [{hk_idx}]""",
                f"""## {h1}
- Map each gateway to an ACC Approval Workflow: WIP→Shared (internal), Shared→Published (formal) [{pb_idx}]
- In each workflow enable **Action Upon Completion → Copy approved files** to the next container folder (e.g. `02_Shared`, `03_Published`) [{pb_idx}]
- Also enable **Update attributes** (Status / Revision / Approval Date); prefer **When = All files approved** [{pb_idx}]
- Remember copy≠move: clean up or archive source files per BEP [{pb_idx}]""",
                f"""## {h2}
1. Docs → **Reviews** → Settings → **Create approval workflow**; pick a template (One/Two/Three Step…) {doc_cite_str}
2. Set Initiator / Reviewer / Approver, time allowed, and File Review Status labels {doc_cite_str}
3. Under **Action Upon Completion**: turn on **Copy approved files**, choose When + target folder (same top-level); turn on **Update attributes** as needed {doc_cite_str}
4. Save/activate; members start reviews with that workflow; approved files copy to the target folder on completion {doc_cite_str}""",
                f"""## {h3}
- **Aligned**: Docs Approval Workflow + Action Upon Completion can implement the HK gateway approve + copy + attribute update path [{hk_idx}][{pb_idx}]{doc_cite_str}
- **Gap**: Action is **copy** not move; target must share the source top-level folder; source cleanup / Archive locking still need BEP discipline [{pb_idx}]""",
            ]
        )
    if lang == "zh-Hant":
        return "\n\n".join(
            [
                f"""## {h0}
- 港標 / ISO 對齊的 CDE 要求信息在轉換容器狀態前走正式 check → review → approve [{hk_idx}]
- Status / suitability 須標明是否還需後續授權或客戶接受 [{hk_idx}]
- Information Gateway = WIP / Shared / Published / Archive 之間帶審計的關卡 [{hk_idx}]""",
                f"""## {h1}
- 每個 Gateway 對應一個 ACC Approval Workflow：WIP→Shared（內部）、Shared→Published（正式） [{pb_idx}]
- 工作流開啟 **Action Upon Completion → Copy approved files** 到下一容器（如 `02_Shared`、`03_Published`） [{pb_idx}]
- 同步開啟 **Update attributes**（Status / Revision / Approval Date）；When 建議 **All files approved** [{pb_idx}]
- copy≠move：源檔清理/歸檔寫入 BEP [{pb_idx}]""",
                f"""## {h2}
1. Docs → **Reviews** → Settings → **Create approval workflow**，選模板（One/Two/Three Step…） {doc_cite_str}
2. 設定 Initiator / Reviewer / Approver、時限與 File Review Status {doc_cite_str}
3. 在 **Action Upon Completion** 開啟 **Copy approved files**（選 When + 目標夾，須同 top-level），並按需開啟 **Update attributes** {doc_cite_str}
4. 保存並啟用；成員用該工作流發起 Review；批准後文件複製到目標夾 {doc_cite_str}""",
                f"""## {h3}
- **對齊**：Docs Approval Workflow + Action Upon Completion 可承載港標 Gateway 的審批、複製與屬性更新 [{hk_idx}][{pb_idx}]{doc_cite_str}
- **缺口**：是 **copy** 非 move；目標須同 top-level；源夾清理 / Archive 鎖定仍靠 BEP 紀律 [{pb_idx}]""",
            ]
        )
    return "\n\n".join(
        [
            f"""## {h0}
- 港标 / ISO 对齐的 CDE 要求信息在转换容器状态前走正式 check → review → approve [{hk_idx}]
- Status / suitability 须标明是否还需后续授权或客户接受 [{hk_idx}]
- Information Gateway = WIP / Shared / Published / Archive 之间带审计的关卡 [{hk_idx}]""",
            f"""## {h1}
- 每个 Gateway 对应一个 ACC Approval Workflow：WIP→Shared（内部）、Shared→Published（正式） [{pb_idx}]
- 工作流开启 **Action Upon Completion → Copy approved files** 到下一容器（如 `02_Shared`、`03_Published`） [{pb_idx}]
- 同步开启 **Update attributes**（Status / Revision / Approval Date）；When 建议 **All files approved** [{pb_idx}]
- copy≠move：源文件清理/归档写入 BEP [{pb_idx}]""",
            f"""## {h2}
1. Docs → **Reviews** → Settings → **Create approval workflow**，选模板（One/Two/Three Step…） {doc_cite_str}
2. 设定 Initiator / Reviewer / Approver、时限与 File Review Status {doc_cite_str}
3. 在 **Action Upon Completion** 开启 **Copy approved files**（选 When + 目标夹，须同 top-level），并按需开启 **Update attributes** {doc_cite_str}
4. 保存并启用；成员用该工作流发起 Review；批准后文件复制到目标夹 {doc_cite_str}""",
            f"""## {h3}
- **对齐**：Docs Approval Workflow + Action Upon Completion 可承载港标 Gateway 的审批、复制与属性更新 [{hk_idx}][{pb_idx}]{doc_cite_str}
- **缺口**：是 **copy** 非 move；目标须同 top-level；源夹清理 / Archive 锁定仍靠 BEP 纪律 [{pb_idx}]""",
        ]
    )


def try_compose_structured_hybrid(
    merged: MergedContexts,
    capability: str | None,
    *,
    question: str = "",
    answer_lang: str = "auto",
) -> str | None:
    lang = resolve_answer_language(question, answer_lang)
    if capability == "folder":
        return compose_folder_hybrid(merged, lang=lang)
    if capability == "workflow":
        return compose_workflow_hybrid(merged, lang=lang)
    return None
