"""从已验收种子条目生成 knowledge/query_kb.jsonl。

用法：
    python scripts/build_query_kb.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PAGES_INDEX = PROJECT_ROOT / "knowledge" / "research" / "pages_index.jsonl"
OUTPUT = PROJECT_ROOT / "knowledge" / "query_kb.jsonl"

# 人工验收种子：aliases + canonical + target_guid
APPROVED_SEEDS: list[dict] = [
    {
        "id": "folder_permissions_set",
        "topic": "permissions",
        "aliases": ["文件夹权限", "设置权限", "权限设置", "folder permissions"],
        "canonical_query_zh": "如何设置文件夹权限",
        "canonical_query_en": "How do I set folder permissions",
        "target_guid": "Folder_Permissions",
        "entry_type": "how_to",
        "external_sources": ["https://help.autodesk.com/cloudhelp/CHT/Docs-Files/"],
    },
    {
        "id": "approval_workflow_config",
        "topic": "reviews",
        "aliases": ["审批", "审阅", "审批流程", "approval workflow", "workflow"],
        "canonical_query_zh": "如何创建和编辑审批工作流",
        "canonical_query_en": "How do I create and edit approval workflows",
        "target_guid": "Reviews_Create_Edit",
        "entry_type": "how_to",
        "external_sources": ["https://www.autodesk.com.cn/support/"],
    },
    {
        "id": "create_review",
        "topic": "reviews",
        "aliases": ["创建审阅", "发起审阅", "提交审阅", "create review"],
        "canonical_query_zh": "如何创建审阅",
        "canonical_query_en": "How do I create a review",
        "target_guid": "Reviews_Start_Review",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "review_approve_files",
        "topic": "reviews",
        "aliases": ["审批文件", "审阅文件", "approve files"],
        "canonical_query_zh": "如何审阅和批准文件",
        "canonical_query_en": "How do I review and approve files",
        "target_guid": "Reviews_Review_and_Approve",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "submit_for_review",
        "topic": "reviews",
        "aliases": ["送审", "提交审批", "submit review"],
        "canonical_query_zh": "如何从文件工具提交审阅",
        "canonical_query_en": "How do I submit files for review",
        "target_guid": "Reviews_Files",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "export_reviews_report",
        "topic": "reviews",
        "aliases": ["审阅报告", "导出审阅", "reviews report"],
        "canonical_query_zh": "如何导出审阅报告",
        "canonical_query_en": "How do I export reviews report",
        "target_guid": "Reviews_Report",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "create_transmittal",
        "topic": "transmittals",
        "aliases": ["附函", "传送件", "transmittal", "发送文件", "创建transmittal"],
        "canonical_query_zh": "如何创建传送件",
        "canonical_query_en": "How do I create a transmittal in Docs",
        "target_guid": "Create_Transmittal",
        "entry_type": "how_to",
        "external_sources": ["https://help.autodesk.com/cloudhelp/CHT/Docs-Files/"],
    },
    {
        "id": "supported_files",
        "topic": "files_formats",
        "aliases": ["支持格式", "能打开什么", "可查看格式", "supported files", "viewable files"],
        "canonical_query_zh": "Web 端支持哪些文件格式",
        "canonical_query_en": "What file formats are supported on web",
        "target_guid": "Supported_Files_Docs",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "file_size_limit",
        "topic": "limitations",
        "aliases": ["文件大小", "最大文件", "单个文件多大", "file size", "5TB"],
        "canonical_query_zh": "单个文件最大可以多大",
        "canonical_query_en": "What is the maximum file size",
        "target_guid": "Product_Limitations",
        "entry_type": "limitations",
        "external_sources": [],
    },
    {
        "id": "product_limitations",
        "topic": "limitations",
        "aliases": ["产品限制", "工具限制", "limitations"],
        "canonical_query_zh": "产品和工具有哪些限制",
        "canonical_query_en": "What are product and tool limitations",
        "target_guid": "Product_Limitations",
        "entry_type": "limitations",
        "external_sources": [],
    },
    {
        "id": "supported_browsers",
        "topic": "limitations",
        "aliases": ["支持浏览器", "浏览器", "browsers", "browser support"],
        "canonical_query_zh": "支持哪些浏览器",
        "canonical_query_en": "What browsers are supported for Autodesk Construction Cloud",
        "target_guid": "System_Requirements_ACC",
        "entry_type": "limitations",
        "external_sources": [],
    },
    {
        "id": "system_requirements",
        "topic": "limitations",
        "aliases": ["系统要求", "system requirements"],
        "canonical_query_zh": "系统要求是什么",
        "canonical_query_en": "What are the system requirements",
        "target_guid": "System_Requirements_ACC",
        "entry_type": "overview",
        "external_sources": [],
    },
    {
        "id": "share_files",
        "topic": "sharing",
        "aliases": ["公开链接", "外部分享", "分享文件", "share files", "public link"],
        "canonical_query_zh": "如何分享文件和文件夹",
        "canonical_query_en": "How do I share files and folders",
        "target_guid": "Share_files",
        "entry_type": "how_to",
        "external_sources": ["https://www.autodesk.com.cn/support/"],
    },
    {
        "id": "share_with_members",
        "topic": "sharing",
        "aliases": ["分享给成员", "项目成员分享"],
        "canonical_query_zh": "如何与项目成员分享文件",
        "canonical_query_en": "How do I share files with project members",
        "target_guid": "Share_Files_Project_Members",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "markups",
        "topic": "markups",
        "aliases": ["标记", "批注", "标注", "markups", "markup"],
        "canonical_query_zh": "Docs 文件工具有哪些标记功能",
        "canonical_query_en": "What are markups in the Files tool",
        "target_guid": "Markups_Files_Docs",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "markups_mobile",
        "topic": "markups",
        "aliases": ["手机标记", "移动端批注"],
        "canonical_query_zh": "如何在移动端使用标记",
        "canonical_query_en": "How do I use markups on mobile",
        "target_guid": "Markups_Mobile_Files_Docs",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "upload_files",
        "topic": "upload",
        "aliases": ["上传", "上传文件", "upload", "upload files"],
        "canonical_query_zh": "如何在 Files 工具上传文件",
        "canonical_query_en": "How do I upload files in the Files tool",
        "target_guid": "Upload_files",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "upload_linked_files",
        "topic": "upload",
        "aliases": ["链接文件", "参照上传", "linked files"],
        "canonical_query_zh": "如何上传链接文件",
        "canonical_query_en": "How do I upload linked files",
        "target_guid": "Upload_Linked_Files_Files_Tool",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "upload_mobile",
        "topic": "upload",
        "aliases": ["手机上传", "移动端上传"],
        "canonical_query_zh": "如何在移动端上传文件",
        "canonical_query_en": "How do I upload files on mobile",
        "target_guid": "Upload_Files_Mobile",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "view_files_web",
        "topic": "files_formats",
        "aliases": ["查看文件", "打开文件", "view files"],
        "canonical_query_zh": "如何在 Web 上查看文件",
        "canonical_query_en": "How do I view files on web",
        "target_guid": "View_Files",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "activity_log",
        "topic": "admin",
        "aliases": ["活动日志", "操作记录", "审计", "activity log"],
        "canonical_query_zh": "如何访问项目活动日志",
        "canonical_query_en": "How do I access the project activity log",
        "target_guid": "Project_Activity_Log",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "desktop_connector",
        "topic": "sync",
        "aliases": ["Desktop Connector", "桌面连接器", "DC"],
        "canonical_query_zh": "Desktop Connector 上传有什么变化",
        "canonical_query_en": "What changed for Desktop Connector uploads",
        "target_guid": "Desktop_Connector_Upload_Changes_FAQ",
        "entry_type": "reference",
        "external_sources": [],
    },
    {
        "id": "background_sync",
        "topic": "sync",
        "aliases": ["后台同步", "background sync"],
        "canonical_query_zh": "什么是后台同步",
        "canonical_query_en": "What is background sync",
        "target_guid": "Mobile_Background_Sync",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "in_project_sync",
        "topic": "sync",
        "aliases": ["项目内同步", "in-project sync"],
        "canonical_query_zh": "什么是项目内同步",
        "canonical_query_en": "What is in-project sync",
        "target_guid": "Mobile_In_Project_Sync",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "file_folder_actions",
        "topic": "files_formats",
        "aliases": ["文件操作", "文件夹操作", "file actions"],
        "canonical_query_zh": "文件和文件夹有哪些操作",
        "canonical_query_en": "What file and folder actions are available",
        "target_guid": "File_Folder_Actions_Docs",
        "entry_type": "reference",
        "external_sources": [],
    },
    {
        "id": "naming_standards_limit",
        "topic": "naming",
        "aliases": ["命名标准", "命名规范", "naming standards"],
        "canonical_query_zh": "如何创建命名标准",
        "canonical_query_en": "How do I create naming standards",
        "target_guid": "Set_Up_Naming_Standard",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "about_acc",
        "topic": "general",
        "aliases": ["ACC", "Autodesk Construction Cloud", "BIM 360 Docs"],
        "canonical_query_zh": "什么是 Autodesk Construction Cloud",
        "canonical_query_en": "What is Autodesk Construction Cloud",
        "target_guid": "About_Autodesk_Construction_Cloud",
        "entry_type": "overview",
        "external_sources": [],
    },
    {
        "id": "create_issues",
        "topic": "issues",
        "aliases": ["创建问题", "issue", "issues"],
        "canonical_query_zh": "如何创建问题",
        "canonical_query_en": "How do I create issues",
        "target_guid": "Issues_Create",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "issues_viewer",
        "topic": "issues",
        "aliases": ["查看器问题", "viewer issues"],
        "canonical_query_zh": "如何在查看器中处理问题",
        "canonical_query_en": "How do I work with issues in the viewer",
        "target_guid": "Work_with_Issues_in_Viewer",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "data_connector",
        "topic": "insight",
        "aliases": ["数据连接器", "data connector"],
        "canonical_query_zh": "什么是 Data Connector",
        "canonical_query_en": "What is Data Connector",
        "target_guid": "Data_Connector",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "handover_package",
        "topic": "packages",
        "aliases": ["移交包", "handover", "竣工包"],
        "canonical_query_zh": "如何组装移交包",
        "canonical_query_en": "How do I assemble handover package",
        "target_guid": "Handover_Assemble_Package",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "export_handover",
        "topic": "packages",
        "aliases": ["导出移交", "export handover"],
        "canonical_query_zh": "如何导出移交包",
        "canonical_query_en": "How do I export handover package",
        "target_guid": "Handover_Export",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "about_bridge",
        "topic": "sharing",
        "aliases": ["Bridge", "桥接", "跨项目"],
        "canonical_query_zh": "什么是 Bridge",
        "canonical_query_en": "What is Bridge",
        "target_guid": "About_Bridge",
        "entry_type": "overview",
        "external_sources": [],
    },
    {
        "id": "bridge_share",
        "topic": "sharing",
        "aliases": ["跨项目分享", "bridge share"],
        "canonical_query_zh": "如何通过 Bridge 分享到其他项目",
        "canonical_query_en": "How do I share with another project from Bridge",
        "target_guid": "Share_From_Outgoing",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "saved_searches",
        "topic": "files_formats",
        "aliases": ["保存搜索", "saved search"],
        "canonical_query_zh": "如何分享保存的搜索",
        "canonical_query_en": "How do I share saved searches",
        "target_guid": "Share_Saved_Searches_Files",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "model_browser",
        "topic": "files_formats",
        "aliases": ["模型浏览器", "model browser"],
        "canonical_query_zh": "如何使用模型浏览器",
        "canonical_query_en": "How do I use model browser",
        "target_guid": "Model_Browser",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "sso_directory_sync",
        "topic": "admin",
        "aliases": ["单点登录", "SSO", "目录同步"],
        "canonical_query_zh": "单点登录和目录同步支持什么",
        "canonical_query_en": "What does SSO and directory sync support",
        "target_guid": "ACC_SSO_Directory_Sync",
        "entry_type": "reference",
        "external_sources": [],
    },
    {
        "id": "activities_tracked",
        "topic": "admin",
        "aliases": ["跟踪活动", "tracked activities"],
        "canonical_query_zh": "活动日志跟踪哪些活动",
        "canonical_query_en": "What activities are tracked in activity log",
        "target_guid": "Activities_Tracked_in_Activity_Log",
        "entry_type": "reference",
        "external_sources": [],
    },
    {
        "id": "bridge_activity_log",
        "topic": "admin",
        "aliases": ["桥接日志", "bridge activity"],
        "canonical_query_zh": "如何查看桥接项目活动日志",
        "canonical_query_en": "How do I view bridged project activity log",
        "target_guid": "Bridge_Activity_Log",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "insight_reports",
        "topic": "insight",
        "aliases": ["Insight报告", "insight reports"],
        "canonical_query_zh": "Insight 中的报告功能",
        "canonical_query_en": "What are reports in Insight",
        "target_guid": "Reports_Insight",
        "entry_type": "overview",
        "external_sources": [],
    },
    {
        "id": "shared_dashboards",
        "topic": "insight",
        "aliases": ["共享仪表板", "dashboard"],
        "canonical_query_zh": "如何共享仪表板",
        "canonical_query_en": "How do I use shared dashboards",
        "target_guid": "Shared_Dashboards",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "sync_troubleshooting",
        "topic": "sync",
        "aliases": ["同步故障", "sync error"],
        "canonical_query_zh": "项目内同步故障排除",
        "canonical_query_en": "How do I troubleshoot in-project sync",
        "target_guid": "Mobile_In_Project_Sync_Troubleshooting",
        "entry_type": "reference",
        "external_sources": [],
    },
    {
        "id": "bridge_troubleshooting",
        "topic": "sharing",
        "aliases": ["Bridge故障", "bridge error"],
        "canonical_query_zh": "Bridge 分享故障排除",
        "canonical_query_en": "How do I troubleshoot sharing with Bridge",
        "target_guid": "Bridge_Troubleshooting",
        "entry_type": "reference",
        "external_sources": [],
    },
    {
        "id": "folder_permission_levels",
        "topic": "permissions",
        "aliases": ["权限级别", "permission levels"],
        "canonical_query_zh": "文件夹权限级别有哪些",
        "canonical_query_en": "What are folder permission levels",
        "target_guid": "Folder_Permissions",
        "entry_type": "how_to",
        "external_sources": [],
    },
    {
        "id": "transmittal_settings",
        "topic": "transmittals",
        "aliases": ["传送件设置", "transmittal settings"],
        "canonical_query_zh": "传送件设置有哪些",
        "canonical_query_en": "What are transmittal settings",
        "target_guid": "Create_Transmittal",
        "entry_type": "how_to",
        "external_sources": [],
    },
]


def load_pages() -> dict[str, dict]:
    by_guid: dict[str, dict] = {}
    if not PAGES_INDEX.is_file():
        return by_guid
    with PAGES_INDEX.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                row = json.loads(line)
                by_guid[row["guid"]] = row
    return by_guid


def main() -> int:
    pages = load_pages()
    rows: list[dict] = []
    skipped = 0
    for seed in APPROVED_SEEDS:
        guid = seed["target_guid"]
        page = pages.get(guid)
        if page:
            target_url = page["source_url"]
            target_title = page["title"]
            evidence = page.get("evidence", "")
        else:
            target_url = f"https://help.autodesk.com/view/DOCS/ENU/?guid={guid}"
            target_title = seed.get("target_title", guid)
            evidence = ""
            skipped += 1
        rows.append(
            {
                "id": seed["id"],
                "topic": seed["topic"],
                "aliases": seed["aliases"],
                "canonical_query_zh": seed["canonical_query_zh"],
                "canonical_query_en": seed["canonical_query_en"],
                "target_title": target_title,
                "target_url": target_url,
                "target_guid": guid,
                "entry_type": seed["entry_type"],
                "evidence": evidence,
                "external_sources": seed.get("external_sources", []),
                "status": "approved",
            }
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"已验收 KB 条目：{len(rows)} 条 → {OUTPUT}")
    if skipped:
        print(f"  警告：{skipped} 条未在 pages_index 中找到（仍使用 guid URL）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
