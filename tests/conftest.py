from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _set_test_rag_source_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep config validation from requiring local output/DOCS in CI."""
    monkeypatch.setenv("RAG_SOURCE_DIR", ".")
