"""检查 RAG 运行前提。

运行：
    python -m rag.preflight
"""

from __future__ import annotations

import importlib
import importlib.util
from collections.abc import Iterable
from typing import Any

from .config import AppConfig, get_config


REQUIRED_MODULES = {
    "chromadb": "chromadb",
    "ollama": "ollama",
    "rank_bm25": "rank-bm25",
}


def _model_name(model: Any) -> str | None:
    if isinstance(model, dict):
        return model.get("model") or model.get("name")
    return getattr(model, "model", None) or getattr(model, "name", None)


def _listed_models(response: Any) -> set[str]:
    if isinstance(response, dict):
        models: Iterable[Any] = response.get("models", [])
    else:
        models = getattr(response, "models", [])
    return {name for model in models if (name := _model_name(model))}


def _check_dependencies() -> list[str]:
    return [
        package
        for module, package in REQUIRED_MODULES.items()
        if importlib.util.find_spec(module) is None
    ]


def _print_config(config: AppConfig) -> None:
    files = sorted(config.corpus.source_dir.glob(config.corpus.file_glob))
    print("RAG 配置")
    print(f"  语料目录：{config.corpus.source_dir}")
    print(f"  Markdown：{len(files)} 个（{config.corpus.file_glob}）")
    print(f"  Embedding：{config.models.embedding_model}")
    print(f"  LLM：{config.models.generation_model}")
    print(f"  Chroma：{config.storage.chroma_dir}")
    print(
        "  Chunk："
        f"{config.chunks.target_tokens} tokens，"
        f"重叠 {config.chunks.overlap_tokens} tokens"
    )


def main() -> int:
    try:
        config = get_config()
    except ValueError as exc:
        print(f"配置错误：{exc}")
        return 1

    _print_config(config)

    files = sorted(config.corpus.source_dir.glob(config.corpus.file_glob))
    if not files:
        print(f"\n未找到语料文件：{config.corpus.file_glob}")
        return 1

    missing_packages = _check_dependencies()
    if missing_packages:
        print("\n缺少 Python 依赖：")
        for package in missing_packages:
            print(f"  - {package}")
        print("请运行：python3 -m pip install -r requirements.txt")
        return 1

    ollama = importlib.import_module("ollama")
    try:
        client = ollama.Client(
            host=config.models.ollama_host,
            timeout=config.models.request_timeout_seconds,
            trust_env=False,
        )
        installed = _listed_models(client.list())
    except Exception as exc:
        print(f"\n无法连接 Ollama（{config.models.ollama_host}）：{exc}")
        print("请先启动 Ollama 服务。")
        return 1

    required = {
        config.models.embedding_model,
        config.models.generation_model,
    }
    missing_models = sorted(required - installed)
    if missing_models:
        print("\n缺少 Ollama 模型：")
        for model in missing_models:
            print(f"  - {model}")
        print("请运行：")
        for model in missing_models:
            print(f"  ollama pull {model}")
        return 1

    print("\n预检通过，可以开始构建 DOCS 索引。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
