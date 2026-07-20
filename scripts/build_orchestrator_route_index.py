#!/usr/bin/env python3
"""构建 orchestrator 语义路由向量索引（track / capability 例句）。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.config import get_config  # noqa: E402
from rag.orchestrator.route_index import OrchestratorRouteIndex  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build orchestrator semantic route index")
    parser.add_argument(
        "--routes",
        type=Path,
        default=None,
        help="Path to orchestrator_routes.jsonl",
    )
    parser.add_argument("--rebuild", action="store_true", help="Drop and rebuild collection")
    args = parser.parse_args(argv)

    config = get_config()
    routes_path = args.routes or config.semantic_router.routes_path
    if not routes_path.is_file():
        print(f"ERROR: routes file missing: {routes_path}", file=sys.stderr)
        return 1

    index = OrchestratorRouteIndex(config)
    result = index.build(routes_path=routes_path, rebuild=args.rebuild)
    print(
        f"Built orchestrator route index: {result.record_count} exemplars "
        f"→ {result.collection_name} @ {result.chroma_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
