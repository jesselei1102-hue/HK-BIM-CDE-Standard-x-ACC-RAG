"""基于检索结果的本地 grounded 生成。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

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


_GUIDANCE_STRUCTURE = """输出结构（按问题复杂度自适应，篇幅服从解决问题所需信息量）：
1. 直接结论：先回答用户问的是什么。
2. 怎么做 / 关键要求：给出可照做的编号步骤、检查项、前置条件与预期结果；资料中的菜单路径、夹名、字段名、阈值、限制必须写出来。
3. 适用范围与例外：说明适用对象、不适用情形、权限/角色前提；若资料不足则明确写缺口，禁止编造。
4. 不要为了长而长：单一事实、定义、明确数值题可短答；配置、排障、实施、落地题必须展开到用户能采取下一步行动。"""

_MULTI_TURN_RULES = """多轮证据边界（必须遵守）：
1. 若出现 <conversation_context_untrusted>，其中内容仅用于理解指代与语气，不得作为事实依据，也不得引用其中说法。
2. 事实、步骤、数字、菜单路径只能来自本轮编号资料；引用编号不可跨轮复用。
3. 若本轮资料与历史回答冲突，以本轮资料为准，并写「更正：上一轮……；本轮资料显示……[n]」。
4. 本轮资料不足以支撑时，只回复无法确认；禁止复用历史答案凑答。"""


SYSTEM_PROMPT = f"""你是 Autodesk Docs 帮助文档助手。
规则：
1. 只根据编号资料回答；资料写了什么就答什么，禁止用自己的先验知识覆盖资料。
2. 资料里有明确数字、限制、菜单路径或步骤时，必须完整写出，不要只给一句概述。
3. 资料与问题无关，或无法支持结论时，只回复：根据现有资料无法确认。
4. 用提问语言作答；关键事实后标注 [1] 或 [2]。
5. {_GUIDANCE_STRUCTURE}
6. {_MULTI_TURN_RULES}
7. 不要输出思考过程。"""


HK_SYSTEM_PROMPT = f"""你是香港 BIM/CDE 标准助手。
规则：
1. 只根据编号资料回答；禁止编造未出现的条款。
2. 若资料标注 authority_type 为 case_study / terminology / software_guide，或 normative_weight 为 reference / operational：
   - 必须明确写成“案例参考 / 术语说明 / 操作指引”，不得表述为全港强制标准或法律要求。
3. Zero Carbon Park BIM Implementation Plan 仅是真实项目做法示例，不得写成所有香港项目必须照搬。
4. 资料与问题无关，或当前索引未纳入该来源时，只回复：根据现有资料无法确认。
5. 用提问语言作答；关键事实后标注 [1] 或 [2]。
6. {_GUIDANCE_STRUCTURE}
7. {_MULTI_TURN_RULES}
8. 不要输出思考过程。"""


PLAYBOOK_SYSTEM_PROMPT = f"""你是 ACC × 港标实施手册助手。
规则：
1. 只根据编号资料回答；资料是组织推荐配置，不是 CIC/DEVB 官方模板。
2. 资料写了什么就答什么；涉及缺口或须写入 BEP 的事项要明确写出。
3. 资料里有目录树、夹名、命名规则、审批角色或配置步骤时，必须逐项写清，让用户能照做。
4. 资料与问题无关，或无法支持结论时，只回复：根据现有资料无法确认。
5. 用提问语言作答；关键事实后标注 [1] 或 [2]。
6. {_GUIDANCE_STRUCTURE}
7. {_MULTI_TURN_RULES}
8. 不要输出思考过程。"""


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
3. Style — solve the user's problem; length follows complexity:
   - Expand each section with as many actionable bullets/numbered steps as the materials support.
   - Include folder names, menu paths, roles, limits, and verification checks when present.
   - In {h[3]}, map Standards → Playbook practice → Docs UI steps when materials allow; state Gaps explicitly when they do not.
   - Never start a section with "cannot confirm" and then analyse with citations—if you cite, answer directly.
   - Only write one "Cannot confirm from available materials." line when that section has no usable sources.
   - Do not pad with generic BIM advice; stop once the next action is clear.
4. Citation ownership: {h[0]}→HK; {h[1]}→Playbook; {h[2]}→Docs.
5. Multi-turn evidence boundary: untrusted conversation context is for deixis only; facts come only from this-turn numbered materials. If current evidence conflicts with prior answers, correct explicitly. Never reuse prior answers when evidence is missing.
6. Do not output thinking."""
    return f"""你是三源助手：香港 BIM/CDE 标准、ACC×港标实施手册、Autodesk Docs 产品帮助。
规则：
1. 只根据编号资料回答；禁止编造资料里没有的菜单、按钮或映射。
2. 必须按以下四段标题作答（标题语言必须与回答语言一致）：
   ## {h[0]}
   ## {h[1]}
   ## {h[2]}
   ## {h[3]}
3. 写法——以解决用户问题为准，篇幅随复杂度变化：
   - 每段按资料能支持的程度展开可执行 bullet / 编号步骤，不要人为限制条数。
   - 资料里有目录树、夹名、菜单路径、角色、限制、验证方式就必须写出来。
   - {h[3]} 尽量写清「标准要求 → 本组织做法 → Docs 操作」的对应；无法对应时明确写「缺口：…」，禁止硬编映射。
   - 禁止在一段里先写「根据现有资料无法确认」再引用 [1][2] 展开分析——有引用就说明能答，直接答。
   - 只有该段完全没有可用编号资料时，才写一句「根据现有资料无法确认」。
   - 不要灌水；信息足够让用户采取下一步后即可结束。
4. 编号归属：{h[0]}→HK；{h[1]}→Playbook；{h[2]}→Docs。
5. 多轮证据边界：若有 <conversation_context_untrusted>，仅用于理解指代；事实只能来自本轮编号资料。与历史冲突时明确更正；本轮无证据时不得复用历史答案。
6. 不要输出思考过程。"""


def _hybrid_few_shot(lang: str) -> str:
    h = hybrid_section_headers(lang)  # type: ignore[arg-type]
    if lang == "en":
        return f"""
Example (folder setup when materials include a tree):
## {h[0]}
- CDE information should move through WIP → Shared → Published → Archive with defined review gates [1]
## {h[1]}
- Under Project Files create: `01_WIP`, `02_Shared`, `03_Published`, `04_Archive` [2]
- Under WIP use discipline subfolders (ARC/STR/MEP…), then Models/Drawings [2]
- Enforce Naming Standard on Shared/Published; WIP may stay flexible [2]
- Confirm reviewers/approvers exist before enabling publish/review workflows [2]
## {h[2]}
- Docs → Files → create the top-level folders, then set folder permissions by role [3]
- Enable Naming Standard on Shared/Published folders after the structure exists [3]
## {h[3]}
- Standards require state control; Playbook supplies the ACC folder tree; Docs provides the UI steps [1][2][3]
- Gap: if BEP naming fields are not listed in materials, do not invent them.
"""
    return f"""
示例（资料含目录树的文件夹配置）：
## {h[0]}
- CDE 信息应按 WIP → Shared → Published → Archive 流转，并设置审阅/发布关口 [1]
## {h[1]}
- 在 Project Files 下建顶层夹：`01_WIP`、`02_Shared`、`03_Published`、`04_Archive` [2]
- WIP 下按专业分子夹（ARC/STR/MEP…），其下 Models/Drawings 等 [2]
- Shared/Published 启用 Naming Standard；WIP 内可不强制 [2]
- 启用发布/审阅前确认审批角色已配置 [2]
## {h[2]}
- Docs → Files 创建顶层夹，并按角色设置文件夹权限 [3]
- 结构建好后，在 Shared/Published 启用 Naming Standard [3]
## {h[3]}
- 标准要求状态管控；Playbook 给出 ACC 目录树；Docs 给出界面操作 [1][2][3]
- 缺口：若资料未列出 BEP 命名字段，不要自行编造。
"""


@dataclass(frozen=True)
class Answer:
    question: str
    answer: str
    contexts: list[RetrievedChunk]
    model: str
    context_tokens: int = 0
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    @property
    def total_tokens(self) -> int | None:
        if self.prompt_tokens is None and self.completion_tokens is None:
            return None
        return int(self.prompt_tokens or 0) + int(self.completion_tokens or 0)


def _context_token_total(chunks: list[RetrievedChunk]) -> int:
    return sum(int(getattr(chunk, "token_count", 0) or 0) for chunk in chunks)


def _ollama_token_counts(response: Any) -> tuple[int | None, int | None]:
    def _get(name: str) -> int | None:
        if isinstance(response, dict):
            value = response.get(name)
        else:
            value = getattr(response, name, None)
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    return _get("prompt_eval_count"), _get("eval_count")


def format_token_usage(answer: Answer) -> str:
    parts = [f"上下文 {answer.context_tokens}"]
    if answer.prompt_tokens is not None:
        parts.append(f"提示 {answer.prompt_tokens}")
    else:
        parts.append("提示 -")
    if answer.completion_tokens is not None:
        parts.append(f"生成 {answer.completion_tokens}")
    else:
        parts.append("生成 -")
    if answer.total_tokens is not None:
        parts.append(f"合计 {answer.total_tokens}")
    return "Token：" + " | ".join(parts)


def build_user_prompt(
    question: str,
    chunks: list[RetrievedChunk],
    *,
    answer_lang: str = "auto",
    rewritten_query: str | None = None,
    conversation_context: str | None = None,
) -> str:
    if not chunks:
        return (
            f"问题：{question}\n\n"
            "当前没有检索到相关资料。请直接说明根据现有资料无法确认。"
        )
    rewritten_line = ""
    if rewritten_query and rewritten_query.strip() != question.strip():
        rewritten_line = f"独立检索问题：{rewritten_query.strip()}\n"
    history_block = ""
    if conversation_context and conversation_context.strip():
        history_block = f"{conversation_context.strip()}\n\n"
    return (
        f"问题：{question}\n"
        f"{rewritten_line}"
        f"{language_instruction(resolve_answer_language(question, answer_lang))}\n\n"
        f"{history_block}"
        "本轮资料（唯一可引用证据）：\n"
        f"{format_context(chunks)}\n\n"
        "请按「结论 → 怎么做/关键要求 → 适用范围与例外 → 资料缺口」输出。"
        "篇幅服从解决问题所需信息量：不要因追求简短而省略关键步骤、前置条件、验证方法或限制；"
        "也不要灌水。关键事实标注 [n]；完全无关才说根据现有资料无法确认。"
        "若本轮资料与不可信历史冲突，以本轮为准并明确更正。"
    )


def build_hybrid_user_prompt(
    question: str,
    merged: MergedContexts,
    *,
    answer_lang: str = "auto",
    rewritten_query: str | None = None,
    conversation_context: str | None = None,
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
    closing = (
        "Write all four sections. Expand enough for the user to take the next action; "
        "include paths/folder names/conditions when present. "
        "Do not open a section with 'cannot confirm' and then analyse. "
        "Facts only from this-turn numbered materials."
        if lang == "en"
        else (
            "请按四段输出；每段展开到用户能采取下一步为止；"
            "资料中有路径/夹名/条件就必须写出；"
            "禁止段首「无法确认」后又长篇分析；"
            "事实只能来自本轮编号资料。"
        )
    )
    rewritten_line = ""
    if rewritten_query and rewritten_query.strip() != question.strip():
        rewritten_line = f"独立检索问题：{rewritten_query.strip()}\n"
    history_block = ""
    if conversation_context and conversation_context.strip():
        history_block = f"{conversation_context.strip()}\n\n"
    return (
        f"问题：{question}\n"
        f"{rewritten_line}"
        f"{language_instruction(lang)}\n"
        f"{header_rule}\n\n"
        f"{history_block}"
        f"{hk_note}；{playbook_note}；{docs_note}\n\n"
        f"{format_partitioned_context(merged)}\n\n"
        f"{_hybrid_few_shot(lang)}\n"
        f"{closing}"
    )


def _should_refuse(chunks: list[RetrievedChunk], minimum_similarity: float) -> bool:
    if not chunks:
        return True
    similarities = [
        chunk.vector_similarity
        for chunk in chunks
        if chunk.vector_similarity is not None
    ]
    if similarities:
        return max(similarities) < minimum_similarity
    # Industry hybrid / family-shadow paths often expose fused RRF scores only.
    # Do not refuse solely because vector_similarity was not populated.
    if any(chunk.score is not None and float(chunk.score) > 0 for chunk in chunks):
        return False
    return True


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
    rewritten_query: str | None = None,
    conversation_context: str | None = None,
) -> Answer:
    app_config = config or get_config()
    if _should_refuse(chunks, app_config.retrieval.minimum_vector_similarity):
        return Answer(
            question=question,
            answer="根据现有资料无法确认。",
            contexts=chunks,
            model=app_config.models.generation_model,
            context_tokens=_context_token_total(chunks),
        )

    prompt = system_prompt or SYSTEM_PROMPT
    product = getattr(getattr(app_config, "corpus", None), "product", "")
    if system_prompt is None and product == "playbook_acc_hk":
        prompt = PLAYBOOK_SYSTEM_PROMPT
    elif system_prompt is None and product == "hk_cde":
        prompt = HK_SYSTEM_PROMPT
    # Also switch when retrieved chunks are clearly HK industry URLs.
    elif system_prompt is None and any(
        (chunk.source_url or "").startswith("hk_cde://") for chunk in chunks
    ):
        prompt = HK_SYSTEM_PROMPT
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
            {
                "role": "user",
                "content": build_user_prompt(
                    question,
                    chunks,
                    answer_lang=answer_lang,
                    rewritten_query=rewritten_query,
                    conversation_context=conversation_context,
                ),
            },
        ],
        think=False,
        options={
            "temperature": 0.0,
            "num_predict": 900,
        },
    )
    prompt_tokens, completion_tokens = _ollama_token_counts(response)
    return Answer(
        question=question,
        answer=_extract_content(response),
        contexts=chunks,
        model=app_config.models.generation_model,
        context_tokens=_context_token_total(chunks),
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )


def generate_hybrid_answer(
    question: str,
    merged: MergedContexts | None,
    config: AppConfig | None = None,
    *,
    answer_lang: str = "auto",
    rewritten_query: str | None = None,
    conversation_context: str | None = None,
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
            context_tokens=_context_token_total(
                [item.chunk for item in merged.tracked]
            ),
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
                    question,
                    merged,
                    answer_lang=answer_lang,
                    rewritten_query=rewritten_query,
                    conversation_context=conversation_context,
                ),
            },
        ],
        think=False,
        options={
            "temperature": 0.0,
            "num_predict": 1800,
        },
    )
    prompt_tokens, completion_tokens = _ollama_token_counts(response)
    contexts = [item.chunk for item in merged.tracked]
    raw = _extract_content(response)
    return Answer(
        question=question,
        answer=polish_hybrid_answer(raw, lang=lang),
        contexts=contexts,
        model=app_config.models.generation_model,
        context_tokens=_context_token_total(contexts),
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
    )


def format_sources(chunks: list[RetrievedChunk]) -> list[str]:
    lines: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        lines.append(f"[{index}] {chunk.title}\n    {chunk.source_url}")
    return lines
