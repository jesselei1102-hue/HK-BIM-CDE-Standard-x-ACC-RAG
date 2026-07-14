"""构建或增量更新 Autodesk Docs 本地向量索引。"""

from __future__ import annotations

import argparse

from rag.chunking import calculate_stats, chunk_documents
from rag.config import get_config
from rag.indexing import index_chunks
from rag.ingestion import load_corpus


def main() -> int:
    parser = argparse.ArgumentParser(description="构建 DOCS Chroma 索引")
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="删除现有 collection 后完整重建",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只解析和切分，不调用 embedding 或写入 Chroma",
    )
    args = parser.parse_args()

    config = get_config()
    ingestion = load_corpus(config.corpus)
    chunks = chunk_documents(ingestion.documents, config.chunks)
    stats = calculate_stats(chunks)

    print("DOCS 索引准备")
    print(f"  Markdown 文件：{ingestion.scanned_files}")
    print(f"  有效页面：{ingestion.accepted_pages}")
    print(f"  跳过页面：{len(ingestion.rejected)}")
    print(f"  Chunks：{stats.chunks}")
    print(f"  Embedding：{config.models.embedding_model}")
    print(f"  Collection：{config.storage.collection_name}")

    if args.dry_run:
        print("\nDry run 完成，未写入 Chroma。")
        return 0

    print("\n开始更新 Chroma：")
    result = index_chunks(chunks, config, rebuild=args.rebuild)
    print("\n索引完成")
    print(f"  总 Chunks：{result.total_chunks}")
    print(f"  新增 Embedding：{result.embedded_chunks}")
    print(f"  未变化：{result.unchanged_chunks}")
    print(f"  已删除旧 Chunk：{result.deleted_chunks}")
    print(f"  向量维度：{result.vector_dimension}")
    print(f"  Chroma 路径：{config.storage.chroma_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
