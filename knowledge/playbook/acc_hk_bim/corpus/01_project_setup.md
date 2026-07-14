---
capability: project_setup
title: "賬戶與項目配置"
title_en: "Account & Project Setup"
authority_refs:
  - "CICBIMS General 2024 §2 (Roles & Responsibilities)"
  - "ISO 19650-2:2018 §5.1-5.3 (Appointment)"
  - "DEVB BIM Harmonisation Guidelines v3.0 §2"
related_product_guids:
  - "Getting_Started_Administration"
  - "Manage_Account_Members"
  - "Manage_Project_Members"
  - "Configure_Templates_Docs"
version: "2.0"
date: "2026-07-13"
disclaimer: "組織推薦配置，非 CIC/DEVB 官方模板。"
---

# 01 — 賬戶與項目配置 (Account & Project Setup)

---

## 1. 賬戶級配置 (Account Administration)

### 1.1 登入 Account Administration

1. 訪問 `https://acc.autodesk.com`
2. 以 Account Administrator 身份登入
3. 點擊左上角 **Account Admin** 進入管理後台

> **Product Help**: [Getting Started for Administration](https://help.autodesk.com/view/DOCS/ENU/?guid=Getting_Started_Administration)

### 1.2 基本賬戶設置

**路徑：Settings → Account Settings**

| 設置項 | 推薦配置 | 說明 |
|--------|----------|------|
| Account Name | `{公司名稱}-HK` | 清晰標識區域 |
| Default Currency | HKD | 本地成本管理 |
| Default Unit System | Metric | 香港使用公制 |
| Timezone | GMT+8 (Hong Kong) | 確保時間戳準確 |

### 1.3 公司 (Company) 管理

**路徑：Account Admin → Companies → + Add Company**

為每個參與方建立公司記錄：

| 字段 | 說明 | 示例 |
|------|------|------|
| Company Name | 公司全稱 | WSP (Asia) Limited |
| Short Code | Originator 代碼（2-6 字符） | `WSP` |
| Trade | 行業/專業 | Engineering Consultant |
| Type | 公司類型 | Consultant / Contractor / Client |

> **對齊 CICBIMS 2024 §3**：Short Code 即為命名規範中的 Originator 字段值，須在 BEP 中確認。

### 1.4 角色模板創建 (Roles)

**路徑：Account Admin → Roles → + Add Role**

| 角色名稱 | 項目訪問級別 | 對應 ISO 19650 角色 | 典型分配 |
|----------|-------------|-------------------|----------|
| `BIM Manager` | Project Admin | Information Manager | 項目 BIM 經理 |
| `BIM Coordinator` | Project Admin | Task Information Manager | 各專業 BIM 協調人 |
| `Document Controller` | Project Admin | — | 文控人員 |
| `Design Lead` | Project Member | Task Team Manager | 設計負責人 |
| `Designer` | Project Member | Task Team Member | 建模人員 |
| `Reviewer` | Project Member | — | 審圖人員 |
| `Client Representative` | Project Member | Appointing Party Rep | 客戶/業主代表 |
| `Contractor PM` | Project Member | Lead Appointed Party | 承建商項目經理 |
| `View Only` | Project Member | — | 僅查看 |

> **Product Help**: [How to Manage Roles](https://help.autodesk.com/view/DOCS/ENU/?guid=Manage_Account_Members)

### 1.5 成員邀請

**路徑：Account Admin → Members → + Invite Members**

1. 輸入成員郵箱
2. 選擇 Company
3. 分配 Role
4. 設定 Account-level 權限（一般為 Member）

---

## 2. 項目創建

### 2.0 優先：從項目樣板創建（推薦）

香港總承包 / Buildings 項目建議先配置 Account 級樣板，再批量開項。樣板目錄、權限、命名、審批與 Forms 見 **`08_project_template.md`**（`ACC HK GC Buildings Template`）。

**路徑：Account Admin → Project templates → Create project template**

| 路徑選擇 | 說明 |
|----------|------|
| 空白樣板 | 按第 08 章從零配置（推薦） |
| Save as template | 從已合規項目另存 |
| EMEA Sample | 僅部分資料區可用，需改為香港目錄與法定路徑 |

> **Product Help**: [Configure Project Templates for Autodesk Docs](https://help.autodesk.com/view/DOCS/ENU/?guid=Configure_Templates_Docs)

### 2.1 新建項目

**路徑：Account Admin → Projects → + Create Project**（可選已發佈的香港 GC 樣板）

| 字段 | 填寫建議 | 示例 |
|------|----------|------|
| Project Name | `{項目編碼} {項目名稱}` | `HK2026-001 MTR Station Extension` |
| Project Number | 合同/工務編號 | `CE/2026/001` |
| Project Type | 按實際選擇 | Infrastructure / Building |
| Start Date | 項目啟動日 | 2026-08-01 |
| End Date | 預計完工日 | 2029-12-31 |
| Address | 項目地址 | Hong Kong SAR |
| Currency | HKD | — |
| Unit System | Metric | — |

### 2.2 激活服務 (Services)

**路徑：Project Admin → Services**

| 服務 | 用途 | 是否必須 |
|------|------|----------|
| **Docs** | CDE / 文檔管理 | ✅ 必須 |
| **Design Collaboration** | Revit 雲協同 | ✅ 必須 |
| **Model Coordination** | 碰撞檢測 / 模型整合 | ✅ 必須 |
| **Insight** | 數據分析 | ⚡ 推薦 |
| **Build** | 施工管理 | 視階段 |
| **Cost** | 成本管理 | 視需求 |

### 2.3 項目設置

**路徑：Project Admin → Project Settings**

- **Timezone**: `(UTC+08:00) Hong Kong`
- **Project Image**: 上傳效果圖/識別圖

---

## 3. 項目成員與角色分配

### 3.1 添加項目成員

**路徑：Project Admin → Members → + Add**

1. 從 Account Members 中選擇（或邀請新成員）
2. 為每人分配 **Project Role**
3. 確認 **Access Level**（Project Admin / Project Member）

### 3.2 角色與 ISO 19650 映射

```
Appointing Party (業主)
  ├── Client Representative ← ACC: Client Rep (Project Member)
  └── Information Manager   ← ACC: BIM Manager (Project Admin)

Lead Appointed Party (總承建商/總顧問)
  ├── Project Manager       ← ACC: Contractor PM (Project Member)
  └── Task Information Mgr  ← ACC: BIM Coordinator (Project Admin)

Task Team (專業團隊)
  ├── Task Team Manager     ← ACC: Design Lead (Project Member)
  └── Task Team Members     ← ACC: Designer (Project Member)
```

> **缺口**：ACC 角色是 **權限概念**，不是組織架構。ISO 19650 的 Appointing Party / Lead Appointed Party 治理關係須在 BEP 文檔中明確，ACC 不提供原生治理層級。

---

## 4. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | Account Name / Timezone / Currency 已正確設置 | ☐ |
| 2 | 所有參與方公司已建立，Short Code 與 BEP 一致 | ☐ |
| 3 | 角色模板已按上表建立 | ☐ |
| 4 | 所有成員已邀請並分配 Company + Role | ☐ |
| 5 | 項目已創建，Project Number 與合同一致 | ☐ |
| 6 | Docs / Design Collaboration / Model Coordination 已啟用 | ☐ |
| 7 | Timezone 確認為 UTC+8 | ☐ |
| 8 | 至少 2 名 Project Admin（BIM Manager + Document Controller） | ☐ |

---

## 5. 缺口 / 需寫入 BEP 的事項

| 事項 | 說明 | BEP 章節建議 |
|------|------|-------------|
| ISO 角色治理 | ACC 角色 ≠ ISO 治理架構；須在 BEP 書面確認 Appointing Party 等 | §2 Organization |
| Short Code 唯一性 | 各 Originator 代碼不得重複；須在 BEP 附錄表格化 | §3 Naming |
| 離職/換人流程 | 當人員離場時如何轉移權限和 ownership | §2 Organization |
| 外部方（法定機構）接入 | 如 BD/FSD 審批人角色如何配置 | §2 Organization |
