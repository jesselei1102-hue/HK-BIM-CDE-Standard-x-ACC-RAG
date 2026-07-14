"""对比 RAG 检索质量与不同 LLM 的生成质量。

用法：
    python compare_models.py "Autodesk Docs 中单个文件最大可以多大？"
    python compare_models.py "问题" --models gemma3:1b,qwen3:4b
    python compare_models.py --file eval/questions.txt

诊断规则：
- 检索来源不对 → RAG / Embedding / 切分问题
- 检索来源对，但模型答错 → LLM 问题
- 换更大模型后答对 → 确认是生成瓶颈
"""

from __future__ import annotations

import argparse
import time
from dataclasses import replace

from rag.config import get_config
from rag.generation import generate_answer
from rag.retrieval import HybridRetriever, RetrievedChunk, format_retrieval_debug


def _print_retrieval(question: str, contexts: list[RetrievedChunk]) -> None:
    print(f"\n{'=' * 72}")
    print(f"问题：{question}")
    print(f"{'=' * 72}")
    print("\n[1] 检索结果（所有模型共用同一上下文）")
    if not contexts:
        print("  (无命中) → 更可能是 RAG / Embedding / 阈值问题")
        return

    for index, chunk in enumerate(contexts, start=1):
        similarity = (
            f"{chunk.vector_similarity:.3f}"
            if chunk.vector_similarity is not None
            else "-"
        )
        print(
            f"  [{index}] {chunk.title}\n"
            f"      sim={similarity}  score={chunk.score:.4f}\n"
            f"      {chunk.source_url}"
        )


def _judge_prompt() -> str:
    return (
        "请先人工判断检索来源是否足以回答问题：\n"
        "  A = 来源正确，且包含答案\n"
        "  B = 来源相关，但不完整\n"
        "  C = 来源错误 / 无关"
    )


def compare_question(
    retriever: HybridRetriever,
    question: str,
    models: list[str],
    top_k: int | None,
    show_retrieval_debug: bool,
) -> None:
    result = retriever.retrieve_with_debug(question, top_k=top_k)
    contexts = result.chunks
    _print_retrieval(question, contexts)
    if show_retrieval_debug:
        print("\n检索路径：")
        print(format_retrieval_debug(result.debug))
    print("\n" + _judge_prompt())

    print("\n[2] 不同 LLM 在同一上下文上的回答")
    if not contexts:
        print("  跳过生成：没有检索上下文。")
        return

    base = retriever.config
    for model in models:
        config = replace(
            base,
            models=replace(base.models, generation_model=model),
        )
        started = time.perf_counter()
        try:
            result = generate_answer(question, contexts, config)
            elapsed = time.perf_counter() - started
            print(f"\n  --- {model} ({elapsed:.1f}s) ---")
            print(f"  {result.answer}")
        except Exception as exc:
            print(f"\n  --- {model} ---")
            print(f"  调用失败：{exc}")

    print(
        "\n[3] 如何归因\n"
        "  - 检索判 C，所有模型都差 → 优先修 RAG\n"
        "  - 检索判 A，小模型错、大模型对 → LLM 瓶颈\n"
        "  - 检索判 A，所有模型都错 → Prompt / 上下文组织问题\n"
        "  - 检索判 B → 先改善切分或 top-k，再比模型"
    )


def _load_questions(path: str) -> list[str]:
    questions: list[str] = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                questions.append(line)
    return questions


def main() -> int:
    parser = argparse.ArgumentParser(description="对比 RAG 与不同 LLM 的瓶颈")
    parser.add_argument("question", nargs="?", help="单个问题")
    parser.add_argument(
        "--file",
        help="从文本文件读取问题，每行一个",
    )
    parser.add_argument(
        "--models",
        default="gemma3:1b",
        help="逗号分隔的 Ollama 生成模型，例如 gemma3:1b,qwen3:4b",
    )
    parser.add_argument("--top-k", type=int, default=None)
    parser.add_argument(
        "--show-retrieval-debug",
        action="store_true",
        help="打印 KB 查表与检索路径调试信息",
    )
    args = parser.parse_args()

    questions: list[str] = []
    if args.question:
        questions.append(args.question)
    if args.file:
        questions.extend(_load_questions(args.file))
    if not questions:
        parser.error("请提供 question 或 --file")

    models = [item.strip() for item in args.models.split(",") if item.strip()]
    if not models:
        parser.error("--models 不能为空")

    config = get_config()
    print(
        f"Embedding：{config.models.embedding_model} | "
        f"对比模型：{', '.join(models)}"
    )
    retriever = HybridRetriever(config)
    for question in questions:
        compare_question(
            retriever,
            question,
            models,
            args.top_k,
            args.show_retrieval_debug,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
