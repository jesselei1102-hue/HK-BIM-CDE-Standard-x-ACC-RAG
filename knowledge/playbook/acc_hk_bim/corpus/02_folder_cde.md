---
capability: folder_cde
title: "文件夾結構 / CDE 容器"
title_en: "Folder Structure / CDE Containers"
authority_refs:
  - "ISO 19650-1:2018 §12 (Common Data Environment)"
  - "CICBIMS General 2024 §4 (CDE)"
  - "CIC CDE Beginner Guide §3"
  - "DEVB BIM Harmonisation Guidelines v3.0 §3"
related_product_guids:
  - "Organize_files_With_Folders"
  - "Create_Manage_Custom_Attributes"
  - "Edit_Attribute_Values_Docs"
version: "2.0"
date: "2026-07-13"
disclaimer: "文件夾樹為組織推薦默認值，非 CIC/DEVB 官方 ACC 模板。"
---

# 02 — 文件夾結構 / CDE 容器 (Folder Structure / CDE Containers)

---

## 1. CDE 四容器概念回顧

ISO 19650-1 §12 定義四個信息容器狀態：

| 容器 | 含義 | 可見性 | 狀態碼範圍 |
|------|------|--------|-----------|
| **Work in Progress (WIP)** | 正在編制中 | 僅所屬 Task Team | S0 |
| **Shared** | 已檢查，適合跨團隊使用 | 所有相關 Task Teams | S1–S4 |
| **Published** | 經正式審批，適合用途（施工/制造等） | 全部授權人員 | A1–A6, B1–B5 |
| **Archive** | 已被取代或最終記錄 | 全部（只讀） | CR |

> **CIC CDE Beginner Guide** 強調：CDE 不等於文件夾——它是 **管理機制**。ACC 用文件夾 + 權限 + 工作流 **模擬** 容器行為，但不是原生狀態機。

---

## 2. WIP 容器配置

### 2.1 文件夾結構

```
Project Files/
└── 01_WIP/
    ├── ARC/          ← Architecture
    │   ├── Models/
    │   │   ├── Central_Models/
    │   │   └── Working_Models/
    │   ├── Drawings/
    │   ├── Schedules/
    │   ├── Reports/
    │   └── Specifications/
    ├── STR/          ← Structural
    │   └── (同上結構)
    ├── MEP/          ← MEP
    │   └── (同上結構)
    ├── CIV/          ← Civil
    ├── LAN/          ← Landscape
    ├── GEO/          ← Geotechnical
    └── SUR/          ← Survey
```

### 2.2 WIP 配置原則

| 原則 | 實現方式 | 缺口 |
|------|----------|------|
| 僅所屬團隊可見 | 文件夾級權限隔離（見 04_permissions） | — |
| 命名不強制 | 不在 WIP 啟用 Naming Standard | 須在 BEP 寫明：WIP 內自由命名的邊界 |
| 允許快速迭代 | 不設審批工作流 | — |
| 不計入正式交付 | WIP 文件不出現在 Transmittal | — |

---

## 3. Shared 容器配置

### 3.1 文件夾結構

```
Project Files/
└── 02_Shared/
    ├── ARC/
    ├── STR/
    ├── MEP/
    ├── CIV/
    ├── LAN/
    ├── GEO/
    └── SUR/
```

### 3.2 Shared 配置原則

| 原則 | 實現方式 | 缺口 |
|------|----------|------|
| 跨團隊可見 | 所有專業 View + Download | — |
| 只有通過審核的文件可進入 | **人工遷夾紀律**：Document Controller 將已審核文件從 WIP 複製到 Shared | ACC **不會** 在 Workflow Approve 後自動遷移文件；須人工操作或 API 腳本 |
| 命名規範強制 | 啟用 Naming Standard | — |
| 每次進入都有記錄 | Version History + 審批工作流記錄 | — |

### 3.3 「進入 Shared」操作流程

```
1. Designer 在 WIP 完成文件
2. Designer 通知 BIM Coordinator 文件已就緒
3. BIM Coordinator 審查（可在 WIP 內做 Review）
4. 審查通過 → Document Controller 手動複製文件到 02_Shared/{Discipline}/
5. Document Controller 更新文件 Custom Attribute: Status = S1/S2
6. （可選）在 02_Shared 夾的 Auto-trigger Review 再次確認命名合規
```

> ⚠️ **不可寫成「Approve 後自動複製到 Shared」**——ACC Docs Approval Workflow 完成後的 action 僅限通知，**不含自動遷夾**。如需自動化，須用 ACC API/Webhook 二次開發。

---

## 4. Published 容器配置

### 4.1 文件夾結構

```
Project Files/
└── 03_Published/
    ├── For_Information/        ← Status A1
    ├── For_Coordination/       ← 協調用途
    ├── For_Approval/           ← Status A3（待客戶審批）
    ├── For_Construction/       ← Status A4 / B1
    ├── For_Manufacture/        ← Status A5
    └── As_Built/               ← Status A6 / CR
```

### 4.2 Published 配置原則

| 原則 | 實現方式 | 缺口 |
|------|----------|------|
| 經正式審批才能進入 | Multi-step Approval Workflow（見 05_workflow） | — |
| 全部授權人員可見（含承建商） | 權限設置（見 04_permissions） | — |
| 命名規範強制 | Naming Standard + 人工驗證 | — |
| 可出 Transmittal | 從 Published 文件夾選取文件發送 | — |
| 文件進入後不可被 Designer 修改 | Published 文件夾 Designer 僅 View | — |

### 4.3 「進入 Published」操作流程

```
1. Design Lead 從 Shared 選取文件，發起 Formal Approval Workflow
2. Step 1: BIM Manager 技術審核
3. Step 2: Document Controller QA（命名/格式）
4. Step 3: Client Representative 審批
5. 全通過 → Document Controller 手動複製文件到 03_Published/{用途}/
6. Document Controller 更新 Status Attribute = A1/A4/A6 等
7. 原 Shared 版本保留（作為歷史記錄）
```

> ⚠️ 同理，遷夾動作為 **人工紀律**，非 Workflow 默認 action。

---

## 5. Archive 容器配置

### 5.1 文件夾結構

```
Project Files/
└── 04_Archive/
    ├── Superseded/        ← 被新版本取代的文件
    └── Final_Record/      ← 竣工/最終記錄
```

### 5.2 Archive 規則

| 規則 | 實現方式 |
|------|----------|
| 只讀 | 所有角色權限設為 View Only（含 BIM Manager） |
| 可追溯 | 保留完整 Version History |
| 歸檔觸發 | 當新版本進入 Published，舊版本由 DC 手動移至 Superseded |
| 項目結束 | 全部 Published 文件複製到 Final_Record |

> **缺口**：ACC 無「自動鎖定」或「自動歸檔」功能；所有 Archive 操作依賴 Document Controller 紀律。

---

## 6. 輔助文件夾

```
Project Files/
├── 05_Templates/
│   ├── BIM_Templates/       ← Revit/AutoCAD 模板
│   ├── Document_Templates/  ← Word/Excel 模板
│   └── Title_Blocks/        ← 圖框
│
└── 06_Reference/
    ├── Standards/           ← BEP, EIR, CICBIMS 文件
    │   └── BEP/
    ├── Client_Requirements/ ← OIR, AIR, 合同附件
    ├── Survey_Data/         ← 測量數據
    └── Existing_Conditions/ ← 現況資料
```

---

## 7. Custom Attributes 配置

**路徑：Project Admin → Docs Settings → Custom Attributes**

為 `02_Shared` 和 `03_Published` 文件夾配置：

| 屬性名稱 | 類型 | 值域 | 用途 |
|----------|------|------|------|
| `Status Code` | Dropdown | S0, S1, S2, S3, S4, A1-A6, B1-B5, CR | ISO 19650 狀態碼 |
| `Suitability` | Dropdown | 按項目定義 | 適用性代碼 |
| `Revision` | Text | P01, P02... C01, C02... | 顯式版本號 |
| `Discipline` | Dropdown | A, S, M, E, C, L, G, Q, T, F | 專業代碼 |
| `Originator` | Dropdown | 從 Company Short Code 列表 | 編制方 |
| `Approval Date` | Date | — | 審批日期 |
| `Supersedes` | Text | 被取代文件的 ID | 追溯鏈 |

### 7.1 狀態維護規則

> **關鍵缺口**：ACC Approval Workflow 完成後 **不會自動更新** Custom Attribute。  
> Status Code 由 Document Controller **手動更新**——這是操作紀律，不是系統自動行為。  
> 如需自動化，可通過 ACC API + Webhook 實現（二次開發）。

---

## 8. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | `01_WIP` 至 `04_Archive` 四個頂層夾已建立 | ☐ |
| 2 | 每個 CDE 容器下專業子夾已按項目建立 | ☐ |
| 3 | WIP 子夾含 Models/Drawings 等標準二級結構 | ☐ |
| 4 | Published 子夾按用途分（For_Construction 等） | ☐ |
| 5 | `05_Templates` 和 `06_Reference` 已建立並上傳模板/標準文件 | ☐ |
| 6 | Custom Attributes 已配置到 Shared/Published 文件夾 | ☐ |
| 7 | 試傳一個文件到 Shared，確認 Naming Standard 啟用 | ☐ |
| 8 | BEP 中已存放於 `06_Reference/Standards/BEP/` | ☐ |

---

## 9. 缺口 / 需寫入 BEP 的事項

| 事項 | 缺口說明 | BEP 章節建議 |
|------|----------|-------------|
| 容器遷移操作 | ACC 無自動遷夾；須約定由誰在何時操作 | §4 CDE Workflow |
| Status Attribute 維護 | 非系統自動；須約定 Document Controller 職責 | §4 CDE Workflow |
| WIP 命名自由度 | 須明確到什麼程度可不合規（如內部草稿 vs 提交審核版） | §3 Naming |
| 狀態表達雙軌 | 容器狀態 = 夾位置 + Attribute；須約定以何為準 | §4 CDE Workflow |
| Archive 鎖定 | ACC 無自動鎖定；須約定權限設置紀律 | §4 CDE Workflow |
| 非 ACC 文件 | 部分文件可能不在 ACC 管理（如 GIS 數據）；邊界須定義 | §1 Scope |
