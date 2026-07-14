---
capability: information_requirements
title: "信息要求落地 (OIR/AIR/PIR/EIR)"
title_en: "Information Requirements Implementation"
authority_refs:
  - "ISO 19650-1:2018 §5-8 (Information requirements hierarchy)"
  - "ISO 19650-2:2018 §5.1-5.2 (EIR)"
  - "CICBIMS General 2024 §2 (Information Requirements)"
  - "DEVB BIM Harmonisation Guidelines v3.0 §2 (D1-D9 fields)"
related_product_guids:
  - "Getting_Started_Administration"
  - "Reviews_Create_Edit"
version: "2.0"
date: "2026-07-13"
disclaimer: "ACC 沒有 OIR/PIR 原生對象。本章說明如何在 ACC 中落地執行信息要求，而非管理信息要求定義本身。"
---

# 07 — 信息要求落地 (Information Requirements Implementation)

---

## 1. 信息要求層級概覽

ISO 19650 定義了一個從組織到項目的信息要求層級：

```
OIR (Organizational Information Requirements)
 │    組織層面：業主做決策需要什麼信息？
 │
 ├── AIR (Asset Information Requirements)
 │    資產層面：運維階段需要什麼信息？
 │
 └── PIR (Project Information Requirements)
      項目層面：回答 OIR/AIR 需要在本項目收集什麼？
      │
      └── EIR (Exchange Information Requirements)
           交換層面：各方如何生產和交付信息？
           │
           ├── 信息標準 (Information Standard)
           ├── 信息生產方法 (Production Methods)
           └── 信息交換的管理流程 (Management Process)
```

---

## 2. 各層要求的定義與 ACC 角色

### 2.1 OIR — 組織信息要求

| 維度 | 說明 |
|------|------|
| **定義者** | Appointing Party（業主/客戶）的組織策略層 |
| **內容** | 組織為了運營決策需要收集什麼信息（如設施管理、投資回報分析） |
| **格式** | 通常是策略文件 / 標準 |
| **ACC 角色** | ❌ ACC 不處理 OIR 邏輯<br>✅ ACC 存儲 OIR 文件：`06_Reference/Client_Requirements/OIR/` |
| **誰負責** | 客戶組織（非項目層面） |

### 2.2 AIR — 資產信息要求

| 維度 | 說明 |
|------|------|
| **定義者** | Appointing Party 的資產管理團隊 |
| **內容** | 資產運維需要什麼數據（如設備清單、維保信息、空間數據） |
| **格式** | 數據需求表 / COBie 模板 / 資產數據標準 |
| **ACC 角色** | ❌ ACC 不是資產管理系統<br>✅ ACC 存儲 AIR 參考文件：`06_Reference/Client_Requirements/AIR/` |
| **交付物** | 通常以 COBie / IFC + 屬性數據交付 |

### 2.3 PIR — 項目信息要求

| 維度 | 說明 |
|------|------|
| **定義者** | Appointing Party 的項目代表 |
| **內容** | 本項目需要回答哪些問題（如：1F 空間是否滿足人流分析？結構方案是否滿足預算？） |
| **格式** | BEP 中的 PIR 回應表 / 獨立文件 |
| **ACC 角色** | ❌ **ACC 沒有 PIR 原生對象**<br>✅ ACC 存儲 PIR 文件：`06_Reference/Standards/BEP/`<br>✅ Approval Workflow 作為 PIR 驗證節點 |
| **驗證** | 在關鍵 Gateway 檢查 PIR 是否已被回答 |

### 2.4 EIR — 交換信息要求

| 維度 | 說明 |
|------|------|
| **定義者** | Appointing Party（通常在 BEP 合同附件中） |
| **內容** | 約束各方如何生產/交換信息 |
| **格式** | BEP 的核心內容 + ACC 配置 |
| **ACC 角色** | ✅ **EIR 的執行面由 ACC 功能分散承載** |

---

## 3. EIR 在 ACC 中的分散落地

EIR 是唯一在 ACC 中有 **大量功能承載** 的信息要求。其三部分落地如下：

### 3.1 信息標準 (Information Standard)

| EIR 要求 | ACC 實現 | 本手冊章節 |
|----------|----------|-----------|
| 命名規範 | Naming Standards 功能 | 03_naming |
| LOD / LOI 定義 | BEP 文件 + Review 時驗證 | 本文 §5 |
| 坐標/單位 | 項目設置 + Revit 模板 | 01_project_setup |
| 文件格式 | BEP 約定 + 上傳時檢查 | 03_naming |
| 分類系統 | Custom Attributes / 模型內 | 本文 §5 |

### 3.2 信息生產方法 (Production Methods)

| EIR 要求 | ACC 實現 | 本手冊章節 |
|----------|----------|-----------|
| CDE 容器結構 | 文件夾結構 | 02_folder_cde |
| 模型拆分策略 | Design Collaboration Teams | 06_design_collab |
| 協同方法（軟件） | DC + Model Coordination | 06_design_collab |
| 碰撞管理流程 | Clash Detection + Issues | 06_design_collab §5 |

### 3.3 信息交換管理流程 (Management Process)

| EIR 要求 | ACC 實現 | 本手冊章節 |
|----------|----------|-----------|
| Gateway 審批流程 | Approval Workflow + 遷夾紀律 | 05_workflow |
| 狀態碼管理 | Custom Attributes + 命名 | 03_naming / 02_folder_cde |
| 發佈/Transmittal | Docs → Transmittals | 05_workflow §6 |
| 審計追蹤 | Activity Log + Workflow History | 05_workflow §7 |
| 權限控制 | Folder Permissions | 04_permissions |

---

## 4. DEVB Harmonisation v3 D1-D9 字段與信息要求

DEVB BIM Harmonisation Guidelines v3.0 §2 定義了 D1-D9 數據字段精煉：

| 字段 | 內容 | ACC 落地 |
|------|------|----------|
| D1 | 項目基本信息 | Project Settings |
| D2 | 信息交換時間表 | BEP + Project Schedule |
| D3 | 命名規範 | Naming Standards |
| D4 | CDE 容器定義 | 文件夾結構 |
| D5 | LOD/LOI 要求 | BEP 文件（ACC 存儲） |
| D6 | 信息交換格式 | BEP 約定 |
| D7 | 碰撞管理 | Model Coordination 配置 |
| D8 | 竣工提交要求 | BEP + LandsD 格式（見 00_overview §5） |
| D9 | 安全信息要求 | 權限設置 + 敏感夾 |

> 這些字段大部分落在 **BEP 文件** 中，ACC 的角色是 **執行和存儲**，不是定義。

---

## 5. LOD/LOI 驗證在 ACC 中的實現

### 5.1 概念

- **LOD (Level of Development)** = LOD-G (圖形精度) + LOD-I (信息精度)
- CICBIMS 2024 和 Harmonisation v3 定義各階段 LOD 要求
- ACC **沒有** 原生 LOD 驗證功能

### 5.2 推薦驗證方式

| 方式 | 實現 | 自動化 |
|------|------|--------|
| Review Workflow 中人工檢查 | Reviewer 對照 LOD 表格驗證 | 人工 |
| Clash Detection 驗證幾何精度 | 間接：模型不夠精細會導致碰撞 | 半自動 |
| 模型審核工具（如 Solibri） | 外部工具導出報告 → 上傳 ACC | 半自動 |
| Custom Attribute 標記 | 為文件添加 `LOD_Achieved` 屬性 | 人工記錄 |
| BIM Manager 在 Gateway 驗證 | Gateway 2 的 Step 1 中包含 LOD 檢查 | 人工 |

### 5.3 缺口

> ACC 不是模型內容驗證工具。LOD 合規性驗證主要靠：
> 1. BIM Manager 在審批流程中的人工判斷
> 2. 外部工具（Solibri / Navisworks / 自定義腳本）的報告
> 3. 碰撞檢測的間接驗證
>
> BEP 須約定 LOD 驗證的責任人、工具和節點。

---

## 6. 信息要求文件的存放與管理

### 6.1 推薦存放結構

```
06_Reference/
├── Standards/
│   ├── BEP/
│   │   ├── BEP_v1.0.pdf           ← 項目 BIM Execution Plan
│   │   ├── PIR_Response_Matrix.xlsx ← PIR 回應矩陣
│   │   └── EIR_Appendix.pdf       ← EIR 附件
│   ├── CICBIMS_2024.pdf
│   ├── Harmonisation_v3.pdf
│   └── ISO_19650_Summary.pdf
│
└── Client_Requirements/
    ├── OIR/
    │   └── Client_OIR_v1.0.pdf
    ├── AIR/
    │   ├── Asset_Data_Requirements.xlsx
    │   └── COBie_Template.xlsx
    └── Contract_BIM_Requirements.pdf
```

### 6.2 版本管理

- BEP 和信息要求文件有版本更新時，新版本上傳覆蓋（ACC 保留版本歷史）
- 通過 Custom Attribute 標記 `Document_Version` = `v1.0`

---

## 7. 信息交換時間表 (Information Exchange Schedule)

### 7.1 概念

EIR 通常定義各階段交付的信息包 (Information Deliverable)：

| 項目階段 | 主要交付 | 狀態 |
|----------|----------|------|
| Concept Design | 概念模型 (LOD 100-200) | S2 → A1 |
| Preliminary Design | 初步設計模型 + 圖紙 | S4 → A2 |
| Detailed Design | 詳細設計全套 | S4 → A3 |
| For Construction | 施工圖 + 碰撞清零 | A4 |
| As-Built | 竣工模型 + COBie | A6 / CR |

### 7.2 在 ACC 中跟蹤

- 使用 **Insight** 模塊監控文件上傳進度
- 對照信息交換時間表（存放在 BEP 中）跟蹤
- ACC **不提供** 原生的交付里程碑管理——這通常在項目管理軟件中處理

---

## 8. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | BEP 已上傳到 `06_Reference/Standards/BEP/` | ☐ |
| 2 | OIR/AIR 文件已存放在 `Client_Requirements/` | ☐ |
| 3 | PIR Response Matrix 已在 BEP 中定義 | ☐ |
| 4 | EIR 三部分已分別映射到 ACC 配置（命名/容器/工作流） | ☐ |
| 5 | LOD 驗證責任人和方法已在 BEP 約定 | ☐ |
| 6 | 信息交換時間表已在 BEP 中定義 | ☐ |
| 7 | D1-D9 字段精煉已對照 Harmonisation 確認（政府工務） | ☐ |
| 8 | 團隊理解「ACC 是執行平台，不是信息要求定義系統」 | ☐ |

---

## 9. 缺口 / 需寫入 BEP 的事項

| 事項 | 缺口說明 | BEP 章節建議 |
|------|----------|-------------|
| PIR 管理系統 | ACC 無 PIR 原生對象；PIR 活在文檔中 | §2 Information Requirements |
| LOD 驗證工具 | ACC 不做模型內容驗證；須約定外部工具 | §5 Quality |
| 信息交換時間表跟蹤 | ACC 無里程碑管理；須與 PM 工具配合 | §6 Schedule |
| D1-D9 完整回應 | 需逐字段在 BEP 中回應 Harmonisation 要求 | §2 Information Requirements |
| OIR/AIR 更新機制 | 客戶更新 OIR/AIR 時如何通知項目團隊 | §2 Information Requirements |
| COBie 交付 | ACC 不原生支持 COBie 驗證；須用外部工具 | §8 Handover |

---

## 10. 核心原則總結

> 1. **OIR/AIR/PIR 是「問題」**——它們定義需要什麼信息。  
> 2. **EIR 是「規則」**——它約束信息如何被生產和交換。  
> 3. **ACC 是「過程引擎」**——它執行 EIR 中的過程要求（命名、審批、權限、版本），並存儲產出的信息容器。  
> 4. **ACC 不是信息要求管理系統**——PIR 的定義和追蹤超出 ACC 能力範圍。  
> 5. **BEP 是橋樑**——它把 OIR/AIR/PIR 翻譯成 EIR，再翻譯成 ACC 配置。
