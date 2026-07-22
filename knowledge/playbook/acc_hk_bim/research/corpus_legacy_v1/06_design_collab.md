---
capability: design_collab
title: "設計協同 / 模型協調"
title_en: "Design Collaboration / Model Coordination"
authority_refs:
  - "CICBIMS General 2024 §5 (Collaboration)"
  - "ISO 19650-2:2018 §5.5 (Collaborative production)"
  - "CIC BIM Standards - MEP (Coordination)"
related_product_guids:
  - "Configure_Templates_Design_Collab"
  - "Upgrade_Revit_Cloud_Models_Docs"
  - "Model_Browser"
  - "Section_Models_Files"
  - "Files_Hypermodel_Docs"
version: "2.0"
date: "2026-07-13"
disclaimer: "組織推薦配置。Design Collaboration Team ≠ ISO 19650 Task Team 完整治理結構。"
---

# 06 — 設計協同 / 模型協調 (Design Collaboration / Model Coordination)

---

## 1. 設計協同概述 (Design Collaboration)

ACC Design Collaboration (DC) 提供 Revit 雲端協同工作能力：

| 功能 | 說明 | ISO 19650 對齊 |
|------|------|----------------|
| Cloud Worksharing | 多人同時編輯 Revit 模型 | Task Team 內部工作 |
| Publish / Consume | 跨團隊模型共享 | WIP → Shared 的輔助機制 |
| Package Management | 模型包管理 | 信息容器管理 |
| Clash Detection | 碰撞檢測（在 MC 模塊） | Spatial Coordination |

---

## 2. 團隊配置 (Teams)

### 2.1 創建 Teams

**路徑：Design Collaboration → Teams → + Create Team**

| Team Name | 成員 | 管理的模型 |
|-----------|------|-----------|
| Architecture Team | ARC Design Lead + ARC Designers | ARC Central Model |
| Structure Team | STR Design Lead + STR Designers | STR Central Model |
| MEP Team | MEP Design Lead + MEP Designers | MEP Central Model |
| Civil Team | CIV Design Lead + CIV Designers | CIV Central Model |

### 2.2 Team 與 ISO 19650 Task Team 的關係

| ACC Team 概念 | ISO 19650 Task Team | 差異 |
|---|---|---|
| 一組人共享 Revit Workset 權限 | 承擔特定信息生產任務的組織單位 | ACC Team 是技術分組；ISO Task Team 有治理/合同意義 |
| 由 Project Admin 創建 | 由 Lead Appointed Party 指定 | — |
| 邊界 = Revit 模型邊界 | 邊界 = 信息生產責任邊界 | ACC 更窄 |

> **缺口**：ACC Design Collaboration Team 只覆蓋 Revit 協同；非 Revit 文件的 Task Team 概念靠文件夾權限（04_permissions）和 BEP 書面定義。

---

## 3. Publish / Consume 流程

### 3.1 概念

- **Publish**: 將本專業模型推送到共享狀態（Team → Shared Space）
- **Consume**: 從共享空間獲取其他專業模型作為 Link 參考

```
ARC Team                STR Team               MEP Team
    │                      │                      │
    ├──Publish──▶ ┌────────┴──────────┐ ◀──Publish──┤
    │             │  Coordination     │             │
    ◀──Consume──  │  Space            │  ──Consume──▶
    │             │  (Shared Models)  │             │
    │             └───────────────────┘             │
```

### 3.2 Publish 操作步驟

1. 在 Revit 中完成階段性編輯
2. 同步到 Cloud（Sync to Central）
3. 在 ACC Design Collaboration 中：
   - 選擇要 Publish 的模型
   - 點擊 **Publish**
   - 添加 Publish 說明（如 `Level 3 floor plan complete`）
4. 其他團隊收到通知可以 Consume

### 3.3 Consume 操作步驟

1. 收到 Publish 通知
2. 在 Design Collaboration 中查看更新內容
3. 點擊 **Consume** 獲取最新版本
4. Revit Link 自動更新到最新 Published 版本

### 3.4 Publish ≠ 遷入 Shared 文件夾

> ⚠️ **重要區分**：
> - DC Publish = Revit 協同層面的模型共享（技術操作）
> - CDE 遷入 Shared = ISO 19650 信息狀態轉移（治理操作）
>
> 兩者可能不同步。DC Publish 後，文件 **仍在 WIP 文件夾**。正式遷入 Shared 仍需走 Gateway 1 流程（05_workflow §3）。
>
> **BEP 須約定**：DC Publish 是否等同於 Gateway 1 的觸發條件（推薦：是）。

---

## 4. Shared Folder 位置設置

**路徑：Design Collaboration → Settings → Shared Folder Location**

推薦設置：
- Shared 文件夾指向 `01_WIP/{Discipline}/Models/Central_Models/`
- 這是 DC 的 **技術 Shared**，不是 CDE 的 `02_Shared` 容器

> **命名歧義警告**：DC 的「Shared」和 CDE 四容器的「Shared」是 **不同概念**：
> - DC Shared = Revit Publish/Consume 的技術層
> - CDE Shared = ISO 19650 的 S1-S4 狀態容器
>
> 須在 BEP 中明確定義，避免混淆。

---

## 5. 模型協調 / 碰撞檢測 (Model Coordination)

### 5.1 配置 Coordination Space

**路徑：Model Coordination → + New Coordination Space**

1. 選擇需要協調的模型源文件夾：
   - `02_Shared/ARC/Models/`
   - `02_Shared/STR/Models/`
   - `02_Shared/MEP/Models/`
2. 設置更新頻率：
   - **推薦**: 每次 DC Publish 後自動更新
   - 或：每日定時更新

### 5.2 碰撞規則配置

**路徑：Model Coordination → Clash Detection → + Create Clash Test**

| Clash Test | Set A | Set B | Tolerance | 優先級 |
|-----------|-------|-------|-----------|--------|
| ARC vs STR | Architecture | Structure | 10mm | High |
| MEP vs STR | MEP Systems | Structure | 25mm | High |
| MEP vs ARC | MEP Systems | Architecture | 25mm | Medium |
| MEP Internal (Duct vs Pipe) | Ductwork | Piping | 10mm | Medium |
| CIV vs STR | Civil | Structure | 50mm | Medium |

### 5.3 碰撞管理流程

```
1. BIM Manager / Coordinator 運行碰撞檢測
2. 審查結果：
   - 排除誤報 (False Positive)
   - 標記有效碰撞
3. 為有效碰撞創建 Issue：
   - 分配責任人（按專業）
   - 設置優先級和截止日
4. 責任人修改模型
5. 重新 Publish + 運行碰撞檢測
6. 驗證碰撞已解決 → Close Issue
```

### 5.4 碰撞報告

- 每週/每兩週生成碰撞匯總報告
- 跟踪指標：
  - 新增碰撞數
  - 已解決碰撞數
  - 未解決碰撞趨勢
  - 平均解決時間
- 報告存放：`02_Shared/{Discipline}/Clash_Reports/`

---

## 6. 非 Revit 文件協同

| 軟件 | 協同方式 | 說明 |
|------|----------|------|
| AutoCAD / Civil 3D | Desktop Connector + ACC Docs | 本地編輯 → 自動同步 |
| Navisworks | Model Coordination 模塊 | 匯入 NWC 進行碰撞 |
| 其他 BIM 軟件 | IFC 導出 → 上傳 ACC Docs | 通過 IFC 互操作 |
| 文檔/報告 | 直接上傳到 WIP 文件夾 | 走標準 CDE Workflow |

---

## 7. 定期協調會議 (BIM Coordination Meeting)

### 7.1 建議頻率

| 階段 | 頻率 | 內容 |
|------|------|------|
| 概念/方案設計 | 每兩週 | 接口確認、空間協調 |
| 初步設計 | 每週 | 碰撞審查、設計確認 |
| 詳細設計 | 每週 | 碰撞解決、施工圖協調 |
| 施工階段 | 每兩週 | 變更管理、竣工模型準備 |

### 7.2 會議輸出

- 會議記錄存放：`06_Reference/` 或專門的 Minutes 文件夾
- 行動項轉化為 ACC Issues 跟蹤
- 碰撞報告作為會議附件

---

## 8. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | Design Collaboration 服務已啟用 | ☐ |
| 2 | 各專業 Team 已創建並分配成員 | ☐ |
| 3 | Shared Folder Location 已設置 | ☐ |
| 4 | 至少一次成功的 Publish + Consume 測試 | ☐ |
| 5 | Model Coordination 服務已啟用 | ☐ |
| 6 | Coordination Space 已建立（指向 Shared 模型） | ☐ |
| 7 | Clash Test 規則已配置（至少 ARC/STR/MEP 三對） | ☐ |
| 8 | 運行一次碰撞檢測確認功能正常 | ☐ |
| 9 | BIM Coordination Meeting 頻率已在 BEP 中定義 | ☐ |
| 10 | DC Shared vs CDE Shared 的區別已在 BEP 中明確 | ☐ |

---

## 9. 缺口 / 需寫入 BEP 的事項

| 事項 | 缺口說明 | BEP 章節建議 |
|------|----------|-------------|
| DC Publish ↔ CDE Gateway 關係 | DC Publish 不等於正式遷入 Shared；須約定觸發關係 | §4 CDE Workflow |
| DC Shared vs CDE Shared 定義 | 名稱相同含義不同；須在 BEP 明確避免混淆 | §4 CDE Workflow |
| Team = Task Team? | ACC Team 是技術分組；ISO Task Team 有治理意義 | §2 Organization |
| 碰撞解決 SLA | 各優先級碰撞的解決時限 | §5 Coordination |
| 非 Revit 文件的協同流程 | DC 不覆蓋 AutoCAD/Civil 3D；需另行約定 | §5 Coordination |
| Publish 頻率 | 每日/每次重要修改？須約定 | §5 Coordination |
| 碰撞報告格式和分發 | 標準模板、接收人、頻率 | §5 Coordination |
