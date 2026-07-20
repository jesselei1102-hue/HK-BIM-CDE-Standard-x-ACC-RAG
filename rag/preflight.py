"""检查三轨 RAG 运行前提。

运行：
    python -m rag.preflight
    python -m rag.preflight --track hk_cde
    python -m rag.preflight --skip-ollama
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import PROJECT_ROOT, AppConfig, get_config
from .industry_hk.config import get_industry_hk_config
from .playbook_acc_hk.config import get_playbook_config


REQUIRED_MODULES = {
    "chromadb": "chromadb",
    "ollama": "ollama",
    "rank_bm25": "rank-bm25",
}


@dataclass
class CheckResult:
    ok: bool
    label: str
    detail: str
    fix: str = ""


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


def _check_dependencies() -> CheckResult:
    missing = [
        package
        for module, package in REQUIRED_MODULES.items()
        if importlib.util.find_spec(module) is None
    ]
    if missing:
        return CheckResult(
            ok=False,
            label="Python deps",
            detail=f"missing: {', '.join(missing)}",
            fix="python -m pip install -r requirements.txt",
        )
    return CheckResult(ok=True, label="Python deps", detail="ok")


def _count_md(source_dir: Path, file_glob: str) -> int:
    if not source_dir.is_dir():
        return 0
    return len(list(source_dir.glob(file_glob)))


def _chroma_count(chroma_dir: Path, collection_name: str) -> int | None:
    if not chroma_dir.is_dir():
        return None
    try:
        chromadb = importlib.import_module("chromadb")
        client = chromadb.PersistentClient(path=str(chroma_dir))
        collection = client.get_collection(collection_name)
        return int(collection.count())
    except Exception:
        return None


def _check_track(
    *,
    name: str,
    source_dir: Path,
    file_glob: str,
    chunks_path: Path,
    chroma_dir: Path,
    collection_name: str,
    bootstrap_hint: str,
) -> list[CheckResult]:
    results: list[CheckResult] = []
    md_count = _count_md(source_dir, file_glob)
    if md_count <= 0:
        results.append(
            CheckResult(
                ok=False,
                label=f"{name} corpus",
                detail=f"no files under {source_dir} ({file_glob})",
                fix=bootstrap_hint,
            )
        )
    else:
        results.append(
            CheckResult(
                ok=True,
                label=f"{name} corpus",
                detail=f"{md_count} markdown files",
            )
        )

    if not chunks_path.is_file():
        results.append(
            CheckResult(
                ok=False,
                label=f"{name} chunks",
                detail=f"missing {chunks_path.relative_to(PROJECT_ROOT)}",
                fix=bootstrap_hint,
            )
        )
    else:
        line_count = sum(1 for _ in chunks_path.open(encoding="utf-8") if _.strip())
        results.append(
            CheckResult(
                ok=True,
                label=f"{name} chunks",
                detail=f"{line_count} lines in {chunks_path.name}",
            )
        )

    count = _chroma_count(chroma_dir, collection_name)
    if count is None or count <= 0:
        results.append(
            CheckResult(
                ok=False,
                label=f"{name} chroma",
                detail=f"collection {collection_name!r} missing or empty",
                fix=bootstrap_hint,
            )
        )
    else:
        results.append(
            CheckResult(
                ok=True,
                label=f"{name} chroma",
                detail=f"{count} vectors in {collection_name}",
            )
        )
    return results


def _check_ollama(config: AppConfig) -> list[CheckResult]:
    ollama = importlib.import_module("ollama")
    try:
        client = ollama.Client(
            host=config.models.ollama_host,
            timeout=config.models.request_timeout_seconds,
            trust_env=False,
        )
        installed = _listed_models(client.list())
    except Exception as exc:
        return [
            CheckResult(
                ok=False,
                label="Ollama",
                detail=f"cannot connect ({config.models.ollama_host}): {exc}",
                fix="Start Ollama, then: ollama serve",
            )
        ]

    results = [
        CheckResult(
            ok=True,
            label="Ollama",
            detail=f"connected ({config.models.ollama_host})",
        )
    ]
    required = {
        config.models.embedding_model,
        config.models.generation_model,
    }
    missing = sorted(required - installed)
    if missing:
        results.append(
            CheckResult(
                ok=False,
                label="Ollama models",
                detail=f"missing: {', '.join(missing)}",
                fix="\n".join(f"ollama pull {model}" for model in missing),
            )
        )
    else:
        results.append(
            CheckResult(
                ok=True,
                label="Ollama models",
                detail=", ".join(sorted(required)),
            )
        )
    return results


def run_preflight(
    *,
    track: str = "all",
    skip_ollama: bool = False,
    require_docs: bool = False,
) -> tuple[int, list[CheckResult]]:
    """Return (exit_code, checks).

    By default Docs index is optional so fresh clones can bootstrap HK+Playbook
    first. Pass ``require_docs=True`` (or ``--track docs|hybrid|all`` with
    ``--require-docs``) when Docs is needed.
    """
    results: list[CheckResult] = []
    results.append(_check_dependencies())

    try:
        docs_config = get_config()
    except ValueError as exc:
        docs_config = None
        results.append(
            CheckResult(
                ok=False,
                label="Docs config",
                detail=str(exc),
                fix="Place Autodesk Docs help Markdown under output/DOCS/, "
                "or set RAG_SOURCE_DIR",
            )
        )

    hk_config = get_industry_hk_config()
    playbook_config = get_playbook_config()

    want_docs = track in {"all", "docs", "hybrid", "auto"}
    want_hk = track in {"all", "hk_cde", "hybrid", "auto"}
    want_playbook = track in {"all", "playbook", "hybrid", "auto"}

    if want_docs and docs_config is not None:
        docs_checks = _check_track(
            name="Docs",
            source_dir=docs_config.corpus.source_dir,
            file_glob=docs_config.corpus.file_glob,
            chunks_path=docs_config.storage.chunks_path,
            chroma_dir=docs_config.storage.chroma_dir,
            collection_name=docs_config.storage.collection_name,
            bootstrap_hint=(
                "Obtain Autodesk Docs help Markdown legally, then:\n"
                "  python ingest.py --rebuild\n"
                "  python scripts/build_query_kb.py\n"
                "  python scripts/build_kb_index.py --rebuild"
            ),
        )
        if not require_docs and track in {"all", "auto"}:
            # Soft: report but do not fail exit code for missing Docs on default.
            for item in docs_checks:
                if not item.ok:
                    item.detail = f"(optional) {item.detail}"
                    item.ok = True
                    item.fix = (
                        "Docs is optional for HK/Playbook-only use. "
                        "For hybrid/docs: " + item.fix
                    )
        results.extend(docs_checks)

    if want_hk:
        results.extend(
            _check_track(
                name="HK CDE",
                source_dir=hk_config.corpus.source_dir,
                file_glob=hk_config.corpus.file_glob,
                chunks_path=hk_config.storage.chunks_path,
                chroma_dir=hk_config.storage.chroma_dir,
                collection_name=hk_config.storage.collection_name,
                bootstrap_hint="bash scripts/bootstrap_indexes.sh",
            )
        )

    if want_playbook:
        results.extend(
            _check_track(
                name="Playbook",
                source_dir=playbook_config.corpus.source_dir,
                file_glob=playbook_config.corpus.file_glob,
                chunks_path=playbook_config.storage.chunks_path,
                chroma_dir=playbook_config.storage.chroma_dir,
                collection_name=playbook_config.storage.collection_name,
                bootstrap_hint="bash scripts/bootstrap_indexes.sh",
            )
        )

    if not skip_ollama and docs_config is not None:
        results.extend(_check_ollama(docs_config))
    elif not skip_ollama:
        # Still try Ollama with defaults even if Docs corpus path is missing.
        from .config import ModelConfig

        class _Shim:
            models = ModelConfig()

        results.extend(_check_ollama(_Shim()))  # type: ignore[arg-type]

    exit_code = 0 if all(item.ok for item in results) else 1
    return exit_code, results


def _print_results(results: list[CheckResult]) -> None:
    print("RAG preflight")
    print(f"  project: {PROJECT_ROOT}")
    for item in results:
        mark = "OK" if item.ok else "FAIL"
        print(f"  [{mark}] {item.label}: {item.detail}")
        if not item.ok and item.fix:
            for line in item.fix.splitlines():
                print(f"         → {line}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check RAG runtime prerequisites")
    parser.add_argument(
        "--track",
        choices=["all", "auto", "docs", "hk_cde", "playbook", "hybrid"],
        default="all",
        help="Which track(s) to verify (default: all; Docs optional unless --require-docs)",
    )
    parser.add_argument(
        "--require-docs",
        action="store_true",
        help="Fail when Docs corpus/index is missing",
    )
    parser.add_argument(
        "--skip-ollama",
        action="store_true",
        help="Skip Ollama connectivity and model checks",
    )
    args = parser.parse_args(argv)

    exit_code, results = run_preflight(
        track=args.track,
        skip_ollama=args.skip_ollama,
        require_docs=args.require_docs or args.track in {"docs", "hybrid"},
    )
    _print_results(results)
    if exit_code == 0:
        print("\nPreflight passed.")
        if args.track in {"all", "auto", "hk_cde"}:
            print("  Try: python ask.py --corpus hk_cde \"What is WIP?\"")
    else:
        print("\nPreflight failed. Fix the items above, then re-run.")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
