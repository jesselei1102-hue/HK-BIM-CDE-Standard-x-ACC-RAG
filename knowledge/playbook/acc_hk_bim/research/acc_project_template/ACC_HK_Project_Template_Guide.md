# ACC Project Template 入門：香港本地規範

本指南說明如何為**香港本地規範**建立兩個 ACC (Autodesk Construction Cloud) 項目模板：**住宅**與**基礎設施**，並如何開始配置。

---

## 一、如何開始（三種方式）

### 方式 1：從空白模板建立（建議用於從零訂製香港規範）

1. **Account Admin** → 左側 **Project templates** → **Create project template**
2. 選擇 **Create blank template** → **Next**
3. 輸入模板名稱，例如：
   - `ACC HK 住宅項目模板 (Residential)`
   - `ACC HK 基礎設施項目模板 (Infrastructure)`
4. 選擇 Account → **Create template**
5. 進入模板的 **Configuration** 頁面後，按下方「二、住宅模板」「三、基礎設施模板」逐項配置。

### 方式 2：從現有項目另存為模板（若已有符合香港習慣的項目）

1. 進入該項目 → **Project Admin** → **Settings**
2. 點 **Save as template**
3. 輸入模板名稱並選擇 Account → **Save as template**
4. 在新建的模板中刪除項目專用內容、保留通用設定與資料夾結構，再依香港規範微調。

### 方式 3：以 EMEA 樣本模板為起點（若帳戶在 EU 資料區）

- **住宅**：可選 **EMEA Buildings Sample Template**，再改為香港用語與規範。
- **基礎設施**：可選 **EMEA Roads Sample Template**，再改為香港道路/基建習慣。
- 路徑：Project picker → **Templates** → **View all templates** → **Sample templates** → 選擇模板 → **Save to account**，然後在模板內調整。

> 注意：樣本模板目前僅提供 US、EU 資料區；若帳戶在其它區域，請用方式 1 或 2。

---

## 二、住宅項目模板（住宅 / Residential）

### 2.1 建立／選擇模板後必做設定

| 步驟 | 位置 | 說明 |
|------|------|------|
| 1 | 建立項目時 | **Project type** 選 **Residential**（或 Buildings，視帳戶選項） |
| 2 | Configuration → Advanced | 需要時勾選 **Publish template**，讓全公司可用此模板建立項目 |
| 3 | 成員與產品 | 在模板的 **Members** 加入常設角色/公司；在 **Products and tools** 只開啟住宅項目會用到的產品（如 Docs、Build、Design Collaboration 等） |

### 2.2 Docs：資料夾結構（可依香港住宅項目習慣調整）

在模板內：**Docs** → **Files**，建立例如：

```
Project Files/
├── 01_行政與合約 Admin & Contract/
├── 02_設計圖則 Design Drawings/
│   ├── 建築 Architectural/
│   ├── 結構 Structural/
│   ├── 機電 MEP/
│   └── 其他 Others/
├── 03_招標與施工 Tender & Construction/
├── 04_驗收與竣工 As-built & Completion/
└── 05_參考與標準 Reference & Standards/
```

- 可再依 **BD（屋宇署）**、**建築物條例**、**消防** 等分冊需要增設子資料夾。
- 在 **Docs** 的 **Folder Permissions** 為各資料夾設定角色/公司權限。

### 2.3 Docs：檔案命名與規範

- **Configuration** → **Files** → **File Naming Standards**：設定命名規則，建議包含：
  - 專業代碼（如 A=建築、S=結構、M=機電）
  - 圖則類型／版本
  - 可選：符合香港常用編號習慣（如 BD 提交編號）
- 可配合公司已有的 **香港 BIM / CAD 標準** 撰寫命名說明。

### 2.4 Issues、Forms、Reports（住宅）

- **Issues**：設定住宅項目常用的 **Issue types**、**Categories**、**Root causes**、**Statuses**；可預設 **Issue templates**（如「缺陷」「安全」「設計變更」）。
- **Forms**：從 **Library** 加入或新建 **Form templates**（如檢查表、日報、品質表），並在模板的 **Forms** 中掛到對應資料夾/流程。
- **Reports**：在模板內配置 **Report templates** 與 **Schedules**（例如每週/每月報告），建立項目時會一併帶入。

### 2.5 香港住宅相關規範可考慮的對應

- **屋宇署 (BD)**：圖則編號、提交階段、審批流程可在資料夾命名與 Forms/Issues 中反映。
- **消防、渠務、環保**：可設對應資料夾或 Issue categories，方便按規範追蹤。
- **語言**：模板名稱、資料夾、Issue/Form 欄位可採 **中英並列**，與 EMEA 雙語樣本做法類似。

---

## 三、基礎設施項目模板（基礎設施 / Infrastructure）

### 3.1 建立／選擇模板後必做設定

| 步驟 | 位置 | 說明 |
|------|------|------|
| 1 | 建立項目時 | **Project type** 選 **Infrastructure** 下合適子類型（如 **Roads**、**Streets/Roads/Highways**、**Tunnel** 等，依 ACC 介面選項） |
| 2 | Configuration | 同上，必要時 **Publish template**；在 **Products and tools** 開啟基建常用產品（Docs、Build、Takeoff、Cost 等） |

### 3.2 Docs：資料夾結構（可依香港基建習慣調整）

可參考 **EMEA Roads** 的權限矩陣與資料夾邏輯，再本地化為香港道路/渠務/隧道等，例如：

```
Project Files/
├── 01_項目管理 Project Management/
├── 02_設計 Design/
│   ├── 道路與排水 Roads & Drainage/
│   ├── 結構與土木 Structures & Civil/
│   └── 機電與交通 M&E & Traffic/
├── 03_招標與合約 Tender & Contract/
├── 04_施工 Construction/
│   ├── 分區/合約 Section / Contract/
│   └── 檢驗與記錄 Inspection & Records/
└── 05_竣工與營運 As-built & Operations/
```

- 若使用 **EMEA Roads Sample Template**，可參考官方 **Roads Permission Matrix** 為資料夾設定權限，再依香港顧問/承建商角色調整。

### 3.3 權限與角色（基礎設施）

- 基建常涉及多顧問、多合約；在模板的 **Docs** → **Folder Permissions** 依「顧問/承建商/業主」設定讀寫權限。
- 官方文件提到 **Building Design by Consultant Permission Matrix**（建築類）與 **Roads Permission Matrix**（道路類）；可下載對應矩陣，在模板 **Files** 中對每個資料夾套用相應權限，減少每個新項目手動設定。

### 3.4 Issues、Forms、Takeoff / Cost（基礎設施）

- **Issues**：設定基建專用類型（如「工地安全」「地底設施」「交通管理」「環境」等）。
- **Forms**：加入 **Library** 中的表單模板，或為基建定製（如 RSI、檢查表、量測記錄）。
- **Takeoff / Cost**：若使用 **Autodesk Takeoff**、**Cost**，在模板的 **Configure Project Templates for Takeoff** 與 **Cost Management** 中預設分類、成本庫、單位，方便投標與合約管理。

### 3.5 香港基礎設施相關規範可考慮的對應

- **路政署、渠務署、土木工程拓展署** 等：資料夾與 Issue categories 可對應不同政府部門/審批階段。
- **香港標準與慣例**（如 **HKIE**、**Geoguide**、**General Specification**）：在 **Reference & Standards** 類資料夾或 Library 中集中放置參考文件連結或範本。

---

## 四、兩個模板的共通配置檢查清單

- [ ] **Account Admin** 或 **Templates** 中已建立「住宅」「基礎設施」兩個模板（或從現有項目/樣本另存）。
- [ ] 每個模板的 **Configuration** → **General**：模板名稱、**Publish** 設定已設定。
- [ ] **Members**：預設角色/公司已加入模板。
- [ ] **Products and tools**：只顯示該類型項目會用到的產品與工具。
- [ ] **Docs**：資料夾結構、**Folder Permissions**、**File Naming Standards** 已設定。
- [ ] **Design Collaboration**（若使用）：Shared folder、Team setup、資料夾對應已設定。
- [ ] **Build**（若使用）：Sheets、Files、Issues、Forms、RFIs、Submittals、Reports 等已按類型配置。
- [ ] **Issues**：Categories、Types、Templates、Statuses、Permissions 已設定。
- [ ] **Forms**：所需 Form templates 已從 Library 加入模板或專案。
- [ ] **Reports**：Report templates、Schedules、語言/時區 已設定。
- [ ] 建立一個**測試項目**分別從「住宅」「基礎設施」模板建立，確認資料夾、權限、表單、報告皆符合預期後再推廣使用。

---

## 五、參考 DOCS 章節（來自本專案 output/DOCS）

- **Create Project Templates**（DOCS_help_004.md）：從空白、從現有項目、從樣本建立。
- **Sample Project Templates for Project Administrators**（DOCS_help_006.md）：EMEA Buildings / Roads 樣本說明與權限矩陣。
- **Configure Project Templates for Autodesk Docs**（DOCS_help_006.md）：Docs 資料夾、權限、命名、Reviews、Issues、Reports。
- **Configure Project Templates for Design Collaboration**（DOCS_help_006.md）：Shared folder、Team、資料夾結構。
- **Configure Project Templates for Autodesk Build**（DOCS_help_006.md）：Build 各工具在模板中的配置。
- **Manage Project Templates**（DOCS_help_006.md）：編輯、歸檔、複製模板。
- **Create project** 對話框（DOCS_help_002.md）：Project type、Template 選擇、必填欄位。

**香港 BIM / 數碼交付**：詳見 [《香港 BIM / 數碼交付指引與 ACC 對照表》](HK_BIM_Digital_Delivery_ACC_Mapping.md) 及本指南 **第七節**。

---

## 六、建議的下一步

1. **先做一個類型**：例如先完成「住宅」模板並用一個試點項目驗證，再複製或另建「基礎設施」模板。
2. **收集香港本地清單**：整理貴司住宅/基建項目常用的資料夾名稱、Issue 類型、表單、報告格式，一次性寫進模板。
3. **與 Library 配合**：把共用的 **Form templates**、**Classifications**、**Costs** 放在 Account **Library**，再在兩個模板中引用，方便日後統一更新。
4. **文件化**：在模板的 **Files** 或公司內網放一份「香港 ACC 模板使用說明」，說明何時選住宅/基礎設施、如何依 BD/政府部門調整資料夾與表單。

完成以上步驟後，即可持續用這兩個香港本地規範模板快速開新項目並保持一致性。

---

## 七、香港 BIM / 數碼交付指引在 ACC 的應用

本節摘要香港政府與行業的 BIM、數碼交付要求，以及如何在 ACC 項目模板中體現。詳細條款與 ACC 對應見 **[《香港 BIM / 數碼交付指引與 ACC 對照表》](HK_BIM_Digital_Delivery_ACC_Mapping.md)**。

### 7.1 資料夾結構如何反映 DEVB / CIC / LandsD 階段

- **DEVB 統一指引（附錄 III）**：建議按「資料過濾」階段劃分資料夾，例如 WIP（進行中）、Shared（共享）、Published（已發布）、Archive（歸檔）。在模板 **Docs** → **Files** 預設對應資料夾，並用 **Folder Permissions** 配合附錄 II 的資訊責任矩陣 (IRAM)。
- **CIC EIR / BEP**：在模板中設「參考與標準」或專用「EIR-BEP」資料夾，存放 Exchange Information Requirements、BIM Execution Plan、PIR/AIR 等文件；新項目建立時即具備一致結構。
- **LandsD 提交（DEVB 附錄 XIV）**：工務項目若需向地政總署提交設計/竣工 BIM，在模板預設「提交 LandsD」或「LandsD Submission」資料夾，並可搭配交付檢查清單 (Forms) 對應 LandsD 指引。

### 7.2 命名規則如何對應 DEVB 附錄與 BD 要求

- **Docs** → **File Naming Standards**：參考 DEVB 附錄 VIII（聯合策略與命名範例）、附錄 IX（項目專用代碼）、附錄 X（Common Codes for Information Container ID）設定命名規則，使檔案名稱符合工務/政府項目慣例。
- **屋宇署 (BD)**：作業備考 ADM-19、ADV-34 規定 BIM 檔案格式與軟件版本。在命名規則說明或「參考與標準」資料夾中註明須符合 BD 要求，並連結 [屋宇署 BIM 技術](https://www.bd.gov.hk/tc/resources/online-tools/building-information-modelling/index.html) 及 ADM-19/ADV-34；實際格式與版本在 Authoring 工具（Revit/ArchiCAD）中控制。

### 7.3 哪些 Forms / Checklist 可支援 EIR、BEP、標書 BIM、LandsD/BD 提交

| 用途 | ACC 位置 | 說明 |
|------|----------|------|
| **EIR 條款檢查** | Build → Forms（或 Library） | 依 CIC EIR 模板建立檢查表，對應規劃/設計與施工階段資訊要求；可加入項目模板供每次交付前勾選。 |
| **BEP 里程碑 / 審批** | Build → Forms | 對應 CIC Pre-Appointment BEP（Appendix D6）；可設 BEP 審批或階段完成表單。 |
| **標書 BIM、合約化交付** | Docs 資料夾 + Forms | TC(W) No. 1/2025 要求標書含 BIM 且部分合約化。模板預設「招標與合約」資料夾；用 Forms 建立「標書 BIM 交付清單」或「合約化 BIM 版本確認」表單。 |
| **LandsD 提交檢查** | Build → Forms | 依 DEVB 附錄 XIV 與地政總署指引建立「提交 LandsD 檢查清單」，掛到模板。 |
| **BD 提交 / 法定圖則** | Build → Forms + Docs | 私營項目可設「提交 BD」檢查表，註明圖則為準、BIM 為補充及 ADM-19/ADV-34 格式要求。 |
| **BIM 物件檢查、項目收尾** | Build → Forms | 對應 DEVB 附錄 VII（BIM Object Check Form）、附錄 XII（Project Close-out Checklist）；表單可放 Account Library 供多項目使用。 |

將上述 Form templates 存入 **Account Library**，再在「香港住宅」「香港基礎設施」兩類項目模板中引用，可統一全公司香港項目的交付品質與合規性。

**一頁式檢查清單**：項目啟動與交付前可使用 [《香港 BIM 數碼交付 + ACC 檢查清單》](HK_BIM_Digital_Delivery_ACC_Checklist.md) 逐項勾選。
