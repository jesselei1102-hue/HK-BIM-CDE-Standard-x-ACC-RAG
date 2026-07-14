from pathlib import Path

from rag.config import CorpusConfig, PROJECT_ROOT
from rag.ingestion import load_corpus


def test_parser_cleans_navigation_without_splitting_body_heading(tmp_path: Path) -> None:
    markdown = """

---

# Standard Page

Source: https://example.com/?guid=Standard_Page

Share
Email
Facebook
Twitter
LinkedIn
Standard Page
Useful content.
# outgoing
Keep this body heading.
Related Resources
Keep this useful label.
Pages in this section
Remove this navigation item.

---

# Untitled

Source: https://example.com/?guid=Empty_Page

---

# Page Without Share

Source: https://example.com/?guid=No_Share

Page Without Share
Second page content.
Parent page:
Navigation only.
"""
    (tmp_path / "DOCS_help_001.md").write_text(markdown, encoding="utf-8")

    report = load_corpus(CorpusConfig(source_dir=tmp_path))

    assert report.total_pages == 3
    assert report.accepted_pages == 2
    assert report.rejection_reasons == {"empty_body": 1}

    first = report.documents[0]
    assert first.title == "Standard Page"
    assert first.text == (
        "Useful content.\n"
        "# outgoing\n"
        "Keep this body heading.\n"
        "Related Resources\n"
        "Keep this useful label."
    )
    assert "Pages in this section" not in first.text
    assert report.documents[1].text == "Second page content."


def test_docs_corpus_page_counts() -> None:
    report = load_corpus(
        CorpusConfig(source_dir=PROJECT_ROOT / "output" / "DOCS")
    )

    assert report.scanned_files == 6
    assert report.total_pages == 550
    assert report.accepted_pages == 530
    assert report.rejection_reasons == {"empty_body": 20}
    assert len({document.source_url for document in report.documents}) == 530
