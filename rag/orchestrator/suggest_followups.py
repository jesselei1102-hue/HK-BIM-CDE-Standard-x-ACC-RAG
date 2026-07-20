"""答后追问建议：锚定本轮 capability / track / 来源；语言跟随提问。"""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag.answer_language import resolve_answer_language
from rag.orchestrator.merge import MergedContexts

# lang -> capability -> questions
_CAPABILITY_FOLLOWUPS: dict[str, dict[str, tuple[str, ...]]] = {
    "en": {
        "folder": (
            "How should discipline subfolders under WIP (ARC/STR/MEP) be set up?",
            "Should Naming Standard be enforced on Shared / Published?",
            "How do the HK four CDE containers map to ACC Project Files?",
        ),
        "permissions": (
            "What are the Docs folder permission levels?",
            "Do subfolder permissions inherit, and how do I change them?",
            "How should WIP permissions isolate disciplines for HK CDE?",
        ),
        "naming": (
            "What fields are in an Information Container ID?",
            "How do I create a Naming Standard in ACC Docs?",
            "How do DEVB / CICBIMS naming align with Docs naming standards?",
        ),
        "workflow": (
            "How does Authorisation Gateway map to ACC Reviews?",
            "How do I configure Action Upon Completion?",
            "After approval, how do files move into Shared / Published?",
        ),
        "project_create": (
            "After creating an ACC project, what defaults should I configure next?",
            "What is the difference between a project template and creating a project?",
            "How do PIR requirements align with project setup steps?",
        ),
        "project_template": (
            "What does the ACC HK GC / Buildings template include?",
            "How do I change the folder structure inside a project template?",
            "After applying a template, what HK items still need manual setup?",
        ),
        "model_viewer": (
            "How do I filter RVT / IFC properties in Model Browser?",
            "What are common Viewer Settings options?",
            "How do I review a federated model by discipline?",
        ),
    },
    "zh-Hans": {
        "folder": (
            "WIP 下专业子文件夹（ARC/STR/MEP）怎么配？",
            "Shared / Published 上要不要开 Naming Standard？",
            "港标四容器和 ACC Project Files 怎么对齐？",
        ),
        "permissions": (
            "文件夹权限级别有哪些？",
            "子文件夹权限会继承吗？怎么改？",
            "按港标怎么给 WIP 做专业隔离权限？",
        ),
        "naming": (
            "Information Container ID 命名字段有哪些？",
            "在 ACC Docs 里怎么创建 Naming Standard？",
            "DEVB / CICBIMS 命名和 Docs 命名标准怎么对齐？",
        ),
        "workflow": (
            "Authorisation Gateway 和 ACC Reviews 怎么对应？",
            "Action Upon Completion 怎么设置？",
            "审批通过后文件如何进入 Shared / Published？",
        ),
        "project_create": (
            "创建 ACC 项目后还要配哪些默认设置？",
            "项目模板和新建项目有什么区别？",
            "港标项目信息要求（PIR）和建项步骤怎么对齐？",
        ),
        "project_template": (
            "ACC HK GC / Buildings 模板包含哪些内容？",
            "项目模板里的文件夹结构怎么改？",
            "用模板落地后还要手动补哪些港标项？",
        ),
        "model_viewer": (
            "Model Browser 怎么过滤 RVT / IFC 属性？",
            "Viewer Settings 有哪些常用选项？",
            "联邦模型审查时怎么按专业查看？",
        ),
    },
    "zh-Hant": {
        "folder": (
            "WIP 下專業子資料夾（ARC/STR/MEP）怎麼配？",
            "Shared / Published 上要不要開 Naming Standard？",
            "港標四容器和 ACC Project Files 怎麼對齊？",
        ),
        "permissions": (
            "資料夾權限級別有哪些？",
            "子資料夾權限會繼承嗎？怎麼改？",
            "按港標怎麼給 WIP 做專業隔離權限？",
        ),
        "naming": (
            "Information Container ID 命名欄位有哪些？",
            "在 ACC Docs 裡怎麼建立 Naming Standard？",
            "DEVB / CICBIMS 命名和 Docs 命名標準怎麼對齊？",
        ),
        "workflow": (
            "Authorisation Gateway 和 ACC Reviews 怎麼對應？",
            "Action Upon Completion 怎麼設置？",
            "審批通過後檔案如何進入 Shared / Published？",
        ),
        "project_create": (
            "建立 ACC 專案後還要配哪些預設設置？",
            "專案範本和新建專案有什麼區別？",
            "港標專案資訊要求（PIR）和建項步驟怎麼對齊？",
        ),
        "project_template": (
            "ACC HK GC / Buildings 範本包含哪些內容？",
            "專案範本裡的資料夾結構怎麼改？",
            "用範本落地後還要手動補哪些港標項？",
        ),
        "model_viewer": (
            "Model Browser 怎麼過濾 RVT / IFC 屬性？",
            "Viewer Settings 有哪些常用選項？",
            "聯邦模型審查時怎麼按專業查看？",
        ),
    },
}

_TRACK_FOLLOWUPS: dict[str, dict[str, tuple[str, ...]]] = {
    "en": {
        "hk_cde": (
            "What is the difference between WIP and Shared?",
            "What does a CDE Gateway do?",
            "What project folder structure does HK CDE recommend?",
        ),
        "docs": (
            "How do I create subfolders in Docs?",
            "How do I share files with project members?",
            "Which file formats does Docs support?",
        ),
        "playbook": (
            "What WIP container setup does the playbook recommend?",
            "What are the playbook default permission settings?",
            "What gaps remain on the HK alignment table?",
        ),
        "hybrid": (
            "How do I implement this HK requirement in ACC?",
            "How do playbook defaults differ from the standard clauses?",
            "What are the detailed Docs menu paths for this?",
        ),
    },
    "zh-Hans": {
        "hk_cde": (
            "WIP 和 Shared 有什么区别？",
            "CDE Gateway 的作用是什么？",
            "港标推荐的项目文件夹结构是什么？",
        ),
        "docs": (
            "在 Docs 里怎么创建子文件夹？",
            "如何分享文件给项目成员？",
            "Docs 支持哪些文件格式？",
        ),
        "playbook": (
            "Playbook 推荐的 WIP 容器配置是什么？",
            "实施手册里权限默认怎么配？",
            "港标对齐表还有哪些缺口？",
        ),
        "hybrid": (
            "ACC 里怎么落实这个港标要求？",
            "Playbook 推荐配置和标准条文有何差异？",
            "产品操作步骤的详细菜单路径是什么？",
        ),
    },
    "zh-Hant": {
        "hk_cde": (
            "WIP 和 Shared 有什麼區別？",
            "CDE Gateway 的作用是什麼？",
            "港標推薦的專案資料夾結構是什麼？",
        ),
        "docs": (
            "在 Docs 裡怎麼建立子資料夾？",
            "如何分享檔案給專案成員？",
            "Docs 支援哪些檔案格式？",
        ),
        "playbook": (
            "Playbook 推薦的 WIP 容器配置是什麼？",
            "實施手冊裡權限預設怎麼配？",
            "港標對齊表還有哪些缺口？",
        ),
        "hybrid": (
            "ACC 裡怎麼落實這個港標要求？",
            "Playbook 推薦配置和標準條文有何差異？",
            "產品操作步驟的詳細選單路徑是什麼？",
        ),
    },
}

_SOURCE_HINTS: tuple[tuple[re.Pattern[str], dict[str, tuple[str, ...]]], ...] = (
    (
        re.compile(r"zcp|zero\s*carbon|figures_transcription|01_Revit\s*Model", re.I),
        {
            "en": (
                "Which folders does ZCP BIMIP require at handover?",
                "What is the ZCP model file naming convention?",
                "How does ZCP move data from Revit to Planon / Forge?",
            ),
            "zh-Hans": (
                "ZCP BIMIP 交接要交哪些文件夹？",
                "ZCP 模型文件命名规则是什么？",
                "ZCP 里 Revit 到 Planon / Forge 的数据流是怎样的？",
            ),
            "zh-Hant": (
                "ZCP BIMIP 交接要交哪些資料夾？",
                "ZCP 模型檔案命名規則是什麼？",
                "ZCP 裡 Revit 到 Planon / Forge 的資料流是怎樣的？",
            ),
        },
    ),
    (
        re.compile(r"amfm|asset\s*management|facility\s*management", re.I),
        {
            "en": (
                "In the AM/FM case, how is BIM integrated with asset information?",
                "How is model geometry and information kept up to date in O&M?",
                "What lessons learnt are documented in the AM/FM case?",
            ),
            "zh-Hans": (
                "AM/FM 案例里 BIM 如何对接资产信息？",
                "运维阶段模型几何和信息怎么维护？",
                "AM/FM 案例有哪些经验教训？",
            ),
            "zh-Hant": (
                "AM/FM 案例裡 BIM 如何對接資產資訊？",
                "運維階段模型幾何和資訊怎麼維護？",
                "AM/FM 案例有哪些經驗教訓？",
            ),
        },
    ),
    (
        re.compile(r"2_wip|WIP\s*容器|01_WIP|folder_cde", re.I),
        {
            "en": (
                "What is a full ARC/STR/MEP subtree example under WIP?",
                "Where is the naming-standard boundary between 01_WIP and 02_Shared?",
                "How are the four containers enforced with ACC permissions?",
            ),
            "zh-Hans": (
                "WIP 下 ARC/STR/MEP 子树完整示例是什么？",
                "01_WIP 和 02_Shared 的命名标准边界怎么定？",
                "四容器在 ACC 里如何用权限落实？",
            ),
            "zh-Hant": (
                "WIP 下 ARC/STR/MEP 子樹完整示例是什麼？",
                "01_WIP 和 02_Shared 的命名標準邊界怎麼定？",
                "四容器在 ACC 裡如何用權限落實？",
            ),
        },
    ),
    (
        re.compile(
            r"work_in_progress|4_2_1_work_in_progress|(?<![A-Za-z])WIP(?![A-Za-z])",
            re.I,
        ),
        {
            "en": (
                "What is the WIP Gateway?",
                "When can information move from WIP to Shared?",
                "Why must each Task Team keep a separate WIP?",
            ),
            "zh-Hans": (
                "WIP Gateway 是什么？",
                "信息何时可以从 WIP 进入 Shared？",
                "各 Task Team 的 WIP 为什么要隔离？",
            ),
            "zh-Hant": (
                "WIP Gateway 是什麼？",
                "資訊何時可以從 WIP 進入 Shared？",
                "各 Task Team 的 WIP 為什麼要隔離？",
            ),
        },
    ),
    (
        re.compile(r"Folder_Permissions|permission", re.I),
        {
            "en": (
                "What can each Docs folder permission level do?",
                "How do I set permissions in bulk by role?",
            ),
            "zh-Hans": (
                "Docs 文件夹权限级别分别能做什么？",
                "如何按角色批量设置权限？",
            ),
            "zh-Hant": (
                "Docs 資料夾權限級別分別能做什麼？",
                "如何按角色批量設置權限？",
            ),
        },
    ),
)

_GAP_FOLLOWUPS: dict[str, tuple[str, ...]] = {
    "en": (
        "How do I implement this in ACC Docs?",
        "Does the playbook have a recommended configuration?",
    ),
    "zh-Hans": (
        "在 ACC Docs 里具体怎么操作落地？",
        "Playbook 有没有对应的推荐配置？",
    ),
    "zh-Hant": (
        "在 ACC Docs 裡具體怎麼操作落地？",
        "Playbook 有沒有對應的推薦配置？",
    ),
}

_FALLBACK_FOLLOWUPS: dict[str, tuple[str, ...]] = {
    "en": (
        "What related HK standard requirements apply?",
        "How is this configured in ACC products?",
        "Are there playbook recommended defaults?",
    ),
    "zh-Hans": (
        "还有哪些相关港标要求？",
        "在 ACC 产品里对应怎么配置？",
        "实施手册有没有推荐默认值？",
    ),
    "zh-Hant": (
        "還有哪些相關港標要求？",
        "在 ACC 產品裡對應怎麼配置？",
        "實施手冊有沒有推薦預設值？",
    ),
}


@dataclass(frozen=True)
class FollowUpSuggestions:
    questions: tuple[str, ...]
    reason: str = "grounded"
    lang: str = "en"


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().casefold())


def _pick_lang(question: str, answer_lang: str | None) -> str:
    # Follow-ups always match the user's question language.
    # Ignore forced answer_lang so EN questions never get ZH chips (and vice versa).
    _ = answer_lang
    lang = resolve_answer_language(question, "auto")
    if lang not in {"en", "zh-Hans", "zh-Hant"}:
        return "en"
    return lang


def _collect_source_blob(
    *,
    chunks_docs: list | None = None,
    chunks_industry: list | None = None,
    chunks_playbook: list | None = None,
    merged: MergedContexts | None = None,
) -> str:
    parts: list[str] = []
    if merged is not None:
        for item in merged.tracked:
            parts.append(item.chunk.title or "")
            parts.append(item.chunk.source_url or "")
            parts.append((item.chunk.text or "")[:240])
    for group in (chunks_docs or [], chunks_industry or [], chunks_playbook or []):
        for chunk in group:
            parts.append(getattr(chunk, "title", "") or "")
            parts.append(getattr(chunk, "source_url", "") or "")
            parts.append((getattr(chunk, "text", "") or "")[:240])
    return "\n".join(parts)


def suggest_followups(
    *,
    question: str,
    answer: str | None = None,
    track: str | None = None,
    capability: str | None = None,
    chunks_docs: list | None = None,
    chunks_industry: list | None = None,
    chunks_playbook: list | None = None,
    merged: MergedContexts | None = None,
    limit: int = 3,
    answer_lang: str | None = None,
) -> FollowUpSuggestions:
    """基于本轮路由与召回来源生成追问建议；语言跟随提问 / answer_lang。"""
    limit = max(1, min(limit, 5))
    lang = _pick_lang(question, answer_lang)
    q_norm = _normalize(question)
    a_norm = _normalize(answer or "")
    blob = _collect_source_blob(
        chunks_docs=chunks_docs,
        chunks_industry=chunks_industry,
        chunks_playbook=chunks_playbook,
        merged=merged,
    )

    candidates: list[str] = []

    for pattern, by_lang in _SOURCE_HINTS:
        if pattern.search(blob) or pattern.search(question or ""):
            candidates.extend(by_lang.get(lang) or by_lang.get("en") or ())

    cap_map = _CAPABILITY_FOLLOWUPS.get(lang) or _CAPABILITY_FOLLOWUPS["en"]
    if capability and capability in cap_map:
        candidates.extend(cap_map[capability])

    track_map = _TRACK_FOLLOWUPS.get(lang) or _TRACK_FOLLOWUPS["en"]
    track_key = (track or "").strip()
    if track_key in track_map:
        candidates.extend(track_map[track_key])

    if answer and re.search(r"Data Gaps|数据缺口|資料缺口|Gap", answer, re.I):
        candidates.extend(_GAP_FOLLOWUPS.get(lang) or _GAP_FOLLOWUPS["en"])

    deduped: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        text = item.strip()
        if not text:
            continue
        key = _normalize(text)
        if key in seen or key == q_norm:
            continue
        if q_norm and (q_norm in key or key in q_norm):
            continue
        if a_norm and key in a_norm:
            continue
        seen.add(key)
        deduped.append(text)
        if len(deduped) >= limit:
            break

    if not deduped:
        deduped = list(_FALLBACK_FOLLOWUPS.get(lang) or _FALLBACK_FOLLOWUPS["en"])[:limit]

    return FollowUpSuggestions(
        questions=tuple(deduped),
        reason="grounded_sources_capability",
        lang=lang,
    )
