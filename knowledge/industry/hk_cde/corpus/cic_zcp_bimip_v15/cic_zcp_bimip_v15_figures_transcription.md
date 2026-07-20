---
source_file: output/HK Standard/CIC_ZCP_BIMIPv1-5_withAppendices.pdf
doc_id: cic_zcp_bimip_v15
section_id: cic_zcp_bimip_v15_figures_transcription
title: ZCP BIMIP Figures Transcription (folder structure, workflows, organisation)
page_start: 30
page_end: 45
authority: CIC ZCP BIM Implementation Plan v1.5 figures (transcribed)
authority_type: case_study
normative_weight: reference
discipline: implementation
lifecycle_stage: project
publication_year: 2022
software: null
priority: high
language: en
source_url: hk_cde://cic_zcp_bimip_v15/cic_zcp_bimip_v15_figures_transcription
extraction_note: Text recovered from embedded figure images (not native PDF text layer). Project-specific practice only.
---

# ZCP BIMIP Figures Transcription

> **Authority note**: Zero Carbon Park BIM Implementation Plan v1.5 is a **case study / project reference**, not a territory-wide mandatory CDE standard. Folder names below are ZCP project practice.

## Figure 9. ZCP standardised folder structure

During project delivery, documents including models were stored/archived under this top-level repository structure agreed with the Appointing Party:

```
01_Revit Model
02_Forge Model
03_CIC Materials
04_Revit Shared Parameter File
05_BIM Object Library
06_Equipment List
07_COBie Worksheet
08_BIM Implementation Plan
09_Technical Requirements
10_Dynamo Tools
11_BIM Interop Tool
12_COBieLite Convertor
```

Notes:

- Naming pattern: `NN_Descriptive Title` (two-digit prefix + underscore + Title Case).
- This is **not** the ISO 19650 / CICBIMS four-container tree (`01_WIP` / `02_Shared` / `03_Published` / `04_Archive`). ZCP used a **deliverable/tool-oriented** top-level layout for project repository handover.
- Folder names imply tool and deliverable roles (Revit, Forge, COBie, Dynamo, interoperability tools).

## Figure 10. ZCP folders designated for handover

At handover, the following folders were designated for submission (subset of the standardised structure):

```
01_Revit Model
02_Forge Model
03_CIC Materials
04_Revit Shared Parameter File
05_BIM Object Library
06_Equipment List
07_COBie Worksheet
08_BIM Implementation Plan
09_Technical Requirements
```

Handover medium (from surrounding text): DVD-ROM with formal transmittal. Contents must also comply with Security Information Requirements (§1.11) and Security Strategy (§2.8 of the BEP).

## Figure 4. Workflow for creation of initial model with asset management data

High-level as-built → AIM pipeline used on ZCP:

1. **As-built Information** feeds an **Equipment List**, which informs the **Revit Model**.
2. Revit model carries CIC common attributes such as `CIC.Common.AssetCode`, `CIC.Common.BIMGUID`, and related attribute data.
3. From Revit, data moves toward FM / digital twin via parallel paths:
   - **BIM Interoperability Tools (Revit plugin)** → **COBie Worksheet** → **COBieLite XML** → **Planon System**
   - **Autodesk Forge Online Platform** → **Forge Model** → **Planon System**
4. **Planon System** (EOMS / FM) exchanges FM data with **Varadise System** (digital twin platform).
5. An **Equipment List with Asset Data** is requested by / linked from Planon and Varadise (including deep links from Varadise).

## Figure 5. Workflow for update of model and data during operations phase

Operations-phase update loop:

1. **User** maintains the **Latest Equipment List** (add new items & input asset data).
2. Update the **Revit Model** (model data + asset data).
3. Export / publish via:
   - Autodesk Forge Online Platform → **Forge Model** → Planon
   - BIM Interoperability Tools → **COBie Spreadsheet** → COBie Toolkit beta 1.4.2 → **COBieLite**
   - Export-Import Excel (Revit plugin) → **Excel Worksheets** (pre-defined FM category worksheets)
4. Manual transfers: Excel worksheets → **Updated Equipment List** → **SDI Template** → **Planon System**.

## Figure 6. Asset / object list schema (model data vs asset data)

The equipment / object list worksheet separates:

- **Model Data** (ATAL object list): Element ID, Family Name, Type Name, Model Category, LOD, OmniClass number/title, etc.
- **Asset Data** (Planon / CIC fields): CIC Common Asset Code (e.g. structured codes like `BG-FIN-RM-AC-FAN-CEL-0001`), UnitID/GUID, Description, Space Code, Storey, Room Number, Space Name, Asset Tag, IoT Code, Asset Key, Barcode.
- Inclusion flags such as **BIM Model Include** / **FM System Include** (Y/N).

## Figure 8. Project organisation chart (roles)

Top: **CIC**, with delivery partners:

- **ATAL** — BIM Team (Information Manager, BIM Manager, BIM Coordinator) and IoT Team (Project Manager, Project Engineer)
- **CIC Construction Digitalisation (including BIM)** — Manager / Assistant Manager / Senior Officer (Industry Development)
- **CIC Estate Office (EO)** — Manager / Assistant Manager / Senior Officer
- **Varadise** — Digital Twin Platform Manager / Consultant
- **Planon** — EOMS Manager / Consultant

These roles support information management / review interfaces; the BIMIP does **not** define an Autodesk Docs Reviews-style approval workflow in these figures.
