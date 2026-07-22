#!/usr/bin/env python3
"""生成 playbook query_kb + sections_index（路由用不进 LLM）。"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.playbook_acc_hk.paths import (  # noqa: E402
    PLAYBOOK_CORPUS_DIR,
    PLAYBOOK_QUERY_KB_PATH,
    PLAYBOOK_SECTIONS_INDEX_PATH,
    playbook_url,
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

SEEDS = [
    {
        "id": "pb_index",
        "capability": "project_template",
        "file": "00_hk_cde_spec_index.md",
        "aliases": [
            "HK CDE Spec",
            "项目规格索引",
            "Buildings还是Civil",
            "ACC HK GC",
            "总包项目说明书",
            "project specification index",
        ],
        "canonical_query_en": "HK CDE Spec Buildings vs Civil project specification index",
        "canonical_query_zh": "HK CDE Spec Buildings和Civil项目规格怎么选用",
    },
    {
        "id": "pb_buildings_roles",
        "capability": "roles",
        "file": "10_buildings_overview_roles.md",
        "aliases": [
            "Buildings角色",
            "楼宇 RACI",
            "Owner权限边界",
            "GC_Management",
            "Buildings role manual",
        ],
        "canonical_query_en": "Buildings Owner GC Consultant Subcon roles and daily operations",
        "canonical_query_zh": "Buildings项目Owner GC顾问分包角色职责和日常操作",
    },
    {
        "id": "pb_buildings_folders",
        "capability": "folder_cde",
        "file": "11_buildings_folders_permissions.md",
        "aliases": [
            "Buildings文件夹",
            "楼宇目录结构",
            "01_WIP Team_Arch",
            "Owner不可见WIP",
            "Buildings folder tree",
            "Buildings权限矩阵",
        ],
        "canonical_query_en": "Buildings ACC folder structure 01_WIP SHARED PUBLISHED permissions matrix",
        "canonical_query_zh": "Buildings项目ACC文件夹结构和权限矩阵怎么配",
    },
    {
        "id": "pb_buildings_workflows",
        "capability": "workflow",
        "file": "12_buildings_issues_workflows.md",
        "aliases": [
            "Buildings审批",
            "WF-A WF-B",
            "Fit-out Defect",
            "Buildings Issue Types",
        ],
        "canonical_query_en": "Buildings WF-A WF-B WF-C WF-D approval workflows and issue types",
        "canonical_query_zh": "Buildings项目WF-A到WF-D审批流和Issue类型",
    },
    {
        "id": "pb_buildings_naming",
        "capability": "naming",
        "file": "13_buildings_naming_fields.md",
        "aliases": [
            "九段命名",
            "Buildings命名",
            "SuitabilityStatus",
            "Revision不进文件名",
            "nine segment naming",
        ],
        "canonical_query_en": "Buildings nine-segment naming Project Originator Building Zone Level Type Role System Number",
        "canonical_query_zh": "Buildings九段命名规则和自定义字段怎么配",
    },
    {
        "id": "pb_buildings_statutory",
        "capability": "workflow",
        "file": "14_buildings_forms_statutory.md",
        "aliases": [
            "BD提交",
            "BD Submission Checklist",
            "2D/3D Consistency",
            "Buildings表单",
            "法定提交包",
        ],
        "canonical_query_en": "Buildings BD statutory submission checklist and forms",
        "canonical_query_zh": "Buildings BD法定提交检查表和表单要求",
    },
    {
        "id": "pb_buildings_assets",
        "capability": "project_template",
        "file": "15_buildings_assets_midp_acceptance.md",
        "aliases": [
            "EMSD_Code",
            "MIDP",
            "Buildings移交",
            "Tandem",
            "Shared冻结",
        ],
        "canonical_query_en": "Buildings EMSD MIDP Shared freeze and handover acceptance",
        "canonical_query_zh": "Buildings EMSD资产分类 MIDP和移交验收",
    },
    {
        "id": "pb_civil_roles",
        "capability": "roles",
        "file": "20_civil_overview_roles.md",
        "aliases": [
            "Civil角色",
            "土木 RACI",
            "区段交付",
            "Civil role manual",
        ],
        "canonical_query_en": "Civil Owner GC Consultant Subcon roles section delivery",
        "canonical_query_zh": "Civil土木项目角色职责和区段交付操作",
    },
    {
        "id": "pb_civil_folders",
        "capability": "folder_cde",
        "file": "21_civil_folders_permissions.md",
        "aliases": [
            "Civil文件夹",
            "土木目录",
            "By Section",
            "LandsD Submission目录",
            "Civil folder tree",
            "SEC-A",
        ],
        "canonical_query_en": "Civil ACC folder structure By Section LandsD Submission permissions",
        "canonical_query_zh": "Civil项目文件夹 By Section和LandsD目录权限",
    },
    {
        "id": "pb_civil_workflows",
        "capability": "workflow",
        "file": "22_civil_issues_workflows.md",
        "aliases": [
            "Civil审批",
            "Underground Utilities",
            "Traffic Management",
            "Temporary Works",
            "WF-C LandsD",
        ],
        "canonical_query_en": "Civil WF-A B C D workflows Underground Utilities Traffic Temporary Works",
        "canonical_query_zh": "Civil审批流和管线交通临时工程Issue",
    },
    {
        "id": "pb_civil_naming",
        "capability": "naming",
        "file": "23_civil_naming_fields.md",
        "aliases": [
            "Civil命名",
            "Building等于区段",
            "Section Chainage",
            "ContractPackage",
            "SEA SEB",
        ],
        "canonical_query_en": "Civil naming Building equals section code Chainage ContractPackage",
        "canonical_query_zh": "Civil命名Building区段码与Section Chainage字段",
    },
    {
        "id": "pb_civil_statutory",
        "capability": "workflow",
        "file": "24_civil_forms_statutory.md",
        "aliases": [
            "LandsD Completeness",
            "PROJECT_BOUNDARY",
            "MODEL_FILE_LIST",
            "Civil表单",
            "工务提交",
        ],
        "canonical_query_en": "Civil LandsD completeness PROJECT_BOUNDARY MODEL_FILE_LIST forms",
        "canonical_query_zh": "Civil LandsD完整性检查边界和模型清单表单",
    },
    {
        "id": "pb_civil_assets",
        "capability": "project_template",
        "file": "25_civil_assets_midp_acceptance.md",
        "aliases": [
            "AssetClass",
            "Civil EMSD子集",
            "Civil移交",
            "土木资产",
        ],
        "canonical_query_en": "Civil AssetClass EMSD subset MIDP handover acceptance",
        "canonical_query_zh": "Civil AssetClass与EMSD子集及移交验收",
    },
]


def _parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def main() -> int:
    PLAYBOOK_QUERY_KB_PATH.parent.mkdir(parents=True, exist_ok=True)
    PLAYBOOK_SECTIONS_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    sections: list[dict] = []

    for seed in SEEDS:
        path = PLAYBOOK_CORPUS_DIR / seed["file"]
        meta = _parse_frontmatter(path.read_text(encoding="utf-8")) if path.is_file() else {}
        title = str(meta.get("title", seed["capability"]))
        chapter_id = path.stem
        target_url = playbook_url(chapter_id)
        related = meta.get("related_product_guids") or []
        if not isinstance(related, list):
            related = []
        authority_refs = meta.get("authority_refs") or []
        authority = (
            "; ".join(str(item) for item in authority_refs[:3])
            if isinstance(authority_refs, list)
            else str(authority_refs)
        )
        source_path = (
            str(path.relative_to(PROJECT_ROOT)) if path.is_file() else ""
        )
        domain = str(meta.get("domain", "mixed"))
        rows.append(
            {
                "id": seed["id"],
                "topic": title,
                "aliases": seed["aliases"],
                "canonical_query_en": seed["canonical_query_en"],
                "canonical_query_zh": seed["canonical_query_zh"],
                "target_title": title,
                "target_url": target_url,
                "target_guid": chapter_id,
                "target_section": chapter_id,
                "source_path": source_path,
                "authority": authority,
                "related_product_guids": related,
                "entry_type": "actual_project_spec",
                "status": "approved",
                "capability": seed["capability"],
                "domain": domain,
            }
        )
        sections.append(
            {
                "doc_id": "acc_hk_cde_spec",
                "section_id": chapter_id,
                "title": title,
                "source_url": target_url,
                "source_path": source_path,
                "capability": seed["capability"],
                "domain": domain,
                "priority": "high",
            }
        )

    with PLAYBOOK_QUERY_KB_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    with PLAYBOOK_SECTIONS_INDEX_PATH.open("w", encoding="utf-8") as handle:
        for row in sections:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"写入 {len(rows)} 条路由 -> {PLAYBOOK_QUERY_KB_PATH}")
    print(f"写入 {len(sections)} 条 sections_index -> {PLAYBOOK_SECTIONS_INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
