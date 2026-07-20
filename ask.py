#!/usr/bin/env python3
"""Autodesk Docs / 香港 CDE / Playbook / 三轨编排 命令行问答。"""

from __future__ import annotations

import argparse
import os
import sys

from rag.config import get_config
from rag.conversation import ConversationSession
from rag.generation import format_sources, format_token_usage
from rag.industry_hk.config import get_industry_hk_config
from rag.orchestrator.merge import format_hybrid_sources
from rag.orchestrator.pipeline import HybridOrchestrator, format_orchestrator_debug
from rag.playbook_acc_hk.config import get_playbook_config
from rag.retrieval import format_retrieval_debug


def _print_answer(
    question: str,
    answer_text: str,
    source_lines: list[str],
    show_context: bool,
    contexts,
    token_line: str | None = None,
    *,
    rewritten_query: str | None = None,
) -> None:
    print(f"\n问题：{question}")
    if rewritten_query and rewritten_query.strip() != question.strip():
        print(f"检索问题：{rewritten_query}")
    print("\n回答：")
    print(answer_text)
    if token_line:
        print(f"\n{token_line}")
    print("\n来源：")
    if source_lines:
        print("\n".join(source_lines))
    else:
        print("(无)")

    if show_context and contexts:
        print("\n检索上下文：")
        for index, chunk in enumerate(contexts, start=1):
            similarity = (
                f"{chunk.vector_similarity:.3f}"
                if chunk.vector_similarity is not None
                else "-"
            )
            print(
                f"\n[{index}] score={chunk.score:.4f} "
                f"sim={similarity} "
                f"tokens={chunk.token_count}\n"
                f"{chunk.title}\n"
                f"{chunk.source_url}\n"
                f"{chunk.text[:500]}{'...' if len(chunk.text) > 500 else ''}"
            )


def ask_once(
    orchestrator: HybridOrchestrator,
    question: str,
    *,
    corpus: str,
    top_k: int | None,
    show_context: bool,
    no_generate: bool,
    show_retrieval_debug: bool,
    answer_lang: str,
    session: ConversationSession | None = None,
    record_turn: bool = True,
) -> int:
    force = None if corpus == "auto" else corpus
    result = orchestrator.ask(
        question,
        force_track=force,
        top_k=top_k,
        no_generate=no_generate,
        answer_lang=answer_lang,
        session=session,
        record_turn=record_turn,
    )

    print(f"轨道：{result.track}")
    if result.debug.is_follow_up:
        print(
            f"追问改写：{result.debug.rewritten_query or '-'} "
            f"({result.debug.rewrite_reason or '-'})"
        )
    if result.validation_ok is not None:
        print(f"validation: {'ok' if result.validation_ok else 'failed'}")
    if result.answer is not None and result.answer.model:
        print(f"生成方式：{result.answer.model}")
    if result.track == "hybrid" and result.merged is not None:
        for item in result.merged.tracked:
            if item.track == "playbook" and "1_cde_四容器概念回顧" in item.chunk.source_url:
                print(
                    "错误：Playbook 来源仍是「概念回顧」段，不会得到正确实施步骤。\n"
                    "请执行：python scripts/ingest_playbook_acc_hk.py --rebuild\n"
                    "并用 --corpus hybrid --no-generate 确认 [2] 为「2. WIP 容器配置」",
                    file=sys.stderr,
                )
                break
    if show_retrieval_debug:
        print("\n编排/检索路径：")
        print(format_orchestrator_debug(result.debug))
        if result.retrieval is not None:
            print("\n单轨检索：")
            print(format_retrieval_debug(result.retrieval.debug))

    if result.track == "hybrid" and result.merged is not None:
        source_lines = format_hybrid_sources(result.merged)
        contexts = [item.chunk for item in result.merged.tracked]
    elif result.track == "meta":
        source_lines = []
        contexts = []
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
        answer_text = "(仅检索模式，未调用生成模型)"
        context_tokens = sum(int(getattr(c, "token_count", 0) or 0) for c in contexts)
        token_line = f"Token：上下文 {context_tokens} | 提示 - | 生成 -"
    else:
        answer_text = result.answer.answer if result.answer else "(无回答)"
        token_line = format_token_usage(result.answer) if result.answer else None

    _print_answer(
        question,
        answer_text,
        source_lines,
        show_context=show_context or no_generate,
        contexts=contexts,
        token_line=token_line,
        rewritten_query=result.debug.rewritten_query,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="查询本地 RAG（Docs / 香港 CDE / Playbook / 三轨编排）"
    )
    parser.add_argument("question", nargs="?", help="要提问的内容")
    parser.add_argument(
        "--corpus",
        choices=["auto", "docs", "hk_cde", "playbook", "hybrid"],
        default="auto",
        help="语料轨：默认 auto=编排分流；hybrid=强制三轨；docs/hk_cde/playbook=单轨",
    )
    parser.add_argument("--top-k", type=int, default=None, help="每轨返回多少个上下文")
    parser.add_argument("--show-context", action="store_true")
    parser.add_argument("--no-generate", action="store_true")
    parser.add_argument("--show-retrieval-debug", action="store_true")
    parser.add_argument(
        "--no-nlp-coarse",
        action="store_true",
        help="关闭 BM25 NLP 粗筛（默认开启）",
    )
    parser.add_argument(
        "--no-nlp-rerank",
        action="store_true",
        help="关闭 NLP 特征精排（默认开启）",
    )
    parser.add_argument(
        "--lang",
        choices=["auto", "en", "zh-Hans", "zh-Hant"],
        default="auto",
        help="回答语言：auto=跟提问；en/简体/繁体可强制",
    )
    args = parser.parse_args(argv)

    if args.no_nlp_coarse:
        os.environ["RAG_NLP_COARSE"] = "false"
    if args.no_nlp_rerank:
        os.environ["RAG_NLP_RERANK"] = "false"

    docs_config = get_config()
    industry_config = get_industry_hk_config()
    playbook_config = get_playbook_config()
    print(
        f"模型：{docs_config.models.generation_model} | "
        f"Embedding：{docs_config.models.embedding_model} | "
        f"corpus={args.corpus} | lang={args.lang} | "
        f"nlp_coarse={docs_config.retrieval.nlp_coarse_enabled} | "
        f"nlp_rerank={docs_config.retrieval.nlp_rerank_enabled}"
    )
    if args.corpus in {"hybrid", "auto"}:
        pb_chunks = playbook_config.storage.chunks_path
        if not pb_chunks.is_file():
            print(
                f"警告：未找到 Playbook 索引 {pb_chunks}\n"
                "  hybrid 文件夹类问题需先运行："
                "python scripts/ingest_playbook_acc_hk.py --rebuild",
                file=sys.stderr,
            )
    _ = industry_config.storage.collection_name
    _ = playbook_config.storage.collection_name

    orchestrator = HybridOrchestrator(
        docs_config=docs_config,
        industry_config=industry_config,
        playbook_config=playbook_config,
    )

    if args.question:
        return ask_once(
            orchestrator,
            args.question,
            corpus=args.corpus,
            top_k=args.top_k,
            show_context=args.show_context,
            no_generate=args.no_generate,
            show_retrieval_debug=args.show_retrieval_debug,
            answer_lang=args.lang,
            session=None,
            record_turn=False,
        )

    session = ConversationSession()
    print("进入交互模式（支持多轮追问）。输入空行或 exit 退出；/clear 清空会话。")
    while True:
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not question or question.lower() in {"exit", "quit", "q"}:
            return 0
        if question.lower() in {"/clear", "clear", "/reset", "reset"}:
            session.clear()
            print("已清空会话历史。下一问将作为独立首轮。")
            continue
        ask_once(
            orchestrator,
            question,
            corpus=args.corpus,
            top_k=args.top_k,
            show_context=args.show_context,
            no_generate=args.no_generate,
            show_retrieval_debug=args.show_retrieval_debug,
            answer_lang=args.lang,
            session=session,
            record_turn=not args.no_generate,
        )


if __name__ == "__main__":
    raise SystemExit(main())
