---
capability: folder
domain: buildings
title: "Buildings 文件夹与权限"
title_en: "Buildings folders and permissions"
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
# Buildings 文件夹与权限

> 来源：`output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md` · domain=`buildings` · capability=`folder`

## 5. 配置明细附录（可直接实施）

### 5.1 Folder 结构（完整）

```text
Project Files/
├── 01_Project Governance/
│   ├── Contract & Commercial/
│   ├── Procedures/
│   └── Meetings & Instructions/
├── 02_Design Coordination/
│   ├── 01_WIP/                          # Suitability = S0；仅作者日用
│   │   ├── Team_GC/
│   │   │   ├── CAD/
│   │   │   ├── BIM/
│   │   │   ├── COORD/
│   │   │   └── EXPORT/
│   │   ├── Team_Arch/
│   │   │   ├── CAD/
│   │   │   ├── BIM/
│   │   │   ├── COORD/
│   │   │   └── EXPORT/
│   │   ├── Team_Struct/
│   │   │   ├── CAD/ BIM/ COORD/ EXPORT/
│   │   ├── Team_MEP/
│   │   │   ├── CAD/ BIM/ COORD/ EXPORT/
│   │   └── Team_FA/
│   │       ├── CAD/ BIM/ COORD/ EXPORT/
│   ├── 02_SHARED/                       # 跨方正式交换（S1–S4 主区）
│   │   ├── Client/
│   │   ├── Lead_Consultant/
│   │   │   ├── 1_Architecture/
│   │   │   ├── 2_Structure/
│   │   │   ├── 3_MEP/
│   │   │   │   ├── ELE/
│   │   │   │   ├── HVAC/
│   │   │   │   ├── FS/
│   │   │   │   └── PH/
│   │   │   └── 4_FA_Plumbing/
│   │   ├── GC/
│   │   ├── Other_Consultant/
│   │   └── 8_BIM/
│   │       ├── 1_BIM_DOCUMENTS/         # BEP、Clash Matrix、MIDP 等
│   │       ├── 2_Authoring_Models/      # 各专业单体模型
│   │       ├── 3_Federated_Model/       # 联邦模型 NWD / Forma
│   │       └── 4_Issues_Management/     # 碰撞/协调报告
│   ├── 03_PUBLISHED/                    # 里程碑已批（A / CP / CR）
│   │   ├── Concept/
│   │   ├── Detail_Design/
│   │   └── Construction_Documents/
│   └── 04_ARCHIVE/                      # 历史冻结副本
├── 03_Buildings Design Packages/        # 正式专业包（建议只收 Published）
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
│   ├── Tender BIM/
│   └── Variations/
├── 07_Handover & Closeout/
│   ├── As-built/
│   ├── O&M/
│   ├── Asset_Information/               # EMSD 分类与资产表
│   └── Defect List/
└── 08_Reference & Standards/
    ├── EIR-BEP/
    ├── BD References/
    ├── EMSD_AIR/                        # 资产分类源表
    └── Project Codes/                   # Originator/Building/Zone/Level 码表
```

可选扩展（按项目启用，非默认强制）：
- `Unit Layout`、`Typical Floor`、`Facade`、`Retail Fitout`
- Forma Design Collaboration 启用时：先固定 `02_Design Coordination/02_SHARED` 再绑定 Shared

目录使用规则：
- `02/01_WIP` = S0 过程稿；**不可**被他方当作已验证引用
- `02/02_SHARED` = 跨团队交换；模型需达 **S1** 才可作为链接背景
- `02/03_PUBLISHED` = 里程碑批准成果
- `02/04_ARCHIVE` = 历史冻结（含每次 Shared 前的 Detach 副本）
- `03` = 专业正式包（从 Published 归档）
- `05` = BD 法定包
- `07` = 移交包（含资产信息）
- 专业分类优先落在：**命名 Role/System** + Shared 专业子目录；不要只靠 WIP 下平铺专业夹

## 5. 配置明细附录（可直接实施）

### 5.2 权限矩阵（完整）

图例：V=View，U=Upload，E=Edit，D=Delete，NA=No Access

| 目录 | Owner | GC_Mgmt | GC_Eng | GC_QS | GC_QHSE | Consultant | Subcon |
|------|-------|---------|--------|-------|---------|------------|--------|
| 01 Governance | V | V/U/E | V | V/U/E | V | V | V |
| 02/01_WIP | NA | V | V/U/E/D | V | V | V* | V/U/E* |
| 02/02_SHARED | V | V/E | V/U/E | V | V | V/U/E | V |
| 02/03_PUBLISHED | V | V/U/E | V | V | V | V | V |
| 02/04_ARCHIVE | V | V/U/E | V | V | V | V | V |
| 03 Design Packages | V | V/U/E | V/U | V | V | V | V |
| 04 Construction | V | V/U/E | V/U/E | V | V/U/E | V | V/U/E* |
| 05 Statutory | V | V/U/E | V/U | V | V | V/U** | V |
| 06 Tender & Change | V | V/U/E | V/U | V/U/E | V | V | V |
| 07 Handover | V | V/U/E | V/U | V | V/U | V | V |
| 08 Reference | V | V/U/E | V | V | V | V | V |

\*仅指定团队/专业子目录（Consultant 对 WIP 默认可 View 他队；写权限仅本队）  
\*\*仅其负责提交包

## 5. 配置明细附录（可直接实施）

### 5.10 协同节奏与状态映射（可直接执行）

#### 适用性状态（SuitabilityStatus）

| 码 | 含义 | 典型目录 |
|----|------|----------|
| S0 | WIP | `01_WIP` |
| S1 | Suitable for Coordination（模型可被链接） | `02_SHARED` |
| S2 | Suitable for Information | `02_SHARED` |
| S3 | Suitable for Review & Comment | `02_SHARED` |
| S4 | Suitable for Milestone Approval | `02_SHARED` → 待 Published |
| A3–A6 | 合同/阶段批准（Concept→Construction） | `03_PUBLISHED` |
| CP | Compliance（规划/消防/BD 等合规） | Statutory / Published |
| CR | Handover / As-constructed | `07_Handover` |

#### 推荐节奏（实施建议）

| 活动 | 频率 | 责任 |
|------|------|------|
| 作者 Sync / 自协调 | 持续 | Information Author |
| 内部协调会 | 每周 | BIM Coordinator |
| Shared 冻结上传 | 每 2–3 周 | Task Team → BIM Manager |
| 联邦模型更新 + Clash 报告 | 每次 Shared 后 | BIM Manager |
| Client / Owner 正式审查 | 按里程碑 / 建议每月 | GC_Management |

#### Shared 前自检（作者必做）

1. 文件名九段合规，且与属性一致  
2. `SuitabilityStatus` 拟设为 S1–S3（模型协调用 S1）  
3. `Revision` 已更新；点修订进入 Shared 应收拢为整修订（如 P01.05→P01）  
4. 无未关闭本专业 High Clash（或已登记 Issue）  
5. Splash/封面注明日期与变更摘要（模型建议）

## 5. 配置明细附录（可直接实施）

### 5.11 EMSD 资产分类（Buildings 默认启用）

源表：`Real case refs/EMSD_AIR_v2_Tandem_Classification.xlsx`（副本亦应放入 `08/.../EMSD_AIR`）

| 项 | 要求 |
|----|------|
| 用途 | 运维/移交资产类型；可导入 Autodesk Tandem |
| 层级 | L1 系统族（37）+ L2 设备类型（232） |
| 模型参数 | Shared Parameter / 属性 `EMSD_Code` = **原 EMSD 码**（如 `HVAC-AHU`） |
| Tandem | 用表内 Mapping 转为累积码（如 `HVAC-AS-AHU`） |
| 与 Naming System | **禁止混用**：Naming System=出图工作包；EMSD=资产分类 |

Buildings 高频 L1（开项即启用）：
`HVAC-AS` / `HVAC-WS` / `EL` / `LTG` / `LVS` / `GEN` / `UPS-UPS` / `FS-AFA` / `FS-WTS` / `LAE` / `ACS-ACS` / `CCTV-CCTV` / `BLR`

移交门禁：`07_Handover/Asset_Information` 中关键设备清单每行必须有 `EMSD_Code`。

## 5. 配置明细附录（可直接实施）

### 5.12 MIDP 控制（最小可运行）

在 `02_SHARED/8_BIM/1_BIM_DOCUMENTS/` 维护项目 MIDP（Excel 即可），每行一个交付物：

| 列 | 说明 |
|----|------|
| Delivery Title | 交付物名称 |
| Originator / Building / Zone / Level / Type / Role / System / Number | 与命名一致 |
| Milestone-1…N | Y/N（该里程碑是否必须交付） |

规则：
- Lead / GC BIM Manager 汇总；各 Task Team 维护本专业行  
- 进入 **WF-B Published** 前，当前里程碑 Y 项必须有对应已发布文件  
- 变更范围时同步改 MIDP，并留版本

---
