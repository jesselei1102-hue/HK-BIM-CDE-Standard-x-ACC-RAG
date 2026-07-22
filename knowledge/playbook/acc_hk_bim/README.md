# ACC × HK implementation playbook (RAG corpus)

Active corpus is the **HK CDE Spec** actual-project specifications (Buildings + Civil).  
Legacy chapters `00–08` are archived under `research/corpus_legacy_v1/` and are **not** ingested.

Sources:

- `output/HK CDE Spec/ACC_HK_GC_Buildings_Project_Specification.md`
- `output/HK CDE Spec/ACC_HK_GC_Civil_Project_Specification.md`

Diff / precedence notes: [`research/hk_cde_spec_diff.md`](research/hk_cde_spec_diff.md)

```bash
python scripts/build_playbook_query_kb.py
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_kb_index.py --rebuild
python ask.py --corpus playbook "Buildings九段命名规则是什么？"
python ask.py --corpus playbook "Civil LandsD提交包最少要有什么？"
```

| Chapter | Domain | Content |
|---------|--------|---------|
| `00_hk_cde_spec_index` | mixed | Buildings vs Civil index |
| `10–15_buildings_*` | buildings | Roles, folders/permissions, issues/WF, naming, BD forms, EMSD/MIDP/acceptance |
| `20–25_civil_*` | civil | Roles, folders/permissions, issues/WF, naming, LandsD forms, AssetClass/MIDP/acceptance |

**Authority:** within the Playbook track these specs override legacy template guidance. CIC/DEVB/ISO stay on the `hk_cde` track; Autodesk product help stays on `docs`.
