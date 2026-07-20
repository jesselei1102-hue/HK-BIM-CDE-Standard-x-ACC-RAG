# Hong Kong CDE industry knowledge base

English chapter Markdown for RAG, plus an alias / Query KB route index. Runs in parallel with the Autodesk Docs product store.

This store is a **source-grounded engineering corpus** for retrieval and evaluation. It is **not** customer acceptance testing and **not** legal interpretation of Hong Kong ordinances.

## Sources and copyright

Official PDFs live under local `output/HK Standard/` (not committed by default). Copyright remains with CIC / Hong Kong government bodies. **Do not redistribute the original PDF packages.**

Canonical registry: `rag/industry_hk/source_registry.py`. Intake report: `research/source_intake_report.json`.

| Family | Examples | Authority | Default ingest |
|--------|----------|-----------|----------------|
| Standards | CIC BIM Standards General 2024, Beginner CDE Guide, DEVB Harmonisation v3, MEP 2021, UU 2021, Object Guide 2021 | `standard` / mandatory or recommended | `high` |
| Statutory | Preparation of Statutory Plan Submissions 2020, Appendix B object summary, BD ADM-19 / ADV-34, LandsD BIM-GIS | `statutory` | `high` |
| Terminology | CIC BIM Dictionary 2024 | `terminology` / reference | `substantive`+ |
| Case studies | AM/FM Case Sharing 2021, Zero Carbon Park BIMIP v1.5 | `case_study` / reference | **`high`** (operational config rules; still cited as project practice, not binding) |
| Software guides | ArchiCAD / Civil 3D / Revit / Tekla 2020 statutory appendices | `software_guide` / operational | `all` only |
| Visual | Appendix A sample drawings | image-heavy; **not text-extracted** | excluded |

Duplicates (same SHA-256) are registered once. Supporting BD/LandsD extracts use `scripts/extract_hk_bd_landsd.py` and keep authority metadata through chunks.

## Layout

```text
knowledge/industry/hk_cde/
  corpus/              # Chapter Markdown with frontmatter provenance
  research/            # page_ledger, manifests, extract_report, source_intake_report
  query_kb.jsonl       # Route entries (approved; may include aliases)
  README.md

.rag_data/industry_hk_cde/                 # production (scope=high)
.rag_data/industry_hk_cde_substantive/     # optional shadow (scope=substantive)
```

## Completeness vs ingest scope

| Metric | Meaning |
|--------|---------|
| **page_coverage_pct** (`extract_report.json`) | Every source PDF page booked in `page_ledger.jsonl` (per document). |
| **section_ingest_pct** / **ingested_page_pct** (`manifest.json`) | Share of corpus sections/pages that entered the active index for the chosen scope. |
| **indexed_doc_ids** | Exact document IDs present in the active index (used by scope-aware eval). |

Ingest scopes (`scripts/ingest_industry_hk_cde.py --scope`):

- **`high`** (production default): curated high-priority standards/statutory material **plus** case-study project-config sources (AM/FM, ZCP); templates deferred. Case studies keep `authority_type=case_study` / `normative_weight=reference` so answers must not claim them as territory-wide mandatory rules.
- **`substantive`**: high + useful normal sections; excludes front matter / TOC noise; **defers** `software_guide` docs. Still useful as shadow for dictionary / software guides.
- **`all`**: unfiltered diagnostic ingest (includes software appendices).

Runtime retrieval resolves source families and, for terminology / software-guide intents (and as backup for case studies), can merge candidates from the substantive shadow without replacing the production high collection.

## ZCP project-configuration reference

`cic_zcp_bimip_v15` (Zero Carbon Park BIM Implementation Plan) is a **case study / reference** implementation, not a binding standard. Project-setup questions can preferentially retrieve its BEP, roles, LOIN, naming, CDE/IT, QA and handover sections. Answers must label it as project-specific practice.

## Evaluation fixtures

| File | Role |
|------|------|
| `eval/hk_cde_cases.jsonl` | Classic no-regression CDE suite (gate R@1 ≥ 95%) |
| `eval/hk_cde_coverage_cases.jsonl` | Expanded section/document recall |
| `eval/hk_cde_requirement_cases.jsonl` | Mandatory-clause / key-fact grounding |
| `eval/hk_cde_negative_cases.jsonl` | Route, refusal, authority-confusion |
| `eval/hk_cde_zcp_cases.jsonl` | ZCP project-config reference retrieval |
| `eval/HK_INDEX_COMPARISON.md` | high vs substantive decision |
| `scripts/run_hk_mvp_loop.py` | Bounded MVP loop runner (shadow-only) |

## Rebuild commands

```bash
cd /path/to/repo
source .venv/bin/activate

python scripts/inventory_hk_sources.py
python scripts/extract_hk_cde_pdfs.py --force
python scripts/extract_hk_bd_landsd.py
python scripts/ingest_industry_hk_cde.py --scope high --rebuild
INDUSTRY_HK_DATA_DIR=.rag_data/industry_hk_cde_substantive \
INDUSTRY_HK_COLLECTION=industry_hk_cde_substantive \
  python scripts/ingest_industry_hk_cde.py --scope substantive --rebuild --skip-validation
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild
python scripts/build_hk_grounded_eval.py
python scripts/compare_hk_indexes.py
python scripts/run_hk_mvp_loop.py --iteration 1 --skip-generation
python scripts/run_eval_suite.py --skip-vs
```

## Q&A CLI

```bash
python ask.py "How should ACC folders be configured for HK CDE?"
python ask.py --corpus hk_cde "What does the Gateway do?"
python ask.py --corpus docs "Set folder permissions"
python ask.py --corpus playbook "How to configure the HK GC ACC project template?"
```

**Hard rules**: Route-index metadata never enters the LLM prompt; single-track answers only use that track’s chunks. Case studies and software guides must not be phrased as binding standards when retrieved.

## Hybrid orchestration

When a question has both **product** and **standards** signals, `auto` / `hybrid` will:

1. Split into capability-aligned sub-queries (industry: requirements; Docs: how-to)
2. Retrieve in parallel, then write four sections: **Standards → Implementation → Product → Alignment & Gaps**
3. Write remaining mismatches as **Gap** lines; never invent menus or fake clause mappings

Eval: `python scripts/eval_hybrid.py` (optional `--generate` to check section headers).

## Boundary vs product store

| Question type | Track |
|---------------|-------|
| CIC / DEVB / BD / LandsD requirements, LOD, CDE states | `hk_cde` |
| ACC / Docs UI how-to | `docs` |
| Project template / playbook procedures | `playbook` |
| Mixed HK + ACC | `auto` / `hybrid` |
