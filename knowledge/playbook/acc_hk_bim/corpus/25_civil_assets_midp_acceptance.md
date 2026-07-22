---
capability: project_template
domain: civil
title: "Civil 资产/MIDP/验收"
title_en: "Civil assets, MIDP and acceptance"
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
# Civil 资产/MIDP/验收

> 来源：`output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md` · domain=`civil` · capability=`project_template`

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

## 6. 验收清单与来源追溯

### 6.1 项目级验收清单

- [ ] 01–08 及 LandsD 增强目录完整；`02` 含团队 WIP / Shared(+8_BIM) / Published / Archive
- [ ] 区段目录与 Section/Building 字段一致可用
- [ ] 权限抽测通过（Owner 不可见 WIP）
- [ ] WF-A/B/C/D 可走通（含驳回与自检门禁）
- [ ] WF-C 缺边界/模型清单可拦截
- [ ] Issue 9 Types 与字段可用
- [ ] 命名九段正例通过、反例可识别
- [ ] SuitabilityStatus / MIDP 抽检通过
- [ ] EMSD 子集或 AssetClass 移交样例可用
- [ ] 9 张 Forms 可发起并归档
- [ ] 四角色可按第 1–4 章完成主流程

### 6.2 来源追溯

| 配置主题 | 来源 |
|----------|------|
| 阶段逻辑与命名思路 | DEVB Harmonisation Guidelines v3.0；Real Case Naming/BEP |
| 九段命名 / Status / MIDP | Real Case File Naming Standard + MIDP |
| 协同节奏与联邦 | Real Case BEP；ACC Digital Delivery Workflow |
| LandsD 提交目录与必交件 | DEVB Appendix XIV；LandsD BIM/GIS Guidelines |
| EMSD 资产分类（适用子集） | EMSD AIR v2 → Tandem Classification |
| 工务标书 BIM 相关 | TC(W) No. 1/2025（按项目适用） |
| EIR/BEP | CIC BIM Standards / EIR Template |
| ACC / Forma 模板可配置范围 | Forma Data Management Project Templates；DOCS_help_006 / DOCS_help_003（历史帮助文档） |
| 案例分析详报 | `Real_Case_Refs_Sanitized_Analysis.md` |
| 内部映射与检查 | `HK_BIM_Digital_Delivery_ACC_Mapping.md`、`HK_BIM_Digital_Delivery_ACC_Checklist.md` |

本地规范目录：`ACC Template/specification/`  
真实案例参考：`Real case refs/`（含 EMSD AIR）
