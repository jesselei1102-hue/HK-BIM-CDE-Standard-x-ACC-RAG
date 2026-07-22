---
capability: project_template
domain: mixed
title: "HK CDE Spec 项目规格索引（Buildings / Civil）"
title_en: "HK CDE Spec project specification index (Buildings / Civil)"
source_type: actual_project_spec
source_path: "output/HK CDE Spec/"
source_version: "2026-07-22"
precedence_rank: 20
supersedes:
  - "knowledge/playbook/acc_hk_bim/research/corpus_legacy_v1/08_project_template.md"
  - "knowledge/playbook/acc_hk_bim/research/corpus_legacy_v1/00_overview_alignment.md"
authority_refs:
  - "ACC HK GC Buildings Project Specification"
  - "ACC HK GC Civil Project Specification"
related_product_guids:
  - "Configure_Templates_Docs"
  - "Organize_files_With_Folders"
  - "File_Naming_Standard"
  - "Reviews_Workflow"
disclaimer: "组织推荐/实际项目规格配置，非 CIC/DEVB 官方 ACC 模板；法定与签约 BEP 仍优先。"
---

# HK CDE Spec 项目规格索引（Buildings / Civil）

> 主动 Playbook 语料已切换为 **HK CDE Spec** 两份实际项目说明书。旧 `00–08` 章节归档至 `research/corpus_legacy_v1/`，检索时不再入库。

## 1. 如何选用 Buildings 或 Civil

| 项目类型 | 选用规格 | 法定路径重点 | 命名差异 |
|----------|----------|--------------|----------|
| 楼宇 / Buildings（住宅、办公、商业等） | `10–15_buildings_*` | BD Submission + 2D/3D Consistency | Building = 楼栋码 |
| 土木 / Civil / Infrastructure | `20–25_civil_*` | LandsD Submission（边界 + 模型清单） | Building = 区段码（SEC*），另填 Section / Chainage / ContractPackage |

产品范围（两者相同）：

- 必选：Forma Data Management（原 Autodesk Docs）
- 建议：Forma Build
- 按需：Forma Design Collaboration（Shared folder 一旦指定不可更改）

## 2. 章节地图（Trunk）

| Capability | Buildings | Civil |
|------------|-----------|-------|
| 角色 / RACI / 日常操作 | `10_buildings_overview_roles` | `20_civil_overview_roles` |
| 文件夹 + 权限矩阵 | `11_buildings_folders_permissions` | `21_civil_folders_permissions` |
| Issue + WF-A/B/C/D | `12_buildings_issues_workflows` | `22_civil_issues_workflows` |
| 九段命名 + 字段 | `13_buildings_naming_fields` | `23_civil_naming_fields` |
| Forms + 法定包 + 配置顺序 | `14_buildings_forms_statutory` | `24_civil_forms_statutory` |
| 协同节奏 / EMSD·AssetClass / MIDP / 验收 | `15_buildings_assets_midp_acceptance` | `25_civil_assets_midp_acceptance` |

## 3. 与旧 Playbook 的关键差异（必须以新为准）

1. **命名**：九段 Real Case；Revision / SuitabilityStatus **不进文件名**。旧短格式 `PRJ001-A-DRW-000123-V02` 视为错误示例。
2. **目录**：`02_Design Coordination` 内使用编号 `01_WIP / 02_SHARED / 03_PUBLISHED / 04_ARCHIVE`；WIP 按 **Team_***，Shared 含 `8_BIM` 联邦子树。
3. **Civil 完整规格**：LandsD 增强目录、区段字段、交通/临时工程 Issue、土木 `AssetClass`。
4. **门禁**：WF-B 依赖 MIDP；Buildings WF-C 依赖 BD 两张强制表；Civil WF-C 依赖 LandsD 完整性 + `PROJECT_BOUNDARY` + `MODEL_FILE_LIST`。

## 4. 推荐配置一页（两端共性）

| 模块 | 必须落地 |
|------|----------|
| Folder | 01–08 业务树 + 编号 CDE 状态夹 |
| Permission | Owner 不可见 WIP；Published / 法定写权限收敛 |
| Workflow | WF-A/B/C/D（自检 + 法定门禁） |
| Naming | 九段；属性承载 Revision / Status |
| Forms | Buildings 8 张 / Civil 9 张最小表单 |
| Asset | Buildings：EMSD；Civil：EMSD 子集 + AssetClass |
| Cadence | 建议每 2–3 周 Shared 冻结；周协调会 |
