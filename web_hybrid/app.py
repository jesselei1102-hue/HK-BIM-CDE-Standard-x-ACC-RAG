#!/usr/bin/env python3
"""HK CDE Assistant — hybrid web demo (separate from Streamlit).

Run from project root:
  source .venv/bin/activate
  python -m web_hybrid.app
  # → http://127.0.0.1:8787
"""

from __future__ import annotations

import html
import json
import os
import random
import re
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from rag.answer_language import resolve_answer_language
from rag.config import PROJECT_ROOT, get_config
from rag.conversation import ConversationSession
from rag.industry_hk.config import get_industry_hk_config
from rag.orchestrator.merge import format_hybrid_sources
from rag.orchestrator.pipeline import HybridOrchestrator
from rag.playbook_acc_hk.config import get_playbook_config

STATIC_DIR = Path(__file__).resolve().parent / "static"

_HEADER_PATTERNS = (
    (
        "standards",
        "Standards Requirement",
        re.compile(
            r"^#{0,3}\s*(标准要求|標準要求|Standards?\s+Requirements?)\s*$",
            re.M | re.I,
        ),
    ),
    (
        "playbook",
        "Implementation Guidance",
        re.compile(
            r"^#{0,3}\s*(实施建议|實施建議|Implementation\s+(?:Guidance|Advice)|Playbook)\s*$",
            re.M | re.I,
        ),
    ),
    (
        "product",
        "Product Steps",
        re.compile(
            r"^#{0,3}\s*(产品操作|產品操作|Product\s+(?:Steps|Operations|Guidance))\s*$",
            re.M | re.I,
        ),
    ),
    (
        "alignment",
        "Alignment & Gaps",
        re.compile(
            r"^#{0,3}\s*(对齐与缺口|對齊與缺口|Alignment\s*(?:&|and)?\s*Gaps?)\s*$",
            re.M | re.I,
        ),
    ),
)

_CITATION_RE = re.compile(r"\[(\d+)\]")
_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")

app = FastAPI(title="HK CDE Assistant", version="1.0")
_orchestrator: HybridOrchestrator | None = None
_sessions: dict[str, ConversationSession] = {}


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    corpus: str = "auto"
    answer_lang: str = "en"
    top_k: int = Field(default=3, ge=1, le=8)
    session_id: str | None = None
    no_generate: bool = False


def get_orchestrator() -> HybridOrchestrator:
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = HybridOrchestrator(
            docs_config=get_config(),
            industry_config=get_industry_hk_config(),
            playbook_config=get_playbook_config(),
        )
    return _orchestrator


def _count_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for _ in handle:
            count += 1
    return count


def _track_score(chunks: list) -> int:
    if not chunks:
        return 0
    sims = [
        float(getattr(chunk, "vector_similarity", None))
        for chunk in chunks
        if getattr(chunk, "vector_similarity", None) is not None
    ]
    if sims:
        return max(8, min(99, int(round(max(sims) * 100))))
    scores = [float(getattr(chunk, "score", 0.0) or 0.0) for chunk in chunks]
    if not scores:
        return 40
    top = max(scores)
    # RRF-ish scores are small; map roughly into a display band.
    return max(12, min(92, int(round(35 + top * 40))))


def _inline_html(text: str) -> str:
    escaped = html.escape(text)
    escaped = _BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = _ITALIC_RE.sub(r"<em>\1</em>", escaped)
    return _CITATION_RE.sub(r'<span class="cite">\1</span>', escaped)


def _body_html(body: str) -> str:
    parts: list[str] = []
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block:
            continue
        raw_lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not raw_lines:
            continue
        bulletish = all(
            line.startswith(("- ", "* ", "• ")) or bool(re.match(r"^\d+[.)]\s+", line))
            for line in raw_lines
        )
        if bulletish:
            items = []
            for line in raw_lines:
                item = re.sub(r"^([-•*]|\d+[.)])\s*", "", line)
                items.append(f"<li>{_inline_html(item)}</li>")
            parts.append("<ul>" + "".join(items) + "</ul>")
        else:
            parts.append(
                "<p>" + "<br>".join(_inline_html(line) for line in raw_lines) + "</p>"
            )
    return "".join(parts) or f"<p>{_inline_html(body)}</p>"


def _split_sections(answer: str) -> list[dict[str, str]]:
    text = answer or ""
    markers: list[tuple[int, str, str]] = []
    for key, fallback_title, pattern in _HEADER_PATTERNS:
        match = pattern.search(text)
        if match:
            title = match.group(1).strip() or fallback_title
            markers.append((match.start(), key, title))
    markers.sort(key=lambda item: item[0])
    if not markers:
        return [
            {
                "key": "product",
                "tag": "Answer",
                "html": _body_html(text),
            }
        ]
    sections: list[dict[str, str]] = []
    for index, (start, key, title) in enumerate(markers):
        header_end = text.find("\n", start)
        body_start = header_end + 1 if header_end != -1 else start
        end = markers[index + 1][0] if index + 1 < len(markers) else len(text)
        body = text[body_start:end].strip()
        tag = next(
            (fallback for k, fallback, _ in _HEADER_PATTERNS if k == key),
            title,
        )
        sections.append({"key": key, "tag": tag, "html": _body_html(body)})
    return sections


def _collect_sources(result) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    if result.merged is not None:
        for item in result.merged.tracked:
            sources.append(
                {
                    "index": item.display_index,
                    "track": item.track,
                    "title": item.chunk.title,
                    "url": item.chunk.source_url,
                }
            )
        return sources

    if result.track == "hk_cde":
        chunks = result.chunks_industry
        track = "hk_cde"
    elif result.track == "playbook":
        chunks = result.chunks_playbook
        track = "playbook"
    else:
        chunks = result.chunks_docs
        track = "docs"
    for index, chunk in enumerate(chunks, start=1):
        sources.append(
            {
                "index": index,
                "track": track,
                "title": chunk.title,
                "url": chunk.source_url,
            }
        )
    return sources


def _serialize_result(result, *, question: str, answer_lang: str) -> dict[str, Any]:
    intent = result.debug.intent
    answer_text = ""
    if result.answer is not None:
        answer_text = result.answer.answer or ""

    docs_chunks = result.chunks_docs or []
    industry_chunks = result.chunks_industry or []
    playbook_chunks = result.chunks_playbook or []
    if result.merged is not None:
        docs_chunks = result.merged.docs_chunks
        industry_chunks = result.merged.industry_chunks
        playbook_chunks = result.merged.playbook_chunks

    used = {
        "standards": bool(industry_chunks) or result.track in {"hk_cde", "hybrid"},
        "playbook": bool(playbook_chunks) or result.track in {"playbook", "hybrid"},
        "docs": bool(docs_chunks) or result.track in {"docs", "hybrid"},
    }
    if result.track == "hk_cde":
        used = {"standards": True, "playbook": False, "docs": False}
    elif result.track == "playbook":
        used = {"standards": False, "playbook": True, "docs": False}
    elif result.track == "docs":
        used = {"standards": False, "playbook": False, "docs": True}
    elif result.track == "meta":
        used = {"standards": False, "playbook": False, "docs": False}

    routing = {
        "standards": {
            "score": _track_score(industry_chunks) if used["standards"] else 0,
            "active": used["standards"],
        },
        "playbook": {
            "score": _track_score(playbook_chunks) if used["playbook"] else 0,
            "active": used["playbook"],
        },
        "docs": {
            "score": _track_score(docs_chunks) if used["docs"] else 0,
            "active": used["docs"],
        },
    }

    return {
        "question": question,
        "track": result.track,
        "capability": intent.capability,
        "answer_lang": resolve_answer_language(question, answer_lang),
        "answer_markdown": answer_text,
        "sections": _split_sections(answer_text) if answer_text else [],
        "routing": routing,
        "sources": _collect_sources(result),
        "suggested_followups": list(result.suggested_followups or []),
        "rewritten_query": result.debug.rewritten_query,
        "latency_ms": result.debug.latency_ms or {},
        "validation_ok": result.validation_ok,
        "model": result.answer.model if result.answer else None,
        "source_lines": (
            format_hybrid_sources(result.merged) if result.merged is not None else []
        ),
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/status")
def status() -> dict[str, Any]:
    docs_chunks = _count_lines(PROJECT_ROOT / ".rag_data" / "chunks.jsonl")
    standards_chunks = _count_lines(
        PROJECT_ROOT / ".rag_data" / "industry_hk_cde" / "chunks.jsonl"
    )
    playbook_chunks = _count_lines(
        PROJECT_ROOT / ".rag_data" / "playbook_acc_hk" / "chunks.jsonl"
    )
    ready = standards_chunks > 0 and playbook_chunks > 0
    return {
        "ready": ready,
        "tracks": {
            "standards": {
                "id": "hk_cde",
                "name": "Standards",
                "meta": "CIC / BD / LandsD",
                "chunks": standards_chunks,
            },
            "playbook": {
                "id": "playbook",
                "name": "Playbook",
                "meta": "ACC × HK guide",
                "chunks": playbook_chunks,
            },
            "docs": {
                "id": "docs",
                "name": "Product Docs",
                "meta": "Autodesk help",
                "chunks": docs_chunks,
            },
        },
    }


def _load_demo_question_bank() -> list[dict[str, Any]]:
    path = PROJECT_ROOT / "knowledge" / "demo_question_bank.json"
    if not path.is_file():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    questions = payload.get("questions") if isinstance(payload, dict) else payload
    if not isinstance(questions, list):
        return []
    return [item for item in questions if isinstance(item, dict) and item.get("id")]


@app.get("/api/demo_questions")
def demo_questions(
    count: int = 3,
    exclude: str = "",
    lang: str = "en",
) -> dict[str, Any]:
    """Sample demo questions for the Try-these chips."""
    bank = _load_demo_question_bank()
    exclude_ids = {item.strip() for item in exclude.split(",") if item.strip()}
    available = [item for item in bank if item.get("id") not in exclude_ids]
    pool = available if len(available) >= count else bank
    sample_size = max(0, min(count, len(pool)))
    picked = random.sample(pool, sample_size) if sample_size else []
    # Prefer not repeating excluded set when pool was exhausted.
    if available and len(available) < count and bank:
        leftover = [item for item in bank if item.get("id") not in {p["id"] for p in picked}]
        need = count - len(picked)
        if need > 0 and leftover:
            picked.extend(random.sample(leftover, min(need, len(leftover))))
    ui_lang = "zh" if lang.lower().startswith("zh") else "en"
    items = []
    for item in picked:
        text = item.get(ui_lang) or item.get("en") or item.get("zh") or ""
        items.append(
            {
                "id": item.get("id"),
                "text": text,
                "en": item.get("en"),
                "zh": item.get("zh"),
                "track": item.get("track"),
                "capability": item.get("capability"),
            }
        )
    return {"count": len(items), "total": len(bank), "questions": items}


@app.post("/api/ask")
def ask(payload: AskRequest) -> dict[str, Any]:
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    corpus = (payload.corpus or "auto").strip().lower()
    if corpus not in {"auto", "hybrid", "docs", "hk_cde", "playbook"}:
        raise HTTPException(status_code=400, detail=f"invalid corpus: {corpus}")

    session_id = payload.session_id or str(uuid.uuid4())
    session = _sessions.setdefault(session_id, ConversationSession())
    force = None if corpus == "auto" else corpus

    try:
        result = get_orchestrator().ask(
            question,
            force_track=force,
            top_k=payload.top_k,
            no_generate=payload.no_generate,
            answer_lang=payload.answer_lang,
            session=session,
            record_turn=not payload.no_generate,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=f"index missing: {exc}") from exc
    except Exception as exc:  # noqa: BLE001 — surface to UI
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    body = _serialize_result(result, question=question, answer_lang=payload.answer_lang)
    body["session_id"] = session_id
    return body


@app.post("/api/session/clear")
def clear_session(session_id: str | None = None) -> dict[str, str]:
    if session_id and session_id in _sessions:
        del _sessions[session_id]
    return {"status": "cleared"}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def main() -> None:
    import uvicorn

    host = os.getenv("HYBRID_UI_HOST", "127.0.0.1")
    port = int(os.getenv("HYBRID_UI_PORT", "8787"))
    uvicorn.run(
        "web_hybrid.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
