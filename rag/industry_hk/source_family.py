"""HK source-family resolver: map queries to doc families and retrieval hints."""

from __future__ import annotations

import re
from dataclasses import dataclass

from rag.industry_hk.source_registry import SOURCE_REGISTRY, SourceSpec


@dataclass(frozen=True)
class FamilyMatch:
    doc_ids: tuple[str, ...]
    authority_types: tuple[str, ...]
    prefer_shadow: bool = False
    implementation_intent: bool = False
    software: str | None = None


_FAMILY_PATTERNS: tuple[tuple[re.Pattern[str], FamilyMatch], ...] = (
    (
        re.compile(
            r"\bMEP\b|mechanical,\s*electrical|plumbing|"
            r"duct|HVAC|机电",
            re.I,
        ),
        FamilyMatch(("cic_mep_2021",), ("standard",)),
    ),
    (
        re.compile(
            r"underground\s+utilit|PAS\s*128|地下管线|地下管線",
            re.I,
        ),
        FamilyMatch(("cic_uu_2021",), ("standard",)),
    ),
    (
        re.compile(
            r"BIM\s*object\s*guide|object\s*(categor|classif|propert|appearance|behaviour)|"
            r"BIM\s*对象|BIM\s*物件",
            re.I,
        ),
        FamilyMatch(("cic_object_guide_2021",), ("standard",)),
    ),
    (
        re.compile(
            r"statutory\s+plan|法定图则|法定圖則|GBP\b|origin\s+point",
            re.I,
        ),
        FamilyMatch(("cic_statutory_plans_2020",), ("statutory",)),
    ),
    (
        re.compile(r"BIM\s*Dictionary|术语表|詞典|词典", re.I),
        FamilyMatch(
            ("cic_dictionary_2024",),
            ("terminology",),
            prefer_shadow=True,
        ),
    ),
    (
        re.compile(
            r"AM/?FM|asset\s*management|facility\s*management|"
            r"case\s*sharing|运维案例|運維案例",
            re.I,
        ),
        FamilyMatch(
            ("cic_amfm_case_2021",),
            ("case_study",),
            prefer_shadow=True,
        ),
    ),
    (
        re.compile(
            r"Zero\s*Carbon\s*Park|(?<![A-Za-z])ZCP(?![A-Za-z])|"
            r"BIM\s*Implementation\s*Plan|BIM\s*IP\b|"
            r"BIM\s*Execution\s*Plan|(?<![A-Za-z])BEP(?![A-Za-z])",
            re.I,
        ),
        FamilyMatch(
            ("cic_zcp_bimip_v15",),
            ("case_study",),
            prefer_shadow=True,
            implementation_intent=True,
        ),
    ),
    (
        re.compile(r"ADM-?\s*19|curtain\s*wall|屋宇署", re.I),
        FamilyMatch(("bd_adm19", "bd_adv34"), ("statutory",)),
    ),
    (
        re.compile(r"ADV-?\s*34", re.I),
        FamilyMatch(("bd_adv34",), ("statutory",)),
    ),
    (
        re.compile(r"LandsD|地政|BIM-?GIS|BIM\s*&\s*GIS", re.I),
        FamilyMatch(("landsd_bim_gis",), ("statutory",)),
    ),
    (
        re.compile(r"ArchiCAD|Archi\s*CAD", re.I),
        FamilyMatch(
            ("cic_stat_archicad_2020",),
            ("software_guide",),
            prefer_shadow=True,
            software="archicad",
        ),
    ),
    (
        re.compile(r"Civil\s*3D", re.I),
        FamilyMatch(
            ("cic_stat_civil3d_2020",),
            ("software_guide",),
            prefer_shadow=True,
            software="civil3d",
        ),
    ),
    (
        re.compile(r"(?<![A-Za-z])Revit(?![A-Za-z])", re.I),
        FamilyMatch(
            ("cic_stat_revit_2020",),
            ("software_guide",),
            prefer_shadow=True,
            software="revit",
        ),
    ),
    (
        re.compile(r"(?<![A-Za-z])Tekla(?![A-Za-z])", re.I),
        FamilyMatch(
            ("cic_stat_tekla_2020",),
            ("software_guide",),
            prefer_shadow=True,
            software="tekla",
        ),
    ),
    (
        re.compile(
            r"(?<![A-Za-z])DEVB(?![A-Za-z])|harmonisation|harmonization",
            re.I,
        ),
        FamilyMatch(("devb_harmonisation_v3",), ("standard",)),
    ),
    (
        re.compile(
            r"(?<![A-Za-z])CICBIMS(?![A-Za-z])|"
            r"CIC\s*BIM\s*Standards?\s*General|"
            r"(?<![A-Za-z])WIP(?![A-Za-z])|(?<![A-Za-z])CDE(?![A-Za-z])|"
            r"Gateway|Shared\s+CDE|Published\s+information",
            re.I,
        ),
        FamilyMatch(("cicbims_2024", "cic_beginner_cde"), ("standard",)),
    ),
)

_IMPLEMENTATION_INTENT_RE = re.compile(
    r"project\s*(setup|config|configuration|template)|"
    r"怎么配置项目|如何配置项目|怎样配置项目|"
    r"项目配置|項目配置|"
    r"BIM\s*implementation|"
    r"responsibility\s*matrix|"
    r"(?<![A-Za-z])MIDP(?![A-Za-z])|(?<![A-Za-z])TIDP(?![A-Za-z])|"
    r"execution\s*plan|"
    r"CDE\s*(and\s+)?IT\s*infrastructure|"
    r"handover\s*procedure|"
    r"mobilisation|mobilization",
    re.I,
)

_SECTION_NUMBER_TITLE_RE = re.compile(
    r"^\s*\d+(?:\.\d+){0,4}\s+\S",
)

_PARAPHRASE_TITLE_RE = re.compile(
    r"^what\s+are\s+the\s+requirements\s+for\s+(.+?)\??\s*$",
    re.I,
)


def resolve_source_family(query: str) -> FamilyMatch | None:
    text = query or ""
    for pattern, match in _FAMILY_PATTERNS:
        if pattern.search(text):
            if _IMPLEMENTATION_INTENT_RE.search(text) and match.doc_ids[0] != "cic_zcp_bimip_v15":
                # Prefer ZCP as implementation reference when config intent is clear.
                zcp = FamilyMatch(
                    ("cic_zcp_bimip_v15", *match.doc_ids),
                    ("case_study", *match.authority_types),
                    prefer_shadow=True,
                    implementation_intent=True,
                )
                return zcp
            return match
    if _IMPLEMENTATION_INTENT_RE.search(text):
        return FamilyMatch(
            ("cic_zcp_bimip_v15",),
            ("case_study",),
            prefer_shadow=True,
            implementation_intent=True,
        )
    return None


def is_section_number_title(query: str) -> bool:
    return bool(_SECTION_NUMBER_TITLE_RE.match((query or "").strip()))


_DOC_SECTION_PREFIX_RE = re.compile(
    r"^[^:\n]{3,90}:\s+(.+)$",
)
_IN_DOC_SUFFIX_RE = re.compile(
    r"\s+in\s+(?:DEVB|CIC|BD|LandsD|Zero Carbon|AM/?FM).+$",
    re.I,
)


def extract_paraphrase_title(query: str) -> str | None:
    match = _PARAPHRASE_TITLE_RE.match((query or "").strip())
    if not match:
        return None
    title = match.group(1).strip()
    title = _IN_DOC_SUFFIX_RE.sub("", title).strip(" ?")
    return title or None


def extract_explicit_section_title(query: str) -> str | None:
    """Pull the section title from 'DOC: Section' or requirements paraphrases."""
    text = (query or "").strip()
    if not text:
        return None
    paraphrased = extract_paraphrase_title(text)
    if paraphrased:
        return paraphrased
    match = _DOC_SECTION_PREFIX_RE.match(text)
    if match:
        return match.group(1).strip()
    return None


def normalize_title(text: str) -> str:
    cleaned = (text or "").strip().lower()
    cleaned = cleaned.replace("&", " and ")
    cleaned = cleaned.replace("/", " ")
    cleaned = cleaned.replace("—", " ").replace("–", " ").replace("-", " ")
    return re.sub(r"\s+", " ", cleaned).strip()


def _title_core(title: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)*\.?\s*", "", normalize_title(title)).strip()


def exact_title_bonus(query: str, chunk_title: str) -> float:
    """Large bonus when query is the section title or a requirements paraphrase.

    Prefer longer / more complete titles over short fragment pages (e.g.
    ``Subscription/Perpetual`` over bare ``Perpetual``).
    """
    q = normalize_title(query)
    title = normalize_title(chunk_title)
    if not q or not title:
        return 0.0

    explicit = extract_explicit_section_title(query)
    explicit_n = normalize_title(explicit) if explicit else ""
    title_core = _title_core(chunk_title)
    explicit_core = _title_core(explicit) if explicit else ""

    if explicit_n and (title == explicit_n or title_core == explicit_core):
        return 4.0 + min(len(title_core), 40) / 100.0
    if explicit_core and title_core and title_core in explicit_core:
        # Fragment title contained in the requested section — smaller bonus.
        coverage = len(title_core) / max(len(explicit_core), 1)
        return 1.2 * coverage
    if explicit_core and title_core and explicit_core in title_core:
        return 3.2 + min(len(title_core), 40) / 100.0

    if q == title:
        return 2.5
    paraphrased = extract_paraphrase_title(query)
    if paraphrased and normalize_title(paraphrased) == title:
        return 2.5
    # Query may include a family label prefix: "Zero Carbon Park … <title>"
    if title and title in q:
        # Longer contained titles outrank short fragments.
        return 2.0 + min(len(title), 40) / 80.0
    if q in title and len(q) >= 12:
        return 1.5
    if title_core and title_core in q:
        return 1.8 + min(len(title_core), 40) / 100.0
    return 0.0


def doc_id_from_url(source_url: str) -> str | None:
    if not source_url.startswith("hk_cde://"):
        return None
    rest = source_url[len("hk_cde://") :]
    return rest.split("/", 1)[0] or None


def source_by_doc_id(doc_id: str) -> SourceSpec | None:
    for spec in SOURCE_REGISTRY:
        if spec.doc_id == doc_id:
            return spec
    return None
