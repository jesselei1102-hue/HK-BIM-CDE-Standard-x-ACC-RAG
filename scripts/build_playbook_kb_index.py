#!/usr/bin/env python3
"""构建 playbook 路由向量索引（不进生成 prompt）。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.playbook_acc_hk.config import get_playbook_config  # noqa: E402
from rag.playbook_acc_hk.paths import PLAYBOOK_SECTIONS_INDEX_PATH  # noqa: E402
from rag.playbook_acc_hk.retrieval import playbook_to_app_config  # noqa: E402
from rag.kb_index import KBRoutingIndex  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="构建 playbook 路由索引")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(argv)

    playbook = get_playbook_config()
    index = KBRoutingIndex(playbook_to_app_config(playbook))
    result = index.build(
        kb_path=playbook.query_kb.kb_path,
        pages_index_path=PLAYBOOK_SECTIONS_INDEX_PATH,
        rebuild=args.rebuild,
    )
    print(
        f"Playbook 路由索引完成：{result.record_count} 条 -> "
        f"{result.collection_name} @ {result.chroma_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
