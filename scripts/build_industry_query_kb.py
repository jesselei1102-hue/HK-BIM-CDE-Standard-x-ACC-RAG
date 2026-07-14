#!/usr/bin/env python3
"""生成香港 CDE 行业 query_kb 路由种子（30–50 条 approved）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.paths import HK_QUERY_KB_PATH, section_url  # noqa: E402

SEEDS = [
    {
        "id": "hk_wip",
        "topic": "Work in Progress (WIP)",
        "aliases": ["WIP", "进行中", "作业区", "wip环境"],
        "canonical_query_en": "What is Work in Progress (WIP) in the CDE?",
        "canonical_query_zh": "CDE 中 WIP（进行中）区域是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_2_1_work_in_progress_wip",
        "authority": "CICBIMS 2024 §4.2.1",
    },
    {
        "id": "hk_gateway",
        "topic": "CDE Gateways",
        "aliases": ["Gateway", "网关", "授权网关", "WIP Gateway"],
        "canonical_query_en": "What are CDE Gateways and how do they work?",
        "canonical_query_zh": "CDE 网关（Gateway）的作用是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_2_the_cde_and_gateways",
        "authority": "CICBIMS 2024 §4.2",
    },
    {
        "id": "hk_shared",
        "topic": "Shared CDE state",
        "aliases": ["Shared", "共享区", "共享环境"],
        "canonical_query_en": "What is the Shared state in CDE?",
        "canonical_query_zh": "CDE 共享区（Shared）的定义与用途？",
        "target_section": "cicbims_2024/cicbims_2024_4_2_6_shared",
        "authority": "CICBIMS 2024 §4.2.6",
    },
    {
        "id": "hk_published",
        "topic": "Published CDE state",
        "aliases": ["Published", "发布区", "已发布"],
        "canonical_query_en": "What is Published information in CDE?",
        "canonical_query_zh": "CDE 发布区（Published）是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_2_11_published",
        "authority": "CICBIMS 2024 §4.2.11",
    },
    {
        "id": "hk_archive",
        "topic": "Archive CDE state",
        "aliases": ["Archive", "归档", "Archived", "归档区"],
        "canonical_query_en": "How does CDE archiving work?",
        "canonical_query_zh": "CDE 归档（Archive）流程是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_2_12_archive",
        "authority": "CICBIMS 2024 §4.2.12",
    },
    {
        "id": "hk_pir",
        "topic": "Project Information Requirements (PIR)",
        "aliases": ["PIR", "项目信息要求", "Project Information Requirements"],
        "canonical_query_en": "What are Project Information Requirements (PIR)?",
        "canonical_query_zh": "项目信息要求（PIR）是什么？",
        "target_section": "cicbims_2024/cicbims_2024_2_3_project_information_requirements_pir_appendix_d3",
        "authority": "CICBIMS 2024 §2.3",
    },
    {
        "id": "hk_oir",
        "topic": "Organisational Information Requirements (OIR)",
        "aliases": ["OIR", "组织信息要求"],
        "canonical_query_en": "What are Organisational Information Requirements (OIR)?",
        "canonical_query_zh": "组织信息要求（OIR）是什么？",
        "target_section": "cicbims_2024/cicbims_2024_2_1_organisational_information_requirements_oir_appendix_d1",
        "authority": "CICBIMS 2024 §2.1",
    },
    {
        "id": "hk_air",
        "topic": "Asset Information Requirements (AIR)",
        "aliases": ["AIR", "资产信息要求"],
        "canonical_query_en": "What are Asset Information Requirements (AIR)?",
        "canonical_query_zh": "资产信息要求（AIR）是什么？",
        "target_section": "cicbims_2024/cicbims_2024_2_2_asset_information_requirements_air_appendix_d2",
        "authority": "CICBIMS 2024 §2.2",
    },
    {
        "id": "hk_eir",
        "topic": "Exchange Information Requirements (EIR)",
        "aliases": ["EIR", "交换信息要求", "Exchange Information Requirements"],
        "canonical_query_en": "What are Exchange Information Requirements (EIR)?",
        "canonical_query_zh": "交换信息要求（EIR）是什么？",
        "target_section": "cicbims_2024/cicbims_2024_2_5_exchange_information_requirements_eir",
        "authority": "CICBIMS 2024 §2.5",
    },
    {
        "id": "hk_cde_principles",
        "topic": "CDE principles",
        "aliases": ["CDE", "Common Data Environment", "公共数据环境", "信息环境"],
        "canonical_query_en": "What are the principles of Common Data Environment (CDE)?",
        "canonical_query_zh": "公共数据环境（CDE）的基本原则是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_common_data_environment_cde_aligned_with_iso_19650",
        "authority": "CICBIMS 2024 §4",
    },
    {
        "id": "hk_status_codes",
        "topic": "CDE status codes",
        "aliases": ["Status Code", "状态码", "Suitability", "适宜性代码"],
        "canonical_query_en": "What are CDE status codes (suitability)?",
        "canonical_query_zh": "CDE 状态码（适宜性）如何定义？",
        "target_section": "cicbims_2024/cicbims_2024_4_4_2_status_code_suitability",
        "authority": "CICBIMS 2024 §4.4.2",
    },
    {
        "id": "hk_handover",
        "topic": "CDE handover",
        "aliases": ["Handover", "移交", "AIM handover", "项目移交"],
        "canonical_query_en": "What are CDE handover procedures?",
        "canonical_query_zh": "CDE 移交（Handover）程序有哪些要求？",
        "target_section": "cicbims_2024/cicbims_2024_4_6_the_cde_handover_procedures",
        "authority": "CICBIMS 2024 §4.6",
    },
    {
        "id": "hk_cde_security",
        "topic": "CDE security",
        "aliases": ["CDE security", "CDE 安全", "安全存储"],
        "canonical_query_en": "What are CDE security and storage requirements?",
        "canonical_query_zh": "CDE 安全与存储规范是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_5_cde_security_storage_and_technology_specification",
        "authority": "CICBIMS 2024 §4.5",
    },
    {
        "id": "hk_beginner_what_cde",
        "topic": "What is CDE (beginner)",
        "aliases": ["什么是CDE", "CDE入门", "CDE 定义"],
        "canonical_query_en": "What is a Common Data Environment (CDE)?",
        "canonical_query_zh": "什么是 CDE（公共数据环境）？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_1_2_what_is_cde",
        "authority": "CIC CDE Beginner Guide §1.2",
    },
    {
        "id": "hk_beginner_select",
        "topic": "CDE selection advice",
        "aliases": ["CDE选型", "选择CDE", "CDE selection"],
        "canonical_query_en": "How to select a CDE platform?",
        "canonical_query_zh": "如何选择 CDE 平台？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_2_advice_in_selection_of_a_cde",
        "authority": "CIC CDE Beginner Guide §2",
    },
    {
        "id": "hk_beginner_functions",
        "topic": "Essential CDE functions",
        "aliases": ["CDE功能", "essential functions"],
        "canonical_query_en": "What are essential functions of CDE?",
        "canonical_query_zh": "CDE 必备功能有哪些？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_1_7_essential_functions_of_cde",
        "authority": "CIC CDE Beginner Guide §1.7",
    },
    {
        "id": "hk_devb_naming",
        "topic": "BIM model naming (DEVB)",
        "aliases": ["命名标准", "BIM naming", "模型命名", "Harmonisation naming"],
        "canonical_query_en": "What is DEVB BIM model naming convention?",
        "canonical_query_zh": "工务署 BIM 模型命名规范是什么？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_federation_and_bim_model_naming",
        "authority": "DEVB Harmonisation v3.0 §4",
    },
    {
        "id": "hk_info_container",
        "topic": "Information Container ID",
        "aliases": ["信息容器", "Information Container", "容器ID", "Information Container ID"],
        "canonical_query_en": "What is Information Container ID in DEVB harmonisation?",
        "canonical_query_zh": "信息容器 ID（Information Container ID）如何定义？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_federation_and_bim_model_naming",
        "authority": "DEVB Harmonisation v3.0 §4.2",
    },
    {
        "id": "hk_devb_landsd",
        "topic": "LandsD BIM submission",
        "aliases": ["LandsD", "地政总署", "提交BIM", "as-built submission"],
        "canonical_query_en": "How to submit BIM models to LandsD?",
        "canonical_query_zh": "如何向地政总署（LandsD）提交 BIM 模型？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_appendix_xiv_guidelines_for_submission_of_design_and_as_built_bim",
        "authority": "DEVB Harmonisation v3.0 Appendix XIV",
    },
    {
        "id": "hk_devb_responsibility",
        "topic": "Information responsibility matrix",
        "aliases": ["责任矩阵", "Information Responsibility", "IRAM"],
        "canonical_query_en": "What is the Information Responsibility Assignment Matrix?",
        "canonical_query_zh": "信息责任分配矩阵是什么？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_appendix_ii_information_responsibility_assignment_matrix_v2",
        "authority": "DEVB Harmonisation v3.0 Appendix II",
    },
    {
        "id": "hk_iso_terms",
        "topic": "ISO 19650 terminologies",
        "aliases": ["ISO 19650", "ISO术语", "19650术语"],
        "canonical_query_en": "What ISO 19650 terminologies are adopted in DEVB guidelines?",
        "canonical_query_zh": "工务署指南采用哪些 ISO 19650 术语？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_appendix_i_iso_19650_terminologies_v2",
        "authority": "DEVB Harmonisation v3.0 Appendix I",
    },
    {
        "id": "hk_federation",
        "topic": "Federation strategy",
        "aliases": ["Federation", "联邦模型", "模型联邦"],
        "canonical_query_en": "What is BIM federation strategy?",
        "canonical_query_zh": "BIM 联邦（Federation）策略是什么？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_appendix_viii_federation_strategy_diagrams_and_naming_examples_v2",
        "authority": "DEVB Harmonisation v3.0 Appendix VIII",
    },
    {
        "id": "hk_authorisation_codes",
        "topic": "Authorisation codes",
        "aliases": ["Authorisation Code", "授权码", "签批代码"],
        "canonical_query_en": "How are authorisation codes applied in CDE workflow?",
        "canonical_query_zh": "CDE 工作流中授权码如何应用？",
        "target_section": "cicbims_2024/cicbims_2024_4_4_4_application_of_authorisation_codes_indicating_workflow_author",
        "authority": "CICBIMS 2024 §4.4.4",
    },
    {
        "id": "hk_folder_structure",
        "topic": "CDE folder structure",
        "aliases": ["文件夹结构", "folder structure", "目录结构"],
        "canonical_query_en": "What folder structure is recommended for CDE?",
        "canonical_query_zh": "CDE 推荐文件夹结构是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_5_5_project_folder_structure",
        "authority": "CICBIMS 2024 §4.5.5",
    },
    {
        "id": "hk_cloud_cde",
        "topic": "Cloud-hosted CDE",
        "aliases": ["云CDE", "cloud CDE", "私有云", "公有云"],
        "canonical_query_en": "What to consider for cloud-hosted CDE?",
        "canonical_query_zh": "云环境 CDE 选型要注意什么？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_2_2_cde_hosted_in_the_cloud_environment",
        "authority": "CIC CDE Beginner Guide §2.2",
    },
    {
        "id": "hk_workflow_cde",
        "topic": "Workflow management in CDE",
        "aliases": ["工作流", "workflow", "审批流程"],
        "canonical_query_en": "How does workflow management work in CDE?",
        "canonical_query_zh": "CDE 工作流管理如何实现？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_2_6_workflow_management_in_cde",
        "authority": "CIC CDE Beginner Guide §2.6",
    },
    {
        "id": "hk_pim_aim",
        "topic": "PIM and AIM",
        "aliases": ["PIM", "AIM", "项目信息模型", "资产信息模型"],
        "canonical_query_en": "What are PIM and AIM in CDE context?",
        "canonical_query_zh": "CDE 语境下 PIM 与 AIM 分别指什么？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_1_4_cde_for_pim_and_aim",
        "authority": "CIC CDE Beginner Guide §1.4",
    },
    {
        "id": "hk_loin",
        "topic": "Level of Information Need",
        "aliases": ["LOIN", "信息需求等级", "Level of Information Need"],
        "canonical_query_en": "What is Level of Information Need (LOIN)?",
        "canonical_query_zh": "信息需求等级（LOIN）是什么？",
        "target_section": "cicbims_2024/cicbims_2024_2_6_level_of_information_need",
        "authority": "CICBIMS 2024 §2.6",
    },
    {
        "id": "hk_template_d3",
        "topic": "PIR template fields",
        "aliases": ["D3模板", "PIR template", "D3字段"],
        "canonical_query_en": "What fields are in CIC PIR template (D3)?",
        "canonical_query_zh": "CIC PIR 模板（D3）包含哪些字段？",
        "target_section": "template_d3/d3_fields",
        "authority": "CICBIMS 2024 Appendix D3",
    },
    {
        "id": "hk_info_mgmt",
        "topic": "Information management ISO 19650",
        "aliases": ["信息管理", "Information Management", "ISO19650流程"],
        "canonical_query_en": "How is information management aligned with ISO 19650?",
        "canonical_query_zh": "信息管理与 ISO 19650 如何对齐？",
        "target_section": "cicbims_2024/cicbims_2024_1_information_management_aligned_with_iso_19650",
        "authority": "CICBIMS 2024 §1",
    },
    {
        "id": "hk_devb_object_files",
        "topic": "BIM object files",
        "aliases": ["BIM Object", "BIM对象", "对象文件"],
        "canonical_query_en": "What are BIM object file requirements in DEVB harmonisation?",
        "canonical_query_zh": "工务署 BIM 对象文件要求是什么？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_bim_object_files",
        "authority": "DEVB Harmonisation v3.0 §3",
    },
    {
        "id": "hk_cde_functional",
        "topic": "CDE functional requirements",
        "aliases": ["功能要求", "functional requirements", "CDE功能需求"],
        "canonical_query_en": "What are CDE functional requirements?",
        "canonical_query_zh": "CDE 功能要求有哪些？",
        "target_section": "cicbims_2024/cicbims_2024_4_3_the_cde_functional_requirements",
        "authority": "CICBIMS 2024 §4.3",
    },
    {
        "id": "hk_cde_process",
        "topic": "CDE process requirements",
        "aliases": ["流程要求", "process requirements", "CDE流程"],
        "canonical_query_en": "What are CDE process requirements?",
        "canonical_query_zh": "CDE 流程要求是什么？",
        "target_section": "cicbims_2024/cicbims_2024_4_4_the_cde_process_requirements",
        "authority": "CICBIMS 2024 §4.4",
    },
    {
        "id": "hk_checklist_cde",
        "topic": "CDE feature checklist",
        "aliases": ["CDE清单", "checklist", "功能清单"],
        "canonical_query_en": "What major CDE features should be checked?",
        "canonical_query_zh": "CDE 主要功能检查清单有哪些？",
        "target_section": "cic_beginner_cde/cic_beginner_cde_3_annex_a_checklist_on_major_features_of_a_cde",
        "authority": "CIC CDE Beginner Guide Annex A",
    },
    {
        "id": "hk_container_codes",
        "topic": "Information Container ID codes",
        "aliases": ["容器ID字段", "Common Codes", "Appendix X"],
        "canonical_query_en": "What are common codes for Information Container ID fields?",
        "canonical_query_zh": "信息容器 ID 字段的通用代码有哪些？",
        "target_section": "devb_harmonisation_v3/devb_harmonisation_v3_appendix_ix_sample_project_specific_codes_for_naming_v3_0",
        "authority": "DEVB Harmonisation v3.0 Appendix X",
    },
    {
        "id": "hk_bd_adv34",
        "topic": "BD PNAP ADV-34 BIM statutory plan submissions",
        "aliases": [
            "ADV-34",
            "ADV34",
            "BD BIM",
            "屋宇署BIM",
            "法定图则BIM",
            "BIM提交BD",
        ],
        "canonical_query_en": (
            "Buildings Department PNAP ADV-34 BIM guidelines for "
            "statutory plan submissions"
        ),
        "canonical_query_zh": "屋宇署 ADV-34 对 BIM 法定图则提交有什么要求？",
        "target_section": "bd_adv34/bd_adv34_bim_submissions_general_guidelines",
        "authority": "BD PNAP ADV-34",
    },
    {
        "id": "hk_bd_adm19_bim",
        "topic": "BD PNAP ADM-19 BIM model data extraction consent",
        "aliases": [
            "ADM-19",
            "ADM19",
            "BIM提取同意",
            "GBP审批",
            "屋宇署审批流程",
        ],
        "canonical_query_en": (
            "BD ADM-19 consent to extraction of information from BIM model "
            "for LandsD PlanD"
        ),
        "canonical_query_zh": "ADM-19 关于从 BIM 模型提取信息给地政规划署有何规定？",
        "target_section": (
            "bd_adm19/bd_adm19_consent_to_extraction_of_information_from_bim_model"
        ),
        "authority": "BD PNAP ADM-19 §BIM",
    },
    {
        "id": "hk_bd_adm19_process",
        "topic": "BD ADM-19 building approval process",
        "aliases": ["审批流程", "plan submission", "GBP提交", "curtailed check"],
        "canonical_query_en": "BD ADM-19 building approval process plan submissions",
        "canonical_query_zh": "屋宇署 ADM-19 建筑图则审批流程是什么？",
        "target_section": "bd_adm19/bd_adm19_processing_of_plan_submissions",
        "authority": "BD PNAP ADM-19",
    },
    {
        "id": "hk_landsd_bim_gis",
        "topic": "LandsD BIM and GIS data integration",
        "aliases": [
            "BIM GIS",
            "BIM-GIS",
            "地政BIM",
            "LandsD BIM",
            "3D Digital Map",
            "CSDI",
        ],
        "canonical_query_en": (
            "LandsD BIM and GIS data integration guidelines modelling "
            "and conversion requirements"
        ),
        "canonical_query_zh": "地政总署 BIM 与 GIS 数据整合有哪些建模与转换要求？",
        "target_section": (
            "landsd_bim_gis/landsd_bim_gis_chapter_2_high_level_requirements_on_bim_modelling"
        ),
        "authority": "LandsD BIM-GIS Guidelines Jun 2023",
    },
    {
        "id": "hk_bd_electronic_cad",
        "topic": "BD ADM-19 Appendix F electronic / CAD-BIM presentation",
        "aliases": ["电子提交", "CAD图层", "CSWP", "电子图则"],
        "canonical_query_en": (
            "BD ADM-19 Appendix F electronic submission CAD BIM layer naming"
        ),
        "canonical_query_zh": "ADM-19 附录 F 电子提交与 CAD/BIM 图层命名要求？",
        "target_section": (
            "bd_adm19/bd_adm19_appendix_f_electronic_submission_cad_bim_presentation"
        ),
        "authority": "BD PNAP ADM-19 Appendix F",
    },
]


def _resolve_section(seed: dict, corpus_root: Path) -> tuple[str, str, str, str, str]:
    target = seed["target_section"]
    if "/" in target:
        doc_id, section_id = target.split("/", 1)
    else:
        doc_id, section_id = target, target
    md_path = corpus_root / doc_id / f"{section_id}.md"
    if not md_path.is_file():
        tokens = [token for token in section_id.split("_") if len(token) > 3]
        candidates = list(corpus_root.rglob("*.md"))
        best: Path | None = None
        best_score = 0
        for candidate in candidates:
            if candidate.parent.name != doc_id and doc_id not in str(candidate):
                continue
            name = candidate.stem
            score = sum(1 for token in tokens if token in name)
            if score > best_score:
                best_score = score
                best = candidate
        if best is not None and best_score >= 2:
            md_path = best
            section_id = md_path.stem
            doc_id = md_path.parent.name
    title = seed["topic"]
    if md_path.is_file():
        text = md_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
    source_path = str(md_path.relative_to(PROJECT_ROOT)) if md_path.is_file() else ""
    target_url = section_url(doc_id, section_id)
    return title, target_url, source_path, doc_id, section_id


def main() -> int:
    corpus_root = PROJECT_ROOT / "knowledge" / "industry" / "hk_cde" / "corpus"
    HK_QUERY_KB_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    for seed in SEEDS:
        title, target_url, source_path, doc_id, section_id = _resolve_section(
            seed, corpus_root
        )
        rows.append(
            {
                "id": seed["id"],
                "topic": seed["topic"],
                "aliases": seed["aliases"],
                "canonical_query_en": seed["canonical_query_en"],
                "canonical_query_zh": seed["canonical_query_zh"],
                "target_title": title,
                "target_url": target_url,
                "target_guid": section_id,
                "target_section": f"{doc_id}/{section_id}",
                "source_path": source_path,
                "authority": seed["authority"],
                "related_product_guids": [],
                "entry_type": "industry_standard",
                "status": "approved",
            }
        )

    with HK_QUERY_KB_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"写入 {len(rows)} 条路由 -> {HK_QUERY_KB_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
