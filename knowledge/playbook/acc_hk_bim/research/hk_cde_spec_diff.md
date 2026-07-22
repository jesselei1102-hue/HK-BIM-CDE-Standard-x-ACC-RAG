# HK CDE Spec vs legacy Playbook — conflict & coverage

Date: 2026-07-22  
New sources (authoritative within Playbook track):

- `output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md`
- `output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md`

Legacy corpus archived to `research/corpus_legacy_v1/` (no longer ingested).

Authority stack (confirmed):

1. Statutory / normative (CIC / DEVB / BD / LandsD / ISO) — **unchanged HK CDE track**
2. Signed project BEP / EIR
3. **These actual-project specs** — Playbook defaults
4. Autodesk / Forma product help — **Docs track** (platform capability limits)

---

## Material overrides (new wins)

| Topic | Legacy (`corpus_legacy_v1` / Config Plan) | New HK CDE Spec |
|-------|-------------------------------------------|----------------|
| Naming | Short `Project-Discipline-Type-Seq-Version` in `08`; CICBIMS 9-field with Status/Revision **in filename** in `03` | Real-Case **9-segment**: `Project-Originator-Building-Zone-Level-Type-Role-System-Number`; Revision / SuitabilityStatus **attributes only** |
| Folder tree | Discipline WIP or top-level four containers; unnumbered WIP/Shared | Numbered `01_WIP→02_SHARED→03_PUBLISHED→04_ARCHIVE`; **team** WIP + Shared org/`8_BIM` subtree |
| Civil | Gap note only in `08` §11 | Full Civil profile (LandsD tree, Section/Chainage, 9 issue types, AssetClass) |
| Product names | Autodesk Docs / Build | Forma Data Management / Build (2025+ rebrand; same capabilities) |
| Workflow tokens | `DRW` / `MOD` | `DR` / `M3` / `CM` / `RP` / `SUB` |
| Status set | S0–S4, A1–A6, B1–B5 (+ filename status) | S0–S4, A3–A6 (Buildings) / A*, CP, CR via `SuitabilityStatus` |
| EMSD / MIDP | Absent from active corpus | Buildings full EMSD; Civil subset + `AssetClass`; MIDP gates WF-B |
| Role ops | Scattered in setup/permissions | Dedicated Owner/GC/Consultant/Subcon manuals |

---

## Coverage map (active corpus)

| Chapter | Domain | Capability | Spec sections |
|---------|--------|------------|---------------|
| `00_hk_cde_spec_index` | mixed | project_template | Index / Buildings vs Civil |
| `10–15_buildings_*` | buildings | roles / folder / workflow / naming / workflow / project_template | Spec §0–6 |
| `20–25_civil_*` | civil | same | Spec §0–6 |

---

## Non-overrides

- CIC/DEVB/ISO normative text remains in `hk_cde` track.
- Product UI mechanics (copy≠move, Shared folder immutability) remain Docs / platform truth.
- Signed BEP still beats these organizational specs for a live project.
