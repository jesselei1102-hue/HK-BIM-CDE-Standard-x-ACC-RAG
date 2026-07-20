---
capability: workflow
title: "審批工作流 / 信息流轉"
title_en: "Approval Workflows / Information Flow & Gateways"
authority_refs:
  - "ISO 19650-2:2018 §5.6 (Information gateway)"
  - "ISO 19650-1:2018 §12.2 (Container state transitions)"
  - "CICBIMS General 2024 §4.3 (CDE Workflow)"
  - "CIC CDE Beginner Guide §5 (Approval & Review)"
related_product_guids:
  - "Reviews_Create_Edit"
  - "Reviews_Workflow"
  - "Reviews_Start_Review"
  - "auto-trigger-reviews-docs"
  - "Transmittals"
  - "Create_Transmittal"
version: "2.1"
date: "2026-07-16"
disclaimer: "ACC Approval Workflow ≠ ISO 19650 Information Gateway 完整定義。Gateway 需 Workflow（含 Action Upon Completion）+ 容器/屬性約定 + 源夾清理紀律共同實現。產品能力以 Docs Reviews_Create_Edit 為準。"
---

# 05 — 審批工作流 / 信息流轉 (Approval Workflows / Information Flow & Gateways)

---

## 1. ISO 19650 Information Gateway 概念

**Information Gateway** = 信息從一個容器狀態轉移到下一個容器狀態的 **正式關卡**。

```
WIP ──[Gateway 1]──▶ Shared ──[Gateway 2]──▶ Published ──[Gateway 3]──▶ Archive
```

每個 Gateway 要求：
- 正式的審核/審批行為
- 記錄（誰、何時、結果）
- 狀態變更

### 1.1 ACC 如何近似實現 Gateway

| Gateway 組件 | ACC 實現方式 | 完整度 |
|---|---|---|
| 審批行為 | Approval Workflow (Reviews) | ✅ |
| 審計記錄 | Workflow history + Activity Log | ✅ |
| 狀態變更（文件夾） | Workflow **Action Upon Completion → Copy approved files** 至目標夾 | ✅ 可配置（**複製**，非移動） |
| 狀態變更（屬性） | Workflow **Action Upon Completion → Update attributes** | ✅ 可配置 |
| 源夾清理 / Archive | 源文件仍留在原夾；須 DC 紀律或二次流程 | ⚠️ 人工 |
| 跨頂層夾遷移 | 目標夾必須與源文件屬 **同一 top-level folder** | ⚠️ 約束 |

> **核心聲明**：ACC Approval Workflow 可在完成時 **自動複製已批准文件到目標文件夾，並更新屬性**（見 Docs `Reviews_Create_Edit` → Action Upon Completion）。完整 ISO Gateway 仍須在 BEP 約定：目標夾映射、屬性值、何時清理 WIP 源文件、以及 Reject 後不觸發複製。

---

## 2. 信息流轉總覽

```
Designer (WIP)
     │
     │ 提交審核
     ▼
┌─────────────────────────┐
│ Gateway 1: Internal     │  ACC: Internal Review Workflow
│ (WIP → Shared)          │  + Action Upon Completion:
│                         │    Copy approved → 02_Shared/...
│                         │  + Update attributes (Status → S1/S2)
└─────────────────────────┘
     │
     ▼
Shared (S1–S4)
     │
     │ 發起正式審批
     ▼
┌─────────────────────────┐
│ Gateway 2: Formal       │  ACC: Formal Approval Workflow
│ (Shared → Published)    │  + Action Upon Completion:
│                         │    Copy approved → 03_Published/...
│                         │  + Update attributes (Status → A1-A6)
└─────────────────────────┘
     │
     ▼
Published (A1–A6)
     │
     │ 被新版取代 / 項目結束
     ▼
┌─────────────────────────┐
│ Gateway 3: Archive      │  ACC: 通常仍由 DC 手動移至 Archive
│ (Published → Archive)   │  + 權限改 View Only
└─────────────────────────┘
```

---

## 3. Gateway 1: WIP → Shared (Internal Review)

### 3.1 工作流配置

**名稱**: `Internal Technical Review`  
**模板**: Two Step Approval

| 步驟 | 角色 | 動作 | 期限 |
|------|------|------|------|
| Step 1: Technical Review | BIM Coordinator | 檢查模型質量、LOD、碰撞 → Approve/Reject | 3 工作日 |
| Step 2: Lead Approval | Design Lead | 確認可供跨專業共享 → Approve/Reject | 2 工作日 |

**Action Upon Completion（建議開啟）**:
- **Copy approved files**: ON → `02_Shared/{Discipline}/`（或允許 Initiator 改目標夾）
- **When**: `All files in the review have been approved`（推薦；避免部分批准即複製）
- **Update attributes**: ON → 寫入 `Status Code` = S1/S2（及必要時 Revision）
- 目標夾可啟用 Naming Standard；若目標為 naming-standard enforced folder，Docs 會自動加入 Status / Revision related attributes

### 3.2 完整 Gateway 操作流程

| 步驟 | 操作者 | ACC 操作 | 自動/人工 |
|------|--------|----------|-----------|
| 1 | Designer | 在 WIP 完成文件，確認質量 | — |
| 2 | Designer | 發起 Internal Technical Review Workflow | 人工提交 |
| 3 | BIM Coordinator | 審核：檢查碰撞/LOD/規範 | 人工審核 |
| 4 | Design Lead | 確認可共享；必要時填 Required attributes | 人工確認 |
| 5 | System | **Copy approved files** → `02_Shared/{Discipline}/` | ✅ Workflow 可自動 |
| 6 | System | **Update attributes**（如 Status Code = S1/S2） | ✅ Workflow 可自動 |
| 7 | Document Controller | 清理/歸檔 WIP 源文件（複製不會刪源） | ⚠️ 人工紀律 |
| 8 | (Optional) System | Shared 文件夾 Auto-trigger 命名驗證 | ✅ 可自動 |

> ✅ Docs：**Action Upon Completion** 可在 Review 完成後複製已批准文件並更新屬性。  
> ⚠️ 仍是 **copy**（源夾保留原文件）；且目標夾必須與源文件在 **同一 top-level folder** 下。

### 3.3 Reject 處理

- Reject 時須附帶 Comment 說明原因
- 文件留在 WIP，Designer 修改後重新提交
- Reject 記錄保留在 Workflow History 中

---

## 4. Gateway 2: Shared → Published (Formal Approval)

### 4.1 工作流配置

**名稱**: `Formal Publication Approval`  
**模板**: Three Step Approval (或 Four Step Group Approval)

| 步驟 | 角色 | 檢查內容 | 期限 |
|------|------|----------|------|
| Step 1: Technical Design Review | BIM Manager | 設計合規性、標準符合度 | 5 工作日 |
| Step 2: QA Check | Document Controller | 命名規範、格式、元數據完整 | 3 工作日 |
| Step 3: Client Approval | Client Representative (Group) | 滿足合同/客戶要求 | 10 工作日 |

### 4.1.1 Action Upon Completion（建議開啟）

- **Copy approved files**: ON → `03_Published/{用途}/`
- **When**: `All files in the review have been approved`
- **Update attributes**: ON → `Status Code`（A1/A4/A6 等）、`Approval Date`；可設 **Required by approver**
- **Update attributes only for target folder** 或 **both target and source**（按 BEP 選擇）
- 可選：Include published markups / Allow approvers to change markups inclusion

### 4.2 完整 Gateway 操作流程

| 步驟 | 操作者 | ACC 操作 | 自動/人工 |
|------|--------|----------|-----------|
| 1 | Design Lead | 從 Shared 選取文件，發起 Formal Approval | 人工提交 |
| 2 | BIM Manager | 技術審核 | 人工 |
| 3 | Document Controller | QA 檢查（命名/格式） | 人工 |
| 4 | Client Rep | 客戶審批；填 Required attributes（如 Status/Date） | 人工 |
| 5 | System | **Copy approved files** → `03_Published/{用途}/` | ✅ Workflow 可自動 |
| 6 | System | **Update attributes**（Status / Approval Date 等） | ✅ Workflow 可自動 |
| 7 | Document Controller | 處理 Shared 源文件（保留/歸檔策略見 BEP） | ⚠️ 人工 |
| 8 | (Optional) | 發 Transmittal 通知接收方 | 人工 |

### 4.3 施工圖發佈加強版

**名稱**: `For Construction Issue`  
適用於 Status A4 的施工圖發佈，增加一步設計管理確認：

| 步驟 | 角色 | 內容 |
|------|------|------|
| Step 1 | Design Lead + BIM Coordinator | 設計完整性、碰撞已解決 |
| Step 2 | Document Controller | 命名/簽名/日期/格式 QA |
| Step 3 | Design Manager | 設計管理層確認 |
| Step 4 | Client/Engineer Rep (Group) | 最終審批 |

---

## 5. 創建審批工作流操作步驟

### 5.1 ACC 操作路徑

**路徑：Docs → Reviews → Approval Workflows → + Create Workflow**

### 5.2 配置步驟

1. **基本信息**
   - Workflow Name（如 `Internal Technical Review`）
   - Description
   - Based on: Template / Custom

2. **添加步驟**
   - 點擊 **+ Add Step**
   - Step Name（如 `Technical Review`）
   - Step Type: `Review` 或 `Approval`
   - Assignee: 選擇 Role 或特定人員
   - Due Date: 設置期限（如 5 business days）
   - Required Action: Approve / Reject / Request Changes

3. **Group Review 設置**（如需多人會審）
   - Assignee Type: Group
   - Condition: `All must approve` 或 `Any one`

4. **完成後動作（Action Upon Completion）** — Docs 原生能力
   - **Copy approved files**: 開啟後，將已批准文件 **複製**到指定目標文件夾
     - **When**: `Any file in the review is approved` 或 `All files in the review have been approved`
     - **Then copy approved files to**: 選擇目標夾（可含 naming-standard enforced folder）
     - **約束**: 目標夾必須與源文件屬 **同一 top-level folder**
     - 可選：Allow initiator to change target folder；Include published markups
   - **Update attributes**: 開啟後，在完成時更新/新增屬性（僅目標夾，或目標+源夾）
     - 可 **Add attributes**，並設 **Required by approver**
     - 可開啟 **Auto-increment**（下拉屬性自動取下一值）
     - 若目標為 naming-standard enforced folder，**Status** 與 **Revision** related attributes 會自動加入
   - File Review Status：每份文件的 approval status 會在 Review 完成後自動更新，並顯示於 Files 的 Review status 欄

5. **保存與激活**
   - Save as Draft → 測試（用測試文件跑一遍，確認複製目標與屬性） → Activate

> **Product Help**: [Create and Edit Approval Workflows](https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Create_Edit) · [Visual Workflow](https://help.autodesk.com/view/DOCS/ENU/?guid=Reviews_Workflow)

### 5.3 Auto-trigger 配置（有助於門控，但 ≠ Gateway）

**用途**: 當文件上傳到特定文件夾時自動發起 Review。

**配置步驟**:
1. 導航至文件夾（如 `02_Shared/ARC/`）
2. 文件夾設置 → **Auto-trigger Workflow**
3. 選擇工作流（如 `Naming QA Check`）
4. 設置觸發條件（新文件上傳時 / 特定文件類型）

**注意**:
- Auto-trigger **有助於** 確保 Shared 文件夾中的文件都經過審核
- 主審批流應搭配 **Action Upon Completion**（複製到下一容器 + 更新屬性）
- Auto-trigger 更適合做 **二次驗證**（如命名合規性 check）而非唯一主審批流

---

## 6. Transmittal（信息正式交換）

### 6.1 概念

Transmittal = 向外部方正式發送文件的 **帶記錄的交換行為**，對應 ISO 19650 的 information exchange。

### 6.2 操作步驟

**路徑：Docs → Transmittals → + New Transmittal**

1. **Transmittal Number**: 自動/手動編號（如 `TR-001`）
2. **To**: 接收方（公司/個人）
3. **Subject**: 主題（如 `For Construction Issue - Architecture Package 01`）
4. **Purpose**: 選擇
   - For Information
   - For Review
   - For Approval
   - For Construction
   - As Recorded
5. **附加文件**: 從 `03_Published` 選取
6. **Notes**: 說明/Cover Letter
7. **Send**: 發送（接收方獲通知）

### 6.3 Transmittal 記錄管理

- 所有 Transmittal 自動存檔並帶時間戳
- 可追蹤接收方是否下載
- 支持導出 Transmittal Log（Excel）
- 作為 ISO 19650 審計證據

> **Product Help**: `help.autodesk.com/view/DOCS/ENU/?guid=Transmittals`

---

## 7. 審計追蹤 (Audit Trail)

ACC 自動記錄的審計信息：

| 記錄項 | 來源 | 用途 |
|--------|------|------|
| Workflow 提交/審核/結果/時間 | Approval Workflow History | Gateway 證據 |
| 文件上傳/下載/修改 | Activity Log | 操作追蹤 |
| 版本歷史 | Version History | 變更追溯 |
| 權限變更 | Audit Log | 安全審計 |
| Transmittal 發送/接收 | Transmittal Log | 交換記錄 |

**導出路徑**: Project Admin → Insight → Activity Log → Export

---

## 8. 版本控制規則

| 情境 | 處理方式 |
|------|----------|
| WIP 內多次修改 | ACC 自動記錄版本（v1, v2...）；文件名 Revision 不變直到遷出 |
| WIP → Shared | 文件名 Revision = P01（首次）/ P02（修改後重新遷出） |
| Shared 內發現問題 | 退回 WIP → 修改 → 重新遷入 Shared（Revision +1） |
| Shared → Published | 文件名 Revision 保持不變；Published 是 Shared 的「快照」 |
| Published 需更新 | 新版本走完整 Gateway → 新 Revision 進 Published；舊版本歸 Archive |
| 施工階段版本 | Revision 前綴改為 C（如 C01） |

---

## 9. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | Internal Technical Review Workflow 已建立並激活 | ☐ |
| 2 | Formal Publication Approval Workflow 已建立並激活 | ☐ |
| 3 | For Construction Issue Workflow 已建立並激活（如需） | ☐ |
| 4 | 每個 Workflow 已指定正確的 Assignee（角色/個人） | ☐ |
| 5 | Due Date 已設置合理期限 | ☐ |
| 6 | 用測試文件跑完一次完整 Workflow，確認流程正確 | ☐ |
| 7 | Auto-trigger 已配置在適當文件夾（如 Shared 的命名 QA） | ☐ |
| 8 | 各 Workflow 已開啟 **Copy approved files** 並指向正確目標夾（同 top-level） | ☐ |
| 9 | 各 Workflow 已配置 **Update attributes**（Status/Revision/Date）及 Required by approver | ☐ |
| 10 | 用測試文件驗證：Approve 後文件出現在目標夾且屬性正確；WIP/Shared 源文件處理紀律已寫入 BEP | ☐ |
| 11 | Document Controller 明確「copy ≠ move」的源夾清理/歸檔職責 | ☐ |
| 12 | Transmittal 模板已配置（編號規則、預設接收方） | ☐ |
| 13 | Activity Log 導出已測試 | ☐ |

---

## 10. 缺口 / 需寫入 BEP 的事項

| 事項 | 缺口說明 | BEP 章節建議 |
|------|----------|-------------|
| Gateway 完整定義 | 產品可自動 **複製+改屬性**；BEP 仍須定義目標夾映射、屬性值、以及源文件是否保留/歸檔 | §4 CDE Workflow |
| Copy ≠ Move | Action Upon Completion 是 **copy**；源夾文件仍在，須約定清理/Archive 責任人與時效 | §4 CDE Workflow |
| 同 top-level 約束 | 目標夾必須與源文件屬同一 top-level folder；跨頂層夾遷移仍需人工或 API | §4 CDE Workflow / §7 Technology |
| When 條件選擇 | `Any file approved` vs `All files approved`——推薦後者，避免半套文件進入下一容器 | §4 CDE Workflow |
| Reject / 部分批准 | Rejected 文件不應進入下一容器；屬性是否回寫源夾須在 workflow 選項中明確 | §4 CDE Workflow |
| Timeout 處理 | 審核人超時不回應如何處理？Escalate / 手動提醒？ | §4 CDE Workflow |
| 版本號遞增時機 | 何時 +1？進入 Shared/Published 時？是否用 Auto-increment？ | §3 Naming |
| Transmittal 觸發條件 | 哪些文件必須通過 Transmittal 發送，哪些可直接分享鏈接 | §4 CDE Workflow |
