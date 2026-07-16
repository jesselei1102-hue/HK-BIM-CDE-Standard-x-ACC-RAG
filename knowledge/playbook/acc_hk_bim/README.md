# ACC × HK implementation playbook (RAG corpus)

Recommended ACC configuration for Hong Kong BIM / CDE delivery — **not** an official CIC/DEVB template. Source drafts sync from `output/acc_hk_bim_playbook/`.

ACC Project Template research syncs from `ACC Project Template/ACC Template` → `research/acc_project_template/`, condensed into `corpus/08_project_template.md`.

```bash
python scripts/build_playbook_query_kb.py
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_kb_index.py --rebuild
python ask.py --corpus playbook "How to configure the HK GC ACC project template?"
```

| Chapter | Content |
|---------|---------|
| 00–07 | Overview, account setup, four-container CDE, naming, permissions, approvals, design collaboration, information requirements |
| 08 | ACC Project Template (HK GC / Buildings) |
