"""元问题：「你能做什么」类能力说明（不走检索/LLM）。"""

from __future__ import annotations

import re

from rag.answer_language import resolve_answer_language

_HELP_RE = re.compile(
    r"("
    r"你可以做什么|你能做什么|你能帮什么|你会什么|"
    r"有什么功能|有哪些功能|能回答什么|可以问什么|"
    r"怎么用|如何使用|使用说明|使用幫助|使用帮助|"
    r"what\s+can\s+you\s+do|what\s+do\s+you\s+do|"
    r"how\s+can\s+you\s+help|your\s+capabilities"
    r")",
    re.I,
)

# 过短或过泛的 help，避免误伤「help with folder permissions」等业务问
_HELP_ONLY_RE = re.compile(
    r"^\s*("
    r"帮助|幫助|help|hello|hi|"
    r"你可以做什么|你能做什么|你能帮什么|你会什么|"
    r"有什么功能|有哪些功能|能回答什么|可以问什么|"
    r"怎么用|如何使用|使用说明|"
    r"what\s+can\s+you\s+do\??|"
    r"what\s+do\s+you\s+do\??|"
    r"how\s+can\s+you\s+help\??|"
    r"your\s+capabilities\??"
    r")\s*$",
    re.I,
)


def is_capabilities_help_question(question: str) -> bool:
    text = (question or "").strip()
    if not text:
        return False
    if _HELP_ONLY_RE.match(text):
        return True
    # 「你是谁 / 介绍一下你自己」等
    if re.search(r"你是谁|你是誰|介绍一下(你|系统)|介紹一下(你|系統)", text):
        return True
    # 带「你可以做什么」短语，且问题不太长（避免夹在复杂业务问里）
    if len(text) <= 40 and _HELP_RE.search(text):
        # 排除明显业务词主导
        if re.search(
            r"文件夹|文件夾|审批|審批|命名|权限|權限|WIP|CDE|ADM|ADV|BIM|ACC|Docs",
            text,
            re.I,
        ):
            return False
        return True
    return False


_HELP_ZH_HANS = """我是本地 **ACC × 港标 RAG 助手**：只根据已入库资料回答，不联网。

## 我能做什么

1. **Autodesk Docs / ACC 产品操作**  
   建文件夹、权限、命名标准、审批流、项目模板、Design Collaboration 等「怎么在界面里做」。

2. **香港 BIM / CDE 标准**  
   CIC、DEVB Harmonisation、ISO 19650 相关、WIP/Shared/Published、以及 BD ADM-19 / ADV-34、LandsD BIM-GIS 等条款要求。

3. **实施手册（Playbook）**  
   组织推荐配置：四容器目录、`ACC HK GC Buildings` 项目样板、权限与工作流落地方案、对齐与缺口。

4. **三轨综合（默认 hybrid）**  
   同一问题给出：**标准要求 → 实施建议 → 产品操作 → 对齐与缺口**。

## 我不能做什么

- 不能替代合同/法定意见；手册内容是推荐配置，不是 CIC/DEVB 官方模板。  
- 不能操作你的真实 ACC 账号，也不能保证与线上最新 Docs 帮助 100% 同步。  
- 资料里没有的内容会回答「根据现有资料无法确认」。

## 可以这样问

- 「WIP 是什么」  
- 「怎么按港标在 ACC 配置文件夹结构」  
- 「屋宇署 ADV-34 对 BIM 法定提交有什么要求」  
- 「香港总包 ACC 项目样板怎么配置」

需要强制三轨用：`--corpus hybrid`；单轨：`--corpus docs` / `hk_cde` / `playbook`；默认 `auto`。更全的命令见项目里的 `COMMANDS.md`。
"""

_HELP_ZH_HANT = """我是本地 **ACC × 港標 RAG 助手**：只根據已入庫資料回答，不聯網。

## 我能做什麼

1. **Autodesk Docs / ACC 產品操作**  
   建資料夾、權限、命名標準、審批流、項目模板、Design Collaboration 等介面操作。

2. **香港 BIM / CDE 標準**  
   CIC、DEVB Harmonisation、ISO 19650、WIP/Shared/Published，以及 BD ADM-19 / ADV-34、LandsD BIM-GIS 等要求。

3. **實施手冊（Playbook）**  
   組織推薦配置：四容器目錄、`ACC HK GC Buildings` 項目樣板、權限與工作流落地、對齊與缺口。

4. **三軌綜合（預設 hybrid）**  
   同一問題給出：**標準要求 → 實施建議 → 產品操作 → 對齊與缺口**。

## 我不能做什麼

- 不能取代合約／法定意見；手冊是推薦配置，非 CIC/DEVB 官方模板。  
- 不能操作真實 ACC 帳號，也不保證與線上最新 Docs 說明完全同步。  
- 資料沒有的內容會回答「根據現有資料無法確認」。

## 可以這樣問

- 「WIP 是什麼」  
- 「怎麼按港標在 ACC 配置文件夾結構」  
- 「屋宇署 ADV-34 對 BIM 法定提交有什麼要求」  
- 「香港總包 ACC 項目樣板怎麼配置」

強制三軌用：`--corpus hybrid`；單軌：`--corpus docs` / `hk_cde` / `playbook`；預設 `auto`。詳見 `COMMANDS.md`。
"""

_HELP_EN = """I'm the local **ACC × Hong Kong BIM RAG assistant**. Answers are grounded in the ingested corpus only (no live web).

## What I can do

1. **Autodesk Docs / ACC how-tos** — folders, permissions, naming standards, reviews, project templates, Design Collaboration.
2. **Hong Kong BIM / CDE standards** — CIC, DEVB Harmonisation, ISO 19650 concepts (WIP/Shared/Published), plus BD ADM-19 / ADV-34 and LandsD BIM–GIS guidance.
3. **Implementation playbook** — recommended ACC setups (folder trees, GC Buildings template, workflows, gaps vs standards).
4. **Hybrid answers (default)** — **Standards → Playbook → Product steps → Alignment & gaps** in one reply.

## What I cannot do

- Replace contractual or statutory advice; playbook text is organisational guidance, not an official CIC/DEVB ACC template.
- Operate your live ACC project or guarantee 100% sync with the public Help site.
- Invent facts when the corpus has no support (“cannot confirm from available materials”).

## Example questions

- “What is WIP in the CDE?”
- “How should we set ACC folders for HK BIM standards?”
- “What does BD ADV-34 require for BIM plan submissions?”
- “How do I configure the HK GC ACC project template?”

Use `--corpus hybrid` to force three tracks; `--corpus docs` / `hk_cde` / `playbook` for a single track; default is `auto`. See `COMMANDS.md` for all CLIs.
"""


def build_capabilities_help(*, question: str, answer_lang: str = "auto") -> str:
    lang = resolve_answer_language(question, answer_lang)
    if lang == "en":
        return _HELP_EN.strip()
    if lang == "zh-Hant":
        return _HELP_ZH_HANT.strip()
    return _HELP_ZH_HANS.strip()
