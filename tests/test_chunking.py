from rag.chunking import chunk_document, estimate_tokens
from rag.config import ChunkConfig
from rag.ingestion import Document


def _document(text: str) -> Document:
    return Document(
        title="Test Page",
        source_url="https://example.com/test",
        text=text,
        source_file="DOCS_help_001.md",
        page_index=1,
        line_start=1,
        product="DOCS",
        content_hash="document-hash",
    )


def test_chunking_is_stable_and_never_crosses_document() -> None:
    document = _document(
        "\n".join(
            f"Step {index} contains enough explanatory text for chunking."
            for index in range(1, 15)
        )
    )
    config = ChunkConfig(target_tokens=60, overlap_tokens=10, minimum_tokens=5)

    first = chunk_document(document, config)
    second = chunk_document(document, config)

    assert len(first) > 1
    assert [chunk.chunk_id for chunk in first] == [
        chunk.chunk_id for chunk in second
    ]
    assert all(chunk.source_url == document.source_url for chunk in first)
    assert all(chunk.text.startswith("# Test Page\n\n") for chunk in first)
    assert all(chunk.chunk_count == len(first) for chunk in first)
    assert max(chunk.token_count for chunk in first) <= 75


def test_token_estimate_counts_cjk_more_densely() -> None:
    assert estimate_tokens("这是中文") == 4
    assert estimate_tokens("four") == 1
