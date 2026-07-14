"""基于检索结果的本地 grounded 生成。"""

from __future__ import annotations

from dataclasses import dataclass

import ollama

from .answer_language import (
    empty_hybrid_answer,
    hybrid_section_headers,
    language_instruction,
    polish_hybrid_answer,
    resolve_answer_language,
)
from .config import AppConfig, get_config
from .orchestrator.merge import MergedContexts, format_partitioned_context
from .retrieval import RetrievedChunk, format_context


SYSTEM_PROMPT = """你是 Autodesk Docs 帮助文档助手。
规则：
1. 只根据编号资料回答；资料写了什么就答什么，禁止用自己的先验知识覆盖资料。
2. 资料里有明确数字、限制或步骤时，直接摘录并回答。
3. 资料与问题无关，或无法支持结论时，只回复：根据现有资料无法确认。
4. 用提问语言作答；关键事实后标注 [1] 或 [2]。
5. 回答简洁，通常 2–5 句，不要复述整段资料，也不要输出思考过程。"""


PLAYBOOK_SYSTEM_PROMPT = """你是 ACC × 港标实施手册助手。
规则：
1. 只根据编号资料回答；资料是组织推荐配置，不是 CIC/DEVB 官方模板。
2. 资料写了什么就答什么；涉及缺口或须写入 BEP 的事项要明确写出。
3. 资料与问题无关，或无法支持结论时，只回复：根据现有资料无法确认。
4. 用提问语言作答；关键事实后标注 [1] 或 [2]。
5. 回答简洁，通常 3–8 句，不要复述整段资料，也不要输出思考过程。"""


def _hybrid_system_prompt(lang: str) -> str:
    h = hybrid_section_headers(lang)  # type: ignore[arg-type]
    if lang == "en":
        return f"""You are a three-source assistant: Hong Kong BIM/CDE standards, ACC×HK playbook, and Autodesk Docs help.
Rules:
1. Answer only from numbered materials; do not invent menus, buttons, or mappings.
2. You MUST use exactly these four section headings:
   ## {h[0]}
   ## {h[1]}
   ## {h[2]}
   ## {h[3]}
3. Style:
   - 2–5 short bullets or numbered steps per section; no essay, no long HK vs Playbook vs Docs comparison.
   - Quote folder names and menu paths when present (e.g. 01_WIP, Docs → Files).
   - Never start a section with "cannot confirm" and then analyse with citations—if you cite, answer directly.
   - Only write one "Cannot confirm from available materials." line when that section has no usable sources.
4. Citation ownership: {h[0]}→HK; {h[1]}→Playbook; {h[2]}→Docs.
5. {h[3]}: at most 3 bullets + one "Gap: …" sentence.
6. Do not output thinking."""
    return f"""你是三源助手：香港 BIM/CDE 标准、ACC×港标实施手册、Autodesk Docs 产品帮助。
规则：
1. 只根据编号资料回答；禁止编造资料里没有的菜单、按钮或映射。
2. 必须按以下四段标题作答（标题语言必须与回答语言一致）：
   ## {h[0]}
   ## {h[1]}
   ## {h[2]}
   ## {h[3]}
3. 写法（必须遵守）：
   - 每段 2–5 条短 bullet 或编号步骤；禁止论文体、禁止「HK vs Playbook vs Docs」三方长对照。
   - 资料里有目录树、夹名、菜单路径就必须直接写出来（如 01_WIP、Docs → Files）。
   - 禁止在一段里先写「根据现有资料无法确认」再引用 [1][2] 展开分析——有引用就说明能答，直接答。
   - 只有该段完全没有可用编号资料时，才写一句「根据现有资料无法确认」。
4. 编号归属：{h[0]}→HK；{h[1]}→Playbook；{h[2]}→Docs。
5. {h[3]}：最多 3 条 bullet + 1 句「缺口：…」。
6. 不要输出思考过程。"""


def _hybrid_few_shot(lang: str) -> str:
    h = hybrid_section_headers(lang)  # type: ignore[arg-type]
    if lang == "en":
        return f"""
Example ({h[1]} when materials include a folder tree):
## {h[1]}
- Under Project Files create: `01_WIP`, `02_Shared`, `03_Published`, `04_Archive` [2]
- Under WIP use discipline subfolders (ARC/STR/MEP…), then Models/Drawings [2]
- Enforce Naming Standard on Shared/Published; WIP may stay flexible [2]
"""
    return f"""
示例（{h[1]}段，资料含目录树时）：
## {h[1]}
- 在 Project Files 下建顶层夹：`01_WIP`、`02_Shared`、`03_Published`、`04_Archive` [2]
- WIP 下按专业分子夹（ARC/STR/MEP…），其下 Models/Drawings 等 [2]
- Shared/Published 启用 Naming Standard；WIP 内可不强制 [2]
"""


@dataclass(frozen=True)
class Answer:
    question: str
    answer: str
    contexts: list[RetrievedChunk]
    model: str


def build_user_prompt(
    question: str, chunks: list[RetrievedChunk], *, answer_lang: str = "auto"
) -> str:
    if not chunks:
        return (
            f"问题：{question}\n\n"
            "当前没有检索到相关资料。请直接说明根据现有资料无法确认。"
        )
    return (
        f"问题：{question}\n\n"
        f"{language_instruction(resolve_answer_language(question, answer_lang))}\n\n"
        "资料：\n"
        f"{format_context(chunks)}\n\n"
        "能答则给简洁步骤并标注编号；完全无关才说根据现有资料无法确认。"
    )


def build_hybrid_user_prompt(
    question: str, merged: MergedContexts, *, answer_lang: str = "auto"
) -> str:
    lang = resolve_answer_language(question, answer_lang)
    h = hybrid_section_headers(lang)
    if not merged.tracked:
        return (
            f"问题：{question}\n\n"
            f"当前没有检索到相关资料。请按四段标题（## {h[0]} …）说明无法确认。"
        )
    hk_note = (
        f"HK 编号：{merged.industry_indices}"
        if merged.industry_indices
        else "HK 编号：无"
    )
    playbook_note = (
        f"Playbook 编号：{merged.playbook_indices}"
        if merged.playbook_indices
        else "Playbook 编号：无"
    )
    docs_note = (
        f"Docs 编号：{merged.docs_indices}"
        if merged.docs_indices
        else "Docs 编号：无"
    )
    header_rule = (
        f"Section headings MUST be exactly: ## {h[0]} / ## {h[1]} / ## {h[2]} / ## {h[3]}"
        if lang == "en"
        else f"四段标题必须原样使用：## {h[0]} / ## {h[1]} / ## {h[2]} / ## {h[3]}"
    )
    return (
        f"问题：{question}\n\n"
        f"{language_instruction(lang)}\n"
        f"{header_rule}\n\n"
        f"{hk_note}；{playbook_note}；{docs_note}\n\n"
        f"{format_partitioned_context(merged)}\n\n"
        f"{_hybrid_few_shot(lang)}\n"
        "请按四段输出；每段短、可照着做；禁止段首「无法确认」后又长篇分析。"
    )


def _should_refuse(chunks: list[RetrievedChunk], minimum_similarity: float) -> bool:
    if not chunks:
        return True
    similarities = [
        chunk.vector_similarity
        for chunk in chunks
        if chunk.vector_similarity is not None
    ]
    if not similarities:
        return True
    return max(similarities) < minimum_similarity


def _extract_content(response: object) -> str:
    message = getattr(response, "message", None)
    if message is None and isinstance(response, dict):
        message = response.get("message", {})
    if isinstance(message, dict):
        content = message.get("content") or ""
        thinking = message.get("thinking") or ""
    else:
        content = getattr(message, "content", None) or ""
        thinking = getattr(message, "thinking", None) or ""
    return (content or thinking).strip()


def generate_answer(
    question: str,
    chunks: list[RetrievedChunk],
    config: AppConfig | None = None,
    *,
    system_prompt: str | None = None,
    answer_lang: str = "auto",
) -> Answer:
    app_config = config or get_config()
    if _should_refuse(chunks, app_config.retrieval.minimum_vector_similarity):
        return Answer(
            question=question,
            answer="根据现有资料无法确认。",
            contexts=chunks,
            model=app_config.models.generation_model,
        )

    prompt = system_prompt or SYSTEM_PROMPT
    product = getattr(getattr(app_config, "corpus", None), "product", "")
    if system_prompt is None and product == "playbook_acc_hk":
        prompt = PLAYBOOK_SYSTEM_PROMPT
    lang_line = language_instruction(resolve_answer_language(question, answer_lang))
    prompt = f"{prompt}\n\n{lang_line}"

    client = ollama.Client(
        host=app_config.models.ollama_host,
        timeout=app_config.models.request_timeout_seconds,
        trust_env=False,
    )
    # qwen3.5 默认 thinking 会占满输出且 content 为空，RAG 场景关闭思考。
    response = client.chat(
        model=app_config.models.generation_model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": build_user_prompt(question, chunks, answer_lang=answer_lang)},
        ],
        think=False,
        options={
            "temperature": 0.0,
            "num_predict": 400,
        },
    )
    return Answer(
        question=question,
        answer=_extract_content(response),
        contexts=chunks,
        model=app_config.models.generation_model,
    )


def generate_hybrid_answer(
    question: str,
    merged: MergedContexts | None,
    config: AppConfig | None = None,
    *,
    answer_lang: str = "auto",
) -> Answer:
    app_config = config or get_config()
    lang = resolve_answer_language(question, answer_lang)
    if merged is None or not merged.tracked:
        return Answer(
            question=question,
            answer=empty_hybrid_answer(lang),
            contexts=[],
            model=app_config.models.generation_model,
        )

    min_sim = app_config.retrieval.minimum_vector_similarity
    docs_ok = (
        not _should_refuse(merged.docs_chunks, min_sim) if merged.docs_chunks else False
    )
    industry_ok = (
        not _should_refuse(merged.industry_chunks, min_sim)
        if merged.industry_chunks
        else False
    )
    playbook_ok = (
        not _should_refuse(merged.playbook_chunks, min_sim)
        if merged.playbook_chunks
        else False
    )
    if not docs_ok and not industry_ok and not playbook_ok:
        h = hybrid_section_headers(lang)
        if lang == "en":
            cannot = "Cannot confirm from available materials."
            gap = "Gap: retrieval similarity on all tracks is too low to align."
        elif lang == "zh-Hant":
            cannot = "根據現有資料無法確認。"
            gap = "缺口：各軌檢索相似度不足，無法對齊。"
        else:
            cannot = "根据现有资料无法确认。"
            gap = "缺口：各轨检索相似度不足，无法对齐。"
        return Answer(
            question=question,
            answer=(
                f"## {h[0]}\n{cannot}\n\n"
                f"## {h[1]}\n{cannot}\n\n"
                f"## {h[2]}\n{cannot}\n\n"
                f"## {h[3]}\n{gap}"
            ),
            contexts=[item.chunk for item in merged.tracked],
            model=app_config.models.generation_model,
        )

    lang_line = language_instruction(lang)
    system = f"{_hybrid_system_prompt(lang)}\n\n{lang_line}"

    client = ollama.Client(
        host=app_config.models.ollama_host,
        timeout=app_config.models.request_timeout_seconds,
        trust_env=False,
    )
    response = client.chat(
        model=app_config.models.generation_model,
        messages=[
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": build_hybrid_user_prompt(
                    question, merged, answer_lang=answer_lang
                ),
            },
        ],
        think=False,
        options={
            "temperature": 0.0,
            "num_predict": 900,
        },
    )
    raw = _extract_content(response)
    return Answer(
        question=question,
        answer=polish_hybrid_answer(raw, lang=lang),
        contexts=[item.chunk for item in merged.tracked],
        model=app_config.models.generation_model,
    )


def format_sources(chunks: list[RetrievedChunk]) -> list[str]:
    lines: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        lines.append(f"[{index}] {chunk.title}\n    {chunk.source_url}")
    return lines
