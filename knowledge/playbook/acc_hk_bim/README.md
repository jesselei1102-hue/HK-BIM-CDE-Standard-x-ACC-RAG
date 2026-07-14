# ACC × 港标实施手册（Playbook）RAG 语料

组织推荐配置，非 CIC/DEVB 官方模板。源稿同步自 `output/acc_hk_bim_playbook/`；  
ACC 项目样板研究同步自 `ACC Project Template/ACC Template` → `research/acc_project_template/`，浓缩章为 `corpus/08_project_template.md`。

```bash
python scripts/build_playbook_query_kb.py
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_kb_index.py --rebuild
python ask.py --corpus playbook "香港总包ACC项目样板怎么配置"
```

| 章节 | 内容 |
|------|------|
| 00–07 | 总览、账户、四容器 CDE、命名、权限、审批、设计协同、信息要求 |
| 08 | ACC Project Template（香港 GC / Buildings） |