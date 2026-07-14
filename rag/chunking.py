"""将清洗后的 DOCS 页面自动切分为可检查的 RAG chunks。

这里的 token 数是无需额外模型 tokenizer 的保守估算值。切分不会跨越
Source URL，并尽量只在原始行边界处截断。

运行预览：
    python -m rag.chunking --export .rag_data/chunks_preview.jsonl
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import statistics
from dataclasses import asdict, dataclass
from pathlib import Path

from .config import ChunkConfig, get_config
from .ingestion import Document, load_corpus


CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?。！？])\s+")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    title: str
    source_url: str
    source_file: str
    page_index: int
    line_start: int
    product: str
    document_hash: str
    chunk_index: int
    chunk_count: int
    token_count: int
    text: str


@dataclass(frozen=True)
class ChunkingStats:
    documents: int
    chunks: int
    multi_chunk_documents: int
    minimum_tokens: int
    median_tokens: int
    p90_tokens: int
    maximum_tokens: int
    below_minimum_chunks: int


def estimate_tokens(text: str) -> int:
    """估算 Qwen tokenizer 数量，适合离线切分和长度保护。"""

    cjk_count = len(CJK_RE.findall(text))
    non_cjk_chars = len(CJK_RE.sub("", text))
    return cjk_count + math.ceil(non_cjk_chars / 4)


def _split_oversized_unit(text: str, maximum_tokens: int) -> list[str]:
    if estimate_tokens(text) <= maximum_tokens:
        return [text]

    sentences = [part.strip() for part in SENTENCE_SPLIT_RE.split(text) if part.strip()]
    if len(sentences) > 1:
        result: list[str] = []
        buffer: list[str] = []
        for sentence in sentences:
            candidate = " ".join((*buffer, sentence))
            if buffer and estimate_tokens(candidate) > maximum_tokens:
                result.extend(_split_oversized_unit(" ".join(buffer), maximum_tokens))
                buffer = [sentence]
            else:
                buffer.append(sentence)
        if buffer:
            result.extend(_split_oversized_unit(" ".join(buffer), maximum_tokens))
        return result

    words = text.split()
    if len(words) <= 1:
        approximate_chars = max(1, maximum_tokens * 4)
        return [
            text[start : start + approximate_chars]
            for start in range(0, len(text), approximate_chars)
        ]

    result = []
    buffer = []
    for word in words:
        candidate = " ".join((*buffer, word))
        if buffer and estimate_tokens(candidate) > maximum_tokens:
            result.append(" ".join(buffer))
            buffer = [word]
        else:
            buffer.append(word)
    if buffer:
        result.append(" ".join(buffer))
    return result


def _document_units(document: Document, maximum_tokens: int) -> list[str]:
    units: list[str] = []
    for line in document.text.splitlines():
        line = line.strip()
        if line:
            units.extend(_split_oversized_unit(line, maximum_tokens))
    return units


def _body_windows(document: Document, config: ChunkConfig) -> list[str]:
    title_tokens = estimate_tokens(document.title) + 2
    body_target = max(16, config.target_tokens - title_tokens)
    units = _document_units(document, body_target)
    if not units:
        return []

    windows: list[str] = []
    start = 0
    while start < len(units):
        end = start
        token_total = 0
        while end < len(units):
            unit_tokens = estimate_tokens(units[end]) + 1
            if end > start and token_total + unit_tokens > body_target:
                break
            token_total += unit_tokens
            end += 1

        windows.append("\n".join(units[start:end]))
        if end >= len(units):
            break

        overlap_start = end
        overlap_tokens = 0
        while overlap_start > start:
            candidate_tokens = estimate_tokens(units[overlap_start - 1]) + 1
            if overlap_tokens and overlap_tokens + candidate_tokens > config.overlap_tokens:
                break
            overlap_tokens += candidate_tokens
            overlap_start -= 1
        start = end if overlap_start <= start else overlap_start

    if len(windows) > 1:
        last_tokens = estimate_tokens(windows[-1])
        merged = f"{windows[-2]}\n{windows[-1]}"
        if (
            last_tokens < config.minimum_tokens
            and estimate_tokens(merged) <= int(config.target_tokens * 1.25)
        ):
            windows[-2:] = [merged]

    return windows


def _chunk_id(document: Document, text: str) -> str:
    value = f"{document.source_url}\0{text}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()[:24]


def chunk_document(document: Document, config: ChunkConfig) -> list[Chunk]:
    bodies = _body_windows(document, config)
    count = len(bodies)
    chunks = []
    for index, body in enumerate(bodies):
        text = f"# {document.title}\n\n{body}"
        chunks.append(
            Chunk(
                chunk_id=_chunk_id(document, text),
                title=document.title,
                source_url=document.source_url,
                source_file=document.source_file,
                page_index=document.page_index,
                line_start=document.line_start,
                product=document.product,
                document_hash=document.content_hash,
                chunk_index=index,
                chunk_count=count,
                token_count=estimate_tokens(text),
                text=text,
            )
        )
    return chunks


def chunk_documents(
    documents: list[Document],
    config: ChunkConfig | None = None,
) -> list[Chunk]:
    chunk_config = config or get_config().chunks
    chunks = [
        chunk
        for document in documents
        for chunk in chunk_document(document, chunk_config)
    ]
    ids = [chunk.chunk_id for chunk in chunks]
    if len(ids) != len(set(ids)):
        raise ValueError("生成了重复 chunk_id，请检查重复内容")
    return chunks


def calculate_stats(chunks: list[Chunk]) -> ChunkingStats:
    if not chunks:
        return ChunkingStats(0, 0, 0, 0, 0, 0, 0, 0)

    token_counts = sorted(chunk.token_count for chunk in chunks)
    document_counts: dict[str, int] = {}
    for chunk in chunks:
        document_counts[chunk.source_url] = document_counts.get(chunk.source_url, 0) + 1

    p90_index = min(len(token_counts) - 1, math.ceil(len(token_counts) * 0.9) - 1)
    minimum = get_config().chunks.minimum_tokens
    return ChunkingStats(
        documents=len(document_counts),
        chunks=len(chunks),
        multi_chunk_documents=sum(count > 1 for count in document_counts.values()),
        minimum_tokens=token_counts[0],
        median_tokens=round(statistics.median(token_counts)),
        p90_tokens=token_counts[p90_index],
        maximum_tokens=token_counts[-1],
        below_minimum_chunks=sum(count < minimum for count in token_counts),
    )


def export_chunks(chunks: list[Chunk], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as output:
        for chunk in chunks:
            output.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 DOCS chunk 预览")
    parser.add_argument("--export", type=Path, required=True, help="JSONL 输出路径")
    args = parser.parse_args()

    app_config = get_config()
    ingestion = load_corpus(app_config.corpus)
    chunks = chunk_documents(ingestion.documents, app_config.chunks)
    stats = calculate_stats(chunks)
    export_chunks(chunks, args.export)

    print("DOCS Chunk 预览")
    print(f"  文档：{stats.documents}")
    print(f"  Chunks：{stats.chunks}")
    print(f"  多 Chunk 文档：{stats.multi_chunk_documents}")
    print(
        "  Token 估算："
        f"min={stats.minimum_tokens}, "
        f"median={stats.median_tokens}, "
        f"p90={stats.p90_tokens}, "
        f"max={stats.maximum_tokens}"
    )
    print(f"  低于最小长度：{stats.below_minimum_chunks}")
    print(f"  已导出：{args.export.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
