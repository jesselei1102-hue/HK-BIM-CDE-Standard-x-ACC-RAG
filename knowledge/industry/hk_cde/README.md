# Hong Kong CDE industry knowledge base

English chapter Markdown for RAG, plus an alias / Query KB route index. Runs in parallel with the Autodesk Docs product store.

## Sources and copyright

| Document | Path |
|----------|------|
| CIC BIM Standards General 2024 | `output/HK Standard/CIC BIM Standards General 2024/` |
| CIC Beginner Guide – Adoption of CDE | `output/HK Standard/CIC Beginner Guide-Adoption of CDE.pdf` |
| DEVB BIM Harmonisation Guidelines v3.0 | `output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with All Appendices.pdf` |
| BD PNAP ADM-19 / ADV-34 | `output/HK Standard/BD_LandsD/` (synced from ACC Template specification) |
| LandsD BIM-GIS Guidelines Jun 2023 | same as above |
| Appendix D1–D9 templates | same CIC tree (field checklists only, not full forms) |

Copyright remains with CIC / Hong Kong government bodies. This store is for internal learning and RAG Q&A only — **do not redistribute the original PDF packages**.

## Layout

```text
knowledge/industry/hk_cde/
  corpus/              # Chapter Markdown extracted in English
  research/            # page_ledger, manifest, extract_report, priority_sections
  query_kb.jsonl       # Route entries (approved; may include aliases)
  README.md

.rag_data/industry_hk_cde/
  chunks.jsonl
  chroma/              # collection: industry_hk_cde
  kb_chroma/           # collection: industry_hk_cde_route
```

## Completeness vs ingest scope

- **page_coverage_pct** (`extract_report.json`): whether every source PDF page is booked in `page_ledger.jsonl`.
- **ingested_page_pct** (`manifest.json`): v1 defaults to `priority: high` chapters only; this can be below 100% page coverage — **expected**.
- Ingest must pass `validate_hk_extract_completeness.py` (exit 0).

## Rebuild commands

```bash
cd /path/to/repo
source .venv/bin/activate
pip install -r requirements.txt

# 1. Extract PDFs + page ledger
python scripts/extract_hk_cde_pdfs.py

# 1b. BD / LandsD supplement (separate script; does not rewrite main page_ledger)
python scripts/extract_hk_bd_landsd.py

# 2. Template fields (D1–D9)
python scripts/extract_hk_templates.py

# 3. Completeness gate
python scripts/validate_hk_extract_completeness.py

# 4. Industry chunk index (high priority by default)
python scripts/ingest_industry_hk_cde.py --rebuild

# 5. Route KB + vector index
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild

# 6. Eval
python scripts/eval_hk_cde.py
```

Full ingest (including `normal` priority): `python scripts/ingest_industry_hk_cde.py --all --rebuild`

## Q&A CLI

```bash
# Default corpus=auto (intent routing; compound questions → hybrid)
python ask.py "How should ACC folders be configured for HK CDE?"

# Force auto / single track
python ask.py --corpus auto "What is WIP?"
python ask.py --corpus hk_cde "What does the Gateway do?"
python ask.py --corpus docs "Set folder permissions"
python ask.py --corpus playbook "How to configure the HK GC ACC project template?"
```

**Hard rules**: Route-index metadata never enters the LLM prompt; single-track answers only use that track’s chunks.

## Hybrid orchestration

When a question has both **product** and **standards** signals, `auto` / `hybrid` will:

1. Split into capability-aligned sub-queries (industry: requirements; Docs: how-to)
2. Retrieve in parallel, then write four sections: **Standards → Implementation → Product → Alignment & Gaps**
3. Write remaining mismatches as **Gap** lines; never invent menus or fake clause mappings

Eval: `python scripts/eval_hybrid.py` (optional `--generate` to check section headers).

After hybrid generation, a light validator checks structure / citation ownership / Docs relevance. Weak Docs pages are dropped before generate; hard failures may retry once. Use `--show-retrieval-debug` to see `validation` warnings.

## Boundary vs product store

| Question type | Track |
|---------------|-------|
| CDE rules, WIP/Gateway, PIR/OIR, DEVB naming | Industry `hk_cde` |
| Autodesk Docs clicks, permissions, UI steps | Product `docs` |
| Standards requirement + product how-to (same capability) | `hybrid` orchestration |

`related_product_guids` in `query_kb.jsonl` is reserved for future bridge boost; current hybrid does not depend on that field.
