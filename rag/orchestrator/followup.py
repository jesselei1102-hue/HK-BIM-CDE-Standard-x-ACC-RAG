"""History-aware standalone query rewrite for multi-turn grounded RAG.

Prior answers may be wrong: they may only resolve deixis ("那/它/子文件夹呢"),
never supply facts into the rewritten retrieval query.
"""

from __future__ import annotations

import json
import re
from typing import Any

import ollama

from rag.config import AppConfig, get_config
from rag.conversation import ConversationSession, ConversationTurn, StandaloneQuery


_FOLLOWUP_CUE_RE = re.compile(
    r"(那|那它|那这个|那這個|还有|還有|另外|继续|繼續|同上|"
    r"子文件夹|子資料夾|继承|繼承|"
    r"\b(what about|and then|also for|same as|those|that one|them)\b|"
    r"(呢)\s*$)",
    re.I,
)

_STANDALONE_RE = re.compile(
    r"(如何|怎么|怎樣|怎样|什么是|什麼是|How\s+to|What\s+is|"
    r"Autodesk|Docs|ACC|CIC|DEVB|港标|港標|WIP|CDE|权限|權限|"
    r"文件夹|資料夾|审批|審批)",
    re.I,
)

_FOLLOWUP_SYSTEM = """你是多轮 RAG 的检索问题改写器。
任务：把当前追问改写成一条独立、完整、可单独检索的问题。

硬规则：
1. 历史答案可能有错，只能用来理解指代（它/那/这个/子文件夹呢），不能把历史说法写成既定事实。
2. 不要抄写历史答案中的数字、菜单路径、结论当作检索问题的前提。
3. 若当前问题本身已完整独立，可几乎原样输出，只做轻微规范化。
4. 只输出严格 JSON，不要 Markdown，不要解释。

JSON schema:
{
  "query": "独立检索问题",
  "track_hint": "docs|hk_cde|playbook|hybrid|null",
  "source_hints": ["可选的上轮相关 URL 子串，最多3个"],
  "is_follow_up": true,
  "rewrite_reason": "简短原因"
}
"""


def looks_like_follow_up(question: str, session: ConversationSession | None) -> bool:
    if session is None or session.empty:
        return False
    text = (question or "").strip()
    if not text:
        return False
    explicit_follow = bool(
        re.search(
            r"^(那|那它|那这个|那這個|还有|還有|另外|what about)\s*",
            text,
            re.I,
        )
        or re.search(r"(呢)\s*[?？]?\s*$", text)
    )
    # Domain-anchored standalone questions are new turns unless clearly deictic.
    if _STANDALONE_RE.search(text) and not explicit_follow:
        return False
    if explicit_follow or _FOLLOWUP_CUE_RE.search(text):
        return True
    # Very short fragments without domain anchors after a prior turn.
    return len(text) <= 8 and not _STANDALONE_RE.search(text)


def _extract_json_object(text: str) -> dict[str, Any] | None:
    raw = (text or "").strip()
    if not raw:
        return None
    try:
        data = json.loads(raw)
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
        return data if isinstance(data, dict) else None
    except json.JSONDecodeError:
        return None


def _normalize_track_hint(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip().lower()
    if text in {"", "null", "none", "auto"}:
        return None
    alias = {
        "industry": "hk_cde",
        "hk": "hk_cde",
        "cde": "hk_cde",
        "product": "docs",
        "doc": "docs",
    }
    text = alias.get(text, text)
    if text in {"docs", "hk_cde", "playbook", "hybrid"}:
        return text
    return None


def _fallback_standalone(
    question: str,
    session: ConversationSession,
) -> StandaloneQuery:
    last = session.turns[-1]
    q = question.strip()
    # Prefer thematic glue from prior rewritten/user question, never from answer facts.
    theme = (last.rewritten_query or last.user_question or "").strip()
    theme_short = theme
    for sep in ("？", "?", "。", ".", "！", "!"):
        if sep in theme_short:
            theme_short = theme_short.split(sep, 1)[0].strip()
            break
    if len(theme_short) > 80:
        theme_short = theme_short[:80].rstrip()

    if looks_like_follow_up(q, session) and theme_short:
        query = f"{theme_short}：{q}" if "：" not in q and ":" not in q else q
        if query == q and theme_short not in q:
            query = f"关于「{theme_short}」的追问：{q}"
    else:
        query = q

    hints = session.last_source_urls(limit=3)
    return StandaloneQuery(
        query=query,
        track_hint=session.last_track(),
        source_hints=hints,
        is_follow_up=True,
        rewrite_reason="conservative_fallback",
    )


def _parse_standalone(
    data: dict[str, Any],
    *,
    question: str,
    session: ConversationSession,
) -> StandaloneQuery:
    query = str(data.get("query") or "").strip() or question.strip()
    hints_raw = data.get("source_hints") or []
    prior_urls = session.last_source_urls(limit=6)
    hints: list[str] = []
    if isinstance(hints_raw, list):
        for item in hints_raw[:3]:
            text = str(item or "").strip()
            if not text:
                continue
            # Prefer real URLs / substrings that match prior turn sources.
            matched = [url for url in prior_urls if text in url or url in text]
            if matched:
                for url in matched:
                    if url not in hints:
                        hints.append(url)
            elif "://" in text or text.startswith("hk_cde://") or text.startswith(
                "playbook://"
            ):
                if text not in hints:
                    hints.append(text)
    if not hints:
        hints = prior_urls[:3]
    is_follow_up = bool(data.get("is_follow_up", True))
    reason = str(data.get("rewrite_reason") or "llm_rewrite").strip() or "llm_rewrite"
    return StandaloneQuery(
        query=query,
        track_hint=_normalize_track_hint(data.get("track_hint")),
        source_hints=hints[:3],
        is_follow_up=is_follow_up,
        rewrite_reason=reason,
    )


def rewrite_followup_query(
    question: str,
    session: ConversationSession | None,
    *,
    config: AppConfig | None = None,
    use_llm: bool = True,
) -> StandaloneQuery:
    """Rewrite a follow-up into a standalone retrieval query.

    When there is no history, returns the original question unchanged.
    """
    text = (question or "").strip()
    if not text:
        return StandaloneQuery(query="", rewrite_reason="empty")
    if session is None or session.empty:
        return StandaloneQuery(
            query=text,
            is_follow_up=False,
            rewrite_reason="no_history",
        )

    # Complete standalone questions skip LLM to reduce latency / drift.
    if not looks_like_follow_up(text, session):
        return StandaloneQuery(
            query=text,
            track_hint=None,
            source_hints=[],
            is_follow_up=False,
            rewrite_reason="standalone_passthrough",
        )

    if not use_llm:
        return _fallback_standalone(text, session)

    app_config = config or get_config()
    history = session.history_for_rewrite()
    user_payload = {
        "current_question": text,
        "recent_turns": history,
        "instruction": (
            "Resolve deixis into a standalone retrieval query. "
            "Do not copy prior answer claims as facts."
        ),
    }
    try:
        client = ollama.Client(
            host=app_config.models.ollama_host,
            timeout=min(45, int(app_config.models.request_timeout_seconds or 60)),
            trust_env=False,
        )
        response = client.chat(
            model=app_config.models.generation_model,
            messages=[
                {"role": "system", "content": _FOLLOWUP_SYSTEM},
                {
                    "role": "user",
                    "content": json.dumps(user_payload, ensure_ascii=False),
                },
            ],
            think=False,
            options={"temperature": 0.0, "num_predict": 280},
        )
        message = getattr(response, "message", None)
        if message is None and isinstance(response, dict):
            message = response.get("message", {})
        if isinstance(message, dict):
            content = message.get("content") or message.get("thinking") or ""
        else:
            content = getattr(message, "content", None) or getattr(
                message, "thinking", None
            ) or ""
        data = _extract_json_object(str(content))
        if data is None:
            return _fallback_standalone(text, session)
        return _parse_standalone(data, question=text, session=session)
    except Exception:
        return _fallback_standalone(text, session)


def turns_as_untrusted_context(
    turns: list[ConversationTurn],
    *,
    answer_chars: int = 240,
) -> str:
    """Format prior turns for generation prompts (explicitly untrusted)."""
    if not turns:
        return ""
    lines: list[str] = [
        "<conversation_context_untrusted>",
        "以下历史仅用于理解指代与语气；其中答案可能有错，不得作为事实依据或引用证据。",
    ]
    for index, turn in enumerate(turns, start=1):
        answer = (turn.answer or "").strip()
        if len(answer) > answer_chars:
            answer = answer[:answer_chars].rstrip() + "…"
        lines.append(f"[历史轮次 {index}]")
        lines.append(f"用户：{turn.user_question}")
        lines.append(f"当时检索问题：{turn.rewritten_query}")
        lines.append(f"轨道：{turn.track}")
        lines.append(f"当时回答（不可信）：{answer}")
    lines.append("</conversation_context_untrusted>")
    return "\n".join(lines)
