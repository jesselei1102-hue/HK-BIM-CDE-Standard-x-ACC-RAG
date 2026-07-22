---
capability: workflow
domain: civil
title: "Civil 表单与 LandsD/工务提交"
title_en: "Civil forms and LandsD / works submission"
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
# Civil 表单与 LandsD/工务提交

> 来源：`output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md` · domain=`civil` · capability=`workflow`

## 5. 配置明细附录（可直接实施）

### 5.7 Forms 明细（检查项级）

#### EIR Clause Check
- 区段交付要求是否覆盖；责任与节点是否明确

#### BEP Milestone Review
- 里程碑、软件、协同规则、Shared 冻结节奏是否更新

#### MIDP Delivery Check（强制，进 Published 前）
- 当前里程碑 Y 项是否已上传且命名字段一致

#### LandsD Completeness Check（强制）
- DESIGN/AS-BUILT 路径正确
- HARMONISED/NON-HARMONISED 标识正确
- 主 BIM 格式存在
- 通过标准：全部必选 Pass，否则不可 WF-C

#### Project Boundary & Model File List Check（强制）
- `PROJECT_BOUNDARY` 存在且版本有效
- `MODEL_FILE_LIST` 与实际模型一致

#### Tender BIM Deliverable Checklist（工务适用）
- 标书 BIM 与图则对应关系清楚；合约化版本已确认

#### Civil Handover Checklist
- As-built、Asset Information、Defect List 齐备
- 适用设备 `EMSD_Code` / 土木 `AssetClass` 已填

#### Defect Rectification Checklist
- 缺陷位置（含 Section）、证据、复检结果完整

#### Project Close-out Checklist
- 归档、权限收敛、未完事项清零

## 5. 配置明细附录（可直接实施）

### 5.8 LandsD / 工务提交包明细

目标目录：`05_Statutory Submission/LandsD Submission`

最少包含：
1. DESIGN 或 AS-BUILT 对应模型/资料
2. HARMONISED 或 NON-HARMONISED 标识路径
3. `PROJECT_BOUNDARY`
4. `MODEL_FILE_LIST`
5. （如适用）`PROJECT_SPECIFIC_CODE`
6. 已完成强制检查表
7. Revision / SoftwareVersion 记录

## 5. 配置明细附录（可直接实施）

### 5.9 后台配置顺序（可照做）

1. Hub Roles 准备  
2. 放入 EMSD（适用子集）与 Project Codes（含 SEC 码）  
3. Forma Data Management 建目录（5.1）  
4. Forma Data Management 配权限（5.2）  
5. Naming + Attributes（5.5/5.6）  
6. Reviews WF-A/B/C/D（5.4）  
7. Issues（5.3）  
8. Forma Build Forms（5.7）  
9. MIDP（5.12）  
10. （可选）Forma Design Collaboration 绑定 `02_SHARED`  
11. 第 6 章验收
