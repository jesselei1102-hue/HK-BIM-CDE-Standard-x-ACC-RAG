# HK BIM CDE Standard × ACC RAG

A local three-source RAG system that keeps **Hong Kong BIM / CDE standards**, an **ACC × HK implementation playbook**, and **Autodesk Docs product help** in separate indexes, then orchestrates single-track or hybrid answers by question intent.

The default answer shape (`--corpus hybrid`) is:

**Standards requirements → Project implementation → Product steps → Alignment & gaps**

## Demo

Watch a short walkthrough of the hybrid RAG in action:


https://github.com/user-attachments/assets/a55a3dec-eee8-4c38-9aef-855a1023afbc


If the player does not render in your GitHub client, open the file directly: [`assets/rag-demo.mp4`](assets/rag-demo.mp4).

## Three source RAGs

The three tracks are **physically isolated** (separate Chroma collections / chunk stores). Embeddings are never merged into one collection. Hybrid mode only combines retrieved chunks after retrieval, with numbered citations.

| Track | ID | What it covers | Corpus / index |
|-------|------|----------------|----------------|
| **1. Standards** | `hk_cde` | Hong Kong industry standards: CIC BIM Standards, CDE Beginner Guide, DEVB Harmonisation, BD ADM-19 / ADV-34, LandsD BIM-GIS, and related chapter Markdown plus Chinese alias routing | `knowledge/industry/hk_cde/` → `.rag_data/industry_hk_cde/` |
| **2. Playbook** | `playbook` | ACC × HK implementation handbook: four-container CDE, naming, permissions, approvals, design collaboration, information requirements, and ACC Project Template (GC / Buildings) guidance | `knowledge/playbook/acc_hk_bim/` → `.rag_data/playbook_acc_hk/` |
| **3. Product (Docs)** | `docs` | Autodesk Docs / ACC official help: folder organization, Naming Standard, permissions, Workflow, Project Template, Model Browser, and related product steps | crawled help → ingest → `.rag_data/` (docs main store) |

Each track also has its own **Query KB (route dictionary)**: maps colloquial / Chinese aliases to preferred sections or URLs for pinning and query rewriting **before** vector search. Route entries themselves **do not** enter the LLM prompt.

```text
Source knowledge (Markdown / help docs)
        │
        ├─ ingest + chunk + embed ──► Chroma (content store)
        └─ build_query_kb ──────────► Route KB (routing only)
```

## Orchestration architecture

Entry point: `ask.py` → `HybridOrchestrator` (`rag/orchestrator/pipeline.py`).

```mermaid
flowchart TD
  Q[User question] --> META{Capabilities help?}
  META -->|yes| HELP[capabilities_help<br/>no retrieve / no LLM]
  META -->|no| CL[classify_intent<br/>capability + track hint]
  CL --> CORPUS{--corpus}
  CORPUS -->|docs / hk_cde / playbook| SINGLE[Single-track HybridRetriever]
  CORPUS -->|hybrid default| PARA[Parallel retrieve on 3 tracks]
  PARA --> PIN[Chunk pin<br/>capability-priority sections]
  PIN --> MERGE[merge_triple_contexts<br/>numbered Docs/HK/Playbook]
  MERGE --> COMPOSE{Rule compose?}
  COMPOSE -->|folder only| RULE[structured_compose<br/>4-section template]
  COMPOSE -->|no| LLM[generate_hybrid_answer<br/>4-section prompt + cites]
  RULE --> POLISH[Localized headers + polish]
  LLM --> VAL[validate_hybrid_answer]
  VAL -->|soft fail may retry| LLM
  VAL --> OUT[Answer + citations]
  SINGLE --> GEN[generate_answer]
  GEN --> OUT
```

### 1. Intent and meta Q&A

- **Capabilities help** (e.g. “what can you do”): returns capability text only; `track=meta`; no retrieve, no Ollama.
- **`classify_intent`**: detects a primary **capability** and track bias, then rewrites per-track sub-queries and drives pinning / Docs relevance filters.

Supported capabilities (single primary label; conflicts use priority order):

| Capability | Typical questions | Docs preference / pin |
|------------|-------------------|------------------------|
| `project_template` | ACC HK GC / project template | prefer `Configure_Templates_Docs` |
| `model_viewer` | Model Browser, filter RVT/IFC properties | hard pin `Model_Browser` + `Viewer_Settings_Files` |
| `permissions` | folder permissions / 设置权限 | prefer `Folder_Permissions` |
| `naming` | naming standard / Information Container ID | Docs Naming Standard + HK / Playbook naming pins |
| `workflow` | approval workflow / Authorisation Gateway | prefer `Reviews_Create_Edit` |
| `project_create` | create ACC project | prefer `Create_Project` |
| `folder` | folder structure / 四容器 | hard pin Organize Files + Playbook WIP tree |

Notes:

- Bare glossary questions like “WIP 是什么” stay on `hk_cde` and **do not** trigger folder pinning or structured compose.
- Multi-signal phrases prefer the more specific capability (e.g. “文件夹权限” → `permissions`, “文件夹命名标准” → `naming`).
- Forced `--corpus docs|hk_cde|playbook|hybrid` **keeps** the detected capability and uses its template sub-queries on that track.

### 2. Single-track vs hybrid

| `--corpus` | Behavior |
|------------|----------|
| `docs` / `hk_cde` / `playbook` | Retrieve only that content store + its Query KB; still applies capability rewrite / soft Docs prefer when detected |
| `hybrid` (default) | Parallel 3-track retrieve → merge → 4-section answer |
| `auto` | Pick track from classifier (product- vs standards-leaning) |

### 3. Hybrid merge and answer writing

1. **Parallel retrieval**: Docs / HK CDE / Playbook each run embedding + BM25 hybrid search with capability-specific queries when available.
2. **Capability pin / prefer**:
   - Strong pins (`folder`, `naming`, `model_viewer`): swap in known good pages when retrieval drifts to overview / noise pages.
   - Soft prefer (`permissions`, `project_create`, `project_template`, `workflow`): put target Docs GUIDs first, keep normal retrieval as the second source.
   - Folder Playbook fallback only accepts explicit WIP tree evidence; otherwise it falls back to normal retrieval (no arbitrary first hit).
3. **`merge_triple_contexts`**: builds a shared numbered context list (`[1]`…) and records which track each chunk came from for later validation.
4. **Answer priority**:
   - `folder` uses **`structured_compose`**: rule-based four sections to reduce empty “cannot confirm” answers from small models.
   - Otherwise **`generate_hybrid_answer`**: enforces the four-section structure; **Route KB never enters the prompt**.
5. **Validation**: Docs capability keyword prefilter drops overview / Power BI / “What’s New” noise; soft warnings may trigger a regenerate retry.
6. **Language**: section headers follow the question language (EN → Standards Requirements / Implementation Guidance / Product Steps / Alignment & Gaps).

### Four-section answer contract

| Chinese | English | Primary source |
|---------|---------|----------------|
| 标准要求 | Standards Requirements | `hk_cde` |
| 实施建议 | Implementation Guidance | `playbook` |
| 产品操作 | Product Steps | `docs` |
| 对齐与缺口 | Alignment & Gaps | Combined (fits + product/process gaps) |

## Evaluation

Frozen baseline comparison suite: [`eval/RESULTS.md`](eval/RESULTS.md).

`scripts/eval_hybrid.py` also asserts `expect_capability` from [`eval/hybrid_cases.jsonl`](eval/hybrid_cases.jsonl). Latest hybrid orchestration run:

| Metric | Result |
|--------|--------|
| Cases | 14 |
| Intent accuracy | **100%** (14/14) |
| Capability accuracy | **100%** (14/14) |
| DualRecall (Docs+HK) | **100%** (7/7 hybrid expects) |
| TripleRecall (+Playbook) | **100%** (7/7) |
| False hybrid (pure track stolen) | **0** |

On cross-domain hybrid-expect cases, forced single-track retrieval still cannot cover more than one source family; see `eval_hybrid_vs_single.py` / `RESULTS.md`.

```bash
python scripts/run_eval_suite.py
# pieces:
python scripts/eval_query_kb.py
python scripts/eval_hk_cde.py
python scripts/eval_playbook_acc_hk.py
python scripts/eval_hybrid.py
python scripts/eval_hybrid_vs_single.py
```

## Quick start

### Dependencies

- Python 3.11+
- [Ollama](https://ollama.com/) for local generation + embedding (defaults in `rag/config.py`)
- Built indexes for all three tracks (or rebuild with the steps below)

```bash
cd /path/to/hk-bim-cde-standard-x-acc-rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Pull generation + embedding models
ollama pull qwen3.5:4b
ollama pull qwen3-embedding:0.6b
```

### Ask questions

```bash
python ask.py "How should Hong Kong CDE folders be set up?"
python ask.py "file naming standard"
python ask.py "what can you do"
python ask.py "按港标要求在ACC配置文件夹权限"
python ask.py "在 ACC 里如何查看并过滤 BIM 模型属性，并对照香港 BIM 要求做审核？"

# Retrieval only + path debug
python ask.py --no-generate --show-retrieval-debug "permissions on folders"

# Single track (capability rewrite still applied when detected)
python ask.py --corpus hk_cde "WIP Shared Published"
python ask.py --corpus docs "Organize Files"
python ask.py --corpus playbook "01_WIP discipline folders"
```

Full CLI reference: [COMMANDS.md](COMMANDS.md).

### Rebuild indexes (summary)

```bash
# Docs product store (requires help HTML / corpus first)
python ingest.py --rebuild
python scripts/build_query_kb.py

# Hong Kong standards store
python scripts/ingest_industry_hk_cde.py --rebuild
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild

# Playbook store
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_query_kb.py
python scripts/build_playbook_kb_index.py --rebuild
```

PDF extraction and copyright notes: `knowledge/industry/hk_cde/README.md`. Official PDFs live under local `output/HK Standard/` (not committed by default).

## Repository layout

```text
ask.py / ingest.py     CLI entry points
rag/                   Retrieval, generation, track configs, orchestrator
knowledge/             Versioned Markdown corpora + route KBs
scripts/               Extract, ingest, eval, research scripts
eval/                  Evaluation cases (+ RESULTS.md baseline)
tests/                 Unit tests (capability / pin / corpus)
output/                Crawl mirrors and official PDFs (local, gitignored)
.rag_data/             Chroma / chunks (local, gitignored)
```

## Design principles

1. **Three separate stores**: standards, playbook, and product help have different semantics; one shared collection pollutes retrieval.
2. **Hybrid synthesizes after retrieve**: each track retrieves independently; then number-merge + four-section writing.
3. **Route ≠ context**: Query KB / route indexes only select chapters and rewrite queries.
4. **Capability-aware routing**: classify once, then rewrite, pin/prefer, and validate so Docs stays on actionable pages (not About / What’s New / Power BI drift).
5. **Small-model friendly**: critical capabilities use structured compose / pinning to cut hallucination and empty answers.
6. **Traceable**: `[n]` citations map to the merged chunk list so each claim can be checked by track.

## License / copyright

- Code and self-authored playbook text may be used under this repository’s normal practice.
- CIC / DEVB / BD / LandsD / Autodesk materials remain copyright of their owners. This project keeps extracted Markdown for RAG; **do not push full official PDF packages to a public repository**.
