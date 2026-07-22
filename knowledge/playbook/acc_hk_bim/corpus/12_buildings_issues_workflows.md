---
capability: workflow
domain: buildings
title: "Buildings Issue 与审批工作流"
title_en: "Buildings issues and approval workflows"
source_type: actual_project_spec
source_path: "output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md"
source_version: "2026-07-22"
precedence_rank: 20
supersedes:
  - "knowledge/playbook/acc_hk_bim/research/corpus_legacy_v1/08_project_template.md"
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/ACC_HK_GC_Buildings_Config_Plan.md"
authority_refs:
  - "ACC HK GC Buildings Project Specification"
  - "Real Case naming/BEP"
  - "BD ADM-19/ADV-34"
related_product_guids:
  - "Organize_files_With_Folders"
  - "File_Naming_Standard"
  - "Reviews_Create_Edit"
  - "Reviews_Workflow"
  - "Configure_Templates_Docs"
  - "Folder_Permissions"
disclaimer: "组织推荐/实际项目规格配置，非 CIC/DEVB 官方 ACC 模板；法定与签约 BEP 仍优先。"
---
# Buildings Issue 与审批工作流

> 来源：`output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md` · domain=`buildings` · capability=`workflow`

## 5. 配置明细附录（可直接实施）

### 5.3 Issue 字典（完整）

#### Types 与默认责任

| Type | 默认责任 | 典型触发 |
|------|----------|----------|
| Design Coordination | GC_Engineering | 碰撞、专业冲突 |
| Site Quality | 对应 Subcon / GC_QHSE | 工艺/观感不合格 |
| Site Safety | GC_QHSE | 安全隐患 |
| RFI / Clarification | GC_Engineering | 图纸疑问 |
| Change / Variation | GC_Commercial_QS | 变更影响 |
| Authority Submission | GC_Management | 法定资料缺口 |
| Fit-out Defect | 对应 Subcon | 精装/收尾缺陷 |

#### Categories

`Architecture` / `Structure` / `MEP` / `FA & Plumbing` / `Finishing` / `Subcontract Interface` / `Statutory Submission`

#### Status 可见性（系统状态，不新建底层状态机）

建议保留可见：`Open` → `In Review` → `Action Required` → `Ready to Close` → `Closed`

#### Issue 必填字段规则

| 字段 | 类型 | 必填 | 选项 |
|------|------|------|------|
| IssueOrigin | Select | Y | Site / Design / RFI / Authority |
| IssueTrade | Select | Y | Architecture / Structure / MEP / FA-Plumbing |
| CostImpactLevel | Select | Y | None / Low / Medium / High |
| TimeImpactDays | Number | Y | >=0 |
| RegulatoryImpact | Select | Y | None / BD / Both |
| RequiresEscalation | Boolean | Y | Yes / No |

## 5. 配置明细附录（可直接实施）

### 5.4 Approval Workflows（逐步配置）

统一规则：
- 每节点 SLA：2 工作日
- 超时升级：通知 `GC_Management`
- 驳回：必须填原因
- 通过后：按目标目录归档；禁止覆盖，只允许新版本
- Shared 前必须完成命名合规 + 自检（见 5.10）

#### WF-A：WIP → Shared

| 项 | 值 |
|----|----|
| 触发目录 | `02_Design Coordination/01_WIP/*` |
| 文件类型 | DR / M3 / CM（及模型导出） |
| 门禁 | 命名合规；`SuitabilityStatus` 拟升至 S1–S3；Originator 自检完成 |
| Reviewer1 | GC_Engineering |
| Reviewer2 | Consultant（跨专业时） |
| Approver | GC_Management / BIM Manager |
| 通过动作 | 复制到 `02_SHARED` 对应团队/专业目录；更新联邦模型触发清单 |
| 驳回动作 | 回 WIP，指派原提交人；保留意见 |

#### WF-B：Shared → Published

| 项 | 值 |
|----|----|
| 触发目录 | `02_Design Coordination/02_SHARED/*` |
| 文件类型 | DR / M3 / RP / SUB |
| 门禁 | 当前里程碑 MIDP 项已勾选；无阻断 Open Clash（High） |
| Reviewer1 | GC_Engineering |
| Reviewer2 | GC_Commercial_QS |
| Approver | GC_Management |
| 通过动作 | 发布到 `03_PUBLISHED`；可同步归档到 `03_Buildings Design Packages`；状态改 A* / CP |
| 驳回动作 | 回 Shared，保留意见历史 |

#### WF-C：BD Statutory

| 项 | 值 |
|----|----|
| 触发目录 | `05_Statutory Submission/BD Submission` |
| 文件类型 | SUB / DR（法定） |
| Reviewer1 | GC_Engineering |
| Reviewer2 | Consultant |
| Approver | GC_Management |
| 强制门禁 | `BD Submission Checklist` + `2D/3D Consistency Check` 均 Pass |
| 通过动作 | 锁定版本并归档；状态可用 CP |
| 驳回动作 | 退回并要求升版重提 |

#### WF-D：Handover

| 项 | 值 |
|----|----|
| 触发目录 | `07_Handover & Closeout/*` |
| 文件类型 | RP / M3 / SUB / Asset |
| Reviewer1 | GC_Engineering |
| Reviewer2 | GC_QHSE |
| Approver | GC_Management |
| 门禁 | `Building Handover Checklist` Pass；关键资产 `EMSD_Code` 已填 |
| 通过动作 | 标记 Ready for Handover；状态 CR；开放 Owner 验收 |
| 驳回动作 | 回缺陷清单，自动关联 Site Quality / Fit-out Defect |
