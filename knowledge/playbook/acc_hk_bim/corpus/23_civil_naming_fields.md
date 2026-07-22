---
capability: naming
domain: civil
title: "Civil 命名与自定义字段"
title_en: "Civil naming and custom fields"
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
# Civil 命名与自定义字段

> 来源：`output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md` · domain=`civil` · capability=`naming`

## 5. 配置明细附录（可直接实施）

### 5.5 Naming Rules（含正反例）

#### 权威结构（与 Buildings 同构，便于跨项目培训）

```text
Project - Originator - Building - Zone - Level - Type - Role - System - Number
```

Civil 字段映射：
- **Building** = 区段码（`SEA`/`SEB`/`ZZZ`…），与 `Section` 属性一致  
- **Level** = 标高/层或里程相关码；也可用 `XXX`，另用属性 `Chainage` 表达里程范围  
- **Zone** = 区段内分区；`ZZ`/`XX` 规则同 Buildings  

硬性规则同 Buildings：仅 `-`、UPPER CASE、ID 不可改、Revision/Status **不进文件名**。

| 字段 | 规则 |
|------|------|
| Project | 项目码 |
| Originator | 3 位组织码 |
| Building | 区段码（SEC 压缩为 3 位，如 `SEA`） |
| Zone | 2 位 |
| Level | 3 位或 `XXX`/`ZZZ` |
| Type | 见下表 |
| Role | C/R/G/T/M/S/E/W/X/BM… |
| System | 出图工作包（道路/排水/结构…）；≠ EMSD |
| Number | 4 位 |

#### Type（最小必用集）

`M3` `M2` `CM` `CR` `DR` `SC` `RP` `SP` `SH` `ST` `SU` `MS` `IR` `SN` + 项目约定 `SUB`

#### Role（Civil 常用）

| Code | 含义 |
|------|------|
| C | Civil 综合 |
| R | Roads / Highways |
| G | Geotechnical |
| T | Traffic |
| M / E / P | MEP（场站/泵房等） |
| S | Structural |
| D | Drainage |
| W | Contractor / GC |
| X | Subcon |
| BM | BIM Management |
| K | Client |

#### System（最小必用集；完整表放 Project Codes）

| Code | 含义 |
|------|------|
| XXX | 不适用 |
| 010–080 | Site / Roads / Drainage / Services |
| 100–170 | Substructure / Foundations |
| 200–280 | Structure |
| 500–580 | Piped services |
| 600–680 | Electrical |

#### 正反例

正确：
- `PRJ001-ACL-SEB-ZZ-XXX-DR-R-040-1001`
- `PRJ001-ACL-SEA-01-L10-M3-C-100-0001`
- `PRJ001-GCX-ZZZ-ZZ-ZZZ-CM-BM-XXX-0001`

错误：
- `PRJ001-C-SECB01-MOD-000045-V01`（旧短格式）
- `SEC-B_model_final.rvt`
- 文件名含 `V02`/`S1`

## 5. 配置明细附录（可直接实施）

### 5.6 Custom Fields 字典（完整）

#### A. 命名拆解字段

| 字段 | 必填 | 说明 |
|------|------|------|
| Project / Originator / Building / Zone / Level / Type / Role / System / Number | Y | 与文件名一致；Building=区段 |

#### B. Civil 扩展与流程字段

| 字段 | 类型 | 必填 | 选项/说明 |
|------|------|------|-----------|
| Section | Select/Text | Y | 与 Building 同步（可读展示用 SECA） |
| Chainage | Text | 建议 | 里程范围 |
| ContractPackage | Select/Text | Y | 合约包 |
| SuitabilityStatus | Select | Y | S0/S1/S2/S3/S4/A*/CP/CR |
| Revision | Text | Y | P##[.##] / C## |
| SubmissionType | Select | Y | Internal / Client / LandsD / OtherAuthority |
| DeliverableStage | Select | Y | WIP / Shared / Published / Statutory / Handover |
| RequiresApproval | Boolean | Y | Yes / No |
| ApprovalWorkflowId | Select | 条件必填 | WF-A/B/C/D |
| StatutoryRelated | Boolean | Y | Yes / No |
| SoftwareVersion | Text | 条件必填 | 模型/提交包 |
| MilestoneID | Select/Text | 建议 | 对齐 MIDP |
| EMSD_Code | Select/Text | 条件必填 | 机电设备对象 |
| AssetClass | Select/Text | 建议 | 土木/道路/排水等非 EMSD 资产 |
