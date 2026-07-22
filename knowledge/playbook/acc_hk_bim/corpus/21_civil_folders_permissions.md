---
capability: folder
domain: civil
title: "Civil 文件夹与权限"
title_en: "Civil folders and permissions"
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
# Civil 文件夹与权限

> 来源：`output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md` · domain=`civil` · capability=`folder`

## 5. 配置明细附录（可直接实施）

### 5.1 Folder 结构（完整）

```text
Project Files/
├── 01_Project Governance/
│   ├── Contract & Commercial/
│   ├── Procedures/
│   └── Meetings & Instructions/
├── 02_Design Coordination/
│   ├── 01_WIP/                              # S0
│   │   ├── Team_GC/
│   │   │   ├── CAD/ BIM/ COORD/ EXPORT/
│   │   ├── Team_Roads_Drainage/
│   │   │   ├── CAD/ BIM/ COORD/ EXPORT/
│   │   ├── Team_Structures_Civil/
│   │   │   ├── CAD/ BIM/ COORD/ EXPORT/
│   │   ├── Team_Geotech/
│   │   │   ├── CAD/ BIM/ COORD/ EXPORT/
│   │   └── Team_ME_Traffic/
│   │       ├── CAD/ BIM/ COORD/ EXPORT/
│   ├── 02_SHARED/                           # S1–S4 主交换区
│   │   ├── Client/
│   │   ├── Lead_Consultant/
│   │   │   ├── 1_Roads_Drainage/
│   │   │   ├── 2_Structures_Civil/
│   │   │   ├── 3_Geotechnical/
│   │   │   └── 4_ME_Traffic/
│   │   ├── GC/
│   │   ├── Other_Consultant/
│   │   └── 8_BIM/
│   │       ├── 1_BIM_DOCUMENTS/             # BEP、MIDP、Clash Matrix
│   │       ├── 2_Authoring_Models/
│   │       ├── 3_Federated_Model/
│   │       └── 4_Issues_Management/
│   ├── 03_PUBLISHED/                        # A / CP / CR
│   │   ├── Concept/
│   │   ├── Detail_Design/
│   │   └── Construction_Documents/
│   └── 04_ARCHIVE/
├── 03_Civil Design Packages/
│   ├── By Section/
│   │   ├── SEC-A/
│   │   ├── SEC-B/
│   │   └── SEC-C/
│   ├── Roads & Drainage/
│   ├── Structures & Civil/
│   ├── Geotechnical/
│   └── M&E & Traffic/
├── 04_Construction & Subcontractors/
│   ├── Method Statements/
│   ├── ITP & Records/
│   ├── Site Instructions/
│   ├── Temporary Works/
│   ├── Traffic Management/
│   └── Subcontractor Deliverables/
├── 05_Statutory Submission/
│   ├── LandsD Submission/
│   │   ├── DESIGN/
│   │   ├── AS-BUILT/
│   │   ├── HARMONISED/
│   │   ├── NON-HARMONISED/
│   │   ├── PROJECT_BOUNDARY/
│   │   ├── MODEL_FILE_LIST/
│   │   └── PROJECT_SPECIFIC_CODE/
│   ├── Other Authorities/
│   └── Works Submission Support/
├── 06_Tender & Change/
│   ├── Tender BIM/
│   └── Variations/
├── 07_Handover & Closeout/
│   ├── As-built/
│   ├── Asset_Information/                   # EMSD 子集 + 土木资产表
│   └── Defect List/
└── 08_Reference & Standards/
    ├── EIR-BEP/
    ├── DEVB-LandsD References/
    ├── EMSD_AIR/
    └── Project Codes/                       # Originator / SEC / Zone / Level
```

目录使用规则：
- `01_WIP` = S0；不可被他方当已验证引用  
- `02_SHARED` = 跨团队交换；模型达 **S1** 才可链接  
- `03_PUBLISHED` = 里程碑批准；再归档到 `03/.../By Section`  
- `05/LandsD Submission` = 地政/工务增强结构（保持 DEVB 口径）  
- 专业/区段分类：命名字段 + Shared 专业夹 + `03/By Section`；不要只靠 WIP 平铺专业夹

## 5. 配置明细附录（可直接实施）

### 5.2 权限矩阵（完整）

图例：V/U/E/D/NA

| 目录 | Owner | GC_Mgmt | GC_Eng | GC_QS | GC_QHSE | Consultant | Subcon |
|------|-------|---------|--------|-------|---------|------------|--------|
| 01 Governance | V | V/U/E | V | V/U/E | V | V | V |
| 02/01_WIP | NA | V | V/U/E/D | V | V | V* | V/U/E* |
| 02/02_SHARED | V | V/E | V/U/E | V | V | V/U/E | V |
| 02/03_PUBLISHED | V | V/U/E | V | V | V | V | V |
| 02/04_ARCHIVE | V | V/U/E | V | V | V | V | V |
| 03 By Section | V | V/U/E | V/U | V | V | V | V |
| 04 Construction | V | V/U/E | V/U/E | V | V/U/E | V | V/U/E* |
| 04 Temporary Works | V | V/U/E | V/U/E | V | V/U/E | V | V/U/E* |
| 04 Traffic Mgmt | V | V/U/E | V/U/E | V | V/U/E | V | V/U/E* |
| 05 LandsD | V | V/U/E | V/U | V | V | V/U** | V |
| 06 Tender & Change | V | V/U/E | V/U | V/U/E | V | V | V |
| 07 Handover | V | V/U/E | V/U | V | V/U | V | V |
| 08 Reference | V | V/U/E | V | V | V | V | V |

\*仅指定团队/区段/专业子目录  
\*\*仅其提交包

## 5. 配置明细附录（可直接实施）

### 5.10 协同节奏与状态映射

| 码 | 含义 | 典型目录 |
|----|------|----------|
| S0 | WIP | `01_WIP` |
| S1 | Coordination（可链接） | `02_SHARED` |
| S2–S4 | Information / Review / Stage Approval | `02_SHARED` |
| A* | 阶段批准 | `03_PUBLISHED` |
| CP | Compliance（LandsD/工务等） | Statutory / Published |
| CR | Handover / As-constructed | `07_Handover` |

推荐节奏：周协调会；每 2–3 周 Shared 冻结；联邦+Clash 报告随 Shared 更新；Owner/工务审查按里程碑。

Shared 前自检：命名九段=属性；拟升 S1–S3；Revision 收拢；本专业 High Clash 已处理或已建 Issue；封面/Splash 注明变更。

## 5. 配置明细附录（可直接实施）

### 5.11 EMSD 资产分类（Civil 适用子集）

源表同 Buildings：`EMSD_AIR_v2_Tandem_Classification.xlsx` → 放入 `08/.../EMSD_AIR`

Civil **默认启用子集**（场站/泵房/照明/发电/消防等机电）：
`EL` / `LTG` / `LVS` / `GEN` / `UPS-UPS` / `FS-AFA` / `FS-WTS` / `HVAC-AS` / `HVAC-WS` / `ACS-ACS` / `CCTV-CCTV`

土木本体（道路、排水构筑物、土石方等）用 `AssetClass` 项目码表，不强制套 EMSD。  
规则：Naming `System` ≠ `EMSD_Code` ≠ `AssetClass`。

## 5. 配置明细附录（可直接实施）

### 5.12 MIDP 控制（最小可运行）

路径：`02_SHARED/8_BIM/1_BIM_DOCUMENTS/`  
列：Delivery Title + 命名九段 + Milestone Y/N（可含 Section/ContractPackage 辅助列）  
规则：Lead/GC BIM Manager 汇总；WF-B 前核对当前里程碑 Y 项。

---
