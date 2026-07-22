---
capability: naming
title: "命名規範"
title_en: "Naming Convention / Information Container ID"
authority_refs:
  - "CICBIMS General 2024 §3 (Naming Convention)"
  - "DEVB BIM Harmonisation Guidelines v3.0 Appendix V (Information Container ID)"
  - "ISO 19650-1:2018 §13 (Naming)"
related_product_guids:
  - "File_Naming_Standard"
  - "Set_Up_Naming_Standard"
  - "Customize_Naming_Standard"
  - "Apply_Naming_Standard_To_Project"
version: "2.0"
date: "2026-07-13"
disclaimer: "命名字段為組織推薦，具體值域須按項目 BEP 確認。"
---

# 03 — 命名規範 (Naming Convention / Information Container ID)

---

## 1. 命名規範層級

香港項目涉及兩套命名體系，需在 BEP 中確認適用哪套：

| 體系 | 來源 | 適用 | 字段數 |
|------|------|------|--------|
| **CICBIMS Naming Convention** | CICBIMS General 2024 §3 | 通用（私人/公營） | 8-10 字段 |
| **DEVB Information Container ID** | Harmonisation v3 Appendix V | 政府工務項目 | 8 字段 |

兩者高度相似但不完全一致。以下分別說明。

---

## 2. CICBIMS 2024 命名規範結構

```
{Project}-{Originator}-{Zone}-{Level}-{Type}-{Role}-{Number}-{Status}-{Revision}
```

| 字段 | 位置 | 字符數 | 說明 | 示例 |
|------|------|--------|------|------|
| Project | 1 | 2-6 | 項目代碼 | `HK001` |
| Originator | 2 | 2-6 | 編制方代碼 | `WSP` |
| Zone | 3 | 2-6 | 區域/棟號 | `ZZ`, `BLKA` |
| Level | 4 | 2-4 | 樓層 | `GF`, `01`, `RF`, `XX` |
| Type | 5 | 2 | 文件類型 | `M3`, `DR`, `RP` |
| Role | 6 | 1-2 | 專業/角色 | `A`, `S`, `M` |
| Number | 7 | 4 | 序號 | `0001` |
| Status | 8 | 2 | 狀態碼 | `S2`, `A4` |
| Revision | 9 | 3 | 版本 | `P01`, `C02` |

**分隔符**: `-`（連字符）

**完整示例**:
```
HK001-WSP-ZZ-XX-M3-A-0001-S2-P03.rvt
HK001-ARP-BLKA-GF-DR-A-0001-A4-C02.pdf
```

---

## 3. 在 ACC 配置 Naming Standard

### 3.1 配置步驟

**路徑：Project Admin → Docs Settings → Naming Standards → + Create**

1. **Name**: `CICBIMS 2024 Naming Convention` (或 `DEVB Container ID` 按適用標準)
2. **配置字段**:

| ACC Field # | Field Name | Type | Validation | 來源 |
|---|---|---|---|---|
| 1 | Project Code | Fixed Value | `HK001` | 項目統一 |
| 2 | Originator | Dropdown | 從 Company Short Code | BEP 定義 |
| 3 | Zone | Dropdown / Free Text | 按項目定義 | BEP 定義 |
| 4 | Level | Dropdown | GF, 01-99, RF, BF, XX | 標準樓層碼 |
| 5 | Type | Dropdown | M3, M2, DR, SP, RP, CO, VS | CICBIMS Table |
| 6 | Role | Dropdown | A, S, M, E, C, L, G, Q, T, F | CICBIMS Table |
| 7 | Number | Auto-increment (4 digits) | 0001-9999 | 系統自動 |
| 8 | Status | Dropdown | S0-S4, A1-A6, B1-B5, CR | ISO 19650 |
| 9 | Revision | Pattern (P/C + 2 digits) | P01, C01 | 規則定義 |

3. **Separator**: `-`
4. **Enforce on Upload**: ✅ 勾選
5. **Apply to Folders**: 選擇 `02_Shared` 和 `03_Published`（及其子文件夾）

### 3.2 啟用命名強制

| 文件夾 | Naming Standard | 原因 |
|--------|----------------|------|
| 01_WIP | ❌ 不啟用 | 內部工作自由迭代 |
| 02_Shared | ✅ 強制 | 跨專業共享須可識別 |
| 03_Published | ✅ 強制 | 正式發佈必須合規 |
| 04_Archive | ✅ 強制 | 歸檔記錄須可追溯 |
| 05_Templates | ❌ 不啟用 | 模板命名自由 |
| 06_Reference | ❌ 不啟用 | 外來文件命名多樣 |

> **Product Help**: ACC Naming Standards 配置 — `help.autodesk.com/view/DOCS/ENU/?guid=File_Naming_Standard` / `Set_Up_Naming_Standard`

---

## 4. 版本號規則 (Revision)

| 階段 | 前綴 | 遞增 | 示例 |
|------|------|------|------|
| 初步設計 (Preliminary) | P | P01, P02, P03... | `...-S2-P03.rvt` |
| 施工 (Construction) | C | C01, C02, C03... | `...-A4-C01.pdf` |
| 竣工 (As-Built) | F | F01 (通常僅一版) | `...-A6-F01.ifc` |

### 4.1 ACC 版本 vs 文件名版本

| 機制 | 性質 | 自動 | 人控 |
|------|------|------|------|
| ACC Version History | 平台自動遞增 (v1, v2, v3...) | ✅ 每次上傳自動 | — |
| 文件名 Revision 段 | 業務語義版本 (P01, C01) | ❌ 人工更新 | ✅ |

> **BEP 須約定**：以文件名 Revision 為業務版本基準。ACC 版本號作為技術追溯用。兩者不一定一一對應（文件名 P02 可能對應 ACC v5）。

---

## 5. DEVB Harmonisation v3 容器 ID 對照

### 5.1 Harmonisation 字段結構

```
{Project}-{Originator}-{FunctionalBreakdown}-{SpatialBreakdown}-{Form}-{Discipline}-{Number}-{StatusRevision}
```

### 5.2 與 ACC Naming Standard 映射

| Harmonisation 字段 | ACC Naming Field | 映射狀態 | 處理方式 |
|---|---|---|---|
| Project Code | Field 1 | ✅ 直接 | — |
| Originator | Field 2 | ✅ 直接 | — |
| Functional Breakdown | ❌ 無原生字段 | ⚠️ 缺口 | 選項 A: 合入 Zone（如 `BLKA.FN01`）<br>選項 B: 記入 Custom Attribute |
| Spatial Breakdown | Field 3 (Zone) + Field 4 (Level) | ⚠️ 拆分 | 合併或截斷規則寫入 BEP |
| Form | Field 5 (Type) | ✅ 接近 | 值域按 Harmonisation 調整 |
| Discipline | Field 6 (Role) | ✅ 直接 | — |
| Number | Field 7 | ✅ 直接 | — |
| Status + Revision | Field 8 + Field 9 | ⚠️ 分兩欄 | ACC 分開處理，可接受 |

### 5.3 當字段數超出 ACC 限制

**推薦截斷規則**（寫入 BEP §3 Naming）：

1. 文件名保留 ACC Naming Standard 可強制的字段
2. 完整 Information Container ID 記錄在 Custom Attribute `Container_ID` (Text) 中
3. 兩者不一致時，以 Custom Attribute 中的完整 ID 為權威

---

## 6. 狀態碼完整對照

| 狀態碼 | ISO 19650 狀態 | 中文 | 容器位置 |
|--------|---------------|------|----------|
| S0 | Work in Progress | 工作中 | 01_WIP |
| S1 | For Coordination | 適合協調 | 02_Shared |
| S2 | For Information | 適合參考 | 02_Shared |
| S3 | For Review & Comment | 適合審查 | 02_Shared |
| S4 | For Stage Approval | 適合審批 | 02_Shared |
| A1 | Authorized & Accepted — Stage 1 | 批准階段 1 | 03_Published/For_Information |
| A2 | Authorized & Accepted — Stage 2 | 批准階段 2 | 03_Published |
| A3 | Authorized & Accepted — Stage 3 | 批准階段 3 | 03_Published/For_Approval |
| A4 | For Construction | 供施工 | 03_Published/For_Construction |
| A5 | For Manufacture | 供製造 | 03_Published/For_Manufacture |
| A6 | As Built | 竣工 | 03_Published/As_Built |
| B1 | Partial Sign-off | 部分簽認 | 03_Published |
| B2-B5 | (Project Defined) | 項目定義 | 03_Published |
| CR | As Constructed Record | 施工記錄 | 04_Archive/Final_Record |

### 6.1 狀態的三種表達方式（需在 BEP 約定以哪個為準）

| 表達方式 | 位置 | 自動 | 說明 |
|----------|------|------|------|
| **文件夾位置** | 01_WIP / 02_Shared / 03_Published | ✅ Workflow 可 Copy approved files | 粗粒度（4 狀態）；源夾清理仍人工 |
| **文件名 Status 段** | 文件名倒數第二段 | ❌ 人工命名 | 細粒度（S0-CR） |
| **Custom Attribute** | 文件屬性面板 | ✅ Workflow 可 Update attributes | 可搜索/篩選；未配置時仍需人工 |

> **BEP 須約定**：三者必須一致。若不一致，以 **Custom Attribute** 為基準（可修改不換文件名），文件夾位置為粗顆粒驗證。

---

## 7. 專業代碼參考表

| 代碼 | 專業 | English |
|------|------|---------|
| A | 建築 | Architecture |
| S | 結構 | Structural |
| M | 機電（綜合） | MEP |
| E | 電氣 | Electrical |
| P | 給排水 | Plumbing |
| H | 暖通 | HVAC |
| C | 土木 | Civil |
| L | 園林 | Landscape |
| G | 岩土 | Geotechnical |
| Q | 工料測量 | Quantity Surveying |
| T | 交通 | Transportation |
| F | 消防 | Fire Services |
| U | 地下管線 | Underground Utilities |
| W | 綜合 | Multi-discipline |

---

## 8. 文件類型代碼

| 代碼 | 類型 | 說明 |
|------|------|------|
| M3 | 3D Model | Revit/IFC 等 |
| M2 | 2D Model | CAD |
| DR | Drawing | 圖紙 |
| SP | Specification | 規格書 |
| RP | Report | 報告 |
| CO | Correspondence | 往來文件 |
| VS | Visualization | 渲染/動畫 |
| SH | Schedule | 進度/明細 |
| DB | Database | 數據庫 |
| CM | Clash Matrix | 碰撞矩陣 |
| MI | Minutes | 會議記錄 |
| PP | Presentation | 演示 |
| HS | Health & Safety | 安全文件 |
| FN | Financial | 財務文件 |

---

## 9. 配置完成驗收清單

| # | 驗收項目 | Yes/No |
|---|----------|--------|
| 1 | Naming Standard 已建立，字段與 BEP §3 一致 | ☐ |
| 2 | Naming Standard 已應用到 02_Shared 和 03_Published | ☐ |
| 3 | 01_WIP 確認不啟用 Naming Standard | ☐ |
| 4 | Enforce on Upload 已啟用 | ☐ |
| 5 | 嘗試上傳一個不合規文件名到 Shared，確認被拒絕 | ☐ |
| 6 | 嘗試上傳合規文件名到 Shared，確認通過 | ☐ |
| 7 | Custom Attribute `Status Code` 下拉值已配置 | ☐ |
| 8 | 若適用 Harmonisation，完整容器 ID 規則已寫入 BEP | ☐ |

---

## 10. 缺口 / 需寫入 BEP 的事項

| 事項 | 缺口說明 | BEP 章節建議 |
|------|----------|-------------|
| WIP 內命名自由度 | 到什麼程度可不合規？提交審核前是否需要先改名？ | §3 Naming |
| 版本基準 | ACC Version 與文件名 Revision 不一定同步，以何為準 | §3 Naming |
| Harmonisation 字段截斷 | Functional Breakdown 如何映射；完整 ID 放哪 | §3 Naming |
| 狀態三軌一致性 | 夾位置 / 文件名 / Attribute 不一致時如何處理 | §4 CDE Workflow |
| Desktop Connector 命名 | ACC Naming Standard 不覆蓋本地同步時的命名行為 | §3 Naming |
| 外來文件重命名 | 第三方文件（如法定機構回覆）不合規時如何處理 | §3 Naming |
