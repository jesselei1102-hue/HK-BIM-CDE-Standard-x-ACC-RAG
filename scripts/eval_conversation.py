#!/usr/bin/env python3
"""Eval multi-turn rewrite + optional re-retrieval evidence boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.conversation import ConversationSession, ConversationTurn  # noqa: E402
from rag.orchestrator.classify import classify_intent  # noqa: E402
from rag.orchestrator.followup import rewrite_followup_query  # noqa: E402
from rag.orchestrator.pipeline import HybridOrchestrator  # noqa: E402


def _load_cases(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def _build_session(history: list[dict]) -> ConversationSession:
    session = ConversationSession()
    for row in history:
        session.append(
            ConversationTurn(
                user_question=str(row.get("user_question") or ""),
                rewritten_query=str(row.get("rewritten_query") or ""),
                answer=str(row.get("answer") or ""),
                track=str(row.get("track") or "docs"),
                source_urls=list(row.get("source_urls") or []),
                source_titles=list(row.get("source_titles") or []),
            )
        )
    return session


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Conversation follow-up eval")
    parser.add_argument(
        "--cases",
        type=Path,
        default=PROJECT_ROOT / "eval" / "conversation_cases.jsonl",
    )
    args = parser.parse_args(argv)
    cases = _load_cases(args.cases)
    orchestrator: HybridOrchestrator | None = None
    passed = 0

    for case in cases:
        session = _build_session(list(case.get("history") or []))
        follow_up = str(case["follow_up"])
        standalone = rewrite_followup_query(
            follow_up,
            session,
            use_llm=bool(case.get("use_llm", False)),
        )
        ok = True
        reasons: list[str] = []

        expect_any = [str(x).lower() for x in case.get("expect_query_contains_any") or []]
        query_l = standalone.query.lower()
        if expect_any and not any(token in query_l for token in expect_any):
            ok = False
            reasons.append(f"query missing any of {expect_any}: {standalone.query!r}")

        for banned in case.get("expect_query_excludes") or []:
            if str(banned).lower() in query_l:
                ok = False
                reasons.append(f"query leaked banned token {banned!r}")

        if "expect_is_follow_up" in case and bool(case["expect_is_follow_up"]) != bool(
            standalone.is_follow_up
        ):
            ok = False
            reasons.append(
                f"is_follow_up={standalone.is_follow_up} "
                f"expected={case['expect_is_follow_up']}"
            )

        track = classify_intent(standalone.query).track
        expect_tracks = list(case.get("expect_track_in") or [])
        if expect_tracks and track not in expect_tracks:
            ok = False
            reasons.append(f"track={track} not in {expect_tracks}")

        if case.get("retrieve"):
            if orchestrator is None:
                orchestrator = HybridOrchestrator()
            force = case.get("force_track")
            result = orchestrator.ask(
                follow_up,
                force_track=force,
                top_k=3,
                no_generate=True,
                session=session,
                record_turn=False,
            )
            urls: list[str] = []
            if result.merged is not None:
                urls = [item.chunk.source_url for item in result.merged.tracked]
            elif result.chunks_docs:
                urls = [c.source_url for c in result.chunks_docs]
            elif result.chunks_industry:
                urls = [c.source_url for c in result.chunks_industry]
            elif result.chunks_playbook:
                urls = [c.source_url for c in result.chunks_playbook]
            needle = str(case.get("expect_top1_url_contains") or "")
            top1 = urls[0] if urls else ""
            if needle and needle not in top1:
                ok = False
                reasons.append(f"top1 url {top1!r} missing {needle!r}")

        status = "OK" if ok else "FAIL"
        print(f"[{status}] {case['id']}")
        print(f"  follow_up: {follow_up}")
        print(f"  rewritten: {standalone.query}")
        print(f"  track: {track} follow_up={standalone.is_follow_up}")
        if reasons:
            for reason in reasons:
                print(f"  - {reason}")
        if ok:
            passed += 1

    total = len(cases)
    print("-" * 40)
    print(f"Conversation eval: {passed}/{total}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
