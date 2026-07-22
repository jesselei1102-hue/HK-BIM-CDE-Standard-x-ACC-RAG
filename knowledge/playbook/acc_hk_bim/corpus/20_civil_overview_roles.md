---
capability: roles
domain: civil
title: "Civil 总览与角色操作"
title_en: "Civil overview and role operations"
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
# Civil 总览与角色操作

> 来源：`output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md` · domain=`civil` · capability=`roles`

## 0. 总览

### 0.1 目标

在 Autodesk Forma / Construction Cloud（原 ACC）中建立 Civil 项目统一规则，覆盖：
- Forma Data Management 资料夹与权限（CDE 状态 + 团队 + Section / Contract Package）
- Issue / Reviews / Forms
- ISO19650 风格命名（Section 映射 Building 字段）、适用性状态与字段
- EMSD 资产分类（机电适用子集）
- LandsD / DEVB 相关交付检查口径
- 角色日常操作、协同节奏与验收标准

### 0.2 适用范围与产品

- 项目类型：Civil / Infrastructure（道路、排水、土木、地工、交通相关等）
- 必选产品：Forma Data Management（原 Autodesk Docs）
- 建议产品：Forma Build（原 Autodesk Build）
- 按需产品：Forma Design Collaboration（原 Design Collaboration）、Takeoff、Cost

> 产品更名说明（2025+ Autodesk rebrand）：配置界面若仍短暂显示旧名，以本说明书新名为准；能力与配置路径对应不变。

> 实施建议：若启用 Forma Design Collaboration，Shared folder 一旦指定不可更改；先建好 `02_Design Coordination/02_SHARED` 再配置。

### 0.3 如何使用本文

1. 先读第 0 章总览与角色矩阵  
2. 按自己角色读第 1–4 章（操作手册）  
3. 实施配置时直接用第 5 章附录明细  
4. 用第 6 章验收清单勾选

### 0.4 角色责任矩阵（RACI）

R=Responsible，A=Accountable，C=Consulted，I=Informed

| 事项 | Owner | GC | Consultant | Subcon |
|------|-------|----|------------|--------|
| 信息要求与区段交付标准 | A | R | C | I |
| 模板/项目配置落地 | I | A/R | C | I |
| 区段/合约包目录维护 | I | A/R | C | I |
| 设计协同（WIP/Shared） | I | A | R | C |
| 正式发布（Published） | I | A/R | C | I |
| LandsD / 工务提交包 | I | A/R | C | I |
| 地下管线/交通/临时工程 Issue | I | A | C | R |
| 移交验收 | A | R | C | C |

### 0.5 配置总览（一页）

| 模块 | 必须落地内容 |
|------|--------------|
| Folder | 01–08；`02` 按 `01_WIP→02_SHARED→03_PUBLISHED→04_ARCHIVE`；LandsD 增强目录；`03/By Section` |
| Permission | 最小授权；Owner 不可见 WIP；Published/LandsD 写权限收敛 |
| Issue | 9 Types + Civil Categories + 状态可见性 |
| Workflow | WF-A/B/C/D（自检门禁 + LandsD 门禁） |
| Naming | `Project-Originator-Building-Zone-Level-Type-Role-System-Number`（Building=区段码 SEC*） |
| Status | SuitabilityStatus：`S0/S1/S2/S3/S4/A*/CP/CR` |
| Fields | 命名九段 + Section/Chainage/ContractPackage + EMSD（适用时） |
| Asset | EMSD 适用子集（EL/FS/GEN/LTG/HVAC…）；土木资产可用 `AssetClass` 扩展 |
| Forms | 9 张最小表单（含 LandsD/MIDP/边界与模型清单） |
| Cadence | 建议每 2–3 周 Shared 冻结；周协调会 |

---

## 1. Owner 角色操作手册

### 1.1 职责边界

- 定义信息要求与区段交付标准
- 接收正式发布与移交包
- 监督 LandsD/工务相关合规结果（不替代官方审批）
- 确认关键变更与移交

### 1.2 目录权限

| 目录 | 权限 | 说明 |
|------|------|------|
| `01_Project Governance` | View | 合约与程序 |
| `02/.../01_WIP` | No Access | 过程稿不对 Owner 开放 |
| `02/.../02_SHARED` | View | 协同稿 |
| `02/.../03_PUBLISHED` | View | 正式成果 |
| `03_Civil Design Packages` | View | 区段正式包 |
| `05_Statutory Submission` | View | LandsD/工务包只读 |
| `07_Handover & Closeout` | View | 移交验收 |
| `08_Reference & Standards` | View | EIR/规范 |

### 1.3 可发起 / 可确认

- 可发起：`RFI / Clarification`、移交验收意见
- 可确认：Published 接受、Handover 通过、关键变更接受
- 不建议担任日常发布 Approver

### 1.4 字段与表单

字段：`DeliverableStage`、`SuitabilityStatus`、`SubmissionType`、`Section`、`ContractPackage`、`Revision`、`EMSD_Code`/`AssetClass`（移交时）  
表单：`EIR Clause Check`、`MIDP Delivery Check`、`Civil Handover Checklist`、`Project Close-out Checklist`

### 1.5 日常流程

**开项**
1. 确认 EIR 与区段交付标准入库  
2. 确认 Section / ContractPackage 编码表已发布  
3. 抽查目录是否按 5.1 建立  

**设计阶段**
1. 只看 `02_SHARED` / `03_PUBLISHED`  
2. 对正式发布提接受意见  
3. 风险通过 Issue 留痕  

**LandsD / 工务节点**
1. 查看 `05_Statutory Submission/LandsD Submission`  
2. 确认完整性检查、边界、模型清单已完成  
3. 确认版本可追溯  

**移交**
1. 按 Civil Handover Checklist 验收  
2. 未关闭关键缺陷不签字  
3. 确认 Close-out 完成  

### 1.6 Owner 验收关注点

- [ ] 不可见 WIP
- [ ] 区段字段可检索
- [ ] LandsD 包含边界与模型清单
- [ ] 移交证据链完整

---

## 2. GC 角色操作手册

### 2.1 职责边界

- 配置落地与维护
- 区段/合约包管理
- 审批推进与交付整合
- LandsD / 工务提交统筹

内部映射：
- `GC_Management`：终批、发布、法定统筹
- `GC_Engineering`：技术协同
- `GC_Commercial_QS`：变更商务
- `GC_QHSE`：质量安全与移交质量

### 2.2 目录权限

| 目录 | GC_Mgmt | GC_Eng | GC_QS | GC_QHSE |
|------|---------|--------|-------|---------|
| WIP | V | V/U/E/D | V | V |
| Shared | V/E | V/U/E | V | V |
| Published | V/U/E | V | V | V |
| LandsD Submission | V/U/E | V/U | V | V |
| Construction | V/U/E | V/U/E | V | V/U/E |
| Handover | V/U/E | V/U | V | V/U |

### 2.3 可发起 / 可审批

- 可发起：全部 Issue Types
- Approver：`GC_Management`
- Reviewer：
  - WF-A/C：`GC_Engineering`
  - WF-B：`GC_Engineering` + `GC_Commercial_QS`
  - WF-D：`GC_Engineering` + `GC_QHSE`

### 2.4 字段与表单

Forma Data Management 必填：
- 命名九段属性（Building=区段码）+ `Section` + `ContractPackage`
- `SuitabilityStatus`、`Revision`、`SubmissionType`、`DeliverableStage`、`RequiresApproval`、`ApprovalWorkflowId`
- 建议：`Chainage`、`MilestoneID`
- 法定包：`StatutoryRelated`、`SoftwareVersion`
- 移交：`EMSD_Code`（机电）或 `AssetClass`（土木）

Issue 必填：
- `IssueOrigin`、`IssueTrade`、`Section`、`ContractPackage`、`CostImpactLevel`、`TimeImpactDays`、`RegulatoryImpact`

Forms：9 张最小表单主责（见 5.7）

### 2.5 日常流程

**配置落地**
1. 建 5.1 目录（团队 WIP + Shared BIM + SEC + LandsD）  
2. 放入 EMSD 子集与 Project Codes  
3. 配 5.2 权限  
4. 配命名与字段（5.5/5.6）  
5. 建 WF-A/B/C/D  
6. 建 Issue、Forms、MIDP  
7. 第 6 章自检  

**协同与发布**
1. `01_WIP`（S0）自检后 WF-A → `02_SHARED`（模型 S1）  
2. 按 5.10 更新联邦/Clash  
3. MIDP 齐备后 WF-B → `03_PUBLISHED`  
4. 归档到 `03_Civil Design Packages/By Section/...`

**LandsD / 工务**
1. 资料进入 LandsD 目录结构  
2. 完成完整性与边界/模型清单检查  
3. 发起 WF-C（CP），通过后锁定版本  

**施工与移交**
1. 管理交通导改、临时工程、质量安全 Issue  
2. 组织 Handover 并校验资产码  
3. WF-D（CR）+ Close-out  

### 2.6 GC 验收关注点

- [ ] Section/ContractPackage 与 Building 字段一致可用
- [ ] WF-C 可拦截缺件包
- [ ] Published 写权限收敛
- [ ] 命名九段抽检通过
- [ ] SuitabilityStatus / MIDP / EMSD 子集抽检通过

---

## 3. Consultant 角色操作手册

### 3.1 职责边界

- 提供道路排水/结构土木/地工/交通相关设计成果
- Shared 协同与技术复核
- 支持 LandsD/工务技术检查
- 响应设计与地下管线 Issue

### 3.2 目录权限

| 目录 | 权限 |
|------|------|
| `01_WIP`（他队） | View |
| `01_WIP`（本队） | View/Upload/Edit |
| `02_SHARED`（对应专业） | View/Upload/Edit |
| `03_PUBLISHED` | View |
| Civil Design Packages | View（可授权 Upload） |
| LandsD Submission | View/Upload（仅其提交包） |
| Handover | View |

### 3.3 可发起 / 可审批

- 可发起：`Design Coordination`、`Underground Utilities`、`RFI / Clarification`、`Authority Submission`
- Reviewer：WF-A / WF-C
- 不可终批 Published

### 3.4 字段与表单

必填：命名九段 + `Section` + `SuitabilityStatus` + `Revision` + `SoftwareVersion`  
建议：`Chainage`、`ContractPackage`  
表单：`MIDP Delivery Check`、`BEP Milestone Review`、`LandsD Completeness Check`、`Project Boundary & Model File List Check`

### 3.5 日常流程

1. 本队 `01_WIP`（S0）按九段命名创作  
2. 自检后 WF-A → `02_SHARED`；模型用 S1；填写 Section/Chainage  
3. 响应管线/设计 Issue（2 个工作日内）；配合联邦  
4. 按 MIDP 与区段归档配合 Published  
5. LandsD 节点配合完整性与边界清单检查；驳回写明原因  

### 3.6 Consultant 验收关注点

- [ ] 命名九段 + Section/Chainage 完整
- [ ] SuitabilityStatus（尤其 S1）正确
- [ ] 复核意见可追溯
- [ ] LandsD 检查完成

---

## 4. Subcon 角色操作手册

### 4.1 职责边界

- 按合约段/专业上传施工资料
- 响应质量、安全、交通、临时工程 Issue
- 不改 Published / 法定终包

### 4.2 目录权限

| 目录 | 权限 |
|------|------|
| `01_WIP`（指定子目录） | View/Upload/Edit |
| `02_SHARED` / `03_PUBLISHED` | View |
| Construction（授权范围） | View/Upload/Edit |
| Temporary Works / Traffic Management | View/Upload/Edit（授权时） |
| Statutory / Handover | View |

### 4.3 可发起 / 可审批

- 可发起：`Site Quality`、`Site Safety`、`Traffic Management`、`Temporary Works`、`RFI / Clarification`
- 通常不担任 Approver

### 4.4 字段与表单

上传文件：命名九段 + `Section` + `SuitabilityStatus` + `Revision`  
Issue 必填：`IssueOrigin`、`IssueTrade`、`Section`、`ContractPackage`、`CostImpactLevel`、`TimeImpactDays`  
表单：`Defect Rectification Checklist`

### 4.5 日常流程

1. 仅在授权区段目录上传  
2. Issue 整改并附证据  
3. 正式文件修订走 GC 提审链路  
4. 移交前关闭未完事项并补资产字段  

### 4.6 Subcon 验收关注点

- [ ] 无越权写 Published
- [ ] 交通/临时工程关闭有证据
- [ ] 命名九段与区段字段完整

---
