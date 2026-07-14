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
        "id": "pb_overview",
        "capability": "overview_alignment",
        "file": "00_overview_alignment.md",
        "aliases": ["对齐表", "总览", "标准概念映射", "playbook overview"],
        "canonical_query_en": "ACC HK BIM playbook overview alignment table",
        "canonical_query_zh": "ACC与港标总览对齐表有哪些映射与缺口",
    },
    {
        "id": "pb_project",
        "capability": "project_setup",
        "file": "01_project_setup.md",
        "aliases": ["项目配置", "账户配置", "角色模板", "创建ACC项目"],
        "canonical_query_en": "ACC account project setup roles recommended for HK BIM",
        "canonical_query_zh": "按港标推荐如何配置ACC账户与项目角色",
    },
    {
        "id": "pb_folder",
        "capability": "folder_cde",
        "file": "02_folder_cde.md",
        "aliases": ["文件夹结构", "CDE容器", "WIP Shared Published", "目录结构"],
        "canonical_query_en": "ACC Docs folder structure CDE containers WIP Shared Published",
        "canonical_query_zh": "按港标在ACC配置WIP Shared Published文件夹结构",
    },
    {
        "id": "pb_naming",
        "capability": "naming",
        "file": "03_naming.md",
        "aliases": ["命名规范", "Information Container ID", "Naming Standard"],
        "canonical_query_en": "ACC naming standard CICBIMS DEVB container ID",
        "canonical_query_zh": "按CICBIMS或DEVB在Docs配置命名标准",
    },
    {
        "id": "pb_permissions",
        "capability": "permissions",
        "file": "04_permissions.md",
        "aliases": ["权限矩阵", "文件夹权限", "WIP隔离"],
        "canonical_query_en": "ACC folder permissions matrix for CDE WIP Shared",
        "canonical_query_zh": "港标CDE在ACC的文件夹权限矩阵怎么配",
    },
    {
        "id": "pb_workflow",
        "capability": "workflow",
        "file": "05_workflow.md",
        "aliases": ["审批工作流", "Information Gateway", "迁夹", "Status Code"],
        "canonical_query_en": "ACC approval workflow information gateway move folder gap",
        "canonical_query_zh": "按ISO网关在ACC配置审批流及人工迁夹缺口",
    },
    {
        "id": "pb_design",
        "capability": "design_collab",
        "file": "06_design_collab.md",
        "aliases": ["设计协同", "Model Coordination", "Publish Consume"],
        "canonical_query_en": "Design Collaboration Model Coordination HK BIM playbook",
        "canonical_query_zh": "设计协同与模型协调按港标怎么配",
    },
    {
        "id": "pb_info_req",
        "capability": "information_requirements",
        "file": "07_information_requirements.md",
        "aliases": ["OIR", "AIR", "PIR", "EIR", "信息要求落地"],
        "canonical_query_en": "OIR AIR PIR EIR implementation in ACC playbook",
        "canonical_query_zh": "OIR PIR EIR在ACC中如何落地执行",
    },
    {
        "id": "pb_project_template",
        "capability": "project_template",
        "file": "08_project_template.md",
        "aliases": [
            "项目样板",
            "项目模板",
            "Project Template",
            "GC模板",
            "总包模板",
            "Buildings模板",
            "ACC HK GC",
        ],
        "canonical_query_en": (
            "ACC HK GC Buildings project template folder permissions "
            "naming workflows forms"
        ),
        "canonical_query_zh": "香港总包ACC项目样板怎么配置文件夹权限命名和审批",
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
                "entry_type": "playbook_recommended",
                "status": "approved",
                "capability": seed["capability"],
            }
        )
        sections.append(
            {
                "doc_id": "acc_hk_bim_playbook",
                "section_id": chapter_id,
                "title": title,
                "source_url": target_url,
                "source_path": source_path,
                "capability": seed["capability"],
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
