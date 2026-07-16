#!/usr/bin/env python3
"""ACC × HK BIM RAG — Streamlit demo (English UI).

Run:
  source .venv/bin/activate
  streamlit run streamlit_demo.py
"""

from __future__ import annotations

import re
import time
from dataclasses import dataclass

import streamlit as st

from rag.answer_language import HYBRID_SECTION_HEADERS, resolve_answer_language
from rag.config import get_config
from rag.generation import format_sources
from rag.industry_hk.config import get_industry_hk_config
from rag.orchestrator.merge import format_hybrid_sources
from rag.orchestrator.pipeline import HybridOrchestrator, format_orchestrator_debug
from rag.playbook_acc_hk.config import get_playbook_config

PAGE_TITLE = "ACC × HK BIM"
EXAMPLES = [
    "How to set up ACC folders to HK CDE standards",
    "file naming standard",
    "How to run HK-aligned approval workflows in ACC",
    "What can you do?",
]

TRACK_COLORS = {
    "hk_cde": "#0B6E4F",
    "playbook": "#B45309",
    "docs": "#1D4ED8",
    "hybrid": "#0F172A",
    "meta": "#64748B",
}

# key, badge, accent, English section title for UI chrome
SECTION_META = (
    ("standards", "HK", "#0B6E4F", "Standards Requirements"),
    ("playbook", "Playbook", "#B45309", "Implementation Guidance"),
    ("product", "Docs", "#1D4ED8", "Product Steps"),
    ("alignment", "Align", "#7C2D12", "Alignment & Gaps"),
)

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
div[data-testid="stSidebar"] .stSlider label {
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


def _render_hybrid_sections(answer_text: str) -> None:
    blocks = _split_sections(answer_text)
    if not blocks:
        st.markdown(answer_text)
        return
    meta_by_key = {key: (badge, color, en_title) for key, badge, color, en_title in SECTION_META}
    cols = st.columns(2)
    for i, block in enumerate(blocks):
        badge, color, en_title = meta_by_key.get(
            block.key, ("?", "#334155", block.title)
        )
        with cols[i % 2]:
            st.markdown(
                f"""
<div class="section-card" style="--accent:{color}">
  <div class="section-label">{badge}</div>
  <div class="section-title">{en_title}</div>
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


def _render_sources(source_lines: list[str]) -> None:
    if not source_lines:
        st.caption("No sources")
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


def _collect_result_payload(result, *, no_generate: bool) -> tuple[str, list[str], list]:
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

    if no_generate:
        answer_text = "(Retrieve-only mode — generation skipped)"
    else:
        answer_text = result.answer.answer if result.answer else "(No answer)"
    return answer_text, source_lines, contexts


def main() -> None:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon="🗂️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _inject_css()

    docs_config = get_config()
    with st.sidebar:
        st.markdown("### Controls")
        corpus = st.selectbox(
            "Corpus",
            options=["auto", "hybrid", "docs", "hk_cde", "playbook"],
            index=0,
            help="auto = router; hybrid = all three tracks; others = single track",
        )
        answer_lang = st.selectbox(
            "Answer language",
            options=["en", "auto", "zh-Hans", "zh-Hant"],
            index=0,
            help="Default English. Use auto to follow the question language.",
        )
        top_k = st.slider("Top-k per track", min_value=1, max_value=8, value=3)
        no_generate = st.checkbox("Retrieve only (no LLM)", value=False)
        show_debug = st.checkbox("Show retrieval debug", value=False)
        show_context = st.checkbox("Show chunk snippets", value=False)
        st.markdown("---")
        st.caption(
            f"LLM · `{docs_config.models.generation_model}`  \n"
            f"Embed · `{docs_config.models.embedding_model}`"
        )
        if corpus == "hybrid":
            lang_key = answer_lang if answer_lang in HYBRID_SECTION_HEADERS else "en"
            expected = HYBRID_SECTION_HEADERS[lang_key]
            st.caption("Hybrid sections: " + " · ".join(expected))

    st.markdown('<div class="hero-kicker">Local grounded RAG</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-title">{PAGE_TITLE}</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">'
        "Three-track grounding: Hong Kong BIM/CDE standards · ACC×HK playbook · Autodesk Docs. "
        "Ask a question — hybrid mode returns four aligned sections with sources."
        "</div>",
        unsafe_allow_html=True,
    )

    if "question" not in st.session_state:
        st.session_state.question = EXAMPLES[0]

    example_cols = st.columns(len(EXAMPLES))
    for col, example in zip(example_cols, EXAMPLES):
        if col.button(example, use_container_width=True):
            st.session_state.question = example

    question = st.text_area(
        "Question",
        height=88,
        key="question",
        placeholder="e.g. How to set up ACC folders to HK CDE standards",
    )
    ask = st.button("Ask", type="primary", use_container_width=False)

    if ask and question.strip():
        orchestrator = get_orchestrator()
        force = None if corpus == "auto" else corpus
        q = question.strip()
        with st.status("Working on your question…", expanded=True) as status:
            status.write("1/2 Retrieving HK · Playbook · Docs sources…")
            t0 = time.perf_counter()
            preview = orchestrator.ask(
                q,
                force_track=force,
                top_k=top_k,
                no_generate=True,
                answer_lang=answer_lang,
            )
            n_src = 0
            if preview.merged is not None:
                n_src = len(preview.merged.tracked)
            elif preview.track == "hk_cde":
                n_src = len(preview.chunks_industry)
            elif preview.track == "playbook":
                n_src = len(preview.chunks_playbook)
            elif preview.track == "docs":
                n_src = len(preview.chunks_docs)
            retrieve_s = time.perf_counter() - t0
            status.write(f"Retrieved {n_src} source(s) in {retrieve_s:.1f}s.")

            if no_generate:
                result = preview
                status.update(
                    label=f"Done (retrieve-only · {retrieve_s:.1f}s)",
                    state="complete",
                )
            else:
                status.write(
                    "2/2 Generating with local LLM "
                    f"(`{docs_config.models.generation_model}`). "
                    "Broad questions often take 20–90s; first run after idle can be slower."
                )
                t1 = time.perf_counter()
                result = orchestrator.ask(
                    q,
                    force_track=force,
                    top_k=top_k,
                    no_generate=False,
                    answer_lang=answer_lang,
                )
                gen_s = time.perf_counter() - t1
                total = retrieve_s + gen_s
                model = result.answer.model if result.answer else "?"
                status.update(
                    label=f"Done · retrieve {retrieve_s:.1f}s · generate {gen_s:.1f}s · total {total:.1f}s · {model}",
                    state="complete",
                )

        st.session_state["last_result"] = result
        st.session_state["last_question"] = q
        st.session_state["last_no_generate"] = no_generate

    result = st.session_state.get("last_result")
    if result is None:
        st.info("Pick an example or type a question, then click Ask.")
        return

    q = st.session_state.get("last_question", "")
    no_gen = st.session_state.get("last_no_generate", False)
    answer_text, source_lines, contexts = _collect_result_payload(result, no_generate=no_gen)

    st.markdown(f"**Q** · {q}")
    _render_meta(result, answer_lang, q)

    left, right = st.columns([1.55, 1], gap="large")
    with left:
        st.subheader("Answer")
        if result.track == "hybrid" and not no_gen:
            _render_hybrid_sections(answer_text)
        else:
            st.markdown(answer_text)

        warnings = result.debug.validation_warnings or []
        if warnings:
            with st.expander(f"Validation notes ({len(warnings)})"):
                for w in warnings:
                    st.text(w)

    with right:
        st.subheader("Sources")
        _render_sources(source_lines)

    if show_debug:
        with st.expander("Orchestrator debug", expanded=False):
            st.code(format_orchestrator_debug(result.debug), language="text")

    if show_context and contexts:
        with st.expander(f"Retrieved chunks ({len(contexts)})", expanded=False):
            for index, chunk in enumerate(contexts, start=1):
                sim = (
                    f"{chunk.vector_similarity:.3f}"
                    if chunk.vector_similarity is not None
                    else "-"
                )
                st.markdown(
                    f"**[{index}]** score=`{chunk.score:.4f}` sim=`{sim}`  \n"
                    f"{chunk.title}  \n"
                    f"`{chunk.source_url}`"
                )
                st.text(chunk.text[:700] + ("…" if len(chunk.text) > 700 else ""))


if __name__ == "__main__":
    main()
