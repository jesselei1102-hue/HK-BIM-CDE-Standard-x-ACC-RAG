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
    re.compile(r"Gateway|网关|網關", re.I),
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
    re.compile(r"statutory\s+plan|statutory\s+user\s+guide|Building\s+Department", re.I),
    re.compile(r"BIM\s*(and|&)?\s*GIS|BIM-GIS", re.I),
    re.compile(r"进行中"),
    re.compile(r"发布区|共享区|归档"),
    re.compile(r"PAS\s*128|underground\s+utilit|地下管线|地下管線", re.I),
    re.compile(r"\bMEP\b|机电|機械電氣", re.I),
    re.compile(r"BIM\s*object|BIM\s*对象|BIM\s*物件", re.I),
    re.compile(r"BIM\s*Dictionary|术语表|詞典|词典", re.I),
    re.compile(r"AM/?FM|case\s*sharing|Zero\s*Carbon\s*Park|(?<![A-Za-z])ZCP(?![A-Za-z])", re.I),
    re.compile(
        r"BIM\s*Manager|BIM\s*经理|BIM\s*經理|"
        r"Information\s*Manager|信息管理(?:者|员|員|职能|職能)?|"
        r"Task\s*Team\s*Manager|Task\s*Information\s*Manager|"
        r"Document\s*Controller|"
        r"Project\s*Information\s*Functions?|"
        r"Assignment\s*Matrix|"
        r"信息管理职能|信息管理職能|职责矩阵|職責矩陣",
        re.I,
    ),
    re.compile(
        r"(?:Revit|ArchiCAD|Archi\s*CAD|Civil\s*3D|Tekla).{0,40}"
        r"(?:statutory|user\s*guide|submission)|"
        r"(?:statutory|user\s*guide|submission).{0,40}"
        r"(?:Revit|ArchiCAD|Archi\s*CAD|Civil\s*3D|Tekla)",
        re.I,
    ),
    re.compile(
        r"港标|港標|"
        r"香港标准|香港標準|"
        r"香港\s*BIM|香港.*BIM\s*standard|香港.*BIM\s*标准|香港.*BIM\s*標準|"
        r"HK\s*BIM|HK\s*CDE|HK\s*standard|"
        r"HK[- ]?aligned|aligned\s+with\s+HK|"
        r"Hong\s*Kong[- ]?aligned|"
        r"Hong\s*Kong\s*(BIM\s*)?standard|"
        r"CIC\s*BIM|"
        r"BIM\s*standard|BIM\s*标准|BIM\s*標準",
        re.I,
    ),
)

_OUT_OF_DOMAIN_PATTERNS = (
    re.compile(r"\bweather\b|天气|天氣|tomorrow\s+for\s+BIM", re.I),
    re.compile(r"\bpoem\b|写一首|寫一首|作诗|作詩", re.I),
    re.compile(r"tax\s+rate\s+for\s+2099|quantum\s+twin|ZZ-99", re.I),
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
    re.compile(r"HK\s*CDE\s*Spec|项目说明书|項目說明書|项目规格|項目規格", re.I),
    re.compile(r"ACC\s*HK\s*GC|GC\s*Buildings|GC\s*Civil", re.I),
    # Actual-project Spec operational cues (Buildings / Civil trunks)
    re.compile(
        r"九段命名|SuitabilityStatus|WF-[ABCD]\b|"
        r"PROJECT_BOUNDARY|MODEL_FILE_LIST|EMSD_Code|AssetClass|"
        r"By\s*Section|区段码|區段碼|MIDP\b",
        re.I,
    ),
    re.compile(
        r"(?:Buildings|Civil|楼宇|樓宇|土木).{0,20}"
        r"(?:文件夹|文件夾|目录|目錄|命名|权限|權限|审批|審批|表单|表單|移交)",
        re.I,
    ),
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
                r"Buildings\s*模板|Civil\s*模板|ACC\s*HK\s*GC",
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
            "ACC HK GC Buildings Civil project template specification "
            "folder permissions naming workflows forms EMSD MIDP"
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
                r"(?<![A-Za-z])gateway(?![A-Za-z])|"
                r"WF-[ABCD]\b|强制检查表|強制檢查表|"
                r"Submission\s*Checklist|Completeness\s*Check",
                re.I,
            ),
        ),
        industry_query=(
            "ISO 19650 CIC CDE authorisation gateway status code "
            "review approve WIP Gateway workflow"
        ),
        product_query=(
            "How to create and edit approval workflows Action Upon Completion "
            "copy approved files update attributes Autodesk Docs Reviews"
        ),
        playbook_query=(
            "ACC approval workflow Action Upon Completion Copy approved files "
            "Update attributes information gateway WIP Shared Published playbook"
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
        key="roles",
        patterns=(
            re.compile(
                r"BIM\s*Manager|BIM\s*经理|BIM\s*經理|"
                r"Information\s*Manager|"
                r"Task\s*Team\s*Manager|Task\s*Information\s*Manager|"
                r"Document\s*Controller|"
                r"Project\s*Information\s*Functions?|"
                r"Assignment\s*Matrix|"
                r"(?:角色|职责|職責|责任|責任|responsibilit).{0,24}"
                r"(?:BIM\s*Manager|Information\s*Manager|ACC)|"
                r"(?:BIM\s*Manager|Information\s*Manager).{0,40}"
                r"(?:角色|职责|職責|责任|責任|responsibilit|功能|ACC|Project\s*Admin)",
                re.I,
            ),
        ),
        industry_query=(
            "BIM Manager Information Manager Task Team Manager "
            "project information functions assignment matrix "
            "CICBIMS information management roles responsibilities"
        ),
        product_query=(
            "ACC Project Admin members companies roles permissions "
            "account administration Autodesk Docs"
        ),
        playbook_query=(
            "BIM Manager Project Admin Information Manager "
            "role mapping ACC HK BIM playbook companies members"
        ),
    ),
    CapabilityTemplate(
        key="folder",
        patterns=(
            re.compile(
                r"文件夹结构|文件夾結構|目录结构|目錄結構|"
                r"folder\s*(structure|tree|hierarch(y|ies)?)|"
                r"folder\s*example|"
                r"project\s*folder|"
                r"discipline\s+folder|"
                r"sub\s*-?\s*folder|"
                r"创建文件夹|建文件夹|创建文件夾|"
                r"文件夹|文件夾|四容器|cde\s*容器|"
                r"four\s*container|4\s*container|"
                r"目录怎么建|目錄怎麼建|By\s*Section|"
                r"LandsD\s*(?:目录|目錄|Submission)|"
                r"(?<![A-Za-z])WIP(?![A-Za-z]).{0,48}"
                r"(folder|tree|discipline|container|subfolder|ARC|STR|MEP|CIV)|"
                r"(folder|tree|discipline|container|subfolder).{0,48}"
                r"(?<![A-Za-z])WIP(?![A-Za-z])|"
                r"01_WIP|02_Shared|02_SHARED|03_Published|03_PUBLISHED|04_Archive|04_ARCHIVE",
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
    "roles",
    "folder",
)


@dataclass(frozen=True)
class IntentDecision:
    track: str  # docs | hk_cde | playbook | hybrid | out_of_domain
    capability: str | None
    product_query: str | None
    industry_query: str | None
    playbook_query: str | None
    has_product_signal: bool
    has_industry_signal: bool
    has_playbook_signal: bool
    reason: str
    routing_source: str = "legacy"  # legacy | semantic | semantic_fallback | shadow
    semantic_hint: str | None = None


def has_industry_signal(query: str) -> bool:
    text = query.strip()
    if not text:
        return False
    # Spec branding contains "CDE" / "HK CDE"; strip it so the product name
    # does not steal the industry (standards) track from Playbook Spec queries.
    text = re.sub(r"HK\s*CDE\s*Spec", " ", text, flags=re.I)
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


def has_out_of_domain_signal(query: str) -> bool:
    text = query.strip()
    if not text:
        return False
    return any(pattern.search(text) for pattern in _OUT_OF_DOMAIN_PATTERNS)


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

# 概括性「港标/CIC/Harmonisation 是什么」→ 改写到实章节，避免捞到前言/致谢
_CICBIMS_OVERVIEW_RE = re.compile(
    r"(CICBIMS|CIC\s*BIM\s*Standards?(?:\s*General)?|"
    r"CIC\s*(?:BIM\s*)?(?:CDE\s*)?[Ss]tandard|"
    r"港标|香港\s*BIM\s*标准|香港\s*BIM\s*標準)",
    re.I,
)
_CIC_OVERVIEW_ASK_RE = re.compile(
    r"(what|know|tell|more|overview|comprehensive|headline|contents?|"
    r"cover|about|knowledge|介绍|什么|哪些|概览|涵盖|讲什么)",
    re.I,
)
_DEVB_HARMONISATION_OVERVIEW_RE = re.compile(
    r"harmonisation|harmonization|"
    r"DEVB\s*BIM|"
    r"BIM\s*协调|BIM\s*調和",
    re.I,
)
_SPECIFIC_SECTION_RE = re.compile(
    r"(?::\s*\S)|"  # "DOC: Section title"
    r"(?:\b\d+(?:\.\d+)+\b)|"  # numbered section 2.3.1
    r"(?:\bAppendix\s+[A-Z0-9]+\b)|"
    r"(?:\bLOIN\b)|"
    r"(?:\bLOD(?:-?I)?\b)|"
    r"(?:\bnaming\b)|"
    r"(?:命名)|"
    r"(?:\bLandsD\b)|"
    r"(?:\bTHE WAY FORWARD\b)|"
    r"(?:\bABBREVIATION\b)|"
    r"(?:\bINFORMATION REQUIREMENTS\b)|"
    r"(?:\bDISTRIBUTION\b)|"
    r"(?:\bBIM OBJECT FILES\b)|"
    r"(?:\bSubscription/?Perpetual\b)|"
    r"(?:\bUse of the Standards\b)|"
    r"(?:requirements?\s+for\s+.+?\s+in\s+)",
    re.I,
)


def rewrite_industry_overview_query(query: str) -> str | None:
    """把空泛的港标总览问句改成可命中 CICBIMS / DEVB 正文的检索句。

    Do **not** rewrite when the user already names a concrete section; otherwise
    overview pins (e.g. EXECUTIVE SUMMARY) steal SectionRecall@1.
    """
    text = (query or "").strip()
    if not text:
        return None
    if _SPECIFIC_SECTION_RE.search(text):
        return None
    if _DEVB_HARMONISATION_OVERVIEW_RE.search(text) and (
        _CIC_OVERVIEW_ASK_RE.search(text)
        or len(text) < 60
        or re.search(r"headline|contents?|overview|comprehensive|guide\b", text, re.I)
    ):
        return (
            "DEVB BIM Harmonisation Guidelines v3 executive summary "
            "foreword table of contents overview Works Departments"
        )
    if _CICBIMS_OVERVIEW_RE.search(text) and (
        _CIC_OVERVIEW_ASK_RE.search(text)
        or len(text) < 80
        or re.search(r"headline|contents?|overview|comprehensive", text, re.I)
    ):
        # 避免塞进 ISO 19650 / CDE 选型词，防止漂到 DEVB 附录或 Beginner Guide
        return (
            "CIC BIM Standards General CICBIMS 2024 introduction purpose "
            "Appointing Party deliverables project delivery cycle overview"
        )
    return None


def _fallback_queries(query: str) -> tuple[str, str, str]:
    """未识别能力对象时：原问分别侧重标准侧 / 产品侧 / 实施手册。"""
    rewritten = rewrite_industry_overview_query(query)
    industry_query = rewritten or (
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


# hybrid 检索时按 capability + domain 提升 playbook 章节召回（URL 前缀匹配）
_PLAYBOOK_CHAPTER_BY_CAPABILITY: dict[str, dict[str, str]] = {
    "folder": {
        "buildings": "11_buildings_folders_permissions",
        "civil": "21_civil_folders_permissions",
    },
    "permissions": {
        "buildings": "11_buildings_folders_permissions",
        "civil": "21_civil_folders_permissions",
    },
    "naming": {
        "buildings": "13_buildings_naming_fields",
        "civil": "23_civil_naming_fields",
    },
    "workflow": {
        "buildings": "12_buildings_issues_workflows",
        "civil": "22_civil_issues_workflows",
    },
    "project_create": {
        "buildings": "10_buildings_overview_roles",
        "civil": "20_civil_overview_roles",
    },
    "project_template": {
        "buildings": "00_hk_cde_spec_index",
        "civil": "00_hk_cde_spec_index",
    },
    "model_viewer": {
        "buildings": "15_buildings_assets_midp_acceptance",
        "civil": "25_civil_assets_midp_acceptance",
    },
    "roles": {
        "buildings": "10_buildings_overview_roles",
        "civil": "20_civil_overview_roles",
    },
}

# 兼容旧调用方：默认 Buildings 前缀
CAPABILITY_PLAYBOOK_URL_PREFIX: dict[str, str] = {
    key: f"playbook://acc_hk_bim/{chapters['buildings']}"
    for key, chapters in _PLAYBOOK_CHAPTER_BY_CAPABILITY.items()
}

_CIVIL_DOMAIN_RE = re.compile(
    r"\bCivil\b|土木|基建|基础设施|基礎設施|LandsD|区段|區段|"
    r"Chainage|ContractPackage|By\s*Section|SEC-[A-C]|道路排水|地工",
    re.I,
)
_BUILDINGS_DOMAIN_RE = re.compile(
    # Prefer plural "Buildings" / 楼宇; avoid bare "Building" (naming field).
    r"\bBuildings\b|楼宇|樓宇|屋宇署|Fit-?out|住宅|办公|辦公|商业|商業|"
    r"(?<![A-Za-z])BD(?![A-Za-z])\s*(?:提交|Submission|法定)",
    re.I,
)


def detect_playbook_domain(question: str) -> str:
    """Return buildings | civil | mixed for Playbook chapter boost."""
    text = question or ""
    has_civil = bool(_CIVIL_DOMAIN_RE.search(text))
    has_buildings = bool(_BUILDINGS_DOMAIN_RE.search(text))
    if has_civil and not has_buildings:
        return "civil"
    if has_buildings and not has_civil:
        return "buildings"
    if has_civil and has_buildings:
        # Field-name collisions (Building=section) should not flip Civil → mixed.
        if re.search(r"Building\s*字段|Building\s*=|Building\s*等于|Building\s*等於", text, re.I):
            return "civil"
        return "mixed"
    return "buildings"


def playbook_url_prefix_for(
    capability: str | None,
    question: str = "",
) -> str | None:
    """Capability + domain aware Playbook URL prefix for retrieval boost."""
    if not capability:
        return None
    chapters = _PLAYBOOK_CHAPTER_BY_CAPABILITY.get(capability)
    if not chapters:
        return CAPABILITY_PLAYBOOK_URL_PREFIX.get(capability)
    domain = detect_playbook_domain(question)
    if domain == "civil":
        chapter = chapters.get("civil") or chapters.get("buildings")
    elif domain == "mixed":
        chapter = "00_hk_cde_spec_index"
    else:
        chapter = chapters.get("buildings") or chapters.get("civil")
    if not chapter:
        return None
    return f"playbook://acc_hk_bim/{chapter}"

# 保留最小确定性措辞，供 legacy 低置信度回退（非主路由路径）
_FOLDER_QUESTION_RE = re.compile(
    r"文件夹|文件夾|目录结构|目錄結構|"
    r"folder\s*(structure|tree|hierarch(y|ies)?)|"
    r"discipline\s+folder|sub\s*-?\s*folder|"
    r"project\s*folder|四容器|cde\s*容器|"
    r"01_WIP|02_Shared|03_Published|04_Archive",
    re.I,
)


def is_folder_question(question: str, capability: str | None = None) -> bool:
    """folder capability 为真；legacy 回退时保留四容器/树形措辞检测。"""
    if capability == "folder":
        return True
    if capability is not None:
        return False
    return bool(_FOLDER_QUESTION_RE.search(question or ""))


def _append_semantic_hint(question: str, hint: str | None) -> str:
    text = question.strip()
    hint = (hint or "").strip()
    if not hint or hint.casefold() in text.casefold():
        return text
    return f"{text} ({hint})"


def _retrieval_queries_from_question(
    question: str,
    *,
    capability: CapabilityTemplate | None,
    semantic_hint: str | None,
    industry_rewrite: str | None,
    track: str,
) -> tuple[str | None, str | None, str | None]:
    """原问句主导召回；仅在语义高置信时追加轻量 hint。"""
    base = question.strip()
    hinted = _append_semantic_hint(base, semantic_hint)

    if track == "out_of_domain":
        return None, None, None

    if track == "hybrid":
        product_q = hinted
        industry_q = industry_rewrite or hinted
        playbook_q = hinted
        if capability:
            # 低分补救模板仅作 hint 后缀，不替换原问句
            for part in (
                capability.product_query,
                capability.industry_query,
                capability.playbook_query,
            ):
                if part and part.casefold() not in hinted.casefold():
                    pass  # templates reserved for conditional pin / low-score retry
        return product_q, industry_q, playbook_q

    if track == "playbook":
        return None, None, hinted

    if track == "hk_cde":
        return None, industry_rewrite or hinted, None

    return hinted, None, None


def _build_intent_decision(
    text: str,
    *,
    product: bool,
    industry: bool,
    playbook: bool,
    capability: CapabilityTemplate | None,
    out_of_domain: bool,
    routing_source: str = "legacy",
    semantic_hint: str | None = None,
    reason_prefix: str = "",
    use_templates: bool = True,
) -> IntentDecision:
    """共享 track 决策；semantic 路径用原问句召回，legacy 保留模板 sub-query。"""
    prefix = f"{reason_prefix}_" if reason_prefix else ""

    def _queries_for(track: str) -> tuple[str | None, str | None, str | None]:
        industry_rewrite = None
        if track == "hk_cde" and not capability:
            industry_rewrite = rewrite_industry_overview_query(text)
        if use_templates and capability:
            if track == "hybrid":
                return (
                    capability.product_query,
                    capability.industry_query,
                    capability.playbook_query,
                )
            if track == "playbook":
                return None, None, capability.playbook_query
            if track == "hk_cde":
                return None, capability.industry_query, None
            if track == "docs":
                return capability.product_query, None, None
        return _retrieval_queries_from_question(
            text,
            capability=capability,
            semantic_hint=semantic_hint,
            industry_rewrite=industry_rewrite,
            track=track,
        )

    cap_key = capability.key if capability else None

    if out_of_domain and not product:
        return IntentDecision(
            track="out_of_domain",
            capability=None,
            product_query=None,
            industry_query=None,
            playbook_query=None,
            has_product_signal=False,
            has_industry_signal=industry,
            has_playbook_signal=False,
            reason=f"{prefix}out_of_domain",
            routing_source=routing_source,
            semantic_hint=semantic_hint,
        )

    if product and industry:
        pq, iq, pbq = _queries_for("hybrid")
        if not use_templates and not capability:
            pq, iq, pbq = _fallback_queries(text)
        reason = f"{prefix}hybrid_capability_{cap_key}" if cap_key else f"{prefix}hybrid_fallback"
        return IntentDecision(
            track="hybrid",
            capability=cap_key,
            product_query=pq,
            industry_query=iq,
            playbook_query=pbq,
            has_product_signal=True,
            has_industry_signal=True,
            has_playbook_signal=playbook,
            reason=reason,
            routing_source=routing_source,
            semantic_hint=semantic_hint,
        )

    if playbook and not product:
        _, _, pbq = _queries_for("playbook")
        return IntentDecision(
            track="playbook",
            capability=cap_key,
            product_query=None,
            industry_query=None,
            playbook_query=pbq or text,
            has_product_signal=False,
            has_industry_signal=industry,
            has_playbook_signal=True,
            reason=f"{prefix}playbook_signal",
            routing_source=routing_source,
            semantic_hint=semantic_hint,
        )

    if playbook and product and not industry:
        pq, _, pbq = _queries_for("playbook")
        return IntentDecision(
            track="playbook",
            capability=cap_key,
            product_query=pq or text,
            industry_query=None,
            playbook_query=pbq or text,
            has_product_signal=True,
            has_industry_signal=False,
            has_playbook_signal=True,
            reason=f"{prefix}playbook_product",
            routing_source=routing_source,
            semantic_hint=semantic_hint,
        )

    if industry:
        _, iq, _ = _queries_for("hk_cde")
        rewritten = rewrite_industry_overview_query(text)
        return IntentDecision(
            track="hk_cde",
            capability=cap_key,
            product_query=None,
            industry_query=iq or (rewritten or text),
            playbook_query=None,
            has_product_signal=False,
            has_industry_signal=True,
            has_playbook_signal=False,
            reason=(
                f"{prefix}industry_overview_rewrite"
                if rewritten and not capability
                else f"{prefix}industry_only"
            ),
            routing_source=routing_source,
            semantic_hint=semantic_hint,
        )

    pq, _, _ = _queries_for("docs")
    return IntentDecision(
        track="docs",
        capability=cap_key,
        product_query=pq or text,
        industry_query=None,
        playbook_query=None,
        has_product_signal=product,
        has_industry_signal=False,
        has_playbook_signal=False,
        reason=f"{prefix}docs_default" if not product else f"{prefix}product_only",
        routing_source=routing_source,
        semantic_hint=semantic_hint,
    )


def classify_intent_legacy(query: str) -> IntentDecision:
    text = query.strip()
    return _build_intent_decision(
        text,
        product=has_product_signal(text),
        industry=has_industry_signal(text),
        playbook=has_playbook_signal(text),
        capability=detect_capability(text),
        out_of_domain=has_out_of_domain_signal(text),
        routing_source="legacy",
        use_templates=True,
    )


def _merge_semantic_decision(
    query: str,
    legacy: IntentDecision,
    semantic: "SemanticRouteResult",
    *,
    use_semantic: bool,
) -> IntentDecision:
    from rag.config import get_config
    from rag.orchestrator.semantic_router import SemanticRouteResult  # noqa: F401

    text = query.strip()
    cfg = get_config().semantic_router
    if not use_semantic or not semantic.index_available:
        source = "legacy" if not use_semantic else "semantic_fallback"
        reason = (
            legacy.reason
            if not use_semantic
            else f"fallback_{semantic.fallback_reason or 'index'}"
        )
        return IntentDecision(
            track=legacy.track,
            capability=legacy.capability,
            product_query=legacy.product_query,
            industry_query=legacy.industry_query,
            playbook_query=legacy.playbook_query,
            has_product_signal=legacy.has_product_signal,
            has_industry_signal=legacy.has_industry_signal,
            has_playbook_signal=legacy.has_playbook_signal,
            reason=reason,
            routing_source=source,
            semantic_hint=semantic.hint_query or None,
        )

    product = legacy.has_product_signal or semantic.product_score >= cfg.min_track_signal_sim
    industry = legacy.has_industry_signal or semantic.industry_score >= cfg.min_track_signal_sim
    playbook = legacy.has_playbook_signal or semantic.playbook_score >= cfg.min_track_signal_sim
    _ = (product, industry, playbook)  # track stays on legacy signals; reserved for future track semantic

    cap_template = detect_capability(text)
    if cap_template is None and legacy.capability is None:
        if (
            semantic.capability_confident
            and semantic.capability == "folder"
            and is_folder_question(text, None)
        ):
            cap_template = capability_template_by_key("folder")
    elif semantic.capability_confident and semantic.capability is None:
        cap_template = None
    elif semantic.capability_confident:
        sem_cap = capability_template_by_key(semantic.capability)
        if sem_cap is not None:
            if cap_template is None:
                if sem_cap.key == "folder" and not is_folder_question(text, None):
                    cap_template = None
                else:
                    cap_template = sem_cap
            else:
                cap_template = min(
                    (cap_template, sem_cap),
                    key=lambda item: _CAPABILITY_PRIORITY.index(item.key),
                )

    # 裸 WIP / 概览问句：null 簇足够强时不落 folder
    if (
        cap_template is not None
        and cap_template.key == "folder"
        and semantic.capability_null_score >= cfg.min_capability_null_sim
        and semantic.capability_null_score >= semantic.capability_score - 0.03
    ):
        cap_template = None

    hint = semantic.hint_query if semantic.capability_confident else None
    return _build_intent_decision(
        text,
        product=legacy.has_product_signal,
        industry=legacy.has_industry_signal,
        playbook=legacy.has_playbook_signal,
        capability=cap_template,
        out_of_domain=legacy.track == "out_of_domain",
        routing_source="semantic",
        semantic_hint=hint,
        reason_prefix="semantic",
        use_templates=False,
    )


def classify_intent(query: str, *, mode: str | None = None) -> IntentDecision:
    """语义优先路由；shadow 模式仅记录对比，行为仍走 legacy。"""
    from rag.config import get_config
    from rag.orchestrator.semantic_router import get_semantic_router

    legacy = classify_intent_legacy(query)
    router_mode = (mode or get_config().semantic_router.mode).lower()
    if router_mode == "off":
        return legacy

    semantic = get_semantic_router().route(query)
    if router_mode == "shadow":
        merged = _merge_semantic_decision(
            query, legacy, semantic, use_semantic=False
        )
        return IntentDecision(
            track=merged.track,
            capability=merged.capability,
            product_query=merged.product_query,
            industry_query=merged.industry_query,
            playbook_query=merged.playbook_query,
            has_product_signal=merged.has_product_signal,
            has_industry_signal=merged.has_industry_signal,
            has_playbook_signal=merged.has_playbook_signal,
            reason=legacy.reason,
            routing_source="shadow",
            semantic_hint=semantic.hint_query or None,
        )

    if router_mode == "on":
        use_semantic = semantic.index_available
        if use_semantic:
            return _merge_semantic_decision(
                query, legacy, semantic, use_semantic=True
            )
        return _merge_semantic_decision(
            query, legacy, semantic, use_semantic=False
        )

    return legacy
