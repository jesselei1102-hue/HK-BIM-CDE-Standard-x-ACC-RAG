---
capability: workflow
domain: civil
title: "Civil Issue 与审批工作流"
title_en: "Civil issues and approval workflows"
source_type: actual_project_spec
source_path: "output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md"
source_version: "2026-07-22"
precedence_rank: 20
supersedes:
  - "knowledge/playbook/acc_hk_bim/research/corpus_legacy_v1/08_project_template.md"
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/ACC_HK_GC_Buildings_Config_Plan.md"
authority_refs:
  - "ACC HK GC Civil Project Specification"
  - "DEVB Appendix XIV"
  - "LandsD BIM/GIS"
related_product_guids:
  - "Organize_files_With_Folders"
  - "File_Naming_Standard"
  - "Reviews_Create_Edit"
  - "Reviews_Workflow"
  - "Configure_Templates_Docs"
  - "Folder_Permissions"
disclaimer: "组织推荐/实际项目规格配置，非 CIC/DEVB 官方 ACC 模板；法定与签约 BEP 仍优先。"
---
# Civil Issue 与审批工作流

> 来源：`output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md` · domain=`civil` · capability=`workflow`

## 5. 配置明细附录（可直接实施）

### 5.3 Issue 字典（完整）

| Type | 默认责任 | 典型触发 |
|------|----------|----------|
| Design Coordination | GC_Engineering | 设计冲突 |
| Site Quality | Subcon / GC_QHSE | 质量偏差 |
| Site Safety | GC_QHSE | 安全隐患 |
| Underground Utilities | GC_Engineering / Consultant | 管线冲突 |
| Traffic Management | GC_QHSE / Subcon | 导改不合规 |
| Temporary Works | GC_Engineering / Subcon | 临建风险 |
| RFI / Clarification | GC_Engineering | 澄清请求 |
| Change / Variation | GC_Commercial_QS | 变更 |
| Authority Submission | GC_Management | 提交缺件 |

Categories：
`Roads & Drainage` / `Structures & Civil` / `Geotechnical` / `M&E & Traffic` / `Subcontract Interface` / `Statutory Submission` / `Progress Risk`

Status 可见性：
`Open` → `In Review` → `Action Required` → `Ready to Close` → `Closed`

Issue 字段：

| 字段 | 类型 | 必填 | 选项 |
|------|------|------|------|
| IssueOrigin | Select | Y | Site / Design / RFI / Authority |
| IssueTrade | Select | Y | Roads-Drainage / Structures-Civil / Geotech / ME-Traffic |
| Section | Text/Select | Y | 项目区段码 |
| ContractPackage | Text/Select | Y | 合约包编码 |
| CostImpactLevel | Select | Y | None / Low / Medium / High |
| TimeImpactDays | Number | Y | >=0 |
| RegulatoryImpact | Select | Y | None / LandsD / Both |
| RequiresEscalation | Boolean | Y | Yes / No |

## 5. 配置明细附录（可直接实施）

### 5.4 Approval Workflows（逐步）

统一规则：SLA 2 工作日；超时升级 GC_Management；驳回必填原因；通过后禁止覆盖；Shared 前完成命名合规 + 自检（5.10）。

#### WF-A WIP → Shared
- 目录：`02/.../01_WIP/*`
- 文件：DR / M3 / CM
- 门禁：命名九段合规；拟升 S1–S3；自检完成
- Reviewers：GC_Engineering、Consultant
- Approver：GC_Management / BIM Manager
- 通过：进入 `02_SHARED` 对应专业目录；触发联邦更新清单

#### WF-B Shared → Published
- 目录：`02/.../02_SHARED/*`
- 文件：DR / M3 / RP / SUB
- 门禁：当前里程碑 MIDP 齐备；无阻断 High Clash
- Reviewers：GC_Engineering、GC_Commercial_QS
- Approver：GC_Management
- 通过：`03_PUBLISHED`，并可归档到 `03/By Section`；状态 A* / CP

#### WF-C LandsD / Works Submission
- 目录：`05_Statutory Submission/LandsD Submission`
- 文件：SUB / DR
- Reviewers：GC_Engineering、Consultant
- Approver：GC_Management
- 强制门禁：
  - `LandsD Completeness Check` = Pass
  - `PROJECT_BOUNDARY` 存在
  - `MODEL_FILE_LIST` 存在
  - 至少一种主 BIM 格式（native 或 openBIM）
- 通过：锁定版本；状态可用 CP
- 驳回：升版重提

#### WF-D Handover
- 目录：`07_Handover & Closeout/*`
- Reviewers：GC_Engineering、GC_QHSE
- Approver：GC_Management
- 门禁：`Civil Handover Checklist` Pass；适用资产已填 `EMSD_Code` 或 `AssetClass`
- 通过：Ready for Handover；状态 CR
- 驳回：回缺陷清单并关联 Issue
