---
capability: workflow
domain: buildings
title: "Buildings 表单与 BD 法定提交"
title_en: "Buildings forms and BD statutory submission"
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
# Buildings 表单与 BD 法定提交

> 来源：`output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md` · domain=`buildings` · capability=`workflow`

## 5. 配置明细附录（可直接实施）

### 5.7 Forms 明细（检查项级）

#### EIR Clause Check
- 信息要求条款是否覆盖设计/施工阶段
- 责任方与交付节点是否明确
- 通过标准：关键条款全部勾选且无 Open 缺口

#### BEP Milestone Review
- 里程碑是否按期
- 软件版本与协同规则是否更新
- Shared 冻结节奏（2–3 周）是否执行
- 通过标准：当前阶段里程碑全部 Closed 或有批准延期

#### MIDP Delivery Check（强制，进 Published 前）
- 本里程碑 MIDP 行是否已标记 Y 且文件已上传
- Type/Role/System/Number 与 MIDP 一致
- 通过标准：当前里程碑无缺失必交项

#### BD Submission Checklist（强制）
- 法定图则与 BIM 补充是否区分
- 图号/版本一致
- 软件版本符合 ADM-19/ADV-34 口径
- 通过标准：全部必选勾选 = Pass，否则不可进 WF-C

#### 2D/3D Consistency Check（强制）
- 关键几何/标注冲突已清理
- 差异项已记录并有责任人
- 通过标准：无未关闭 High 差异

#### Building Handover Checklist
- As-built / O&M / Defect List 齐备
- 关键资产 `EMSD_Code` 已填并可导出
- 未关闭缺陷已分类并有计划
- 通过标准：Owner 可验收项全部完成

#### Defect Rectification Checklist
- 缺陷描述、位置、证据、复检结果完整
- 通过标准：对应 Issue 可转 Ready to Close

#### Project Close-out Checklist
- 合同交付物、归档、权限收敛完成
- 通过标准：Close-out 无 Open 阻断项

## 5. 配置明细附录（可直接实施）

### 5.8 BD 法定提交包明细

目标目录：`05_Statutory Submission/BD Submission`

提交包最少包含：
1. 法定图则包（Statutory Drawings）
2. BIM Supporting Files（补充）
3. 已完成的 `BD Submission Checklist`
4. 已完成的 `2D/3D Consistency Check`
5. 版本记录（Revision / SoftwareVersion / StatutoryRefNo）

原则：
- 图纸为准，BIM 为补充
- 驳回后必须升版重提

## 5. 配置明细附录（可直接实施）

### 5.9 后台配置顺序（可照做）

1. Hub 准备 Roles：Owner / GC_* / Consultant / Subcon  
2. 将 EMSD 码表与 Project Codes 放入 `08_Reference & Standards`  
3. Forma Data Management → Files：建目录（5.1）  
4. Forma Data Management → Files：配权限（5.2）  
5. Forma Data Management → Files：Naming Standards（5.5）  
6. Forma Data Management → Files：Attributes（5.6，含 SuitabilityStatus / EMSD_Code）  
7. Forma Data Management → Reviews：WF-A/B/C/D（5.4）  
8. Forma Data Management / Forma Build → Issues：Types/Categories/Fields/Status visibility（5.3）  
9. Forma Build → Forms：建立 8 张表单（5.7）  
10. 建立项目 MIDP 表（可用 Excel，存 `02_SHARED/8_BIM/1_BIM_DOCUMENTS`）  
11. （可选）Forma Design Collaboration：绑定 `02_SHARED`  
12. 按第 6 章验收
