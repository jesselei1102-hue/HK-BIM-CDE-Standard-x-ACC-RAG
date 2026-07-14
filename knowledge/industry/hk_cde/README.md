# 香港 CDE 行业知识库

英文章节原文 RAG + 中文别名路由索引；与 Autodesk Docs 产品库并行。

## 来源与版权

| 文档 | 路径 |
|------|------|
| CIC BIM Standards General 2024 | `output/HK Standard/CIC BIM Standards General 2024/` |
| CIC Beginner Guide – Adoption of CDE | `output/HK Standard/CIC Beginner Guide-Adoption of CDE.pdf` |
| DEVB BIM Harmonisation Guidelines v3.0 | `output/HK Standard/DEVB BIM Harmonisation Guidelines for WDs (v3_0) with All Appendices.pdf` |
| BD PNAP ADM-19 / ADV-34 | `output/HK Standard/BD_LandsD/`（自 ACC Template specification 同步） |
| LandsD BIM-GIS Guidelines Jun 2023 | 同上 |
| Appendix D1–D9 模板 | 同上 CIC 目录（仅字段清单入库，非全文） |

材料版权归 CIC / 香港政府所有。本库仅供内部学习与 RAG 问答，**不得对外分发 PDF 原文包**。

## 目录结构

```text
knowledge/industry/hk_cde/
  corpus/              # 按章节抽取的英文 Markdown
  research/            # page_ledger、manifest、extract_report、priority_sections
  query_kb.jsonl       # 路由条目（approved，含中文别名）
  README.md

.rag_data/industry_hk_cde/
  chunks.jsonl
  chroma/              # collection: industry_hk_cde
  kb_chroma/           # collection: industry_hk_cde_route
```

## 完整性 vs 入库范围

- **page_coverage_pct**（`extract_report.json`）：源 PDF 每一页是否在 `page_ledger.jsonl` 记账。
- **ingested_page_pct**（`manifest.json`）：v1 默认仅 `priority: high` 章节进入向量库；可低于 100% 页覆盖率，**这是预期行为**。
- ingest 前必须通过 `validate_hk_extract_completeness.py`（exit 0）。

## 重建命令

```bash
cd /path/to/爬虫项目
source .venv/bin/activate
pip install -r requirements.txt

# 1. 抽取 PDF + 页账
python scripts/extract_hk_cde_pdfs.py

# 1b. BD / LandsD 补充（独立脚本，不改主 page_ledger）
python scripts/extract_hk_bd_landsd.py

# 2. 模板字段（D1–D9）
python scripts/extract_hk_templates.py

# 3. 完整性门禁
python scripts/validate_hk_extract_completeness.py

# 4. 行业 chunk 索引（默认仅 high）
python scripts/ingest_industry_hk_cde.py --rebuild

# 5. 路由 KB + 向量索引
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild

# 6. 评测
python scripts/eval_hk_cde.py
```

全量 ingest（含 normal 优先级）：`python scripts/ingest_industry_hk_cde.py --all --rebuild`

## 问答 CLI

```bash
# 默认 hybrid（三轨：港标 + Playbook + Docs）
python ask.py "怎么按港标在 ACC 配置文件夹结构"

# 自动分流 / 强制单轨
python ask.py --corpus auto "WIP 是什么"            # 编排分流
python ask.py --corpus hk_cde "Gateway 的作用"
python ask.py --corpus docs "设置权限"
python ask.py --corpus playbook "香港总包ACC项目样板怎么配置"
```

**硬约束**：路由索引元数据不进 LLM prompt；单轨答案只来自该轨 chunk。

## 复合问答（V2 编排）

当问题同时含**产品操作**与**标准/制度**信号时，`auto` / `hybrid` 会：

1. 按同一能力对象拆成两路子查询（行业：要求是什么；Docs：怎么做）
2. 并行检索后一次生成三段：**标准要求 → 产品操作 → 对齐与缺口**
3. 对不上的映射写「缺口」，禁止编造菜单与条款假对应

评测：`python scripts/eval_hybrid.py`（可选 `--generate` 检查三段标题）

Hybrid 生成后有一层轻量校验（结构 / 编号归属 / 产品页相关性）；弱相关 Docs 页会在生成前剔除，硬失败最多重试一次。`--show-retrieval-debug` 可见 `validation` 警告。

## 与产品库边界

| 问题类型 | 轨道 |
|----------|------|
| CDE 制度、WIP/Gateway、PIR/OIR、DEVB 命名 | 行业 `hk_cde` |
| Autodesk Docs 怎么点、权限、界面操作 | 产品 `docs` |
| 标准要求 + 产品怎么做（同一能力） | `hybrid` 编排 |

`query_kb.jsonl` 中 `related_product_guids` 预留给 V2.1 桥接 boost；当前 hybrid 不依赖该字段。
