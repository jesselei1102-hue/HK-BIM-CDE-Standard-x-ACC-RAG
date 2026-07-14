#!/usr/bin/env python3
"""构建香港 CDE 行业路由向量索引（不进生成 prompt）。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.industry_hk.config import get_industry_hk_config  # noqa: E402
from rag.industry_hk.paths import HK_SECTIONS_INDEX_PATH  # noqa: E402
from rag.industry_hk.retrieval import industry_to_app_config  # noqa: E402
from rag.kb_index import KBRoutingIndex  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="构建行业 HK CDE 路由索引")
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(argv)

    industry = get_industry_hk_config()
    index = KBRoutingIndex(industry_to_app_config(industry))
    result = index.build(
        kb_path=industry.query_kb.kb_path,
        pages_index_path=HK_SECTIONS_INDEX_PATH,
        rebuild=args.rebuild,
    )
    print(
        f"行业路由索引完成：{result.record_count} 条 -> "
        f"{result.collection_name} @ {result.chroma_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
