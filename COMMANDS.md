# ACC × 港标 RAG — 指令手册

本地三轨 RAG（Docs / 香港 CDE / Playbook）的全部常用命令。  
项目根目录：任意含 `ask.py` 的路径（下文以 `<项目根>` 表示）。

---

## 0. 环境准备（每次开始）

```bash
cd /Users/jiaxi/Documents/爬虫项目
source .venv/bin/activate          # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt    # 首次或依赖变更时
```

检查 Ollama 与依赖：

```bash
ollama serve                       # 若服务未启动
ollama pull qwen3-embedding:0.6b
ollama pull qwen3.5:4b
python -m rag.preflight
```

---

## 1. 问答（最常用）

入口：`ask.py`  
**默认** `--corpus hybrid`**（三轨）**。

```bash
# 默认 hybrid：港标 + Playbook + Docs
python ask.py "怎么按港标在 ACC 配置文件夹结构"

# 能力说明（不检索）
python ask.py "你可以做什么"

# 交互模式（不传问题）
python ask.py
# 输入问题；空行 / exit / quit / q 退出
```



### 1.1 `--corpus` 语料轨


| 值          | 含义                                                 |
| ---------- | -------------------------------------------------- |
| `hybrid`   | **默认**。强制三轨并行检索并作四段答                               |
| `auto`     | 意图分流：产品→docs / 港标→hk_cde / 实施→playbook / 复合→hybrid |
| `docs`     | 仅 Autodesk Docs 帮助                                 |
| `hk_cde`   | 仅香港 CDE / CIC / DEVB / BD / LandsD                 |
| `playbook` | 仅 ACC×港标实施手册                                       |


```bash
python ask.py --corpus auto "WIP 是什么"
python ask.py --corpus docs "如何创建文件夹"
python ask.py --corpus hk_cde "ADM-19 关于从BIM模型提取信息的规定"
python ask.py --corpus playbook "香港总包ACC项目样板怎么配置"
python ask.py --corpus hybrid "符合港标的审批流怎么在 ACC 做"
```



### 1.2 其他参数


| 参数                               | 说明                               |
| -------------------------------- | -------------------------------- |
| `--top-k N`                      | 每轨返回上下文条数（hybrid 默认 Docs=2、其它=1） |
| `--no-generate`                  | 只检索、不调用 LLM（预检来源）                |
| `--show-context`                 | 打印检索到的上下文摘要                      |
| `--show-retrieval-debug`         | 打印编排意图、检索路径、校验警告                 |
| `--lang auto|en|zh-Hans|zh-Hant` | 回答语言（默认 `auto` 跟提问）              |


```bash
python ask.py --no-generate "怎么按港标在 ACC 配置文件夹结构"
python ask.py --show-context --show-retrieval-debug "设置权限"
python ask.py --lang zh-Hans --top-k 3 "命名标准怎么配"
```

---



## 2. 重建索引（语料变更后）

按轨执行。改语料后至少重建受影响的轨。

### 2.1 Docs 产品轨

```bash
python ingest.py --rebuild          # 完整重建 Chroma
python ingest.py --dry-run          # 只切分，不写向量
python scripts/build_query_kb.py    # 生成 Docs 路由 KB 种子
python scripts/build_kb_index.py --rebuild
```



### 2.2 香港 CDE（行业轨）

```bash
# 从 PDF 抽章节（源在 output/HK Standard/）
python scripts/extract_hk_cde_pdfs.py
python scripts/extract_hk_cde_pdfs.py --force   # 忽略哈希强制重抽

# BD ADM-19 / ADV-34 / LandsD BIM-GIS 补充
python scripts/extract_hk_bd_landsd.py
python scripts/extract_hk_bd_landsd.py --dry-run

# CIC 模板字段 D1–D9
python scripts/extract_hk_templates.py

# 完整性门禁（ingest 前必须通过）
python scripts/validate_hk_extract_completeness.py
python scripts/validate_hk_extract_completeness.py --acknowledge-quality

# 向量索引（默认仅 priority=high）
python scripts/ingest_industry_hk_cde.py --rebuild
python scripts/ingest_industry_hk_cde.py --rebuild --all      # 含 normal
python scripts/ingest_industry_hk_cde.py --dry-run
python scripts/ingest_industry_hk_cde.py --skip-validation

# 路由 KB
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild
```



### 2.3 Playbook（实施手册轨）

```bash
python scripts/build_playbook_query_kb.py
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/ingest_playbook_acc_hk.py --dry-run
python scripts/build_playbook_kb_index.py --rebuild
```



### 2.4 三轨一键重建（参考）

```bash
source .venv/bin/activate

python ingest.py --rebuild
python scripts/build_query_kb.py
python scripts/build_kb_index.py --rebuild

python scripts/extract_hk_cde_pdfs.py
python scripts/extract_hk_bd_landsd.py
python scripts/extract_hk_templates.py
python scripts/validate_hk_extract_completeness.py
python scripts/ingest_industry_hk_cde.py --rebuild
python scripts/build_industry_query_kb.py
python scripts/build_industry_kb_index.py --rebuild

python scripts/build_playbook_query_kb.py
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_kb_index.py --rebuild
```

---



## 3. 评测

```bash
python scripts/eval_hk_cde.py
python scripts/eval_hk_cde.py --cases eval/hk_cde_cases.jsonl

python scripts/eval_hybrid.py
python scripts/eval_hybrid.py --generate   # 额外检查 hybrid 生成结构（慢）
python scripts/eval_hybrid.py --cases eval/hybrid_cases.jsonl

python scripts/eval_playbook_acc_hk.py
python scripts/eval_playbook_acc_hk.py --cases eval/playbook_acc_hk_cases.jsonl

python scripts/eval_query_kb.py
python scripts/eval_query_kb.py --cases eval/query_kb_cases.jsonl
```

Pytest（切分 / 入库 / KB 等单元测试）：

```bash
pytest tests/ -q
```

---



## 4. 模型对比与调试

```bash
# 同一检索结果对比多个本地 LLM
python compare_models.py "怎么创建文件夹"
python compare_models.py --models "gemma3:1b,qwen3.5:4b" "设置权限"
python compare_models.py --file questions.txt --top-k 3 --show-retrieval-debug
```

Docs / 检索研究辅助：

```bash
python scripts/research_corpus.py
python scripts/research_corpus.py --output-dir knowledge/research

python scripts/research_retrieval.py
python scripts/research_retrieval.py --queries path/to/queries.txt --output out.jsonl

python scripts/research_external.py
python scripts/research_external.py --pages-index ... --output ...

python scripts/merge_kb_candidates.py
```

---



## 5. 爬虫（语料采集，非问答）

详见根目录原 `README.md`（爬虫教程）。简要：

```bash
# 通用 HTML 文档站
python download_help_docs.py "https://example.com/docs/"
python download_help_docs.py "URL" -n 50 -d 1 -f markdown --base "URL前缀"

# Autodesk Help（需 Playwright）
pip install playwright && playwright install chromium
python download_autodesk_help.py "https://help.autodesk.com/view/DOCS/ENU/"
```

Docs 语料默认来自 `output/DOCS/DOCS_help_*.md`（由 `RAG_FILE_GLOB` 控制）。

---



## 6. 常用环境变量

三轨共用（Docs / 行业 / Playbook 多数继承）：


| 变量                       | 默认                       | 含义                |
| ------------------------ | ------------------------ | ----------------- |
| `OLLAMA_HOST`            | `http://127.0.0.1:11434` | Ollama 地址         |
| `RAG_EMBEDDING_MODEL`    | `qwen3-embedding:0.6b`   | 向量模型              |
| `RAG_LLM_MODEL`          | `qwen3.5:4b`             | 生成模型              |
| `RAG_CHUNK_TOKENS`       | `600`                    | 切块目标 token        |
| `RAG_CHUNK_OVERLAP`      | `100`                    | 切块重叠              |
| `RAG_TOP_K`              | `3`                      | 单轨默认 top-k        |
| `RAG_MAX_CONTEXT_TOKENS` | `2000`                   | 喂给 LLM 的上下文上限     |
| `RAG_MIN_SIMILARITY`     | Docs `0.55` / 其它轨或不同     | 最低向量相似度           |
| `RAG_DATA_DIR`           | `.rag_data`              | Docs 索引目录         |
| `RAG_COLLECTION`         | `autodesk_docs`          | Docs collection 名 |


Playbook 专用示例：`PLAYBOOK_CORPUS_DIR`、`PLAYBOOK_DATA_DIR`、`PLAYBOOK_COLLECTION`、`PLAYBOOK_KB_*`。  
行业轨：`INDUSTRY_*` / 见 `rag/industry_hk/config.py`。

临时指定模型：

```bash
RAG_LLM_MODEL=qwen3.5:4b python ask.py "问题"
```

---



## 7. 数据目录一览


| 路径                                      | 内容                       |
| --------------------------------------- | ------------------------ |
| `knowledge/query_kb.jsonl`              | Docs 路由 KB               |
| `knowledge/industry/hk_cde/corpus/`     | 港标 Markdown 语料           |
| `knowledge/playbook/acc_hk_bim/corpus/` | Playbook 语料              |
| `.rag_data/`                            | Docs chunks + Chroma     |
| `.rag_data/industry_hk_cde/`            | 港标索引                     |
| `.rag_data/playbook_acc_hk/`            | Playbook 索引              |
| `output/HK Standard/`                   | 港标 PDF 源（含 `BD_LandsD/`） |
| `output/DOCS/`                          | Docs 爬取原文                |
| `eval/*.jsonl`                          | 评测用例                     |


---



## 8. 推荐日常用法

```bash
# 日常问答（默认 hybrid）
python ask.py "你的问题"

# 纯标准（更快、不凑产品页）
python ask.py --corpus hk_cde "香港 BIM standard 有什么要求"

# 答得怪时先看检索再决定
python ask.py --no-generate --show-retrieval-debug "问题"

# 改完 playbook MD 后
python scripts/build_playbook_query_kb.py
python scripts/ingest_playbook_acc_hk.py --rebuild
python scripts/build_playbook_kb_index.py --rebuild
```

---



## 9. 脚本索引（按文件）


| 脚本                                                 | 作用               |
| -------------------------------------------------- | ---------------- |
| `ask.py`                                           | 问答入口             |
| `ingest.py`                                        | Docs 向量索引        |
| `compare_models.py`                                | 多 LLM 对比         |
| `python -m rag.preflight`                          | 依赖与模型检查          |
| `scripts/extract_hk_cde_pdfs.py`                   | 港标主 PDF 抽取       |
| `scripts/extract_hk_bd_landsd.py`                  | BD/LandsD PDF 抽取 |
| `scripts/extract_hk_templates.py`                  | D1–D9 模板字段       |
| `scripts/validate_hk_extract_completeness.py`      | 港标抽取门禁           |
| `scripts/ingest_industry_hk_cde.py`                | 港标向量索引           |
| `scripts/ingest_playbook_acc_hk.py`                | Playbook 向量索引    |
| `scripts/build_*_query_kb.py`                      | 生成路由种子 jsonl     |
| `scripts/build_*_kb_index.py`                      | 路由向量索引           |
| `scripts/eval_*.py`                                | 评测               |
| `scripts/research_*.py` / `merge_kb_candidates.py` | Docs/KB 研究辅助     |
| `download_help_docs.py`                            | 通用爬虫             |
| `download_autodesk_help.py`                        | Autodesk 爬虫      |


任意脚本可加 `-h` / `--help` 查看最新参数。