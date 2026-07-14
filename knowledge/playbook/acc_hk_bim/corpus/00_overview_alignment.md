---
capability: overview_alignment
title: "ACC × 港標實施手冊 — 總覽與對齊表"
title_en: "ACC × HK BIM Standards Implementation Playbook — Overview & Alignment"
authority_refs:
  - "CICBIMS General 2024"
  - "DEVB BIM Harmonisation Guidelines v3.0"
  - "CIC CDE Beginner Guide"
  - "ISO 19650-1:2018"
  - "ISO 19650-2:2018"
  - "DEVB TC(W) No.12/2020"
  - "DEVB TC(W) No.7/2021"
related_product_guids:
  - "Getting_Started_Administration"
  - "Manage_Project_Members"
  - "Organize_files_With_Folders"
  - "Reviews_Create_Edit"
  - "Reviews_Workflow"
  - "File_Naming_Standard"
  - "Transmittals"
  - "Configure_Templates_Docs"
  - "Configure_Templates_Design_Collab"
  - "Model_Browser"
related_playbook_files:
  - "01_project_setup.md"
  - "02_folder_cde.md"
  - "03_naming.md"
  - "04_permissions.md"
  - "05_workflow.md"
  - "06_design_collab.md"
  - "07_information_requirements.md"
  - "08_project_template.md"
version: "2.0"
date: "2026-07-13"
disclaimer: >
  本文件為組織推薦配置（Recommended Configuration），非 CIC/DEVB 官方 ACC 模板。
  文件夾樹、角色名稱、命名字段均為推薦默認值，應結合項目 BEP 調整。
---

# ACC × 港標實施手冊 — 總覽與對齊表

> **Disclaimer**: 本手冊所有文件夾結構、角色命名、工作流配置均為 **組織推薦默認 (Recommended Configuration)**，而非 CIC/DEVB 官方 ACC 模板。實施時須結合項目 BIM Execution Plan (BEP) 作具體調整。

---

## 1. 權威版本對齊

### 1.1 引用標準清單

| 標準/文件 | 版本 | 發佈機構 | 本手冊引用範圍 |
|-----------|------|----------|---------------|
| CICBIMS General | **2024** | 建造業議會 (CIC) | 命名規範、LOD、CDE 概念、信息要求 |
| DEVB BIM Harmonisation Guidelines | **v3.0** | 發展局 | Information Container ID、政府工務適用條款、LandsD 提交 |
| CIC CDE Beginner Guide | 最新版 | CIC | CDE 選型必備功能、四容器原則入門 |
| ISO 19650-1:2018 | — | ISO | 信息管理概念與原則 |
| ISO 19650-2:2018 | — | ISO | 資產交付階段信息管理 |
| DEVB TC(W) No.12/2020 | — | 發展局 | HK$3,000萬以上政府工務工程強制 BIM |
| DEVB TC(W) No.7/2021 | — | 發展局 | 擴展 BIM 使用範圍 |

### 1.2 「本文推薦 vs 標準條文」差異聲明

| 本文推薦配置 | 對應標準 §/條文 | 差異說明 |
|-------------|----------------|----------|
| `01_WIP / 02_Shared / 03_Published / 04_Archive` 頂層夾名 | ISO 19650-1 §12; CIC CDE Beginner Guide §3 | 名稱為推薦；標準只定義四容器 **概念**，不規定夾名 |
| 命名 9 字段格式 | CICBIMS 2024 §3; Harmonisation v3 Appendix V | 字段順序與分隔符按 CICBIMS 推薦，但具體值須匹配項目 BEP |
| 角色名稱 (BIM Manager, Document Controller 等) | ISO 19650-2 §5; CICBIMS 2024 §2 | 名稱為通用參考，不等同 CIC/DEVB 定義的法定角色 |
| 審批工作流 3 步 (Tech → QA → Client) | ISO 19650-2 §5.6 Information Gateway | ACC Workflow ≠ ISO Gateway 完整定義（見缺口表） |
| 專業代碼 A/S/M/E/C/L | CICBIMS 2024 Table 3-2; Harmonisation v3 Appendix V | 代碼與義務一致，但 Harmonisation 有額外字段 |

---

## 2. 標準概念 → ACC 對象 總對齊表

| 標準概念 (Standard Concept) | ACC 對象 (ACC Object) | 本手冊章節 | 缺口 / BEP 約定 |
|---|---|---|---|
| **WIP 容器** (Work in Progress) | 文件夾 `01_WIP` + 權限隔離 | 02_folder_cde §2, 04_permissions §3 | ACC 無原生「狀態機」；容器狀態靠 **夾位置 + Custom Attribute** 共同表達 |
| **Shared 容器** | 文件夾 `02_Shared` + 跨專業可見權限 | 02_folder_cde §3, 04_permissions §4 | 文件需 **人工遷夾或 Document Controller 操作**，非 Workflow 自動完成 |
| **Published 容器** | 文件夾 `03_Published` | 02_folder_cde §4, 05_workflow §4 | 同上；需搭配 Transmittal 作正式發佈記錄 |
| **Archived 容器** | 文件夾 `04_Archive` (只讀) | 02_folder_cde §5 | 歸檔靠操作紀律；ACC 無「自動鎖定」 |
| **Information Gateway** | Approval Workflow + **人工遷夾紀律** | 05_workflow §3-4 | ACC Workflow 管審批流；但「通過後移至下一容器」須人工或二次開發實現 |
| **Status / Suitability Code** | Custom Attribute (下拉) / 文件名 Status 段 | 03_naming §2-3, 02_folder_cde §6 | ACC Workflow 完成 **不自動** 寫屬性值；需 Document Controller 手動更新或 API 腳本 |
| **Revision** | ACC Version History + 文件名 Revision 段 | 03_naming §4 | 雙軌：ACC 自動版本 + 文件名顯式版本號，需在 BEP 定義以誰為準 |
| **Information Container ID** | 文件名 + Naming Standard | 03_naming §5 | Harmonisation v3 字段數可能 > ACC Naming Standard 支持字段，需截斷規則 |
| **Naming Convention** | Docs → Naming Standards 功能 | 03_naming §3 | 只在已啟用的文件夾內強制；不覆蓋 Desktop Connector 本地命名 |
| **OIR / AIR / PIR / EIR** | 文檔附件（BEP / EIR 文件）+ Review 節點 | 07_information_requirements | ACC **沒有** OIR/PIR 原生對象；PIR 活在文檔裏，ACC 承載過程與文件 |
| **Task Team** | ACC Team (Design Collaboration) | 06_design_collab §2 | Team 概念對齊；但 DC Team ≠ ISO Task Team 完整治理結構 |
| **Lead Appointed Party** | Company + Role (Project Admin) | 01_project_setup §3 | 角色映射需在 BEP 明確 |
| **Clash Detection / Spatial Coordination** | Model Coordination → Clash Detection | 06_design_collab §5 | 原生功能對齊良好 |
| **Transmittal** | Docs → Transmittals | 05_workflow §6 | 功能對齊良好；但不覆蓋 LandsD 電子提交格式要求 |
| **Audit Trail** | ACC Activity Log + Version History | 05_workflow §7 | 原生功能對齊良好 |

---

## 3. 信息要求層級 (OIR/AIR/PIR/EIR) 落地橋

### 3.1 概念定義

| 縮寫 | 全稱 | 中文 | 管什麼 |
|------|------|------|--------|
| **OIR** | Organizational Information Requirements | 組織信息要求 | 組織層面需要什麼信息來做決策 |
| **AIR** | Asset Information Requirements | 資產信息要求 | 資產運維階段需要什麼信息 |
| **PIR** | Project Information Requirements | 項目信息要求 | 本項目需要什麼信息來回答 OIR/AIR |
| **EIR** | Exchange Information Requirements | 交換信息要求 | 約束各方在交付階段如何生產/交換信息 |

### 3.2 在 ACC 中的落地位置

| 信息要求 | ACC 承載方式 | 存放位置 | 備註 |
|----------|-------------|----------|------|
| OIR | PDF/DOCX 文件（業主提供） | `06_Reference/Client_Requirements/` | ACC 不處理 OIR 邏輯，僅存儲 |
| AIR | PDF/DOCX / 資產數據需求表 | `06_Reference/Client_Requirements/` | 可配合 COBie 模板 |
| PIR | BEP 文件 §「PIR 回應」 | `06_Reference/Standards/BEP/` | **ACC 沒有 PIR 原生對象** |
| EIR | BEP + Naming Standard + Approval Workflow | 多處配置（03_naming, 05_workflow） | EIR 的執行面由 ACC 各功能分散承載 |

### 3.3 缺口聲明

> **ACC 不是 PIR/OIR 管理系統**。PIR 定義在文檔中，ACC 的角色是：  
> 1. 存儲 PIR/EIR 參考文件  
> 2. 通過命名規範和審批工作流 **執行** EIR 中的過程要求  
> 3. 通過 Custom Attributes 記錄狀態/適用性  
>  
> 不要把 ACC 表單/屬性等同於 PIR 本身。PIR 是「問題」，ACC 管的是「過程與產物」。

---

## 4. DEVB Harmonisation v3 / 信息容器 ID 對照

### 4.1 Harmonisation v3 容器 ID 字段結構

根據 DEVB BIM Harmonisation Guidelines v3.0 Appendix V：

```
{Project Code}-{Originator}-{Functional Breakdown}-{Spatial Breakdown}-{Form}-{Discipline}-{Number}-{Status+Revision}
```

### 4.2 與 ACC Naming Standard 字段映射

| Harmonisation 字段 | ACC Naming Standard 字段 | 對齊狀態 | 處理方式 |
|---|---|---|---|
| Project Code | Field 1: Project Code | ✅ 直接映射 | — |
| Originator | Field 2: Originator | ✅ 直接映射 | — |
| Functional Breakdown | ❌ ACC 無原生字段 | ⚠️ 缺口 | 合入 Zone 字段 或 Custom Attribute |
| Spatial Breakdown | Field 3: Zone + Field 4: Level | ⚠️ 拆分映射 | 需定義合併/截斷規則 |
| Form | Field 5: Type | ✅ 接近 | 值域需按 Harmonisation 調整 |
| Discipline | Field 6: Role | ✅ 直接映射 | — |
| Number | Field 7: Number | ✅ 直接映射 | — |
| Status + Revision | Field 8 + Field 9 | ⚠️ 分成兩字段 | ACC 分開處理可接受 |

### 4.3 當字段數不一致時

**問題**：Harmonisation v3 定義 8 個語義字段，ACC Naming Standard 實際可配字段有限。

**推薦截斷規則**（寫入項目 BEP）：

1. `Functional Breakdown` 合入 `Zone` 字段，以 `.` 分隔（如 `BLK-A.FN01`）
2. 若 ACC 字段長度不足，在 Custom Attribute 中補充完整容器 ID
3. 文件名保留 ACC Naming Standard 可執行的字段；完整容器 ID 記錄在屬性中

### 4.4 政府工務 vs 私人項目適用性

| 條款/要求 | 政府工務 (Capital Works) | 私人項目 |
|-----------|------------------------|----------|
| DEVB TC(W) 12/2020 強制 BIM | ✅ HK$3,000萬以上 | ❌ 自願 |
| Harmonisation v3 容器 ID | ✅ 強制 | ❌ 參考 |
| CICBIMS 2024 命名規範 | ✅ 推薦（可被合同約束） | ⚡ 推薦 |
| LandsD 竣工提交格式 | ✅ 強制（見 Harmonisation Appendix XIV） | ❌ 不適用 |
| ISO 19650 合規 | ⚡ 鼓勵 | ⚡ 鼓勵 |
| CIC CDE 必備功能 | ✅ CDE 須滿足 | ⚡ 推薦 |

---

## 5. LandsD / 竣工提交簡述

### 5.1 工務項目竣工 BIM 提交

根據 DEVB BIM Harmonisation Guidelines v3.0 Appendix XIV：

- 竣工模型須以 **IFC 格式** 提交至 LandsD 空間數據平台
- 命名須符合 Harmonisation 容器 ID 規範
- 元數據須包括 COBie 基本欄位
- 提交前需通過 Model Validation（幾何 + 數據完整性）

### 5.2 ACC 中的準備工作

| 步驟 | 操作 | ACC 位置 |
|------|------|----------|
| 1. 導出 IFC | 從 Revit / 其他軟件導出 IFC 2x3 / IFC4 | 本地操作 |
| 2. 命名檢查 | 確保文件名符合 Harmonisation 容器 ID | Naming Standard 驗證 |
| 3. 存放 | 存入 `03_Published/As_Built/` | Docs |
| 4. 審批 | 經竣工審批工作流 | Approval Workflow |
| 5. Transmittal | 正式傳送至 LandsD | Transmittals 功能 |
| 6. 歸檔 | 複製到 `04_Archive/Final_Record/` | 人工操作 |

### 5.3 缺口

> ACC 不直接對接 LandsD 提交系統。IFC 導出和數據驗證在 ACC 外完成，ACC 負責過程管理和審計追蹤。

---

## 6. 安全 / 信息安全簡述 (Security / SIR)

| 控制措施 | ACC 配置 | 備註 |
|----------|----------|------|
| 最小權限原則 | Folder-level Permissions (見 04_permissions) | — |
| 敏感文件夾 | 額外權限限制 + 審計日誌 | 如造價文件、安全設計 |
| 外部 Transmittal | 限定接收人 + 下載追蹤 | — |
| 雙重認證 | Autodesk ID 支持 MFA | 建議所有 Project Admin 啟用 |
| 離職處理 | 即時移除項目權限 | Account Admin 操作 |
| 數據駐留 | ACC 數據存於 Autodesk 指定區域 | 需確認是否滿足合規要求 |

---

## 7. 手冊使用說明

### 7.1 文件結構

```
acc_hk_bim_playbook/
├── 00_overview_alignment.md    ← 本文件（總覽、對齊表、OIR/PIR、Harmonisation）
├── 01_project_setup.md         ← 賬戶與項目配置
├── 02_folder_cde.md            ← 文件夾結構 / CDE 容器（四容器頂層）
├── 03_naming.md                ← 命名規範
├── 04_permissions.md           ← 權限管理
├── 05_workflow.md              ← 審批工作流 / 信息流轉
├── 06_design_collab.md         ← 設計協同 / 模型協調
├── 07_information_requirements.md ← 信息要求落地（OIR/PIR/EIR 詳細）
└── 08_project_template.md      ← ACC 項目樣板（香港 GC / Buildings）
```

> **兩套目錄策略**：第 02 章為設計/顧問向「四容器頂層」；第 08 章為總包 Buildings 樣板（業務夾 + 設計協同內嵌 WIP/Shared/Published/Archive）。項目 BEP 須擇一或混合裁剪。

### 7.2 RAG 切分建議

每篇 MD 以 YAML frontmatter 標識 `capability`，可按此切分為獨立 chunk：
- 每個 `##` 二級標題為一個語義段
- 每篇 ≤ 400 行，避免 chunk 過大主題混雜
- `authority_refs` 和 `related_product_guids` 作為檢索元數據

### 7.3 Autodesk Help GUID 快速索引

| 功能 | Help GUID（須與 Docs 索引一致） | URL 模式 |
|------|-----------|----------|
| 項目管理 | `Getting_Started_Administration` | `help.autodesk.com/view/DOCS/ENU/?guid=...` |
| 成員管理 | `Manage_Project_Members` | 同上 |
| 項目樣板 | `Configure_Templates_Docs` | 同上 |
| 文件夾操作 | `Organize_files_With_Folders` | 同上 |
| 文件夾權限 | `Folder_Permissions` | 同上 |
| 審批工作流 | `Reviews_Create_Edit` / `Reviews_Workflow` | 同上 |
| 命名規範 | `File_Naming_Standard` / `Set_Up_Naming_Standard` | 同上 |
| 設計協同（模板） | `Configure_Templates_Design_Collab` | 同上（Docs 無獨立 DC Overview GUID） |
| 模型瀏覽 | `Model_Browser` | 同上（Docs 無獨立 MC Overview GUID） |
| Transmittals | `Transmittals` | 同上 |
