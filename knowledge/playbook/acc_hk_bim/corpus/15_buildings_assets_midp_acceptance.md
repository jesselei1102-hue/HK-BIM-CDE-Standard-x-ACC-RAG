---
capability: project_template
domain: buildings
title: "Buildings 资产/MIDP/验收"
title_en: "Buildings assets, MIDP and acceptance"
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
# Buildings 资产/MIDP/验收

> 来源：`output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md` · domain=`buildings` · capability=`project_template`

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

## 6. 验收清单与来源追溯

### 6.1 项目级验收清单

- [ ] 01–08 目录完整；`02` 含 `01_WIP`（按团队）/`02_SHARED`（含 8_BIM）/`03_PUBLISHED`/`04_ARCHIVE`
- [ ] 权限矩阵按角色抽测通过（含 Owner 不可见 WIP）
- [ ] WF-A/B/C/D 均可走通（含驳回与自检门禁）
- [ ] WF-C 缺强制表单会被拦截
- [ ] Issue Types/Categories/Fields 可用
- [ ] 命名九段正例通过、反例可识别；Revision/Status 不进文件名
- [ ] SuitabilityStatus 与目录映射抽检通过（S0/S1/A/CP/CR）
- [ ] MIDP 已建立且当前里程碑可核对
- [ ] EMSD 码表已放入 08；移交样例含 `EMSD_Code`
- [ ] 8 张 Forms 可发起并归档
- [ ] 四角色均能按第 1–4 章完成主流程

### 6.2 来源追溯

| 配置主题 | 来源 |
|----------|------|
| 阶段逻辑 WIP/Shared/Published/Archive | DEVB Harmonisation；Real Case BEP/CDE |
| 九段命名 / Status / Revision | Real Case File Naming Standard（ISO19650 定制） |
| 协同节奏与联邦 | Real Case BEP-A/B；ACC Digital Delivery Workflow |
| MIDP | Real Case MIDP 实践 |
| EMSD 资产分类 | EMSD AIR v2 → Tandem Classification |
| BD 提交格式与一致性 | BD ADM-19、ADV-34 |
| EIR/BEP 管理 | CIC BIM Standards / EIR Template |
| 模板可配置范围 | Forma Data Management Project Templates |
| Buildings 配置基线 | `ACC_HK_GC_Buildings_Config_Plan.md` |
| 案例分析详报 | `Real_Case_Refs_Sanitized_Analysis.md` |

内部文件：
- `HK_BIM_Digital_Delivery_ACC_Mapping.md`
- `HK_BIM_Digital_Delivery_ACC_Checklist.md`
- `specification/` 下 BD/DEVB/CIC 资料
- `Real case refs/`（含 EMSD AIR）
