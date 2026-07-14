# ACC 香港本土模板（General Contractor 版）

本指南用于在 Autodesk Construction Cloud (ACC) 中建立一套适用于香港项目的总承包商（General Contractor, GC）项目模板。目标是让新项目可以快速复制统一的资料结构、权限规则、命名标准与交付检查流程。

---

## 1. 模板定位与范围

**适用对象**
- 香港本地项目的总承包商团队（工务与私营均可按需裁剪）。
- 需要统一管理设计资料、施工过程、分包协作、法定/合约交付文件的项目。

**目标**
- 固化资料夹结构（含 WIP/Shared/Published/Archive）。
- 固化角色权限矩阵（GC、分包、顾问、业主）。
- 固化命名规则与版本追踪。
- 固化关键表单（EIR/BEP、交付检查、收尾检查）。

---

## 2. 建模原则（香港本地化）

- **合规优先**：优先对齐 DEVB、CIC、BD、LandsD 相关要求。
- **交付导向**：以“标书/合约交付”“设计交付”“竣工交付”为主线组织资料。
- **最小可用模板**：先上线 Docs + 权限 + 命名 + Forms 基础集，再迭代 Build 细节。
- **中英并列命名**：建议关键资料夹采用中英并列，便于跨团队协作。

---

## 3. 建议产品启用范围（GC 最小集）

在模板 `Products and tools` 中建议启用：
- Autodesk Docs（必选）
- Autodesk Build（建议）
- Design Collaboration（有设计协同时启用）
- Takeoff / Cost（有算量或成本管理需求时启用）

不确定是否使用的产品先关闭，避免项目启动后界面过重。

---

## 4. Docs 资料夹结构（GC 推荐）

建议在 `Project Files/` 下建立：

```text
Project Files/
├── 01_项目治理 Project Governance/
│   ├── 合约与商务 Contract & Commercial/
│   ├── 程序与制度 Procedures/
│   └── 会议与批示 Meetings & Instructions/
├── 02_设计协同 Design Coordination/
│   ├── WIP/
│   ├── Shared/
│   ├── Published/
│   └── Archive/
├── 03_施工与分包 Construction & Subcontractors/
│   ├── 施工方案 Method Statements/
│   ├── 检验与测试 ITP & Records/
│   ├── 现场签证 Site Instructions/
│   └── 分包交付 Subcontractor Deliverables/
├── 04_质量安全环保 QHSE/
│   ├── Quality/
│   ├── Safety/
│   └── Environmental/
├── 05_法定与政府提交 Statutory & Authority Submission/
│   ├── 提交 BD Submission/
│   ├── 提交 LandsD Submission/
│   └── 其他部门 Other Authorities/
├── 06_招标与变更 Tender & Change/
├── 07_竣工与移交 Handover & Closeout/
└── 08_参考与标准 Reference & Standards/
```

说明：
- 工务项目重点使用 `提交 LandsD` 与 TC 1/2025 相关交付资料。
- 私营项目重点使用 `提交 BD` 与 ADM-19/ADV-34 对应资料。
- `02_设计协同` 建议固定 WIP/Shared/Published/Archive 结构。

---

## 5. 权限矩阵（GC 角色建议）

先在模板中定义角色组（可映射为 Company + Role）：
- GC_Management（总包管理）
- GC_Engineering（总包工程/技术）
- Subcontractor（分包）
- Consultant（顾问）
- Client_Owner（业主/业代）

权限建议（示例）：
- `WIP`：仅 GC_Engineering 可编辑，分包按专业范围可编辑，顾问/业主默认不可写。
- `Shared`：GC 与顾问可读写，分包可读（必要时可提交子目录），业主可读。
- `Published`：仅 GC_Management 或授权角色发布，其他角色只读。
- `Statutory & Authority Submission`：仅法定交付小组可写，其他只读。
- `Handover & Closeout`：收尾阶段由 GC_Management 控制写权限。

重点：权限先“保守收敛”，再按项目需求逐步放开，避免早期误发布。

---

## 6. 命名规则（File Naming Standards）

建议字段包含：
- 项目代码（Project Code）
- 专业代码（A/S/M/C 等）
- 区域/楼层/分段（可选）
- 文件类型（DRW/MOD/RPT/SUB 等）
- 顺序号
- 版本号

示例：
- `PRJ001-A-DRW-000123-V02`
- `PRJ001-C-MOD-SECB01-000045-V01`

香港本地注意点：
- 对齐 DEVB 附录 VIII-IX-X 的命名思路。
- 涉及 BD 提交时，在资料夹说明中明确 ADM-19/ADV-34 格式与版本要求。

---

## 7. Forms 与检查清单（GC 必备）

建议至少配置以下 Form templates（可放 Account Library）：
- EIR 条款检查表
- BEP 里程碑审查表
- 标书 BIM 交付清单
- 合约化 BIM 版本确认表
- LandsD 提交检查表（工务项目）
- BD 提交检查表（私营项目）
- 项目收尾检查表（Closeout）

执行建议：
- 项目启动时完成一次“模板落地检查”。
- 每次重要交付前（招标/设计/竣工）执行对应检查表。

---

## 8. Issues 分类建议（GC 常用）

Issue Types 建议：
- Design Coordination
- Site Quality
- Site Safety
- RFI / Clarification
- Change / Variation
- Authority Submission

Issue Categories 建议：
- 建筑 / 结构 / 机电 / 土木
- 分包接口
- 法定提交
- 进度风险

Status 建议：
- Open → In Review → Action Required → Ready to Close → Closed

---

## 9. 实施节奏（建议 2 周）

**第 1 周**
- 完成模板最小集：资料夹、权限、命名、Forms。
- 用 1 个测试项目验证角色访问与版本流程。

**第 2 周**
- 加入 Build 的 Issues / Reports 规则。
- 根据试点反馈调整权限边界和命名字段。
- 发布 v1.0 并在新项目强制使用。

---

## 10. 与现有文档关系

- 本文档是 GC 版“执行指南”。
- 规范依据和法规映射：`HK_BIM_Digital_Delivery_ACC_Mapping.md`
- 启动与交付前核查：`HK_BIM_Digital_Delivery_ACC_Checklist.md`
- 通用框架参考：`ACC_HK_Project_Template_Guide.md`

---

## 11. 下一步可直接执行

- 在 ACC 中创建模板：`ACC HK GC Template`
- 按第 4~7 节完成配置并保存为账号级模板。
- 用一个真实在建项目复制模板进行 UAT。
- UAT 通过后冻结模板版本，进入变更管理（每月评审一次）。
