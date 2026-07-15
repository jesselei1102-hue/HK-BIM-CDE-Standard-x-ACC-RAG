"""复合意图分类：产品/行业信号 + 能力对象 + 同主题子查询模板。"""

from __future__ import annotations

import re
from dataclasses import dataclass


# 不依赖 ASCII 词边界，避免「符合CIC」匹配失败
_INDUSTRY_PATTERNS = (
    re.compile(r"(?<![A-Za-z])CIC(?![A-Za-z])", re.I),
    re.compile(r"CICBIMS", re.I),
    re.compile(r"(?<![A-Za-z])DEVB(?![A-Za-z])", re.I),
    re.compile(r"ISO\s*19650", re.I),
    re.compile(r"(?<![A-Za-z])WIP(?![A-Za-z])", re.I),
    re.compile(r"(?<![A-Za-z])PIR(?![A-Za-z])", re.I),
    re.compile(r"(?<![A-Za-z])OIR(?![A-Za-z])", re.I),
    re.compile(r"(?<![A-Za-z])AIR(?![A-Za-z])", re.I),
    re.compile(r"(?<![A-Za-z])EIR(?![A-Za-z])", re.I),
    re.compile(r"Gateway", re.I),
    re.compile(r"Harmonisation|Harmonization", re.I),
    re.compile(r"工务"),
    re.compile(r"信息容器"),
    re.compile(r"命名标准"),
    re.compile(r"Common Data Environment|(?<![A-Za-z])CDE(?![A-Za-z])", re.I),
    re.compile(r"信息要求"),
    re.compile(r"LandsD", re.I),
    re.compile(r"(?<![A-Za-z])BD(?![A-Za-z])", re.I),
    re.compile(r"ADM-?\s*19|ADV-?\s*34", re.I),
    re.compile(r"屋宇署|地政总署|地政總署"),
    re.compile(r"法定提交|法定图则|法定圖則|GBP"),
    re.compile(r"BIM\s*(and|&)?\s*GIS|BIM-GIS", re.I),
    re.compile(r"进行中"),
    re.compile(r"发布区|共享区|归档"),
    re.compile(
        r"港标|港標|"
        r"香港标准|香港標準|"
        r"香港\s*BIM|香港.*BIM\s*standard|香港.*BIM\s*标准|香港.*BIM\s*標準|"
        r"HK\s*BIM|HK\s*CDE|HK\s*standard|"
        r"Hong\s*Kong\s*(BIM\s*)?standard|"
        r"CIC\s*BIM|"
        r"BIM\s*standard|BIM\s*标准|BIM\s*標準",
        re.I,
    ),
)

_PRODUCT_PATTERNS = (
    re.compile(r"(?<![A-Za-z])ACC(?![A-Za-z])", re.I),
    re.compile(r"(?<![A-Za-z])Docs(?![A-Za-z])", re.I),
    re.compile(r"Autodesk", re.I),
    re.compile(r"Account\s*Admin", re.I),
    re.compile(r"创建项目|建项目|新建项目"),
    re.compile(r"创建文件夹|建文件夹|文件夹结构|目录结构"),
    re.compile(r"权限|權限|成员|分享|共享"),
    re.compile(r"审批|工作流|审阅"),
    re.compile(r"Review|Approval\s*Workflow|workflow", re.I),
    re.compile(r"怎么做|如何做|怎样做|如何创建|怎么创建|怎样创建"),
    re.compile(r"命名标准"),  # 产品侧也可能问 Docs 命名标准
    re.compile(r"Model\s*Browser|模型浏览器|模型瀏覽器", re.I),
    re.compile(r"模型属性|模型屬性|属性过滤|屬性過濾"),
    re.compile(
        r"(查看|过滤|過濾).{0,12}(模型|属性|屬性|BIM)|"
        r"(filter|view).{0,24}(propert|model\s*browser|RVT|IFC)",
        re.I,
    ),
)

# 实施手册 / 推荐配置信号（单轨 playbook，或强化 hybrid 走手册）
_PLAYBOOK_PATTERNS = (
    re.compile(r"playbook", re.I),
    re.compile(r"实施手册|實施手冊"),
    re.compile(r"推荐配置|推薦配置|推荐默认|推薦默認"),
    re.compile(r"怎么配|怎樣配|如何配置|怎么配置|怎樣配置"),
    re.compile(r"对齐表|對齊表"),
    re.compile(r"落地|落实|落實"),
    re.compile(r"项目样板|項目樣板|项目模板|項目模板|project\s*template", re.I),
)


@dataclass(frozen=True)
class CapabilityTemplate:
    key: str
    patterns: tuple[re.Pattern[str], ...]
    industry_query: str
    product_query: str
    playbook_query: str


CAPABILITY_TEMPLATES: tuple[CapabilityTemplate, ...] = (
    CapabilityTemplate(
        key="project_template",
        patterns=(
            re.compile(
                r"项目样板|項目樣板|项目模板|項目模板|"
                r"project\s*template|GC\s*模板|总包模板|總包模板|"
                r"Buildings\s*模板|ACC\s*HK\s*GC",
                re.I,
            ),
        ),
        industry_query=(
            "CIC BIM Standard DEVB Harmonisation project template "
            "CDE folder IRAM BD LandsD delivery"
        ),
        product_query=(
            "Configure Project Templates Autodesk Docs Files Reviews "
            "Issues Design Collaboration"
        ),
        playbook_query=(
            "ACC HK GC Buildings project template folder structure "
            "permissions naming workflows forms playbook"
        ),
    ),
    CapabilityTemplate(
        key="model_viewer",
        patterns=(
            re.compile(
                r"Model\s*Browser|模型浏览器|模型瀏覽器|"
                r"模型属性|模型屬性|属性过滤|屬性過濾|"
                r"(查看|过滤|過濾).{0,12}(BIM\s*)?(模型|属性|屬性)|"
                r"(filter|view).{0,24}(BIM\s*)?(model\s*)?(propert|browser)|"
                r"(RVT|IFC).{0,16}(propert|filter|view)|"
                r"Viewer\s*Settings",
                re.I,
            ),
        ),
        industry_query=(
            "CIC BIM CDE federated model display filter properties "
            "Annex audit information container model review"
        ),
        product_query=(
            "Model Browser filter RVT IFC properties "
            "Viewer Settings Autodesk Docs"
        ),
        playbook_query=(
            "Design Collaboration Model Coordination Model Browser "
            "ACC HK BIM playbook"
        ),
    ),
    CapabilityTemplate(
        key="permissions",
        patterns=(
            re.compile(
                r"文件夹权限|資料夾權限|文件夹權限|"
                r"设置权限|設置權限|权限设置|權限設置|"
                r"folder\s*permissions?|permission\s*levels?|"
                r"(?<![A-Za-z])permissions?(?![A-Za-z])|"
                r"权限|權限",
                re.I,
            ),
        ),
        industry_query=(
            "CIC CDE access control role based folder permissions "
            "information security container permission"
        ),
        product_query=(
            "Manage Folder Permissions permission levels "
            "Autodesk Docs Files tool"
        ),
        playbook_query=(
            "ACC folder permissions roles companies "
            "recommended default HK BIM playbook"
        ),
    ),
    CapabilityTemplate(
        key="naming",
        patterns=(
            re.compile(
                r"命名标准|命名標準|命名规范|命名規範|"
                r"Information\s*Container\s*(ID|naming)|"
                r"naming\s*standard|文件名|"
                r"命名",
                re.I,
            ),
        ),
        industry_query=(
            "DEVB BIM model naming Information Container ID federation naming"
        ),
        product_query="How to create naming standards in Autodesk Docs",
        playbook_query=(
            "ACC naming standard CICBIMS DEVB Information Container ID "
            "recommended fields playbook"
        ),
    ),
    CapabilityTemplate(
        key="workflow",
        patterns=(
            re.compile(
                r"审批|工作流|审阅|approval|"
                r"Authorisation\s*Gateway|Authorization\s*Gateway|"
                r"授权网关|授權網關|"
                r"(?<![A-Za-z])workflow(?![A-Za-z])|"
                r"(?<![A-Za-z])gateway(?![A-Za-z])",
                re.I,
            ),
        ),
        industry_query=(
            "ISO 19650 CIC CDE authorisation gateway status code "
            "review approve WIP Gateway workflow"
        ),
        product_query=(
            "How to create review approval workflows in Autodesk Docs"
        ),
        playbook_query=(
            "ACC approval workflow information gateway move folder status "
            "attribute gap recommended playbook"
        ),
    ),
    CapabilityTemplate(
        key="project_create",
        patterns=(
            re.compile(
                r"创建项目|建项目|新建项目|创建.{0,6}项目|"
                r"create\s+(an?\s+)?(ACC\s+)?project",
                re.I,
            ),
        ),
        industry_query=(
            "CIC BIM Standard project information requirements CDE principles "
            "OIR PIR project setup"
        ),
        product_query="How to create and manage projects in Autodesk Docs ACC",
        playbook_query=(
            "ACC account project setup roles companies recommended configuration "
            "HK BIM playbook"
        ),
    ),
    CapabilityTemplate(
        key="folder",
        patterns=(
            re.compile(
                r"文件夹结构|文件夾結構|目录结构|目錄結構|"
                r"folder\s*structure|project\s*folder|"
                r"创建文件夹|建文件夹|创建文件夾|"
                r"文件夹|文件夾|四容器|cde\s*容器",
                re.I,
            ),
        ),
        industry_query=(
            "CICBIMS DEVB CDE project folder structure resource folder requirements"
        ),
        product_query=(
            "Organize files with folders create subfolders "
            "Autodesk Docs Files tool"
        ),
        playbook_query=(
            "01_WIP 02_Shared 03_Published 04_Archive folder tree "
            "WIP container configuration ACC HK BIM playbook"
        ),
    ),
)


# 多能力同时命中时的优先级（越靠前越优先）
_CAPABILITY_PRIORITY: tuple[str, ...] = (
    "project_template",
    "model_viewer",
    "permissions",
    "naming",
    "workflow",
    "project_create",
    "folder",
)


@dataclass(frozen=True)
class IntentDecision:
    track: str  # docs | hk_cde | playbook | hybrid
    capability: str | None
    product_query: str | None
    industry_query: str | None
    playbook_query: str | None
    has_product_signal: bool
    has_industry_signal: bool
    has_playbook_signal: bool
    reason: str


def has_industry_signal(query: str) -> bool:
    text = query.strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in _INDUSTRY_PATTERNS)


def has_product_signal(query: str) -> bool:
    text = query.strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in _PRODUCT_PATTERNS)


def has_playbook_signal(query: str) -> bool:
    text = query.strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in _PLAYBOOK_PATTERNS)


def detect_capability(query: str) -> CapabilityTemplate | None:
    """按优先级选择唯一 capability；避免第一个正则命中抢答。"""
    matched = [
        template
        for template in CAPABILITY_TEMPLATES
        if any(pattern.search(query) for pattern in template.patterns)
    ]
    if not matched:
        return None
    by_key = {template.key: template for template in matched}
    for key in _CAPABILITY_PRIORITY:
        if key in by_key:
            return by_key[key]
    return matched[0]


def capability_template_by_key(key: str | None) -> CapabilityTemplate | None:
    if not key:
        return None
    for template in CAPABILITY_TEMPLATES:
        if template.key == key:
            return template
    return None


_VIEWER_QUERY_RE = re.compile(
    r"Model\s*Browser|模型浏览器|模型瀏覽器|模型属性|模型屬性|"
    r"(查看|过滤|過濾).{0,12}(属性|屬性|模型)|"
    r"(filter|view).{0,24}(propert|RVT|IFC|browser)",
    re.I,
)


def _fallback_queries(query: str) -> tuple[str, str, str]:
    """未识别能力对象时：原问分别侧重标准侧 / 产品侧 / 实施手册。"""
    industry_query = (
        f"{query} CIC DEVB ISO 19650 CDE information requirements"
    )
    if _VIEWER_QUERY_RE.search(query):
        product_query = (
            "Model Browser filter RVT IFC properties "
            "Viewer Settings Autodesk Docs"
        )
    else:
        product_query = f"{query} Autodesk Docs ACC how to"
    playbook_query = (
        f"{query} ACC HK BIM playbook recommended configuration alignment gap"
    )
    return product_query, industry_query, playbook_query


# hybrid 检索时按 capability 提升 playbook 章节召回（URL 前缀匹配）
CAPABILITY_PLAYBOOK_URL_PREFIX: dict[str, str] = {
    "folder": "playbook://acc_hk_bim/02_folder_cde",
    "naming": "playbook://acc_hk_bim/03_naming",
    "workflow": "playbook://acc_hk_bim/05_workflow",
    "project_create": "playbook://acc_hk_bim/01_project_setup",
    "project_template": "playbook://acc_hk_bim/08_project_template",
    "model_viewer": "playbook://acc_hk_bim/06_design_collab",
    "permissions": "playbook://acc_hk_bim/04_permissions",
}

# 明确文件夹操作措辞；不含裸 WIP/Shared 等术语（那些属行业概念）
_FOLDER_QUESTION_RE = re.compile(
    r"文件夹|文件夾|目录结构|目錄結構|folder\s*structure|"
    r"project\s*folder|四容器|cde\s*容器|"
    r"01_WIP|02_Shared|03_Published|04_Archive",
    re.I,
)


def is_folder_question(question: str, capability: str | None = None) -> bool:
    """仅在 folder capability 或明确文件夹结构措辞时为真。

    裸「WIP 是什么」不应触发文件夹硬钉选/结构化拼装。
    """
    if capability == "folder":
        return True
    if capability is not None:
        # 已识别为其他能力时，不要因夹杂 folder 词误开文件夹管线
        return False
    return bool(_FOLDER_QUESTION_RE.search(question or ""))


def classify_intent(query: str) -> IntentDecision:
    text = query.strip()
    product = has_product_signal(text)
    industry = has_industry_signal(text)
    playbook = has_playbook_signal(text)
    capability = detect_capability(text)

    if product and industry:
        if capability:
            return IntentDecision(
                track="hybrid",
                capability=capability.key,
                product_query=capability.product_query,
                industry_query=capability.industry_query,
                playbook_query=capability.playbook_query,
                has_product_signal=True,
                has_industry_signal=True,
                has_playbook_signal=playbook,
                reason=f"hybrid_capability_{capability.key}",
            )
        product_query, industry_query, playbook_query = _fallback_queries(text)
        return IntentDecision(
            track="hybrid",
            capability=None,
            product_query=product_query,
            industry_query=industry_query,
            playbook_query=playbook_query,
            has_product_signal=True,
            has_industry_signal=True,
            has_playbook_signal=playbook,
            reason="hybrid_fallback",
        )

    # 实施手册信号优先于纯标准轨（避免「怎么配置」被当成只查 CIC 条文）
    if playbook and not product:
        return IntentDecision(
            track="playbook",
            capability=capability.key if capability else None,
            product_query=None,
            industry_query=None,
            playbook_query=(
                capability.playbook_query if capability else text
            ),
            has_product_signal=False,
            has_industry_signal=industry,
            has_playbook_signal=True,
            reason="playbook_signal",
        )

    if playbook and product and not industry:
        # 产品 + 实施措辞但无港标词：仍走 playbook 单轨（手册已含产品路径）
        return IntentDecision(
            track="playbook",
            capability=capability.key if capability else None,
            product_query=(
                capability.product_query if capability else text
            ),
            industry_query=None,
            playbook_query=(
                capability.playbook_query if capability else text
            ),
            has_product_signal=True,
            has_industry_signal=False,
            has_playbook_signal=True,
            reason="playbook_product",
        )

    if industry:
        return IntentDecision(
            track="hk_cde",
            capability=capability.key if capability else None,
            product_query=None,
            industry_query=(
                capability.industry_query if capability else text
            ),
            playbook_query=None,
            has_product_signal=False,
            has_industry_signal=True,
            has_playbook_signal=False,
            reason="industry_only",
        )

    return IntentDecision(
        track="docs",
        capability=capability.key if capability else None,
        product_query=(
            capability.product_query if capability else text
        ),
        industry_query=None,
        playbook_query=None,
        has_product_signal=product,
        has_industry_signal=False,
        has_playbook_signal=False,
        reason="docs_default" if not product else "product_only",
    )
