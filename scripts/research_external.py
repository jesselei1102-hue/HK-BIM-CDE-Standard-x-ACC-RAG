"""整理外部行业术语并对齐本地语料 guid。

本脚本使用人工验收的种子术语表，不抓取网页内容入库。
外部来源 URL 仅作审计证据。

用法：
    python scripts/research_external.py
    python scripts/research_external.py --pages-index knowledge/research/pages_index.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 种子术语：来自官方帮助站 ENU/CHT 与中文支持文章归纳，须对齐本地 pages_index。
SEED_GLOSSARY: list[dict] = [
    {
        "term_zh": "文件夹权限",
        "term_en": "folder permissions",
        "aliases": ["设置权限", "权限设置", "資料夾權限"],
        "topic": "permissions",
        "local_target_guid": "Folder_Permissions",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Folder_Permissions",
            "https://help.autodesk.com/cloudhelp/CHT/Docs-Files/",
        ],
        "notes": "Manage Folder Permissions 为 canonical how-to 页",
    },
    {
        "term_zh": "审批",
        "term_en": "approval workflow",
        "aliases": ["审阅", "审批流程", "審閱"],
        "topic": "reviews",
        "local_target_guid": "Reviews_Create_Edit",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit",
            "https://www.autodesk.com.cn/support/",
        ],
        "notes": "Create and Edit Approval Workflows",
    },
    {
        "term_zh": "附函",
        "term_en": "transmittal",
        "aliases": ["传送件", "发送文件", "傳送件"],
        "topic": "transmittals",
        "local_target_guid": "Create_Transmittal",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Create_Transmittal",
            "https://help.autodesk.com/cloudhelp/CHT/Docs-Files/",
        ],
        "notes": "Create Transmittals",
    },
    {
        "term_zh": "支持格式",
        "term_en": "supported files",
        "aliases": ["能打开什么文件", "可查看格式", "文件格式"],
        "topic": "files_formats",
        "local_target_guid": "Supported_Files_Docs",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Supported_Files_Docs",
        ],
        "notes": "Supported Files on Web",
    },
    {
        "term_zh": "文件大小限制",
        "term_en": "file size limit",
        "aliases": ["最大文件", "单个文件多大", "文件大小"],
        "topic": "limitations",
        "local_target_guid": "Product_Limitations",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations",
        ],
        "notes": "Maximum file size: 5 TB",
    },
    {
        "term_zh": "浏览器",
        "term_en": "supported browsers",
        "aliases": ["支持浏览器", "用什么浏览器"],
        "topic": "limitations",
        "local_target_guid": "System_Requirements_ACC",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=System_Requirements_ACC",
        ],
        "notes": "System Requirements",
    },
    {
        "term_zh": "公开链接",
        "term_en": "public link",
        "aliases": ["外部分享", "分享链接"],
        "topic": "sharing",
        "local_target_guid": "Share_files",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Share_files",
            "https://www.autodesk.com.cn/support/",
        ],
        "notes": "Share Files and Folders",
    },
    {
        "term_zh": "标记",
        "term_en": "markups",
        "aliases": ["批注", "标注"],
        "topic": "markups",
        "local_target_guid": "Markups_Files_Docs",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Markups_Files_Docs",
        ],
        "notes": "Markups toolbar",
    },
    {
        "term_zh": "上传文件",
        "term_en": "upload files",
        "aliases": ["上传", "怎么上传"],
        "topic": "upload",
        "local_target_guid": "Upload_files",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Upload_files",
        ],
        "notes": "Upload Files",
    },
    {
        "term_zh": "命名标准",
        "term_en": "naming standards",
        "aliases": ["文件命名", "命名规范"],
        "topic": "naming",
        "local_target_guid": "Product_Limitations",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Product_Limitations",
        ],
        "notes": "命名标准限制在 Product Limitations 页",
    },
    {
        "term_zh": "Desktop Connector",
        "term_en": "desktop connector",
        "aliases": ["桌面连接器", "DC"],
        "topic": "sync",
        "local_target_guid": "Desktop_Connector_Upload_Changes_FAQ",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Desktop_Connector_Upload_Changes_FAQ",
        ],
        "notes": "Desktop Connector 上传与处理",
    },
    {
        "term_zh": "活动日志",
        "term_en": "activity log",
        "aliases": ["审计", "操作记录"],
        "topic": "admin",
        "local_target_guid": "Project_Activity_Log",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Project_Activity_Log",
        ],
        "notes": "Project Activity Log",
    },
    {
        "term_zh": "创建审阅",
        "term_en": "create review",
        "aliases": ["发起审阅", "提交审阅"],
        "topic": "reviews",
        "local_target_guid": "Reviews_Start_Review",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Start_Review",
        ],
        "notes": "Create a Review",
    },
    {
        "term_zh": "BIM 360 Docs",
        "term_en": "BIM 360 Docs",
        "aliases": ["ACC", "Autodesk Construction Cloud"],
        "topic": "general",
        "local_target_guid": "About_Autodesk_Construction_Cloud",
        "external_sources": [
            "https://help.autodesk.com/view/DOCS/ENU/?guid=About_Autodesk_Construction_Cloud",
        ],
        "notes": "历史产品称呼，易出现在用户短句",
    },
]


def load_pages_index(path: Path) -> dict[str, dict]:
    by_guid: dict[str, dict] = {}
    if not path.is_file():
        return by_guid
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            by_guid[row["guid"]] = row
    return by_guid


def guid_to_url(guid: str) -> str:
    return f"https://help.autodesk.com/view/DOCS/ENU/?guid={guid}"


def align_glossary(pages_by_guid: dict[str, dict]) -> list[dict]:
    aligned: list[dict] = []
    for entry in SEED_GLOSSARY:
        guid = entry["local_target_guid"]
        local = pages_by_guid.get(guid)
        row = dict(entry)
        if local:
            row["local_target_url"] = local["source_url"]
            row["local_target_title"] = local["title"]
            row["alignment_status"] = "matched"
            row["evidence"] = local.get("evidence", "")
        else:
            row["local_target_url"] = guid_to_url(guid)
            row["local_target_title"] = ""
            row["alignment_status"] = "out_of_corpus"
            row["evidence"] = ""
        aligned.append(row)
    return aligned


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="导出行业术语表并对齐本地 guid")
    parser.add_argument(
        "--pages-index",
        type=Path,
        default=PROJECT_ROOT / "knowledge" / "research" / "pages_index.jsonl",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "knowledge" / "research" / "industry_glossary.jsonl",
    )
    args = parser.parse_args()

    pages_by_guid = load_pages_index(args.pages_index)
    glossary = align_glossary(pages_by_guid)
    write_jsonl(args.output, glossary)

    matched = sum(1 for row in glossary if row["alignment_status"] == "matched")
    out_of_corpus = len(glossary) - matched
    print(f"行业术语：{len(glossary)} 条 → {args.output}")
    print(f"  已对齐本地页：{matched}")
    print(f"  out_of_corpus：{out_of_corpus}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
