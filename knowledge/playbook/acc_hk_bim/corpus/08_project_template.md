---
capability: project_template
title: "ACC 項目樣板（香港 GC / Buildings）"
title_en: "ACC Project Template — HK General Contractor / Buildings"
authority_refs:
  - "CICBIMS General 2024"
  - "DEVB BIM Harmonisation Guidelines v3.0"
  - "DEVB TC(W) No.1/2025"
  - "BD ADM-19 / ADV-34"
  - "ISO 19650-1/2:2018"
related_product_guids:
  - "Configure_Templates_Docs"
  - "Configure_Templates_Design_Collab"
  - "Organize_files_With_Folders"
  - "File_Naming_Standard"
  - "Reviews_Create_Edit"
  - "Reviews_Workflow"
source_research:
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/ACC_HK_General_Contractor_Template_Guide.md"
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/ACC_HK_GC_Buildings_Config_Plan.md"
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/ACC_HK_Project_Template_Guide.md"
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/HK_BIM_Digital_Delivery_ACC_Mapping.md"
  - "knowledge/playbook/acc_hk_bim/research/acc_project_template/HK_BIM_Digital_Delivery_ACC_Checklist.md"
related_playbook_files:
  - "01_project_setup.md"
  - "02_folder_cde.md"
  - "03_naming.md"
  - "04_permissions.md"
  - "05_workflow.md"
version: "1.0"
date: "2026-07-13"
disclaimer: "組織推薦配置（GC Buildings 樣板），非 CIC/DEVB 官方 ACC 模板。與 02_folder_cde 四容器頂層結構可並存，按項目角色選用。"
---

# 08 — ACC 項目樣板（香港 GC / Buildings）

> **定位**：總承包商（General Contractor）在 ACC **Account Admin → Project templates** 落地香港 Buildings 項目樣板。  
> **與第 02 章關係**：`02_folder_cde` 以 **ISO 四容器頂層夾**（`01_WIP`…`04_Archive`）為設計/顧問向 CDE；本章以 **GC 業務資料夾 + 設計協同內嵌 WIP/Shared/Published/Archive** 為施工總包向樣板。兩者皆為推薦配置，寫入 BEP 時二選一或混合裁剪。

---

## 1. 樣板定位與產品範圍

[capability=project_template] [recommended_configuration]

### 1.1 模板身份

| 項 | 推薦值 |
|----|--------|
| Template Name | `ACC HK GC Buildings Template` |
| Project Type | `Buildings` |
| 適用對象 | 香港本地總承包商；工務/私營可按法定路徑裁剪 |

### 1.2 Products and tools（最小集）

| 產品 | 建議 |
|------|------|
| Autodesk Docs | 必選 |
| Autodesk Build | 建議 |
| Design Collaboration | 有設計協同時啟用 |
| Takeoff / Cost | 有算量或成本需求時啟用 |

不確定是否使用的產品先關閉，避免界面過重。

### 1.3 建立樣板三種方式

1. **空白模板**：Account Admin → Project templates → Create blank template（從零訂製香港規範，推薦）
2. **項目另存**：Project Admin → Settings → Save as template（已有合規項目時）
3. **EMEA 樣本再改**（僅 US/EU 資料區）：EMEA Buildings / Roads Sample → Save to account → 改為香港用語與目錄

> **Product Help**: [Configure Project Templates for Autodesk Docs](https://help.autodesk.com/view/DOCS/ENU/?guid=Configure_Templates_Docs)

---

## 2. Docs 資料夾結構（GC Buildings）

[capability=project_template] [folder] [recommended_configuration]

在 `Project Files/` 下建立：

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

可選擴展（按項目類型啟用）：`Unit Layout`、`Typical Floor`、`Facade`、`Retail Fitout`。

| 項目類型 | 法定路徑重點 |
|----------|--------------|
| 私營 Buildings | `05_Statutory Submission/BD Submission`（ADM-19 / ADV-34） |
| 工務 | 可增 `LandsD Submission`；對齊 TC(W) No.1/2025、Harmonisation 附錄 XIV |

**與第 02 章對照**：四容器狀態表達放在 `02_Design Coordination/{WIP,Shared,Published,Archive}`；治理、施工、法定、移交為 GC 業務夾，不強制與 ISO 容器同名。

---

## 3. 角色與權限（最小授權）

[capability=project_template] [permissions]

角色組：
- `GC_Management`、`GC_Engineering`、`GC_Commercial_QS`、`GC_QHSE`
- `Subcontractor`、`Consultant`、`Client_Owner`

關鍵目錄：

| 路徑 | 寫入原則 |
|------|----------|
| `02_Design Coordination/WIP` | GC_Engineering 可編輯；分包僅指定子目錄；顧問 View；業主 No Access |
| `…/Shared` | GC + 顧問可讀寫；分包 View；業主 View |
| `…/Published` | 僅 GC_Management（或授權角色）可發布；其餘 View |
| `05_Statutory Submission/*` | 法定交付小組可寫；其餘 View |
| `07_Handover & Closeout/*` | GC_Management 控寫；工程/QHSE 可上傳；外部 View |

原則：權限先「保守收斂」，再按項目放開。

---

## 4. 命名規則

[capability=project_template] [naming]

標準格式：

```text
ProjectCode-Discipline-FileType-Sequence-Version
```

| 字段 | 建議取值 |
|------|----------|
| Discipline | `A` / `S` / `M` / `P` |
| FileType | `DRW` / `MOD` / `RPT` / `SUB` |
| Version | `V01` 起 |

示例：
- `PRJ001-A-DRW-000123-V02`
- `PRJ001-M-MOD-000045-V01`
- 法定提交：`STAT-PRJ001-A-SUB-000001-V01`

對齊思路：DEVB Harmonisation 附錄 VIII–X；BD 提交另在資料夾說明中標明 ADM-19/ADV-34 格式與軟件版本要求。細部 CIC 九字段見 `03_naming.md`。

---

## 5. Approval Workflows（Buildings）

[capability=project_template] [workflow]

統一：每節點 SLA 2 工作日；超時升級通知 `GC_Management`；駁回必填原因。

| ID | 路徑 | 檔案類型 | Reviewers | Approver | 門禁 |
|----|------|----------|-----------|----------|------|
| WF-A | WIP → Shared | DRW, MOD | GC_Engineering, Consultant | GC_Management | — |
| WF-B | Shared → Published | DRW, MOD, RPT, SUB | GC_Engineering, GC_Commercial_QS | GC_Management | — |
| WF-C | BD Statutory | SUB（建議 `STAT-` 前綴） | GC_Engineering, Consultant | GC_Management | BD Checklist + 2D/3D Consistency |
| WF-D | Handover | RPT, MOD, SUB | GC_Engineering, GC_QHSE | GC_Management | — |

> **缺口**：ACC Workflow 通過後 **不會**自動把檔案從 WIP 遷到 Shared；須文控人工遷夾或 API。見 `05_workflow.md`。

---

## 6. Issues / Forms / Custom Attributes

[capability=project_template]

### 6.1 Issue Types（Build）

`Design Coordination`、`Site Quality`、`Site Safety`、`RFI / Clarification`、`Change / Variation`、`Authority Submission`、`Fit-out Defect`

Categories：`Architecture`、`Structure`、`MEP`、`FA & Plumbing`、`Finishing`、`Subcontract Interface`、`Statutory Submission`

Status 可見性（用系統標準狀態，不新增底層狀態機）：  
`Open` → `In Review` → `Action Required` → `Ready to Close` → `Closed`

### 6.2 Forms 最小清單

- EIR Clause Check / BEP Milestone Review  
- BD Submission Checklist / 2D/3D Consistency Check  
- Building Handover Checklist / Defect Rectification / Project Close-out Checklist  
- 工務可加：LandsD 提交檢查、標書 BIM 交付、合約化 BIM 版本確認

### 6.3 Custom Fields（最小）

Issues：`IssueOrigin`、`IssueTrade`、`CostImpactLevel`、`TimeImpactDays`、`RegulatoryImpact`、`RequiresEscalation`  

Docs 屬性：`SubmissionType`、`DeliverableStage`、`Discipline`、`RequiresApproval`、`ApprovalWorkflowId`、`StatutoryRelated`、`StatutoryRefNo`、`SoftwareVersion`、`Revision`  

Buildings 可選：`BlockNo`、`FloorNo`、`UnitType`、`FlatNo`、`Zone`、`Area`、`PackageNo`

---

## 7. Design Collaboration 約束

[capability=project_template] [design_collab]

1. 先在 Docs 建好 `02_Design Coordination/Shared`（含專業子目錄）  
2. 再進入 Design Collaboration → Settings，指定 Shared folder  
3. **Shared folder 一旦指定，後續不可更改**  

> **Product Help**: [Configure Project Templates for Design Collaboration](https://help.autodesk.com/view/DOCS/ENU/?guid=Configure_Templates_Design_Collab)

---

## 8. 模板內配置順序（實施）

[capability=project_template]

1. Account Admin → Project templates → Create → `ACC HK GC Buildings Template`  
2. **Docs**：Files（目錄 / Folder Permissions / Naming Standards / Attributes）→ Reviews（WF-A/B/C/D）→ Issues（Types/Categories/Fields/Statuses）  
3. **Design Collaboration**：Settings 指向已建 Shared；Team setup  
4. **Build**：Issues / Forms / RFIs / Submittals / Reports  
5. 用測試項目 UAT → 凍結 v1.0 → 變更管理（建議每月評審）

建議節奏：第 1 週 Docs 最小集；第 2 週 Build Issues/Reports 與權限微調。

---

## 9. 啟動與交付檢查（摘要）

[capability=project_template]

**開項目時**：選用香港 GC/住宅或基建樣板；確認 WIP/Shared/Published（或設計協同內嵌）；Naming + Folder Permissions；EIR/BEP 存放；Forms 就緒。

**交付前**：標書/合約化 BIM（TC 1/2025，工務）；LandsD 或 BD 提交包與檢查表；命名與版本可追溯；Close-out Checklist。

完整勾選表見研究稿 `HK_BIM_Digital_Delivery_ACC_Checklist.md`；條款映射見 `HK_BIM_Digital_Delivery_ACC_Mapping.md`。

---

## 10. 港標 ↔ ACC 樣板對齊要點

| 港標要求 | ACC 樣板落點 |
|----------|--------------|
| CDE / 四階段 | `02_Design Coordination` 下 WIP/Shared/Published/Archive |
| IRAM 責任 | Folder Permissions 按角色/公司 |
| Information Container 命名 | File Naming Standards |
| EIR/BEP/收尾 | Docs 參考夾 + Build Forms |
| BD / LandsD 提交 | `05_Statutory Submission` + 專用 Checklist |
| TC 1/2025 標書 BIM | `06_Tender & Change` + 交付確認 Form |

---

## 11. 缺口 / 須寫入 BEP

| 事項 | 說明 |
|------|------|
| 兩套目錄策略 | 第 02 章頂層四容器 vs 本章 GC 業務樹；項目須選定並寫入 BEP |
| Shared folder 不可逆 | Design Collaboration 指定前必須凍結路徑 |
| 審批≠遷夾 | Workflow 通過後仍需人工遷夾與更新 Status 屬性 |
| 法定格式 | BD ADM-19/ADV-34、LandsD 附錄 XIV 細節在 Authoring/外部流程完成，ACC 負責存放與門禁勾選 |
| Civil vs Buildings | Civil 偏 LandsD；Buildings 偏 BD；勿混用同一法定子樹而不標註 |

---

## 12. 研究來源（本地）

本節濃縮自：

- `research/acc_project_template/ACC_HK_General_Contractor_Template_Guide.md`
- `research/acc_project_template/ACC_HK_GC_Buildings_Config_Plan.md`
- `research/acc_project_template/ACC_HK_Project_Template_Guide.md`
- `research/acc_project_template/HK_BIM_Digital_Delivery_ACC_Mapping.md`
- `research/acc_project_template/HK_BIM_Digital_Delivery_ACC_Checklist.md`
