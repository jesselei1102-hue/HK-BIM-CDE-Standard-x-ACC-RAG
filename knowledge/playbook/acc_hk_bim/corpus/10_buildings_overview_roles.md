---
capability: roles
domain: buildings
title: "Buildings 总览与角色操作"
title_en: "Buildings overview and role operations"
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
# Buildings 总览与角色操作

> 来源：`output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md` · domain=`buildings` · capability=`roles`

## 0. 总览

### 0.1 目标

在 Autodesk Forma / Construction Cloud（原 ACC）中建立 Buildings 项目统一规则，覆盖：
- Forma Data Management 资料夹与权限（按 CDE 状态 + 团队组织）
- Issue / Reviews / Forms
- ISO19650 风格命名、适用性状态（S0–S4/A/CP/CR）与字段
- EMSD 资产分类（移交/Tandem）
- BD 法定提交流程口径
- 角色日常操作、协同节奏与验收标准

### 0.2 适用范围与产品

- 项目类型：Buildings（住宅/办公/商业等；可选扩展按项目启用）
- 必选产品：Forma Data Management（原 Autodesk Docs）
- 建议产品：Forma Build（原 Autodesk Build）
- 按需产品：Forma Design Collaboration（原 Design Collaboration）、Takeoff、Cost

> 产品更名说明（2025+ Autodesk rebrand）：配置界面若仍短暂显示旧名，以本说明书新名为准；能力与配置路径对应不变。

> 实施建议：若启用 Forma Design Collaboration，Shared folder 一旦指定不可更改；先建好 `02_Design Coordination/02_SHARED` 再配置。

### 0.3 如何使用本文

1. 先读第 0 章总览与角色矩阵  
2. 按自己角色读第 1–4 章（操作手册）  
3. 实施配置时直接用第 5 章附录明细（无需另找附录包）  
4. 用第 6 章验收清单勾选

### 0.4 角色责任矩阵（RACI）

R=Responsible 主责，A=Accountable 终责，C=Consulted 协商，I=Informed 知会

| 事项 | Owner | GC | Consultant | Subcon |
|------|-------|----|------------|--------|
| 信息要求（EIR/PIR）确认 | A | R | C | I |
| 模板/项目配置落地 | I | A/R | C | I |
| Folder 与权限维护 | I | A/R | C | I |
| 设计协同（WIP/Shared） | I | A | R | C |
| 正式发布（Published） | I | A/R | C | I |
| BD 法定提交包 | I | A/R | C | I |
| 现场质量/安全 Issue | I | A | C | R |
| Fit-out 缺陷闭环 | I | A | C | R |
| 移交验收 | A | R | C | C |

### 0.5 配置总览（一页）

| 模块 | 必须落地内容 |
|------|--------------|
| Folder | 01–08 主结构；`02` 按 `01_WIP→02_SHARED→03_PUBLISHED→04_ARCHIVE`，Shared 下按团队 + BIM 子树 |
| Permission | 按角色最小授权；Owner 不可见 WIP；Published/Statutory 写权限收敛 |
| Issue | 7 Types + 7 Categories + 状态可见性 |
| Workflow | WF-A/B/C/D（含自检门禁 + BD 门禁） |
| Naming | `Project-Originator-Building-Zone-Level-Type-Role-System-Number`（修订/状态进属性，不进文件名） |
| Status | SuitabilityStatus：`S0/S1/S2/S3/S4/A3–A6/CP/CR` |
| Fields | Forma Data Management 命名字段 + 流程字段 + `EMSD_Code`；Issue 字段 6 项 |
| Asset | EMSD AIR L1/L2（见 5.11）；Naming `System` ≠ EMSD 资产码 |
| Forms | 8 张最小表单（含 BD/一致性/MIDP/移交） |
| Cadence | 建议每 2–3 周 Shared 冻结一次；周协调会 |

---

## 1. Owner 角色操作手册

### 1.1 职责边界

- 定义并确认信息要求、移交标准
- 接收正式发布与移交包
- 监督合规结果（不替代 BD 法定审批）
- 对关键变更与移交给出业主确认

### 1.2 目录权限（应看到什么）

| 目录 | 权限 | 说明 |
|------|------|------|
| `01_Project Governance` | View | 合约、程序、会议纪要 |
| `02/.../01_WIP` | No Access | 过程稿不对 Owner 开放 |
| `02/.../02_SHARED` | View | 可看协同稿 |
| `02/.../03_PUBLISHED` | View | 正式发布成果 |
| `03_Buildings Design Packages` | View | 正式专业包 |
| `05_Statutory Submission` | View | 法定包只读 |
| `07_Handover & Closeout` | View | 移交包验收 |
| `08_Reference & Standards` | View | EIR/规范参考 |

### 1.3 可发起 / 可确认事项

- 可发起 Issue：`RFI / Clarification`、移交验收意见
- 可确认：Published 成果是否接受、Handover 是否通过、关键变更是否接受
- 不建议担任日常文件发布 Approver（默认 GC_Management）

### 1.4 必须关注的字段与表单

字段：`DeliverableStage`、`SuitabilityStatus`、`SubmissionType`、`StatutoryRelated`、`Revision`、`EMSD_Code`（移交时）  
表单：`EIR Clause Check`、`MIDP Delivery Check`、`Building Handover Checklist`、`Project Close-out Checklist`

### 1.5 日常流程（逐步）

**A. 开项（Day 0–3）**
1. 确认 EIR / 移交标准已放入 `08_Reference & Standards`
2. 确认角色矩阵与验收口径已写入项目程序
3. 抽查 Folder 是否按第 5.1 建立

**B. 设计阶段**
1. 只查看 Shared/Published，不干预 WIP
2. 对正式发布结果提出接受/不接受意见
3. 重大设计风险通过 Issue 留痕

**C. 法定提交节点**
1. 查看 `05_Statutory Submission/BD Submission`
2. 确认 `BD Submission Checklist` 与 `2D/3D Consistency Check` 已完成
3. 确认版本号与 `StatutoryRefNo` 可追溯

**D. 移交**
1. 按 `Building Handover Checklist` 逐项验收
2. 未关闭缺陷不得签字接收
3. 确认 Close-out 表单完成

### 1.6 Owner 验收关注点

- [ ] 看不到 WIP（权限隔离正确）
- [ ] Published / Handover 可追溯审批记录
- [ ] BD 包有检查表与版本
- [ ] 缺陷关闭有证据

---

## 2. GC 角色操作手册

### 2.1 职责边界

GC 是执行主责方，负责：
- 配置落地与持续维护
- 权限与审批推进
- 交付包整合
- BD 法定提交统筹

建议内部角色映射：
- `GC_Management`：终批、发布、法定统筹
- `GC_Engineering`：技术协同与复核
- `GC_Commercial_QS`：变更与商务复核
- `GC_QHSE`：质量安全与移交质量

### 2.2 目录权限（应配置并自用）

| 目录 | GC_Management | GC_Engineering | GC_Commercial_QS | GC_QHSE |
|------|---------------|----------------|------------------|---------|
| WIP | V | V/U/E/D | V | V |
| Shared | V/E | V/U/E | V | V |
| Published | V/U/E | V | V | V |
| Statutory | V/U/E | V/U | V | V |
| Handover | V/U/E | V/U | V | V/U |
| Construction | V | V/U/E | V | V/U/E |

### 2.3 可发起 / 可审批事项

- 可发起：全部 Issue Types
- Approver（默认）：`GC_Management`（WF-A/B/C/D）
- Reviewer：
  - WF-A/C：`GC_Engineering`
  - WF-B：`GC_Engineering` + `GC_Commercial_QS`
  - WF-D：`GC_Engineering` + `GC_QHSE`

### 2.4 必须填写/维护的字段与表单

Forma Data Management 必填（提审前）：
- 命名九段属性：`Project` / `Originator` / `Building` / `Zone` / `Level` / `Type` / `Role` / `System` / `Number`
- `SuitabilityStatus`、`Revision`、`SubmissionType`、`DeliverableStage`、`RequiresApproval`、`ApprovalWorkflowId`
- 法定包另填：`StatutoryRelated=Yes`、`StatutoryRefNo`、`SoftwareVersion`
- 移交资产：`EMSD_Code`

Issue 必填：
- `IssueOrigin`、`IssueTrade`、`CostImpactLevel`、`TimeImpactDays`、`RegulatoryImpact`

Forms 主责：
- 全部 8 张最小表单（见 5.7）

### 2.5 日常流程（逐步）

**A. 配置落地（开项前）**
1. 建齐第 5.1 目录（含团队 WIP + Shared BIM 子树）
2. 放入 EMSD 与 Project Codes（5.11 / 08）
3. 按第 5.2 配权限
4. 配命名规则（5.5）与字段（5.6）
5. 建 WF-A/B/C/D（5.4）
6. 建 Issue Types/Categories（5.3）
7. 建 Forms（5.7）与 MIDP（5.12）
8. 用第 6 章验收清单自检

**B. 设计协同**
1. 作者在 `01_WIP/Team_*/BIM|CAD` 创作（S0）
2. 自检后发起 WF-A → `02_SHARED`（模型 S1 才可被链接）
3. 按 5.10 节奏更新联邦模型与 Clash
4. MIDP 当前里程碑齐备后发起 WF-B → `03_PUBLISHED`
5. 仅 Published 成果归档到 `03_Buildings Design Packages`

**C. BD 法定**
1. 汇集资料到 `05_Statutory Submission/BD Submission`
2. 完成两张强制表单
3. 发起 WF-C（可用 CP 状态）
4. 通过后锁定版本，禁止覆盖（只允许新版本）

**D. 施工与移交**
1. 管理分包目录与 Issue 闭环
2. 组织 Handover 包并校验 `EMSD_Code`
3. 发起 WF-D（CR）并归档 Close-out

### 2.6 GC 验收关注点

- [ ] 角色与审批流引用一致
- [ ] Published 仅 GC_Management 可写
- [ ] WF-C 缺检查表不可通过
- [ ] 命名九段抽检通过率 100%（样本）
- [ ] Shared 前自检与 SuitabilityStatus 抽检通过
- [ ] 移交资产 EMSD 覆盖率达标

---

## 3. Consultant 角色操作手册

### 3.1 职责边界

- 提供 A/S/MEP 等专业成果
- Shared 协同与技术复核
- 支持 BD 技术检查与一致性确认
- 响应设计协同 Issue

### 3.2 目录权限

| 目录 | 权限 |
|------|------|
| `01_WIP`（他队） | View |
| `01_WIP`（本队） | View/Upload/Edit |
| `02_SHARED`（对应专业） | View/Upload/Edit |
| `03_PUBLISHED` | View |
| Design Packages | View（项目可授权 Upload） |
| BD Submission | View/Upload（仅其提交包） |
| Handover | View |

### 3.3 可发起 / 可审批

- 可发起：`Design Coordination`、`RFI / Clarification`、`Authority Submission`
- 可审批：WF-A / WF-C Reviewer
- 不可：Published 终批

### 3.4 字段与表单

必填：命名九段属性 + `SuitabilityStatus` + `Revision` + `SoftwareVersion`（模型）；法定相关再填 `StatutoryRelated`  
模型协调共享用 **S1**。  
表单：`MIDP Delivery Check`、`BEP Milestone Review`、`BD Submission Checklist`、`2D/3D Consistency Check`

### 3.5 日常流程

1. 在本队 `01_WIP` 创作（S0），按九段命名  
2. 自检后提 WF-A 至 `02_SHARED`  
3. 响应 Clash/Issue；仅链接 S1+ 模型  
4. 按 MIDP 配合进 Published；驳回需写原因  
5. BD 节点配合一致性检查  

### 3.6 Consultant 验收关注点

- [ ] Shared 文件命名九段与版本正确
- [ ] SuitabilityStatus 使用正确（尤其 S1）
- [ ] 本专业 MIDP 行与实际上传一致
- [ ] BD 一致性检查已完成

---

## 4. Subcon 角色操作手册

### 4.1 职责边界

- 在授权范围内上传施工资料与分包交付
- 响应质量/安全/Fit-out Issue
- 不修改 Published / 法定终包

### 4.2 目录权限

| 目录 | 权限 |
|------|------|
| `01_WIP`（指定团队/专业子目录） | View/Upload/Edit |
| `02_SHARED` / `03_PUBLISHED` | View |
| `04_Construction & Subcontractors`（授权范围） | View/Upload/Edit |
| Statutory / Handover | View |

### 4.3 可发起 / 可审批

- 可发起：`Site Quality`、`Site Safety`、`Fit-out Defect`、`RFI / Clarification`
- 通常不担任 Approver

### 4.4 字段与表单

上传文件：命名九段 + `SuitabilityStatus=S0/S1` + `Revision`；设备相关填 `EMSD_Code`  
Issue 必填：`IssueOrigin`、`IssueTrade`、`CostImpactLevel`、`TimeImpactDays`  
可选：`Zone`、`Area`、`PackageNo`（住宅可加 Block/Floor）  
表单：`Defect Rectification Checklist`

### 4.5 日常流程

1. 仅在授权目录上传方法声明、ITP、分包交付  
2. Issue 指派后按时限整改并上传证据  
3. 需改正式文件时，提交给 GC 走 WF，不直改 Published  
4. 移交前关闭缺陷清单并补齐资产码  

### 4.6 Subcon 验收关注点

- [ ] 无越权写 Published
- [ ] 缺陷关闭有表单与附件
- [ ] 命名九段与必填字段完整

---
