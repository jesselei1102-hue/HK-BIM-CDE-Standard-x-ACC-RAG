#!/usr/bin/env python3
"""ACC × HK BIM RAG — Streamlit demo (EN / 中文 UI).

Run:
  source .venv/bin/activate
  streamlit run streamlit_demo.py
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Any

import streamlit as st

from rag.answer_language import HYBRID_SECTION_HEADERS, resolve_answer_language
from rag.config import get_config
from rag.conversation import ConversationSession
from rag.generation import format_sources
from rag.industry_hk.config import get_industry_hk_config
from rag.orchestrator.merge import format_hybrid_sources
from rag.orchestrator.pipeline import HybridOrchestrator, format_orchestrator_debug
from rag.playbook_acc_hk.config import get_playbook_config

PAGE_TITLE = "ACC × HK BIM"

UI_COPY: dict[str, dict[str, Any]] = {
    "en": {
        "controls": "Controls",
        "ui_language": "UI language",
        "corpus": "Corpus",
        "corpus_help": "auto = router; hybrid = all three tracks; others = single track",
        "answer_language": "Answer language",
        "answer_language_help": (
            "Follow UI uses the selected interface language. "
            "Auto follows the question language."
        ),
        "answer_lang_options": {
            "follow_ui": "Follow UI",
            "auto": "Auto (question)",
            "en": "English",
            "zh-Hans": "简体中文",
            "zh-Hant": "繁體中文",
        },
        "top_k": "Top-k per track",
        "no_generate": "Retrieve only (no LLM)",
        "show_debug": "Show retrieval debug",
        "show_context": "Show chunk snippets",
        "new_conversation": "New conversation",
        "turns_caption": "Turns · `{n}` (session memory only)",
        "hybrid_sections": "Hybrid sections",
        "followups_note": (
            "Follow-ups re-retrieve every turn. "
            "Prior answers are untrusted context only."
        ),
        "hero_kicker": "Local grounded RAG",
        "hero_sub": (
            "Three-track grounding: Hong Kong BIM/CDE standards · ACC×HK playbook · "
            "Autodesk Docs. Multi-turn follow-ups rewrite the question, then "
            "re-retrieve this turn's evidence."
        ),
        "examples": [
            "How to set up ACC folders to HK CDE standards",
            "file naming standard",
            "How to run HK-aligned approval workflows in ACC",
            "What can you do?",
        ],
        "chat_placeholder": "Ask a question or follow up…",
        "empty_hint": "Pick an example or type a question to start a multi-turn session.",
        "you_might_ask": "You might also ask",
        "sources": "Sources",
        "no_sources": "No sources",
        "validation_notes": "Validation notes",
        "orchestrator_debug": "Orchestrator debug",
        "retrieved_chunks": "Retrieved chunks",
        "standalone_query": "Standalone retrieval query",
        "status_working": "Working on your question…",
        "status_retrieving": "Retrieving + answering (single pass)…",
        "status_sources": "Sources",
        "status_retrieve": "retrieve",
        "status_generate": "generate",
        "status_total": "total",
        "status_standalone": "Standalone query",
        "status_done": "Done",
        "status_retrieve_only": "retrieve-only",
        "missing_index": "Missing index",
        "missing_index_body": (
            "Index or corpus missing: {exc}\n\n"
            "Run `bash scripts/bootstrap_indexes.sh` "
            "or `python -m rag.preflight` for repair commands."
        ),
        "request_failed": "Request failed",
        "could_not_answer": "Could not answer: {exc}",
        "retrieve_only_answer": "(Retrieve-only mode — generation skipped)",
        "no_answer": "(No answer)",
        "section_titles": {
            "standards": "Standards Requirements",
            "playbook": "Implementation Guidance",
            "product": "Product Steps",
            "alignment": "Alignment & Gaps",
        },
    },
    "zh": {
        "controls": "控制面板",
        "ui_language": "界面语言",
        "corpus": "语料轨道",
        "corpus_help": "auto = 自动路由；hybrid = 三轨联查；其余 = 单轨",
        "answer_language": "回答语言",
        "answer_language_help": "跟随界面使用当前界面语言；自动则跟随提问语言。",
        "answer_lang_options": {
            "follow_ui": "跟随界面",
            "auto": "自动（跟随提问）",
            "en": "English",
            "zh-Hans": "简体中文",
            "zh-Hant": "繁體中文",
        },
        "top_k": "每轨 Top-k",
        "no_generate": "仅检索（不调用大模型）",
        "show_debug": "显示检索调试信息",
        "show_context": "显示原文片段",
        "new_conversation": "新对话",
        "turns_caption": "轮次 · `{n}`（仅会话记忆）",
        "hybrid_sections": "混合回答章节",
        "followups_note": "追问每轮都会重新检索。上一轮答案仅作不可信上下文。",
        "hero_kicker": "本地有据可查 RAG",
        "hero_sub": (
            "三轨 grounding：香港 BIM/CDE 标准 · ACC×HK Playbook · Autodesk Docs。"
            "多轮追问会改写问题，并按本轮证据重新检索。"
        ),
        "examples": [
            "如何按港标搭建 ACC 文件夹结构",
            "文件命名标准",
            "如何在 ACC 跑符合港标的审批流程",
            "你能做什么？",
        ],
        "chat_placeholder": "输入问题或继续追问…",
        "empty_hint": "点选示例，或直接输入问题开始多轮对话。",
        "you_might_ask": "你还可以问",
        "sources": "来源",
        "no_sources": "暂无来源",
        "validation_notes": "校验说明",
        "orchestrator_debug": "编排调试",
        "retrieved_chunks": "检索片段",
        "standalone_query": "本轮独立检索问句",
        "status_working": "正在处理你的问题…",
        "status_retrieving": "检索 + 生成（单次）…",
        "status_sources": "来源",
        "status_retrieve": "检索",
        "status_generate": "生成",
        "status_total": "合计",
        "status_standalone": "独立问句",
        "status_done": "完成",
        "status_retrieve_only": "仅检索",
        "missing_index": "索引缺失",
        "missing_index_body": (
            "索引或语料缺失：{exc}\n\n"
            "请运行 `bash scripts/bootstrap_indexes.sh` "
            "或 `python -m rag.preflight` 查看修复命令。"
        ),
        "request_failed": "请求失败",
        "could_not_answer": "无法回答：{exc}",
        "retrieve_only_answer": "（仅检索模式 — 已跳过生成）",
        "no_answer": "（无回答）",
        "section_titles": {
            "standards": "标准要求",
            "playbook": "实施建议",
            "product": "产品操作",
            "alignment": "对齐与缺口",
        },
    },
}

TRACK_COLORS = {
    "hk_cde": "#0B6E4F",
    "playbook": "#B45309",
    "docs": "#1D4ED8",
    "hybrid": "#0F172A",
    "meta": "#64748B",
}

SECTION_META = (
    ("standards", "HK", "#0B6E4F"),
    ("playbook", "Playbook", "#B45309"),
    ("product", "Docs", "#1D4ED8"),
    ("alignment", "Align", "#7C2D12"),
)


def _t(ui_lang: str) -> dict[str, Any]:
    return UI_COPY["zh" if ui_lang == "zh" else "en"]


def _resolve_answer_lang_choice(choice: str, ui_lang: str) -> str:
    if choice == "follow_ui":
        return "zh-Hans" if ui_lang == "zh" else "en"
    return choice

_HEADER_PATTERNS = (
    (
        "standards",
        re.compile(
            r"^#{0,3}\s*(标准要求|標準要求|Standards?\s+Requirements?)\s*$",
            re.M | re.I,
        ),
    ),
    (
        "playbook",
        re.compile(
            r"^#{0,3}\s*(实施建议|實施建議|Implementation\s+(?:Guidance|Advice)|Playbook)\s*$",
            re.M | re.I,
        ),
    ),
    (
        "product",
        re.compile(
            r"^#{0,3}\s*(产品操作|產品操作|Product\s+(?:Steps|Operations|Guidance))\s*$",
            re.M | re.I,
        ),
    ),
    (
        "alignment",
        re.compile(
            r"^#{0,3}\s*(对齐与缺口|對齊與缺口|Alignment\s*(?:&|and)?\s*Gaps?)\s*$",
            re.M | re.I,
        ),
    ),
)


@dataclass(frozen=True)
class SectionBlock:
    key: str
    title: str
    body: str


def _inject_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
  font-family: "IBM Plex Sans", sans-serif;
}
.stApp {
  background:
    radial-gradient(ellipse 80% 50% at 10% -10%, #dbeafe 0%, transparent 55%),
    radial-gradient(ellipse 60% 40% at 100% 0%, #fef3c7 0%, transparent 50%),
    linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
}
.block-container {
  padding-top: 1.4rem;
  max-width: 1180px;
}
h1, h2, h3 { font-family: "Fraunces", Georgia, serif !important; letter-spacing: -0.02em; }
.hero-kicker {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.78rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #64748b;
  margin-bottom: 0.35rem;
}
.hero-title {
  font-family: "Fraunces", Georgia, serif;
  font-size: 2.15rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.15;
  margin: 0 0 0.4rem 0;
}
.hero-sub {
  color: #475569;
  font-size: 1.02rem;
  max-width: 42rem;
  margin-bottom: 1.1rem;
}
.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin: 0.6rem 0 1rem 0;
}
.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  border: 1px solid #cbd5e1;
  background: rgba(255,255,255,0.82);
  color: #0f172a;
  border-radius: 999px;
  padding: 0.22rem 0.7rem;
  font-size: 0.78rem;
  font-family: "IBM Plex Mono", monospace;
}
.pill-ok { border-color: #86efac; background: #f0fdf4; color: #166534; }
.pill-bad { border-color: #fecaca; background: #fef2f2; color: #991b1b; }
.section-card {
  background: rgba(255,255,255,0.9);
  border: 1px solid #e2e8f0;
  border-left: 4px solid var(--accent, #0f172a);
  border-radius: 10px;
  padding: 0.85rem 1rem 0.95rem;
  margin-bottom: 0.85rem;
  min-height: 9.5rem;
}
.section-label {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent, #0f172a);
  margin-bottom: 0.2rem;
}
.section-title {
  font-family: "Fraunces", Georgia, serif;
  font-size: 1.12rem;
  font-weight: 650;
  color: #0f172a;
  margin-bottom: 0.45rem;
}
.source-item {
  background: rgba(255,255,255,0.88);
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.65rem 0.8rem;
  margin-bottom: 0.5rem;
}
.source-title {
  font-weight: 600;
  color: #0f172a;
  font-size: 0.92rem;
}
.source-url {
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.74rem;
  color: #64748b;
  word-break: break-all;
}
.track-badge {
  display: inline-block;
  font-family: "IBM Plex Mono", monospace;
  font-size: 0.68rem;
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  color: white;
  margin-right: 0.35rem;
}
div[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
}
div[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
div[data-testid="stSidebar"] .stSelectbox label,
div[data-testid="stSidebar"] .stCheckbox label,
div[data-testid="stSidebar"] .stSlider label,
div[data-testid="stSidebar"] .stRadio label {
  color: #cbd5e1 !important;
}
</style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource(show_spinner=False)
def get_orchestrator() -> HybridOrchestrator:
    return HybridOrchestrator(
        docs_config=get_config(),
        industry_config=get_industry_hk_config(),
        playbook_config=get_playbook_config(),
    )


def _split_sections(answer: str) -> list[SectionBlock]:
    text = answer or ""
    markers: list[tuple[int, str, str]] = []
    for key, pattern in _HEADER_PATTERNS:
        match = pattern.search(text)
        if match:
            title = match.group(1).strip()
            markers.append((match.start(), key, title))
    markers.sort(key=lambda item: item[0])
    if not markers:
        return []
    blocks: list[SectionBlock] = []
    for index, (start, key, title) in enumerate(markers):
        header_end = text.find("\n", start)
        body_start = header_end + 1 if header_end != -1 else start
        end = markers[index + 1][0] if index + 1 < len(markers) else len(text)
        blocks.append(SectionBlock(key=key, title=title, body=text[body_start:end].strip()))
    return blocks


def _pill(label: str, *, kind: str = "") -> str:
    klass = "pill"
    if kind == "ok":
        klass += " pill-ok"
    elif kind == "bad":
        klass += " pill-bad"
    return f'<span class="{klass}">{label}</span>'


def _render_meta(result, answer_lang: str, question: str) -> None:
    resolved = resolve_answer_language(question, answer_lang)
    intent = result.debug.intent
    track_color = TRACK_COLORS.get(result.track, "#334155")
    pills = [
        _pill(f"track · {result.track}"),
        _pill(f"lang · {resolved}"),
        _pill(f"capability · {intent.capability or '—'}"),
    ]
    if result.answer and result.answer.model:
        pills.append(_pill(f"gen · {result.answer.model}"))
    if result.validation_ok is True:
        pills.append(_pill("validation · ok", kind="ok"))
    elif result.validation_ok is False:
        pills.append(_pill("validation · failed", kind="bad"))
    st.markdown(
        f'<div class="meta-row">{"".join(pills)}</div>'
        f'<div style="height:3px;background:{track_color};border-radius:2px;margin-bottom:0.9rem;"></div>',
        unsafe_allow_html=True,
    )


def _render_hybrid_sections(answer_text: str, *, ui_lang: str) -> None:
    blocks = _split_sections(answer_text)
    if not blocks:
        st.markdown(answer_text)
        return
    titles = _t(ui_lang)["section_titles"]
    meta_by_key = {key: (badge, color) for key, badge, color in SECTION_META}
    cols = st.columns(2)
    for i, block in enumerate(blocks):
        badge, color = meta_by_key.get(block.key, ("?", "#334155"))
        title = titles.get(block.key, block.title)
        with cols[i % 2]:
            st.markdown(
                f"""
<div class="section-card" style="--accent:{color}">
  <div class="section-label">{badge}</div>
  <div class="section-title">{title}</div>
</div>
                """,
                unsafe_allow_html=True,
            )
            with st.container():
                st.markdown(block.body)


def _parse_source_line(line: str) -> tuple[str, str, str, str]:
    """Return (index, track_label, title, url)."""
    parts = line.split("\n", 1)
    head = parts[0]
    url = parts[1].strip() if len(parts) > 1 else ""
    m = re.match(r"^\[(\d+)\]\s+(\[[^\]]+\])\s+(.*)$", head)
    if m:
        return m.group(1), m.group(2).strip("[]"), m.group(3), url
    m2 = re.match(r"^\[(\d+)\]\s+(.*)$", head)
    if m2:
        return m2.group(1), "source", m2.group(2), url
    return "?", "source", head, url


def _track_from_label(label: str) -> str:
    low = label.lower()
    if "hk" in low:
        return "hk_cde"
    if "playbook" in low:
        return "playbook"
    if "docs" in low:
        return "docs"
    return "hybrid"


def _render_sources(source_lines: list[str], *, ui_lang: str) -> None:
    if not source_lines:
        st.caption(_t(ui_lang)["no_sources"])
        return
    for line in source_lines:
        idx, label, title, url = _parse_source_line(line)
        track = _track_from_label(label)
        color = TRACK_COLORS.get(track, "#64748B")
        st.markdown(
            f"""
<div class="source-item">
  <div class="source-title">
    <span class="track-badge" style="background:{color}">[{idx}] {label}</span>
    {title}
  </div>
  <div class="source-url">{url}</div>
</div>
            """,
            unsafe_allow_html=True,
        )


def _collect_result_payload(
    result, *, no_generate: bool, ui_lang: str
) -> tuple[str, list[str], list]:
    if result.track == "hybrid" and result.merged is not None:
        source_lines = format_hybrid_sources(result.merged)
        contexts = [item.chunk for item in result.merged.tracked]
    elif result.track == "meta":
        source_lines, contexts = [], []
    elif result.track == "hk_cde":
        source_lines = format_sources(result.chunks_industry)
        contexts = result.chunks_industry
    elif result.track == "playbook":
        source_lines = format_sources(result.chunks_playbook)
        contexts = result.chunks_playbook
    else:
        source_lines = format_sources(result.chunks_docs)
        contexts = result.chunks_docs

    copy = _t(ui_lang)
    if no_generate:
        answer_text = copy["retrieve_only_answer"]
    else:
        answer_text = result.answer.answer if result.answer else copy["no_answer"]
    return answer_text, source_lines, contexts


def _render_followup_suggestions(
    followups: list[str],
    *,
    key_prefix: str,
    ui_lang: str,
) -> None:
    """Render clickable follow-ups. Must be shown on every rerun so clicks register."""
    if not followups:
        return
    st.markdown(f"**{_t(ui_lang)['you_might_ask']}**")
    cols = st.columns(min(len(followups), 3))
    for index, suggestion in enumerate(followups):
        col = cols[index % len(cols)]
        if col.button(
            suggestion,
            key=f"{key_prefix}_{index}",
            use_container_width=True,
        ):
            st.session_state["_pending_question"] = suggestion


def main() -> None:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="🗂️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_css()

    docs_config = get_config()
    if "conversation" not in st.session_state:
        st.session_state.conversation = ConversationSession()
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "ui_lang_radio" not in st.session_state:
        st.session_state.ui_lang_radio = "English"

    with st.sidebar:
        st.radio(
            "界面语言 / UI language",
            options=["English", "中文"],
            horizontal=True,
            key="ui_lang_radio",
        )
        ui_lang = "zh" if st.session_state.ui_lang_radio == "中文" else "en"
        copy = _t(ui_lang)

        st.markdown(f"### {copy['controls']}")
        corpus = st.selectbox(
            copy["corpus"],
            options=["auto", "hybrid", "docs", "hk_cde", "playbook"],
            index=0,
            help=copy["corpus_help"],
        )
        answer_lang_labels = copy["answer_lang_options"]
        answer_lang_keys = list(answer_lang_labels.keys())
        answer_lang_choice = st.selectbox(
            copy["answer_language"],
            options=answer_lang_keys,
            format_func=lambda key: answer_lang_labels[key],
            index=0,
            help=copy["answer_language_help"],
        )
        answer_lang = _resolve_answer_lang_choice(answer_lang_choice, ui_lang)
        top_k = st.slider(copy["top_k"], min_value=1, max_value=8, value=3)
        no_generate = st.checkbox(copy["no_generate"], value=False)
        show_debug = st.checkbox(copy["show_debug"], value=False)
        show_context = st.checkbox(copy["show_context"], value=False)
        if st.button(copy["new_conversation"], use_container_width=True):
            st.session_state.conversation = ConversationSession()
            st.session_state.chat_messages = []
            st.rerun()
        st.markdown("---")
        st.caption(
            f"LLM · `{docs_config.models.generation_model}`  \n"
            f"Embed · `{docs_config.models.embedding_model}`  \n"
            + copy["turns_caption"].format(n=len(st.session_state.conversation.turns))
        )
        if corpus == "hybrid":
            lang_key = answer_lang if answer_lang in HYBRID_SECTION_HEADERS else "en"
            expected = HYBRID_SECTION_HEADERS[lang_key]
            st.caption(f"{copy['hybrid_sections']}: " + " · ".join(expected))
        st.caption(copy["followups_note"])

    st.markdown(
        f'<div class="hero-kicker">{copy["hero_kicker"]}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="hero-title">{PAGE_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero-sub">{copy["hero_sub"]}</div>',
        unsafe_allow_html=True,
    )

    examples = copy["examples"]
    example_cols = st.columns(len(examples))
    for col, example in zip(example_cols, examples):
        if col.button(example, use_container_width=True):
            st.session_state["_pending_question"] = example

    for msg_index, message in enumerate(st.session_state.chat_messages):
        role = message.get("role", "assistant")
        with st.chat_message(role):
            if role == "user":
                st.markdown(message.get("content", ""))
            else:
                payload = message
                result = payload.get("result")
                q = payload.get("question", "")
                no_gen = payload.get("no_generate", False)
                answer_text, source_lines, contexts = _collect_result_payload(
                    result, no_generate=no_gen, ui_lang=ui_lang
                )
                rewritten = getattr(result.debug, "rewritten_query", None)
                if rewritten and rewritten != q:
                    st.caption(f"{copy['standalone_query']} · {rewritten}")
                _render_meta(result, answer_lang, q)
                if result.track == "hybrid" and not no_gen:
                    _render_hybrid_sections(answer_text, ui_lang=ui_lang)
                else:
                    st.markdown(answer_text)
                with st.expander(copy["sources"], expanded=False):
                    _render_sources(source_lines, ui_lang=ui_lang)
                warnings = result.debug.validation_warnings or []
                if warnings:
                    with st.expander(f"{copy['validation_notes']} ({len(warnings)})"):
                        for w in warnings:
                            st.text(w)
                if show_debug:
                    with st.expander(copy["orchestrator_debug"], expanded=False):
                        st.code(
                            format_orchestrator_debug(result.debug), language="text"
                        )
                if show_context and contexts:
                    with st.expander(
                        f"{copy['retrieved_chunks']} ({len(contexts)})",
                        expanded=False,
                    ):
                        for index, chunk in enumerate(contexts, start=1):
                            sim = (
                                f"{chunk.vector_similarity:.3f}"
                                if chunk.vector_similarity is not None
                                else "-"
                            )
                            st.markdown(
                                f"**[{index}]** score=`{chunk.score:.4f}` "
                                f"sim=`{sim}`  \n"
                                f"{chunk.title}  \n"
                                f"`{chunk.source_url}`"
                            )
                            st.text(
                                chunk.text[:700]
                                + ("…" if len(chunk.text) > 700 else "")
                            )
                _render_followup_suggestions(
                    list(payload.get("suggested_followups") or []),
                    key_prefix=f"hist_followup_{msg_index}",
                    ui_lang=ui_lang,
                )

    pending = st.session_state.pop("_pending_question", None)
    prompt = st.chat_input(copy["chat_placeholder"])
    user_text = pending or prompt
    if not user_text:
        if not st.session_state.chat_messages:
            st.info(copy["empty_hint"])
        return

    q = user_text.strip()
    st.session_state.chat_messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)

    orchestrator = get_orchestrator()
    force = None if corpus == "auto" else corpus
    conversation: ConversationSession = st.session_state.conversation

    with st.chat_message("assistant"):
        with st.status(copy["status_working"], expanded=True) as status:
            status.write(copy["status_retrieving"])
            t0 = time.perf_counter()
            try:
                result = orchestrator.ask(
                    q,
                    force_track=force,
                    top_k=top_k,
                    no_generate=no_generate,
                    answer_lang=answer_lang,
                    session=conversation,
                    record_turn=not no_generate,
                )
            except FileNotFoundError as exc:
                status.update(label=copy["missing_index"], state="error")
                st.error(copy["missing_index_body"].format(exc=exc))
                st.session_state.chat_messages.pop()
                return
            except Exception as exc:  # noqa: BLE001 — surface to UI
                status.update(label=copy["request_failed"], state="error")
                st.error(copy["could_not_answer"].format(exc=exc))
                st.session_state.chat_messages.pop()
                return

            latency = result.debug.latency_ms or {}
            retrieve_s = latency.get("retrieve", 0.0) / 1000.0
            generate_s = latency.get("generate", 0.0) / 1000.0
            total_s = time.perf_counter() - t0
            n_src = 0
            if result.merged is not None:
                n_src = len(result.merged.tracked)
            elif result.track == "hk_cde":
                n_src = len(result.chunks_industry)
            elif result.track == "playbook":
                n_src = len(result.chunks_playbook)
            elif result.track == "docs":
                n_src = len(result.chunks_docs)

            rewritten = result.debug.rewritten_query
            if rewritten and rewritten != q:
                status.write(f"{copy['status_standalone']}: {rewritten}")
            status.write(
                f"{copy['status_sources']}: {n_src} · "
                f"{copy['status_retrieve']} {retrieve_s:.1f}s"
                + (
                    f" · {copy['status_generate']} {generate_s:.1f}s"
                    if not no_generate
                    else ""
                )
                + f" · {copy['status_total']} {total_s:.1f}s"
            )
            status.update(
                label=(
                    f"{copy['status_done']} ("
                    f"{copy['status_retrieve_only'] if no_generate else result.track}"
                    f" · {total_s:.1f}s)"
                ),
                state="complete",
            )

        answer_text, source_lines, contexts = _collect_result_payload(
            result, no_generate=no_generate, ui_lang=ui_lang
        )
        rewritten = getattr(result.debug, "rewritten_query", None)
        if rewritten and rewritten != q:
            st.caption(f"{copy['standalone_query']} · {rewritten}")
        _render_meta(result, answer_lang, q)
        if result.track == "hybrid" and not no_generate:
            _render_hybrid_sections(answer_text, ui_lang=ui_lang)
        else:
            st.markdown(answer_text)
        with st.expander(copy["sources"], expanded=True):
            _render_sources(source_lines, ui_lang=ui_lang)

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "question": q,
            "result": result,
            "no_generate": no_generate,
            "suggested_followups": list(
                getattr(result, "suggested_followups", None) or []
            ),
        }
    )
    # Rerun so follow-up buttons are owned by history (required for click handling).
    st.rerun()


if __name__ == "__main__":
    main()
