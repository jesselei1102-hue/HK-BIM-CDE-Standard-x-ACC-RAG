# 香港 BIM / 數碼交付指引與 ACC 對照表

本對照表按「來源文件 → 條款/附錄 → 要求摘要 → ACC 對應位置 → 備註」列出香港 BIM 與數碼交付相關要求，以及其在 Autodesk Construction Cloud (ACC) 中的落實方式。  
**引用版本與日期**：以各官網為準；本表撰寫時 DEVB 統一指引為 v3.0 (Dec 2025)，TC(W) No. 1/2025 生效日 2025年2月1日。

---

## 一、香港要求 ↔ ISO 19650 ↔ ACC 功能概覽

| 香港常見要求 | ISO 19650 對應 | ACC 功能（CDE/配置） |
|-------------|----------------|----------------------|
| 共同數據環境 CDE、單一資訊來源 | ISO 19650-1/2 資訊管理、CDE 概念 | Autodesk Docs 作為 CDE；支援版本、狀態、權限 |
| 資料夾與階段劃分、資料過濾 | ISO 19650-2 資訊容器、狀態碼 | Docs 資料夾結構、Folder Permissions、File Naming Standards |
| 資訊容器命名、狀態碼 (S0–S7 等) | ISO 19650-2 附錄 A 狀態碼與元數據 | Docs 檔案命名、版本/修訂；部分狀態需在 Authoring 或流程中標註 |
| 資訊責任與存取控制 | ISO 19650-2 責任矩陣、存取權 | Docs Folder Permissions；角色/公司對應 IRAM |
| EIR / BEP / OIR-PIR-AIR 文件管理 | ISO 19650-1/2 附錄 A 資訊要求 | Docs 預設資料夾存放 EIR/BEP；Forms/Checklist 對應條款檢查 |
| 標書與合約化 BIM 交付 | 合約/採購要求（非 ISO 條文） | 項目模板「招標/合約」資料夾、交付清單 Forms |

*ACC 已取得 BSI Kitemark 認證支援 ISO 19650；上述對應為規劃層面，實際合規須依項目合約與審核要求。*

---

## 二、分來源對照表

### 2.1 發展局 DEVB — BIM Harmonisation Guidelines for Works Departments (v3.0, Dec 2025)

| 條款/附錄 | 要求摘要 | ACC 對應位置 | 備註 / 適用性 |
|-----------|----------|--------------|----------------|
| **附錄 I** – ISO 19650 Terminologies | 術語與定義（CDE、資訊容器、狀態等） | 全平台：Docs 作為 CDE；命名與狀態配置時依術語理解 | 工務項目 |
| **附錄 II** – Information Responsibility Assignment Matrix (IRAM) | 資訊責任分配矩陣 | **Docs** → Folder Permissions：按角色/公司設定資料夾讀寫，對應 IRAM 責任 | 工務項目 |
| **附錄 III** – Data Filtering Rule Table | 資料過濾規則、項目資料夾劃分 | **Docs** → Files：在項目模板預設資料夾結構（如 WIP / Shared / Published / Archive），對應過濾階段 | 工務項目；可與 CIC 階段對齊 |
| **附錄 VI** – LOD-I Requirements, Creation and Extraction | LOD-I 要求、建立與提取、通用屬性 | **Docs**：資料夾區分設計/竣工階段；LOD 與屬性在 Revit/Civil 3D 等 Authoring 工具完成 | 在 Authoring 工具 / 外部流程完成 LOD 與屬性 |
| **附錄 VII** – Sample BIM Object Check Form | BIM 物件檢查表範本 | **Build** → Forms：可建立或從 Library 加入檢查表 Form template，對應物件檢查 | 工務項目 |
| **附錄 VIII** – Federation Strategy Diagrams and Naming Examples | 聯合策略與命名範例 | **Docs** → File Naming Standards：設定命名規則，參考附錄 VIII 與附錄 IX/X | 工務項目 |
| **附錄 IX** – Sample Project-Specific Codes for Naming | 項目專用命名代碼 | **Docs** → File Naming Standards：項目代碼、專業代碼等納入命名規則 | 工務項目 |
| **附錄 X** – Common Codes for Information Container ID Fields | 資訊容器 ID 欄位通用代碼 | **Docs** → File Naming Standards：檔案命名欄位對應 Common Codes | 工務項目 |
| **附錄 XI** – Sample Spreadsheet for BIM File Name Validation | 檔案名稱驗證範本 | **Docs**：命名規則設定後，可配合外部驗證表或流程；ACC 不提供試算表驗證 | 在外部流程完成驗證 |
| **附錄 XII** – Sample Project Close-out Checklist | 項目收尾檢查清單 | **Build** → Forms：建立或引用 Close-out Checklist 表單，掛到模板 | 工務項目 |
| **附錄 XIII** – Project Boundary Authoring and Model File List | 項目邊界與模型檔案清單 | **Docs**：專用資料夾存放「模型清單」文件；邊界與模型在 Authoring 完成 | 工務項目 |
| **附錄 XIV** – Guidelines for Submission of Design and As-built BIM Models to LandsD | 設計/竣工 BIM 提交地政總署指引 | **Docs**：項目模板設「提交 LandsD」或「LandsD Submission」資料夾；**Forms**：交付檢查清單對應 LandsD 要求 | 工務項目；涉及政府土地/地政時 |

*DEVB 主文及附錄下載：[DEVB BIM Harmonisation Guidelines](https://www.devb.gov.hk/en/publications_and_press_releases/publications/devb-harmonisation-guideline/index.html)*

---

### 2.2 發展局 DEVB — Technical Circular (Works) No. 1/2025

| 條款/要點 | 要求摘要 | ACC 對應位置 | 備註 / 適用性 |
|-----------|----------|--------------|----------------|
| 標書包含 BIM 模型 | BIM 模型作為標書資料一部分 | **項目模板** → Docs：預設「招標與合約」或「Tender」資料夾，存放標書階段 BIM 與圖則 | 工務項目；生效 2025/2/1 |
| BIM 合約化 | 與 2D 標書圖則對應的 BIM 元素具合約約束力（2025/4/1 起；MEP 等可暫為參考） | **項目模板**：招標/合約資料夾、權限設定；交付清單 (Forms/Checklist) 標示「合約化 BIM」與版本 | 工務項目 |
| 部門 AIR 與資產管理策略 | 工務部門須訂立並實施 AIR 及資產管理策略 | **Docs**：可設「Asset Information」或「AIR」資料夾存放 AIR 文件；資產數據多在營運階段系統處理 | 工務項目 |

*TC 1/2025 取代 TC(W) No. 2/2021；標準合約文件（如 GCT）已配合更新。*

---

### 2.3 建造業議會 CIC — BIM Standards - General (2024) 及 Appendix D 模板

| 條款/附錄 | 要求摘要 | ACC 對應位置 | 備註 / 適用性 |
|-----------|----------|--------------|----------------|
| **OIR** (Appendix D1 – Organisational Information Requirements) | 機構資訊要求 | **Docs**：模板內「參考與標準」或「Project Information」資料夾存放 OIR | 工務/私營均可參考 |
| **AIR** (Appendix D2 – Asset Information Requirements) | 資產資訊要求 | **Docs**：同上或專設「AIR」資料夾；營運階段可連結資產系統 | 工務/私營均可參考 |
| **PIR** (Appendix D3 – Project Information Requirements) | 項目資訊要求 | **Docs**：PIR 與 EIR 同放「參考與標準」或專用資料夾 | 工務/私營均可參考 |
| **SIR** (Appendix D4 – Security Information Requirements) | 安全資訊要求 | **Docs**：權限與保密文件存放；**Folder Permissions** 配合 SIR 存取控制 | 工務/私營均可參考 |
| **EIR** (CIC EIR Template，含規劃/設計與施工階段) | 資訊交換要求、BIM 規格 | **Docs**：專用資料夾存放 EIR；**Forms**：可建 EIR 條款檢查表 (Checklist) | 工務/私營均可參考 |
| **Pre-Appointment BEP** (Appendix D6) | 委任前 BIM 執行計劃 | **Docs**：BEP 存放於「參考與標準」或「BEP」資料夾；**Forms**：BEP 里程碑或審批表單 | 工務/私營均可參考 |
| **Pre-Appointment Implementation Plan** (Appendix D5) | 委任前實施計劃 | **Docs**：與 BEP 一併存放 | 工務/私營均可參考 |
| **BIM Capability Assessments** (D7)、**Capability Summary & Software Schedule** (D8)、**Project Member Resume** (D9) | 能力評估、軟件清單、成員履歷 | **Docs**：可設「Capability / Team」資料夾；或 **Library** 存表單模板，項目引用 | 工務/私營均可參考 |

*CIC 2024 取代 2021 版；EIR 另有單獨出版 [CIC EIR Template](https://www.bim.cic.hk/en/resources/publications_detail/84)（可參考 Version 1.1 – 2021）。*

---

### 2.4 屋宇署 BD — 建築信息模擬技術與作業備考

| 條款/來源 | 要求摘要 | ACC 對應位置 | 備註 / 適用性 |
|-----------|----------|--------------|----------------|
| **作業備考 ADV-34**（附錄 A）、**ADM-19** | BIM 檔案格式、軟件版本、呈交方式 | **Docs** → File Naming Standards 及資料夾說明：註明須符合 BD 格式與軟件版本；在 **參考與標準** 放 ADM-19/ADV-34 連結或摘要 | 私營/法定提交項目 |
| **BIM 面積/衞生/消防/間距工具** (Revit、ArchiCAD) | 樓面面積、衞生設備、消防安全、建築物間距核查 | **Docs**：在「提交 BD」或「Reference」資料夾說明使用 BD 工具；實際核查在 Revit/ArchiCAD 外掛完成 | 在 Authoring 工具完成核查 |
| **BIM 結構工具**（電子系統、openBIM） | 結構圖則與分析模型比對、IFC 匯出 | **Docs**：存放 IFC 匯出設定說明或 BST 外掛說明連結；實際操作在結構軟件與電子系統完成 | 在 Authoring 工具 / 屋宇署電子系統完成 |
| **法定申請呈交** | 圖則為準；BIM 為補充參考 | **Docs**：區分「法定圖則」與「BIM 參考」資料夾；命名與版本標示清楚 | 私營項目 |

*參考：[屋宇署 BIM 技術](https://www.bd.gov.hk/tc/resources/online-tools/building-information-modelling/index.html)、[應用 BIM 呈交法定申請指引](https://www.bd.gov.hk/tc/resources/online-tools/building-information-modelling/index_statutory_submissions.html)*

---

### 2.5 地政總署 LandsD — BIM 與 GIS 指引

| 條款/來源 | 要求摘要 | ACC 對應位置 | 備註 / 適用性 |
|-----------|----------|--------------|----------------|
| **BIM and GIS Data Integration Guidelines** (Jun 2023) | BIM 與 GIS 數據整合標準 | **Docs**：「參考與標準」或「LandsD Submission」存放指引連結；交付清單註明符合 LandsD 整合要求 | 涉及政府土地/地政時 |
| **Manual for Producing Harmonised IFC in Archicad** | Archicad 統一 IFC 製作 | **Docs**：參考資料夾；Revit/Civil 3D 設置參照 DEVB 統一指引 | 工務/私營可參考 |
| **DEVB 附錄 XIV**（提交設計/竣工 BIM 至 LandsD） | 提交格式、階段、檢查 | **Docs**：專設「提交 LandsD」資料夾；**Forms**：LandsD 提交檢查清單 | 工務項目 |

*參考：[地政總署 BIM 指引及規格](https://www.landsd.gov.hk/tc/resources/bim-guides-specifications.html)*

---

### 2.6 建築署 ArchSD — BIM 設計指引

| 條款/來源 | 要求摘要 | ACC 對應位置 | 備註 / 適用性 |
|-----------|----------|--------------|----------------|
| BIM Guide for Architectural Design（如 v3.1） | 工務建築設計 BIM 慣例、分工與交付 | **Docs**：資料夾結構與命名與 DEVB 統一指引一致；可與附錄 VIII–X 一併套用 | 工務建築項目 |

*ArchSD 指引通常與 DEVB Harmonisation Guidelines 一併使用。*

---

## 三、ACC 配置項與香港指引對照摘要

| ACC 配置項 | 對應香港指引 | 建議做法 |
|------------|--------------|----------|
| **Docs 資料夾結構** | DEVB 附錄 III、附錄 XIV；CIC EIR/BEP 階段 | 模板預設 WIP / Shared / Published（或等同階段）、招標/合約、提交 LandsD、參考與標準、EIR-BEP |
| **File Naming Standards** | DEVB 附錄 VIII–X、BD 作業備考 | 納入專業代碼、項目代碼、資訊容器 ID 通用代碼；註明 BD 軟件版本與格式 |
| **Folder Permissions** | DEVB 附錄 II IRAM、CIC SIR、ISO 19650 存取 | 按角色/公司設定讀寫權限，與 IRAM 對齊 |
| **Forms / Library** | CIC EIR/BEP 檢查、DEVB 附錄 VII/XII、LandsD/BD 提交 | EIR 條款檢查表、BIM 物件檢查表、項目收尾清單、LandsD/BD 提交檢查表；可放 Account Library 供模板引用 |
| **Project Templates** | TC 1/2025、DEVB、CIC、BD、LandsD 綜合 | 香港住宅、香港基礎設施兩類模板整合上述資料夾、命名、權限、表單；招標/合約資料夾與交付清單支援合約化 BIM |

---

## 四、適用性標註說明

- **工務項目**：DEVB 統一指引、TC 1/2025、DEVB 附錄 XIV（LandsD 提交）為直接適用；CIC 標準與模板建議採用。
- **私營項目**：CIC BIM Standards、EIR、BEP、屋宇署 BD 作業備考與 BIM 路線圖為主要參考；DEVB 附錄命名與資料夾邏輯可選用。
- **在 Authoring 工具 / 外部流程完成**：LOD 與屬性、BIM 物件幾何、BD 自動核查、結構工具、檔案名稱試算表驗證等，在 Revit / Civil 3D / ArchiCAD 或外部系統完成；ACC 負責存放、版本、權限與交付檢查。

---

*本對照表為規劃與實施參考，不取代合約或法定要求；實際合規須以最新官方文件及項目合約為準。*
