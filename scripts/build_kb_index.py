"""构建 KB 标题/术语路由索引（独立 Chroma 集合，不进入生成上下文）。

用法：
    python scripts/build_kb_index.py
    python scripts/build_kb_index.py --rebuild
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.config import get_config
from rag.kb_index import KBRoutingIndex


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 KB 标题/术语路由向量索引")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="删除并重建路由索引",
    )
    parser.add_argument(
        "--kb-path",
        type=Path,
        default=None,
        help="query_kb.jsonl 路径",
    )
    parser.add_argument(
        "--pages-index",
        type=Path,
        default=PROJECT_ROOT / "knowledge" / "research" / "pages_index.jsonl",
        help="语料 pages_index.jsonl（派生页面标题）",
    )
    args = parser.parse_args()

    config = get_config()
    index = KBRoutingIndex(config)
    result = index.build(
        kb_path=args.kb_path or config.query_kb.kb_path,
        pages_index_path=args.pages_index,
        rebuild=args.rebuild,
    )
    print(
        f"路由索引：{result.record_count} 条术语/标题\n"
        f"  集合：{result.collection_name}\n"
        f"  路径：{result.chroma_dir}\n"
        f"  用途：短句 Top-{config.query_kb.route_top_k} 召回路由（不进入生成 prompt）"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
