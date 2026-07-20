#!/usr/bin/env python3
"""Generate source-grounded HK CDE evaluation fixtures from corpus metadata."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.ingestion import is_noise_section  # noqa: E402
from rag.industry_hk.paths import HK_CORPUS_DIR  # noqa: E402

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
SHALL_RE = re.compile(
    r"([^.!?\n]{0,80}\b(?:shall|must|required|should)\b[^.!?\n]{0,160}[.!?])",
    re.I,
)
NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?%?|\bS[0-9]\b|\bA[0-9]\b|\bLOD(?:-G|-I)?\b|\bLOIN\b", re.I)

ZH_ALIASES = {
    "work in progress": "进行中",
    "gateway": "网关",
    "common data environment": "公共数据环境",
    "naming": "命名标准",
    "information container": "信息容器",
    "level of information need": "信息需求等级",
    "underground utilities": "地下管线",
    "mechanical, electrical and plumbing": "机电",
    "statutory": "法定图则",
}


def _parse(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw
    return yaml.safe_load(match.group(1)) or {}, raw[match.end() :]


def _iter_sections() -> list[tuple[Path, dict, str]]:
    rows: list[tuple[Path, dict, str]] = []
    for path in sorted(HK_CORPUS_DIR.rglob("*.md")):
        if path.parent.name == "templates":
            continue
        meta, body = _parse(path)
        if not meta or is_noise_section(meta):
            continue
        if len(body.strip()) < 120:
            continue
        rows.append((path, meta, body))
    return rows


def _coverage_cases(sections: list[tuple[Path, dict, str]], limit: int) -> list[dict]:
    preferred_docs = {
        "cicbims_2024",
        "cic_beginner_cde",
        "devb_harmonisation_v3",
        "cic_mep_2021",
        "cic_uu_2021",
        "cic_object_guide_2021",
        "cic_statutory_plans_2020",
        "bd_adm19",
        "bd_adv34",
        "landsd_bim_gis",
    }
    generic_title_re = re.compile(
        r"^(?:\d+(?:\.\d+)*\s+)?(references?|document\s+structure|contents?|"
        r"introduction|overview|appendix)\b",
        re.I,
    )
    doc_labels = {
        "cic_mep_2021": "CIC MEP 2021",
        "cic_uu_2021": "CIC Underground Utilities 2021",
        "cic_object_guide_2021": "CIC BIM Object Guide 2021",
        "cic_statutory_plans_2020": "CIC Statutory Plan Submissions 2020",
        "cicbims_2024": "CIC BIM Standards General 2024",
        "devb_harmonisation_v3": "DEVB Harmonisation v3",
        "cic_beginner_cde": "CIC CDE Beginner Guide",
    }
    per_doc_quota = max(4, limit // max(len(preferred_docs), 1))
    by_doc: dict[str, list[tuple[Path, dict, str]]] = {doc: [] for doc in preferred_docs}
    for path, meta, body in sections:
        doc_id = meta.get("doc_id")
        if doc_id not in preferred_docs:
            continue
        if meta.get("authority_type") not in {"standard", "statutory"}:
            continue
        title = str(meta.get("title", "")).strip()
        if len(title) < 4 or generic_title_re.search(title):
            continue
        by_doc[doc_id].append((path, meta, body))

    cases: list[dict] = []
    rng = random.Random(42)
    for doc_id, rows in by_doc.items():
        rng.shuffle(rows)
        for path, meta, body in rows[:per_doc_quota]:
            if len(cases) >= limit:
                break
            title = str(meta.get("title", "")).strip()
            section_id = meta["section_id"]
            label = doc_labels.get(doc_id, doc_id)
            base = {
                "expected_doc": doc_id,
                "expected_section": section_id,
                "expected_section_contains": section_id.lower(),
                "authority_type": meta.get("authority_type", "standard"),
                "discipline": meta.get("discipline", "general"),
                "source_path": str(path.relative_to(PROJECT_ROOT)),
                "expect_track": "industry",
            }
            cases.append(
                {
                    "id": f"cov_title_{len(cases)+1:03d}",
                    "query": f"{label}: {title}",
                    "lang": "en",
                    "case_type": "title",
                    **base,
                }
            )
            if len(cases) >= limit:
                break
            cases.append(
                {
                    "id": f"cov_nl_{len(cases)+1:03d}",
                    "query": f"What are the requirements for {title} in {label}?",
                    "lang": "en",
                    "case_type": "paraphrase",
                    **base,
                }
            )
            lowered = title.lower()
            for en, zh in ZH_ALIASES.items():
                if en in lowered and len(cases) < limit:
                    cases.append(
                        {
                            "id": f"cov_zh_{len(cases)+1:03d}",
                            "query": f"{label} {zh}有什么要求",
                            "lang": "zh",
                            "case_type": "bilingual",
                            **base,
                        }
                    )
                    break
        if len(cases) >= limit:
            break
    return cases[:limit]


def _requirement_cases(sections: list[tuple[Path, dict, str]], limit: int) -> list[dict]:
    cases: list[dict] = []
    for path, meta, body in sections:
        if meta.get("authority_type") not in {"standard", "statutory"}:
            continue
        if meta.get("normative_weight") not in {"mandatory", "recommended", None}:
            continue
        title = str(meta.get("title") or "").strip()
        if len(title) < 4:
            continue
        for match in SHALL_RE.finditer(body):
            sentence = " ".join(match.group(1).split())
            if len(sentence) < 40:
                continue
            keys = [
                item
                for item in NUMBER_RE.findall(sentence)
                if len(str(item)) >= 2
            ]
            modality = "shall"
            low = sentence.lower()
            if " must " in f" {low} ":
                modality = "must"
            elif "required" in low:
                modality = "required"
            elif "should" in low:
                modality = "should"
            # Retrieval-friendly query: section title + short obligation cue.
            cue = sentence
            for token in ("shall", "must", "required", "should"):
                idx = cue.lower().find(token)
                if idx >= 0:
                    cue = cue[max(0, idx - 40) : idx + 80]
                    break
            cue = " ".join(cue.split())
            cases.append(
                {
                    "id": f"req_{len(cases)+1:03d}",
                    "query": f"{title} — {cue}",
                    "expected_doc": meta["doc_id"],
                    "expected_section": meta["section_id"],
                    "expected_section_contains": str(meta["section_id"]).lower(),
                    "authority_type": meta.get("authority_type", "standard"),
                    "normative_weight": meta.get("normative_weight", "recommended"),
                    "discipline": meta.get("discipline", "general"),
                    "source_sentence": sentence,
                    "required_modality": modality,
                    "key_facts": keys[:8],
                    "expect_track": "industry",
                    "source_path": str(path.relative_to(PROJECT_ROOT)),
                }
            )
            if len(cases) >= limit:
                return cases
            break  # one requirement case per section for diversity
    return cases


def _negative_cases() -> list[dict]:
    cases = [
        {
            "id": "neg_docs_permissions",
            "query": "How do I set folder permissions in Autodesk Docs?",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_docs_upload",
            "query": "How to upload files in ACC Docs",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_docs_share",
            "query": "Create a public link to share a file in Docs",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_docs_markup",
            "query": "How to add markups on a PDF in Autodesk Docs",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_authority_case_study",
            "query": "Is the CIC AM/FM Case Sharing a mandatory CIC BIM Standard?",
            "expect_track": "industry",
            "expected_doc": "cic_amfm_case_2021",
            "expected_authority_type": "case_study",
            "must_not_claim_mandatory": True,
            "ingest_scope_min": "substantive",
            "case_type": "authority_confusion",
        },
        {
            "id": "neg_authority_dictionary",
            "query": "Does the CIC BIM Dictionary create binding project requirements?",
            "expect_track": "industry",
            "expected_doc": "cic_dictionary_2024",
            "expected_authority_type": "terminology",
            "must_not_claim_mandatory": True,
            "ingest_scope_min": "substantive",
            "case_type": "authority_confusion",
        },
        {
            "id": "neg_authority_software",
            "query": "Is the 2020 Revit statutory user guide a legal Building Department code?",
            "expect_track": "industry",
            "expected_doc": "cic_stat_revit_2020",
            "expected_authority_type": "software_guide",
            "must_not_claim_mandatory": True,
            "ingest_scope_min": "all",
            "case_type": "authority_confusion",
        },
        {
            "id": "neg_authority_zcp",
            "query": "Must every Hong Kong project copy the Zero Carbon Park BIM Implementation Plan?",
            "expect_track": "industry",
            "expected_doc": "cic_zcp_bimip_v15",
            "expected_authority_type": "case_study",
            "must_not_claim_mandatory": True,
            "ingest_scope_min": "substantive",
            "case_type": "authority_confusion",
        },
        {
            "id": "neg_cross_bd_vs_cic",
            "query": "ADM-19 curtain wall fast track checklist",
            "expect_track": "industry",
            "expected_doc": "bd_adm19",
            "expected_section_contains": "curtain",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_cross_landsd",
            "query": "LandsD BIM GIS data conversion requirements",
            "expect_track": "industry",
            "expected_doc": "landsd_bim_gis",
            "expected_section_contains": "data_conversion",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_cross_mep",
            "query": "CIC MEP LOD-I requirements for ducts",
            "expect_track": "industry",
            "expected_doc": "cic_mep_2021",
            "expected_section_contains": "lod",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_cross_uu",
            "query": "Underground utilities PAS128 quality level requirements",
            "expect_track": "industry",
            "expected_doc": "cic_uu_2021",
            "expected_section_contains": "pas",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_cross_object_guide",
            "query": "CIC BIM object property naming requirements",
            "expect_track": "industry",
            "expected_doc": "cic_object_guide_2021",
            "expected_section_contains": "property",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_cross_statutory_plans",
            "query": "BIM origin point and orientation for statutory plan submissions",
            "expect_track": "industry",
            "expected_doc": "cic_statutory_plans_2020",
            "expected_section_contains": "origin",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_refuse_unknown",
            "query": "What is the mandatory CIC BIM tax rate for 2099?",
            "expect_track": "out_of_domain",
            "expect_refusal": True,
            "case_type": "refusal",
        },
        {
            "id": "neg_refuse_invented_code",
            "query": "Explain CIC BIM Standard ZZ-99 quantum twin mandatory clause",
            "expect_track": "out_of_domain",
            "expect_refusal": True,
            "case_type": "refusal",
        },
        {
            "id": "neg_docs_review",
            "query": "Create an approval workflow in Autodesk Docs Reviews",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_docs_naming_ui",
            "query": "Where is the Naming Standards button in Autodesk Docs settings",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_docs_transmittal",
            "query": "How to create a transmittal in ACC Docs",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_docs_browser",
            "query": "What browsers are supported for Autodesk Construction Cloud",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
        {
            "id": "neg_confuse_devb_naming",
            "query": "DEVB information container ID naming fields",
            "expect_track": "industry",
            "expected_doc": "devb_harmonisation_v3",
            "expected_section_contains": "naming",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_confuse_wip_gateway",
            "query": "ISO 19650 WIP authorisation gateway in CIC standards",
            "expect_track": "industry",
            "expected_doc": "cicbims_2024",
            "expected_section_contains": "gateway",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_confuse_cde_beginner",
            "query": "CDE beginner guide approval and review process",
            "expect_track": "industry",
            "expected_doc": "cic_beginner_cde",
            "expected_section_contains": "approv",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_confuse_adv34",
            "query": "BD ADV-34 BIM submission general guidelines",
            "expect_track": "industry",
            "expected_doc": "bd_adv34",
            "expected_section_contains": "adv34",
            "case_type": "cross_authority",
        },
        {
            "id": "neg_software_archicad",
            "query": "ArchiCAD statutory plan submission user guide steps",
            "expect_track": "industry",
            "expected_doc": "cic_stat_archicad_2020",
            "expected_authority_type": "software_guide",
            "case_type": "software_specific",
        },
        {
            "id": "neg_software_civil3d",
            "query": "Civil 3D statutory plan BIM user guide",
            "expect_track": "industry",
            "expected_doc": "cic_stat_civil3d_2020",
            "expected_authority_type": "software_guide",
            "case_type": "software_specific",
        },
        {
            "id": "neg_software_tekla",
            "query": "Tekla statutory plan submissions BIM user guide",
            "expect_track": "industry",
            "expected_doc": "cic_stat_tekla_2020",
            "expected_authority_type": "software_guide",
            "case_type": "software_specific",
        },
        {
            "id": "neg_refuse_weather",
            "query": "What will the weather be in Hong Kong tomorrow for BIM handover?",
            "expect_track": "out_of_domain",
            "expect_refusal": True,
            "case_type": "refusal",
        },
        {
            "id": "neg_refuse_unrelated",
            "query": "Write a poem about Revit family creation with no sources",
            "expect_track": "out_of_domain",
            "expect_refusal": True,
            "case_type": "refusal",
        },
        {
            "id": "neg_docs_model_browser",
            "query": "How to filter RVT properties in Model Browser",
            "expect_track": "docs",
            "case_type": "product_not_industry",
        },
    ]
    return cases


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build HK grounded eval fixtures")
    parser.add_argument("--coverage-limit", type=int, default=100)
    parser.add_argument("--requirement-limit", type=int, default=40)
    parser.add_argument("--out-dir", type=Path, default=PROJECT_ROOT / "eval")
    args = parser.parse_args(argv)

    sections = _iter_sections()
    coverage = _coverage_cases(sections, args.coverage_limit)
    requirements = _requirement_cases(sections, args.requirement_limit)
    negatives = _negative_cases()

    cov_path = args.out_dir / "hk_cde_coverage_cases.jsonl"
    req_path = args.out_dir / "hk_cde_requirement_cases.jsonl"
    neg_path = args.out_dir / "hk_cde_negative_cases.jsonl"
    _write_jsonl(cov_path, coverage)
    _write_jsonl(req_path, requirements)
    _write_jsonl(neg_path, negatives)

    print("Generated grounded HK eval fixtures")
    print(f"  coverage: {len(coverage)} -> {cov_path}")
    print(f"  requirements: {len(requirements)} -> {req_path}")
    print(f"  negatives: {len(negatives)} -> {neg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
