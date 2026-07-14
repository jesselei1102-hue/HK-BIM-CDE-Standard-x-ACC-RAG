---
capability: permissions
title: "權限管理"
title_en: "Permissions & Access Control"
authority_refs:
  - "ISO 19650-1:2018 §12.3 (Access control)"
  - "CICBIMS General 2024 §2.4 (CDE access)"
  - "CIC CDE Beginner Guide §4 (Permission requirements)"
related_product_guids:
  - "Manage_Project_Members"
  - "Organize_files_With_Folders"
  - "Folder_Permissions"
  - "Folder_Permission_Levels"
version: "2.0"
date: "2026-07-13"
disclaimer: "權限矩陣為組織推薦默認值，須按項目 BEP 調整。"
---

# 04 — 權限管理 (Permissions & Access Control)

---

## 1. 權限層級架構

ACC 權限分三層：

```
Account Level（賬戶級）
  └── Project Level（項目級）
        └── Folder Level（文件夾級）← 最關鍵
```

- **Account Level**: Account Admin / Member — 控制能否建項目
- **Project Level**: Project Admin / Project Member — 控制項目內角色
- **Folder Level**: No Access / View / View+Download / Upload / Edit / Full Control — **CDE 隔離的核心**

> **CIC CDE Beginner Guide §4**: CDE 須支持按角色限制對不同容器的訪問——這在 ACC 中通過 Folder-level Permission 實現。

---

## 2. 權限級別定義

| ACC 權限級別 | 能力 | 適用場景 |
|---|---|---|
| **No Access** | 完全不可見 | 其他專業看不到的 WIP |
| **View Only** | 查看（不可下載/標注） | 受限查看者 |
| **View + Download** | 查看 + 下載 | 跨專業查看 Shared 文件 |
| **View + Download + Markup** | 加標注評論 | 審圖人員 |
| **Upload** | 可上傳新文件 | Designer 向 WIP 上傳 |
| **Upload + Edit** | 可上傳 + 替換現有文件 | Task Team 在 WIP 內工作 |
| **Full Control** | 一切操作含刪除/權限管理 | BIM Manager / Document Controller |

---

## 3. WIP 容器權限矩陣

**核心原則**: 各專業 WIP 相互隔離，僅本專業可讀寫。

| 角色 | 01_WIP/ARC | 01_WIP/STR | 01_WIP/MEP | 01_WIP/CIV |
|------|-----------|-----------|-----------|-----------|
| BIM Manager | View+DL | View+DL | View+DL | View+DL |
| Document Controller | View+DL | View+DL | View+DL | View+DL |
| ARC Design Lead | Upload+Edit | ❌ No Access | ❌ No Access | ❌ No Access |
| ARC Designer | Upload+Edit | ❌ No Access | ❌ No Access | ❌ No Access |
| STR Design Lead | ❌ No Access | Upload+Edit | ❌ No Access | ❌ No Access |
| STR Designer | ❌ No Access | Upload+Edit | ❌ No Access | ❌ No Access |
| MEP Design Lead | ❌ No Access | ❌ No Access | Upload+Edit | ❌ No Access |
| Reviewer | ❌ No Access | ❌ No Access | ❌ No Access | ❌ No Access |
| Client Rep | ❌ No Access | ❌ No Access | ❌ No Access | ❌ No Access |
| Contractor | ❌ No Access | ❌ No Access | ❌ No Access | ❌ No Access |

> **ISO 19650 對齊**: WIP 信息「must not be visible or accessible to anyone outside the relevant task team」。

---

## 4. Shared 容器權限矩陣

**核心原則**: 所有專業可見，但不可編輯（由 DC 管理進出）。

| 角色 | 02_Shared（所有子夾） |
|------|----------------------|
| BIM Manager | Full Control |
| Document Controller | Upload + Edit + Manage |
| All Design Leads | View + Download |
| All Designers | View + Download |
| Reviewer | View + Download + Markup |
| Client Rep | View + Download |
| Contractor | View + Download |

> **關鍵**: Designer 對 Shared 文件夾僅有 View + Download——**不能直接上傳到 Shared**。遷入 Shared 的動作由 Document Controller 執行。

---

## 5. Published 容器權限矩陣

| 角色 | 03_Published（所有子夾） |
|------|-------------------------|
| BIM Manager | Full Control |
| Document Controller | Upload + Edit |
| Design Leads | View + Download |
| Designers | View + Download |
| Reviewer | View + Download |
| Client Rep | View + Download |
| Contractor | View + Download |

---

## 6. Archive 容器權限矩陣

| 角色 | 04_Archive |
|------|-----------|
| BIM Manager | View + Download |
| Document Controller | Upload（僅用於歸檔操作） |
| 所有其他角色 | View Only |

> **缺口**: ACC 無「只讀鎖定」功能。Document Controller 仍有 Upload 權限以執行歸檔操作，須通過操作紀律防止誤改。

---

## 7. 輔助文件夾權限

| 文件夾 | BIM Manager | Document Controller | Design Lead | Designer | Client |
|--------|-------------|-------------------|-------------|----------|--------|
| 05_Templates | Full Control | Upload+Edit | View+DL | View+DL | View |
| 06_Reference | Full Control | Upload+Edit | View+DL | View+DL | View+DL |

---

## 8. 配置操作步驟

### 8.1 設置文件夾權限

**路徑：Docs → 導航至目標文件夾 → 右鍵 / ⋯ → Permissions**

1. 選擇權限模式：
   - **Role-based** (推薦) — 按角色批量設置
   - **Individual** — 逐人設置（僅特殊情況使用）
2. 為每個角色設定權限級別
3. 保存

### 8.2 繼承與斷開

- **子文件夾默認繼承父文件夾權限**
- 需要特殊設置時：**Break Inheritance** → 獨立配置
- 斷開後，父文件夾權限變更不再傳導到子文件夾

### 8.3 權限驗證（必做）

1. 以 Designer (ARC) 身份登入
2. 確認 ✅ 能看到 `01_WIP/ARC`
3. 確認 ❌ 看不到 `01_WIP/STR`, `01_WIP/MEP`
4. 確認 ✅ 能看到 `02_Shared/STR` (View Only)
5. 確認 ❌ 不能上傳到 `02_Shared`
6. 以 Client Rep 身份登入
7. 確認 ❌ 看不到任何 `01_WIP` 子夾
8. 確認 ✅ 能看到 `03_Published`

---

## 9. 最佳實踐

| ✅ 推薦 | ❌ 避免 |
|---------|---------|
| 使用 Role-based Permission | 逐人設置（難維護） |
| WIP 必須做專業隔離 | 全部 WIP 對所有人可見 |
| Designer 對 Shared/Published 僅 View | 給 Designer Edit 到 Published |
| 定期審計（每月） | 設完不再檢查 |
| BIM Manager + DC 才有 Full Control | 全員 Full Control |
| 離職即時移除權限 | 拖延處理 |
| MFA 對 Project Admin 啟用 | 無雙因素驗證 |

---

## 10. 敏感文件夾特殊處理

某些文件夾需要額外權限限制：

| 文件夾 | 敏感原因 | 建議權限 |
|--------|----------|----------|
| 造價/QS 文件 | 商業機密 | 僅 QS 團隊 + Client |
| 安全設計 | 保安敏感 | 限定人員 |
| 合同文件 | 法律敏感 | 僅 PM + Legal |
| 人事/組織 | 隱私 | 僅 PM |

對這些文件夾：
1. 建立獨立子夾（如 `06_Reference/Confidential/`）
2. Break Inheritance
3. 設置僅限授權人員訪問
4. 審計日誌定期檢查

---

## 11. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | 所有 WIP 子夾已設置專業隔離（彼此 No Access） | ☐ |
| 2 | BIM Manager / DC 對所有 WIP 有 View+DL（但非 Edit） | ☐ |
| 3 | Designer 對 Shared/Published 僅 View+Download | ☐ |
| 4 | Document Controller 對 Shared 有 Upload+Edit（執行遷夾） | ☐ |
| 5 | Client Rep 對 WIP 完全 No Access | ☐ |
| 6 | Contractor 對 Published 有 View+Download | ☐ |
| 7 | Archive 文件夾除 DC 外所有人 View Only | ☐ |
| 8 | 已用非管理員賬號驗證權限隔離正確 | ☐ |
| 9 | 敏感文件夾已 Break Inheritance 並單獨設置 | ☐ |
| 10 | 權限審計責任人和頻率已在 BEP 中定義 | ☐ |

---

## 12. 缺口 / 需寫入 BEP 的事項

| 事項 | 缺口說明 | BEP 章節建議 |
|------|----------|-------------|
| 權限審計頻率 | ACC 無自動合規檢查；須約定每月手動審計 | §5 Security |
| 離職流程 | 即時移除的 SLA 和責任人 | §2 Organization |
| Archive 鎖定替代 | ACC 無原生鎖定；靠權限設置模擬 | §4 CDE Workflow |
| 外部方臨時訪問 | 法定機構審批人（BD/FSD）的短期權限如何管理 | §2 Organization |
| DC Full Control 風險 | DC 有 Edit 權限可能誤改文件；須搭配操作紀律 | §5 Security |
| 子夾繼承異常 | 新增子夾會自動繼承；須在新增時確認權限正確 | §4 CDE Workflow |
