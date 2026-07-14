# ACC HK GC 配置单（Buildings 通用版）

本配置单仅面向香港本地 **General Contractor** 的 **Buildings** 项目模板。
目标是让实施同事可直接按此在 ACC Project Template 后台逐项配置。

---

## 1. 模板定位

- Template Name: `ACC HK GC Buildings Template`
- Project Type: `Buildings`
- Services:
  - 必选：Docs
  - 建议：Build
  - 按需：Design Collaboration、Takeoff、Cost

Design Collaboration 关键约束（先确认再配置）：
- Shared folder 一旦在模板/项目中指定，后续不可更改。
- 建议先在 Docs 建好 `02_Design Coordination/Shared` 后，再进入 Design Collaboration 设置。

---

## 2. Folder 配置（Docs）

在 `Project Files/` 下创建：

```text
Project Files/
├── 01_Project Governance/
│   ├── Contract & Commercial/
│   ├── Procedures/
│   └── Meetings & Instructions/
├── 02_Design Coordination/
│   ├── WIP/
│   │   ├── Architectural/
│   │   ├── Structural/
│   │   ├── MEP/
│   │   └── FA & Plumbing/
│   ├── Shared/
│   │   ├── Architectural/
│   │   ├── Structural/
│   │   ├── MEP/
│   │   └── FA & Plumbing/
│   ├── Published/
│   │   ├── Architectural/
│   │   ├── Structural/
│   │   ├── MEP/
│   │   └── FA & Plumbing/
│   └── Archive/
├── 03_Buildings Design Packages/
│   ├── Architectural/
│   ├── Structural/
│   ├── MEP/
│   └── FA & Plumbing/
├── 04_Construction & Subcontractors/
│   ├── Method Statements/
│   ├── ITP & Records/
│   ├── Site Instructions/
│   └── Subcontractor Deliverables/
├── 05_Statutory Submission/
│   ├── BD Submission/
│   ├── Statutory Drawings/
│   └── BIM Supporting Files/
├── 06_Tender & Change/
├── 07_Handover & Closeout/
│   ├── As-built/
│   ├── O&M/
│   └── Defect List/
└── 08_Reference & Standards/
```

可选扩展目录（按项目类型启用）：
- `Unit Layout`（住宅项目）
- `Typical Floor`（住宅/办公）
- `Facade`（高层或幕墙项目）
- `Retail Fitout`（商业项目）

---

## 3. 角色与权限配置

角色组：
- `GC_Management`
- `GC_Engineering`
- `GC_Commercial_QS`
- `GC_QHSE`
- `Subcontractor`
- `Consultant`
- `Client_Owner`

关键目录权限（最小授权策略）：

- `02_Design Coordination/WIP`
  - GC_Engineering: View/Upload/Edit/Delete
  - Subcontractor: View/Upload/Edit（仅指定子目录）
  - Consultant: View
  - Client_Owner: No Access
  - GC_Management: View

- `02_Design Coordination/Shared`
  - GC_Engineering: View/Upload/Edit
  - Consultant: View/Upload/Edit
  - Subcontractor: View
  - Client_Owner: View
  - GC_Management: View/Edit

- `02_Design Coordination/Published`
  - GC_Management: View/Upload/Edit（发布责任）
  - GC_Engineering: View
  - GC_Commercial_QS: View
  - GC_QHSE: View
  - Subcontractor: View
  - Consultant: View
  - Client_Owner: View

- `05_Statutory Submission/*`
  - GC_Management: View/Upload/Edit
  - GC_Engineering: View/Upload
  - Consultant: View/Upload（仅其提交包）
  - Subcontractor: View
  - Client_Owner: View

- `07_Handover & Closeout/*`
  - GC_Management: View/Upload/Edit
  - GC_Engineering: View/Upload
  - GC_QHSE: View/Upload
  - GC_Commercial_QS: View
  - Consultant/Subcontractor/Client_Owner: View

---

## 4. Issue 配置（Build）

Issue Types:
- `Design Coordination`
- `Site Quality`
- `Site Safety`
- `RFI / Clarification`
- `Change / Variation`
- `Authority Submission`
- `Fit-out Defect`

Issue Categories:
- `Architecture`
- `Structure`
- `MEP`
- `FA & Plumbing`
- `Finishing`
- `Subcontract Interface`
- `Statutory Submission`

Issue Status 配置口径（按 ACC Docs/Build 能力）：
- 使用系统标准状态，不自定义新的底层状态机。
- 在模板中配置“状态可见性（Issue Statuses Settings）”，建议保留以下业务可见状态：
  - `Open`
  - `In Review`
  - `Action Required`
  - `Ready to Close`
  - `Closed`
- 若账号默认状态名称不同，按同等业务语义映射，不强制同名。

默认责任：
- `Design Coordination` -> `GC_Engineering`
- `Site Safety` -> QHSE 负责人
- `Authority Submission` -> `GC_Management`
- `Fit-out Defect` -> 对应分包负责人

---

## 5. Approval Workflows（Buildings）

统一设置：
- 每节点 SLA: 2 工作日
- 超时升级：通知 `GC_Management`
- 驳回必须填原因

Workflow A（WIP -> Shared）：
- Folder: `02_Design Coordination/WIP`
- Files: `DRW`, `MOD`
- Reviewers: `GC_Engineering`, `Consultant`
- Approver: `GC_Management`

Workflow B（Shared -> Published）：
- Folder: `02_Design Coordination/Shared`
- Files: `DRW`, `MOD`, `RPT`, `SUB`
- Reviewers: `GC_Engineering`, `GC_Commercial_QS`
- Approver: `GC_Management`

Workflow C（BD Statutory Submission）：
- Folder: `05_Statutory Submission/BD Submission`
- Files: `SUB`（建议 `STAT-` 前缀）
- Reviewers: `GC_Engineering`, `Consultant`
- Approver: `GC_Management`
- 门禁：必须完成 `BD Submission Checklist` + `2D/3D Consistency Check`

Workflow D（Handover）：
- Folder: `07_Handover & Closeout`
- Files: `RPT`, `MOD`, `SUB`
- Reviewers: `GC_Engineering`, `GC_QHSE`
- Approver: `GC_Management`

---

## 6. 命名规则（File Naming Standards）

标准规则：
- `ProjectCode-Discipline-FileType-Sequence-Version`

建议取值：
- Discipline: `A/S/M/P`
- FileType: `DRW/MOD/RPT/SUB`
- Version: `V01` 起

示例：
- `PRJ001-A-DRW-000123-V02`
- `PRJ001-M-MOD-000045-V01`

法定提交：
- `STAT-PRJ001-A-SUB-000001-V01`

---

## 7. Custom Fields（最小必配）

Build Issues 可配字段（模板内直接配置）：
- `IssueOrigin` (`Site/Design/RFI/Authority`)
- `IssueTrade` (`Architecture/Structure/MEP/FA-Plumbing`)
- `CostImpactLevel` (`None/Low/Medium/High`)
- `TimeImpactDays` (Number)
- `RegulatoryImpact` (`None/BD/Both`)
- `RequiresEscalation` (`Yes/No`)

Docs 文件属性字段（通过 Files attributes + naming + review workflow 管理）：
- `SubmissionType` (`Internal/Client/BD/OtherAuthority`)
- `DeliverableStage` (`WIP/Shared/Published/Statutory/Handover`)
- `Discipline` (`A/S/M/P`)
- `RequiresApproval` (`Yes/No`)
- `ApprovalWorkflowId` (`WF-A/WF-B/WF-C/WF-D`)
- `StatutoryRelated` (`Yes/No`)
- `StatutoryRefNo` (Text)
- `SoftwareVersion` (Text)
- `Revision` (Text)

Buildings 可选扩展字段（按项目启用，不设默认必填）：
- `BlockNo` (Text)
- `FloorNo` (Text)
- `UnitType` (Text)
- `FlatNo` (Text)
- `Zone` (Text)
- `Area` (Text)
- `PackageNo` (Text)

---

## 8. Forms 最小清单

- `EIR Clause Check`
- `BEP Milestone Review`
- `BD Submission Checklist`
- `2D/3D Consistency Check`
- `Building Handover Checklist`
- `Defect Rectification Checklist`
- `Project Close-out Checklist`

---

## 8A. 模板内配置路径（实施顺序）

1. `Account Admin -> Project templates -> Create template`（`ACC HK GC Buildings Template`）  
2. Product picker 选择 `Docs`  
   - `Files`: 建目录、Folder Permissions、File Naming Standards、File Attributes  
   - `Reviews`: 建 Approval Workflows（A/B/C/D）  
   - `Issues`: 配 Types/Categories/Custom Fields/Root Causes/Permissions/Statuses visibility  
3. Product picker 选择 `Design Collaboration`  
   - `Settings`: 指向已创建的 Shared folder（不可逆）  
   - `Team setup`: 绑定团队和包含目录  
4. Product picker 选择 `Build`  
   - `Issues/Forms/RFIs/Submittals/Reports` 按本配置单落地  

---

## 9. 数据来源（规范依据）

内部基线：
- `ACC_HK_General_Contractor_Template_Guide.md`
- `HK_BIM_Digital_Delivery_ACC_Mapping.md`
- `HK_BIM_Digital_Delivery_ACC_Checklist.md`

外部规范：
- DEVB：`specification/DEVB_DEVB_BIM_Harmonisation_Guidelines_v3_0_with_All_Appendices.pdf`
  - 用于 WIP/Shared/Published/Archive 阶段逻辑、职责分工与命名思路
- BD：`specification/BD_BD_ADM019.pdf`、`specification/BD_BD_ADV034.pdf`
  - 用于 Buildings 法定提交（BD）流程、提交格式与一致性要求
- CIC：`specification/CIC_CIC_BIM_Standards_General_2024_page.html`
  - 用于 EIR/BEP 与信息交付管理框架

ACC Docs 官方能力边界（本地离线 docs）：
- `DOCS/DOCS_help_006.md`
  - Configure Project Templates for Autodesk Docs（Files/Reviews/Issues/Reports）
  - Configure Project Templates for Design Collaboration（Shared folder 不可更改）
- `DOCS/DOCS_help_003.md`
  - Submit for review / approval workflows / review status 行为

---

## 10. 与 Civil 项目差异（简述）

本配置单已对 Buildings 做了通用化，和 Civil 相比主要差异：
- 重点法定路径为 `BD Submission`（而非 LandsD 主导）
- 目录和字段强调建筑专业协同与楼宇交付
- 缺陷类型使用 `Fit-out Defect`，不限定住宅单位口径

---

## 11. 实施前自检（避免配置偏差）

- 角色是否包含 `GC_Commercial_QS` 与 `GC_QHSE`（审批流依赖）
- `02_Design Coordination` 下是否已创建专业子目录（WIP/Shared/Published）
- Design Collaboration 的 Shared folder 是否已最终确认（不可逆）
- Issue Status 是否采用“可见性配置”而非新增底层状态
- Workflow C 是否强制 `BD Submission Checklist` + `2D/3D Consistency Check`
