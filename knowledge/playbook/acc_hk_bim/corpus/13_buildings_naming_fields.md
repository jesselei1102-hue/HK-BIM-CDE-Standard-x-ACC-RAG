---
capability: naming
domain: buildings
title: "Buildings 命名与自定义字段"
title_en: "Buildings naming and custom fields"
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
# Buildings 命名与自定义字段

> 来源：`output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md` · domain=`buildings` · capability=`naming`

## 5. 配置明细附录（可直接实施）

### 5.5 Naming Rules（含正反例）

#### 权威结构（对齐 ISO19650 定制实践）

```text
Project - Originator - Building - Zone - Level - Type - Role - System - Number
```

硬性规则：
- 分隔符仅 `-`；全部 **UPPER CASE**
- CDE 中一旦分配 Unique ID，**文件名不可改**；后续修订同名
- **Revision / SuitabilityStatus / 描述标题不进文件名**（进 Forma Data Management 属性与图框）
- 文档类可选末尾 `_Description`（如 `_ConditionalSurvey`）

| 字段 | 长度 | 规则 |
|------|------|------|
| Project | 建议 6 | 项目统一码；写入 `08/.../Project Codes`；不得跨项目复用 |
| Originator | 3 | 产出组织码（签约前冻结） |
| Building | 3 | 楼栋/体量；`ZZZ`=全部，`XXX`=无 |
| Zone | 2 | 分区；`ZZ`=全部，`XX`=不适用；不得跨楼重叠 |
| Level | 3 | 层；`L10/L20…` 或项目层码；`ZZZ`=多层，`XXX`=无 |
| Type | 2 | 信息类型（见下表） |
| Role | 1–2 | 角色（见下表） |
| System | 3 | **文件/出图工作包**码（见下表）；≠ EMSD 资产码 |
| Number | 4 | 自 `0001`；保留前导零 |

#### Type（最小必用集；可按项目扩展）

| Code | 用途 |
|------|------|
| M3 | 3D 模型 |
| M2 | 2D / XREF |
| CM | 联邦模型 |
| CR | Clash rendition |
| DR | 图纸 |
| SC | 系统图 |
| RP | 报告 |
| SP | 规格 |
| SH | 表单/计划表 |
| ST | 标准/BEP/EIR |
| SU | 测量 |
| MS | Method statement |
| IR | Inspection report |
| SN | Snagging / Defect |
| SUB | 法定/正式提交包（项目扩展码，可用 `IE`/`IS` 替代时在码表注明） |

#### Role（最小必用集）

| Code | 含义 |
|------|------|
| A | Architect |
| S | Structural |
| M | Mechanical |
| E | Electrical |
| P | Public Health / Plumbing |
| C | Civil（若楼宇项目含外场） |
| W | Contractor / GC |
| X | Subcontractor |
| Y | Specialist |
| K | Client / Owner |
| BM | BIM Management |
| Z | General |

#### System（出图工作包，最小必用集）

| Code | 含义 |
|------|------|
| XXX | 无系统 / 不适用 |
| 200–280 | Structure（墙/楼板/楼梯/屋面/框架） |
| 300–370 | Completions（门窗/天花等） |
| 500–580 | Piped/Ducted（给排水/暖通/消防） |
| 600–680 | Electrical |
| 660 | Lifts |
| 010–080 | Site（外场时） |

> 完整码表放入 `08_Reference & Standards/Project Codes`。资产设备分类用 **EMSD**（5.11），不要写入本字段。

#### Number 首位建议（DR）

| 首位 | 用途 |
|------|------|
| 0 | General |
| 1 | Plans |
| 2 | Elevations |
| 3 | Sections |
| 5 | Details |
| 6 | Schedules |

#### 正反例

正确：
- `PRJ001-ACL-BA1-ZZ-L10-DR-A-310-1001`
- `PRJ001-ACL-BA1-02-L20-M3-M-570-0001`
- `PRJ001-GCX-ZZZ-ZZ-ZZZ-CM-BM-XXX-0001`
- `PRJ001-ACL-BA2-XX-XXX-RP-W-XXX-0001_ConditionalSurvey`

错误（应拒）：
- `PRJ001-A-DRW-000123-V02`（旧短格式；缺字段）
- `PRJ001 A DR L10`（空格）
- `final_model.rvt`（无规则）
- 文件名中带 `V02` / `S1`（应放属性）

## 5. 配置明细附录（可直接实施）

### 5.6 Custom Fields 字典（完整）

#### A. 命名拆解字段（Forma Data Management Attributes；上传必填）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Project | Text | Y | 与文件名一致 |
| Originator | Select/Text | Y | 组织码 |
| Building | Select/Text | Y | 楼栋码 |
| Zone | Select/Text | Y | 分区码 |
| Level | Select/Text | Y | 层码 |
| Type | Select | Y | 见 5.5 Type |
| Role | Select | Y | 见 5.5 Role |
| System | Select/Text | Y | 出图工作包码 |
| Number | Text | Y | 4 位 |

#### B. 状态与流程字段

| 字段 | 类型 | 必填 | 选项/说明 |
|------|------|------|-----------|
| SuitabilityStatus | Select | Y | S0 / S1 / S2 / S3 / S4 / A3 / A4 / A5 / A6 / CP / CR |
| Revision | Text | Y | `P01` / `P01.05` / `C01`（优先）；软件限制可用整数但须写入 BEP |
| SubmissionType | Select | Y | Internal / Client / BD / OtherAuthority |
| DeliverableStage | Select | Y | WIP / Shared / Published / Statutory / Handover |
| RequiresApproval | Boolean | Y | Yes / No |
| ApprovalWorkflowId | Select | 条件必填 | WF-A/B/C/D |
| StatutoryRelated | Boolean | Y | Yes / No |
| StatutoryRefNo | Text | 条件必填 | StatutoryRelated=Yes |
| SoftwareVersion | Text | 条件必填 | 模型/法定包建议必填 |
| MilestoneID | Select/Text | 建议 | 对齐 MIDP 里程碑 |

#### C. 资产字段（移交相关必填）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| EMSD_Code | Select/Text | 条件必填 | 设备/资产对象必填；见 5.11 |
| AssetTag | Text | 建议 | 现场资产标签 |

#### D. Buildings 可选扩展（默认非必填）

`BlockNo`、`FloorNo`、`UnitType`、`FlatNo`、`Area`、`PackageNo`
