"""In-memory multi-turn conversation state for grounded RAG.

History is for resolving follow-up intent only. Prior answers are never
evidence for the current turn.
"""

from __future__ import annotations

from dataclasses import dataclass, field


DEFAULT_HISTORY_TURNS = 4
DEFAULT_ANSWER_SUMMARY_CHARS = 480


@dataclass(frozen=True)
class ConversationTurn:
    user_question: str
    rewritten_query: str
    answer: str
    track: str
    source_urls: list[str] = field(default_factory=list)
    source_titles: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class StandaloneQuery:
    query: str
    track_hint: str | None = None
    source_hints: list[str] = field(default_factory=list)
    is_follow_up: bool = False
    rewrite_reason: str = "passthrough"


@dataclass
class ConversationSession:
    """Session-scoped turn buffer. Not persisted across process restarts."""

    turns: list[ConversationTurn] = field(default_factory=list)
    max_history_turns: int = DEFAULT_HISTORY_TURNS
    answer_summary_chars: int = DEFAULT_ANSWER_SUMMARY_CHARS

    def clear(self) -> None:
        self.turns.clear()

    def append(self, turn: ConversationTurn) -> None:
        self.turns.append(turn)

    @property
    def empty(self) -> bool:
        return not self.turns

    def recent_turns(self, limit: int | None = None) -> list[ConversationTurn]:
        n = self.max_history_turns if limit is None else max(0, limit)
        if n <= 0:
            return []
        return list(self.turns[-n:])

    def summarize_turn(self, turn: ConversationTurn) -> dict[str, object]:
        answer = (turn.answer or "").strip()
        if len(answer) > self.answer_summary_chars:
            answer = answer[: self.answer_summary_chars].rstrip() + "…"
        return {
            "user_question": turn.user_question,
            "rewritten_query": turn.rewritten_query,
            "track": turn.track,
            "answer_summary": answer,
            "source_urls": list(turn.source_urls[:6]),
            "source_titles": list(turn.source_titles[:6]),
        }

    def history_for_rewrite(self) -> list[dict[str, object]]:
        return [self.summarize_turn(turn) for turn in self.recent_turns()]

    def last_source_urls(self, limit: int = 6) -> list[str]:
        if not self.turns:
            return []
        urls: list[str] = []
        seen: set[str] = set()
        for url in self.turns[-1].source_urls:
            if not url or url in seen:
                continue
            seen.add(url)
            urls.append(url)
            if len(urls) >= limit:
                break
        return urls

    def last_track(self) -> str | None:
        return self.turns[-1].track if self.turns else None
