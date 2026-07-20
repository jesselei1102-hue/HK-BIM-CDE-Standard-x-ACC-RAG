"""Canonical HK Standard source registry with authority metadata."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from rag.config import PROJECT_ROOT
from rag.industry_hk.extract_utils import sha256_file

HK_SOURCES_DIR = PROJECT_ROOT / "output" / "HK Standard"
CIC_STANDARD_DIR = HK_SOURCES_DIR / "CIC BIM Standard"
STATUTORY_DIR = (
    CIC_STANDARD_DIR
    / "CIC BIM Standards for Preparation of Statutory Plan Submissions Dec2020"
)
BD_LANDSD_DIR = HK_SOURCES_DIR / "BD_LandsD"
GENERAL_2024_DIR = CIC_STANDARD_DIR / "CIC BIM Standards General 2024"


@dataclass(frozen=True)
class SourceSpec:
    doc_id: str
    relative_path: str
    kind: str  # pdf | template | image_heavy
    authority_prefix: str
    authority_type: str
    # standard | terminology | case_study | software_guide | statutory | template
    normative_weight: str  # mandatory | recommended | reference | operational
    discipline: str = "general"
    lifecycle_stage: str = "project"
    publication_year: int | None = None
    software: str | None = None
    toc_strategy: str = "outline"
    toc_pages: tuple[int, int] | None = None
    main_body_end_page: int | None = None
    extract: bool = True
    default_priority: str = "normal"
    notes: str = ""

    @property
    def path(self) -> Path:
        return PROJECT_ROOT / self.relative_path


# Existing core sources + newly added publications.
SOURCE_REGISTRY: tuple[SourceSpec, ...] = (
    SourceSpec(
        doc_id="cicbims_2024",
        relative_path=str(
            GENERAL_2024_DIR.relative_to(PROJECT_ROOT)
            / "CIC BIM Standards General (Version 2024).pdf"
        ),
        kind="pdf",
        authority_prefix="CICBIMS 2024",
        authority_type="standard",
        normative_weight="mandatory",
        publication_year=2024,
        toc_strategy="dots",
        toc_pages=(5, 9),
        default_priority="high",
    ),
    SourceSpec(
        doc_id="cic_beginner_cde",
        relative_path=str(
            (CIC_STANDARD_DIR / "CIC Beginner Guide-Adoption of CDE.pdf").relative_to(
                PROJECT_ROOT
            )
        ),
        kind="pdf",
        authority_prefix="CIC CDE Beginner Guide",
        authority_type="standard",
        normative_weight="recommended",
        publication_year=2021,
        toc_strategy="outline",
        default_priority="high",
    ),
    SourceSpec(
        doc_id="devb_harmonisation_v3",
        relative_path=str(
            (
                HK_SOURCES_DIR
                / "DEVB BIM Harmonisation Guidelines for WDs (v3_0) with All Appendices.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="DEVB BIM Harmonisation v3.0",
        authority_type="standard",
        normative_weight="mandatory",
        publication_year=2023,
        toc_strategy="devb_mixed",
        main_body_end_page=41,
        default_priority="high",
    ),
    SourceSpec(
        doc_id="cic_mep_2021",
        relative_path=str(
            (
                CIC_STANDARD_DIR
                / "CIC BIM Standards for Mechanical, Electrical and Plumbing (Version 2 - 2021).pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC BIM Standards MEP 2021",
        authority_type="standard",
        normative_weight="mandatory",
        discipline="mep",
        publication_year=2021,
        toc_strategy="outline",
        default_priority="high",
    ),
    SourceSpec(
        doc_id="cic_uu_2021",
        relative_path=str(
            (
                CIC_STANDARD_DIR
                / "CIC BIM Standards for Underground Utilities (Version 2 - 2021).pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC BIM Standards UU 2021",
        authority_type="standard",
        normative_weight="mandatory",
        discipline="underground_utilities",
        publication_year=2021,
        toc_strategy="outline",
        default_priority="high",
    ),
    SourceSpec(
        doc_id="cic_object_guide_2021",
        relative_path=str(
            (
                CIC_STANDARD_DIR
                / "CIC Production of BIM Object Guide - General Requirements (2021).pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC BIM Object Guide 2021",
        authority_type="standard",
        normative_weight="recommended",
        discipline="bim_objects",
        publication_year=2021,
        toc_strategy="outline",
        default_priority="high",
    ),
    SourceSpec(
        doc_id="cic_statutory_plans_2020",
        relative_path=str(
            (
                STATUTORY_DIR
                / "CIC BIM Standards for Preparation of Statutory Plan Submissions Dec2020.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC Statutory Plan Submissions 2020",
        authority_type="statutory",
        normative_weight="mandatory",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        toc_strategy="outline",
        default_priority="high",
    ),
    SourceSpec(
        doc_id="cic_dictionary_2024",
        relative_path=str(
            (HK_SOURCES_DIR / "CIC BIM Dictionary 2024.pdf").relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC BIM Dictionary 2024",
        authority_type="terminology",
        normative_weight="reference",
        publication_year=2024,
        toc_strategy="outline",
        default_priority="normal",
    ),
    SourceSpec(
        doc_id="cic_amfm_case_2021",
        relative_path=str(
            (
                HK_SOURCES_DIR
                / "CIC BIM for Asset Management and Facility Management Case Sharing 2021.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC AM/FM Case Sharing 2021",
        authority_type="case_study",
        normative_weight="reference",
        discipline="am_fm",
        lifecycle_stage="operations",
        publication_year=2021,
        toc_strategy="outline",
        default_priority="normal",
        notes="Implementation case study; not a binding standard.",
    ),
    SourceSpec(
        doc_id="cic_zcp_bimip_v15",
        relative_path=str(
            (HK_SOURCES_DIR / "CIC_ZCP_BIMIPv1-5_withAppendices.pdf").relative_to(
                PROJECT_ROOT
            )
        ),
        kind="pdf",
        authority_prefix="CIC ZCP BIM Implementation Plan v1.5",
        authority_type="case_study",
        normative_weight="reference",
        discipline="implementation",
        publication_year=2022,
        toc_strategy="outline",
        default_priority="normal",
        notes="Project BIM Implementation Plan reference.",
    ),
    SourceSpec(
        doc_id="cic_stat_archicad_2020",
        relative_path=str(
            (
                STATUTORY_DIR
                / "Appendix 1 CIC BIM User Guide for Preparation of Statutory Plan Submissions ArchiCAD Dec2020.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC Statutory ArchiCAD Guide 2020",
        authority_type="software_guide",
        normative_weight="operational",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        software="ArchiCAD",
        toc_strategy="outline",
        default_priority="normal",
    ),
    SourceSpec(
        doc_id="cic_stat_civil3d_2020",
        relative_path=str(
            (
                STATUTORY_DIR
                / "Appendix 2 CIC BIM User Guide for Preparation of Statutory Plan Submissions Civil 3D Dec2020.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC Statutory Civil 3D Guide 2020",
        authority_type="software_guide",
        normative_weight="operational",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        software="Civil 3D",
        toc_strategy="outline",
        default_priority="normal",
    ),
    SourceSpec(
        doc_id="cic_stat_revit_2020",
        relative_path=str(
            (
                STATUTORY_DIR
                / "Appendix 3 CIC BIM User Guide for Preparation of Statutory Plan Submissions Revit Dec2020.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC Statutory Revit Guide 2020",
        authority_type="software_guide",
        normative_weight="operational",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        software="Revit",
        toc_strategy="outline",
        default_priority="normal",
    ),
    SourceSpec(
        doc_id="cic_stat_tekla_2020",
        relative_path=str(
            (
                STATUTORY_DIR
                / "Appendix 4 CIC BIM User Guide for Preparation of Statutory Plan Submissions Tekla Dec2020.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC Statutory Tekla Guide 2020",
        authority_type="software_guide",
        normative_weight="operational",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        software="Tekla",
        toc_strategy="outline",
        default_priority="normal",
    ),
    SourceSpec(
        doc_id="cic_stat_object_summary_2020",
        relative_path=str(
            (
                STATUTORY_DIR / "Appendix B BIM Object Presentation Summary Dec2020.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="CIC Statutory Object Presentation Summary 2020",
        authority_type="statutory",
        normative_weight="recommended",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        toc_strategy="outline",
        default_priority="normal",
    ),
    SourceSpec(
        doc_id="cic_stat_sample_drawings_2020",
        relative_path=str(
            (STATUTORY_DIR / "Appendix A Sample Drawings Dec2020.pdf").relative_to(
                PROJECT_ROOT
            )
        ),
        kind="image_heavy",
        authority_prefix="CIC Statutory Sample Drawings 2020",
        authority_type="statutory",
        normative_weight="reference",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=2020,
        extract=False,
        notes="Primarily visual sample drawings; requires OCR/image QA before answer use.",
    ),
    SourceSpec(
        doc_id="bd_adm19",
        relative_path=str((BD_LANDSD_DIR / "BD_BD_ADM019.pdf").relative_to(PROJECT_ROOT)),
        kind="pdf",
        authority_prefix="BD PNAP ADM-19",
        authority_type="statutory",
        normative_weight="mandatory",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        publication_year=None,
        extract=False,
        notes="Extracted by scripts/extract_hk_bd_landsd.py",
    ),
    SourceSpec(
        doc_id="bd_adv34",
        relative_path=str((BD_LANDSD_DIR / "BD_BD_ADV034.pdf").relative_to(PROJECT_ROOT)),
        kind="pdf",
        authority_prefix="BD PNAP ADV-34",
        authority_type="statutory",
        normative_weight="mandatory",
        discipline="statutory_submission",
        lifecycle_stage="statutory",
        extract=False,
        notes="Extracted by scripts/extract_hk_bd_landsd.py",
    ),
    SourceSpec(
        doc_id="landsd_bim_gis",
        relative_path=str(
            (
                BD_LANDSD_DIR
                / "LandsD_LandsD_BIM_and_GIS_Data_Integration_Guidelines_Jun2023.pdf"
            ).relative_to(PROJECT_ROOT)
        ),
        kind="pdf",
        authority_prefix="LandsD BIM-GIS Guidelines Jun 2023",
        authority_type="statutory",
        normative_weight="mandatory",
        discipline="gis",
        publication_year=2023,
        extract=False,
        notes="Extracted by scripts/extract_hk_bd_landsd.py",
    ),
)


TEMPLATE_SPECS: tuple[SourceSpec, ...] = tuple(
    SourceSpec(
        doc_id=f"template_d{num}",
        relative_path=str(
            (
                GENERAL_2024_DIR
                / filename
            ).relative_to(PROJECT_ROOT)
        ),
        kind="template",
        authority_prefix=f"CIC Template D{num}",
        authority_type="template",
        normative_weight="recommended",
        publication_year=2021,
        extract=False,
        notes=name,
    )
    for num, filename, name in (
        (1, "D1_CIC BIM_OIR_Template.docx", "OIR"),
        (2, "D2_CIC BIM_AIR_Template.docx", "AIR"),
        (3, "D3_CIC BIM_PIR_Template.docx", "PIR"),
        (4, "D4_CIC BIM_SIR_Template.docx", "SIR"),
        (
            5,
            "D5_CIC Pre-Appointment Implementation Plan_Template.docx",
            "Pre-Appointment IP",
        ),
        (
            6,
            "D6_CIC Pre-Appointment BIM Execution Plan_Template.docx",
            "Pre-Appointment BEP",
        ),
        (7, "D7_CIC BIM Capability Assessment_Template.docx", "Capability Assessment"),
        (
            8,
            "D8_CIC BIM Capability Summary Sheet and Schedule of Software Use.xlsx",
            "Capability Summary",
        ),
        (9, "D9_CIC Project Member Resume.docx", "Project Member Resume"),
    )
)


def iter_registry() -> Iterable[SourceSpec]:
    yield from SOURCE_REGISTRY
    yield from TEMPLATE_SPECS


def pdf_extract_specs() -> list[dict]:
    """Legacy-compatible dict specs for extract_hk_cde_pdfs.py."""
    specs: list[dict] = []
    for item in SOURCE_REGISTRY:
        if item.kind != "pdf" or not item.extract:
            continue
        payload = {
            "doc_id": item.doc_id,
            "path": item.path,
            "authority_prefix": item.authority_prefix,
            "authority_type": item.authority_type,
            "normative_weight": item.normative_weight,
            "discipline": item.discipline,
            "lifecycle_stage": item.lifecycle_stage,
            "publication_year": item.publication_year,
            "software": item.software,
            "toc_strategy": item.toc_strategy,
            "default_priority": item.default_priority,
            "notes": item.notes,
        }
        if item.toc_pages is not None:
            payload["toc_pages"] = item.toc_pages
        if item.main_body_end_page is not None:
            payload["main_body_end_page"] = item.main_body_end_page
        specs.append(payload)
    return specs


def template_extract_specs() -> list[dict]:
    specs: list[dict] = []
    for item in TEMPLATE_SPECS:
        num = int(item.doc_id.rsplit("_d", 1)[-1])
        specs.append(
            {
                "doc_id": item.doc_id,
                "path": item.path,
                "template_num": num,
                "name": item.notes or item.doc_id,
            }
        )
    return specs


def inventory_sources() -> dict:
    """Scan registry files, hash them, and report duplicates / missing / image-heavy."""
    accepted: list[dict] = []
    missing: list[dict] = []
    image_heavy: list[dict] = []
    by_hash: dict[str, list[str]] = {}

    for item in iter_registry():
        row = {
            **asdict(item),
            "absolute_path": str(item.path),
            "exists": item.path.is_file(),
        }
        if not item.path.is_file():
            missing.append(row)
            continue
        digest = sha256_file(item.path)
        row["sha256"] = digest
        row["byte_size"] = item.path.stat().st_size
        by_hash.setdefault(digest, []).append(item.doc_id)
        if item.kind == "image_heavy" or not item.extract:
            if item.kind == "image_heavy":
                image_heavy.append(row)
            accepted.append(row)
        else:
            accepted.append(row)

    duplicates = [
        {"sha256": digest, "doc_ids": ids}
        for digest, ids in by_hash.items()
        if len(ids) > 1
    ]
    return {
        "accepted": accepted,
        "missing": missing,
        "image_heavy": image_heavy,
        "duplicates": duplicates,
        "counts": {
            "accepted": len(accepted),
            "missing": len(missing),
            "image_heavy": len(image_heavy),
            "duplicates": len(duplicates),
            "extractable_pdfs": len(pdf_extract_specs()),
        },
    }


def resolve_spec(doc_id: str) -> SourceSpec | None:
    for item in iter_registry():
        if item.doc_id == doc_id:
            return item
    return None
