"""Tests for HK CDE Spec playbook corpus, domain boost, and ingestion."""

from __future__ import annotations

from pathlib import Path

from rag.orchestrator.classify import (
    detect_playbook_domain,
    playbook_url_prefix_for,
)
from rag.playbook_acc_hk.ingestion import (
    PlaybookCorpusLoadConfig,
    load_playbook_corpus,
)
from rag.playbook_acc_hk.paths import PLAYBOOK_CORPUS_DIR


def test_detect_playbook_domain_buildings_vs_civil() -> None:
    assert detect_playbook_domain("Buildings九段命名") == "buildings"
    assert detect_playbook_domain("Civil LandsD 提交包") == "civil"
    assert detect_playbook_domain("ACC文件夹怎么配") == "buildings"


def test_playbook_url_prefix_domain_aware() -> None:
    b = playbook_url_prefix_for("folder", "Buildings 目录结构")
    c = playbook_url_prefix_for("folder", "Civil By Section 目录")
    assert b and "11_buildings_folders_permissions" in b
    assert c and "21_civil_folders_permissions" in c
    naming_c = playbook_url_prefix_for("naming", "Civil Building等于区段码")
    assert naming_c and "23_civil_naming_fields" in naming_c


def test_load_playbook_corpus_has_buildings_and_civil() -> None:
    report = load_playbook_corpus(
        PlaybookCorpusLoadConfig(source_dir=PLAYBOOK_CORPUS_DIR)
    )
    assert report.scanned_files >= 13
    assert report.accepted_pages >= 20
    urls = " ".join(doc.source_url for doc in report.documents)
    assert "11_buildings_folders_permissions" in urls
    assert "21_civil_folders_permissions" in urls
    assert "13_buildings_naming_fields" in urls
    assert "23_civil_naming_fields" in urls
    # No legacy chapters
    assert "02_folder_cde" not in urls
    assert "08_project_template" not in urls
    # Domain tags present
    assert any("[domain=buildings]" in d.text for d in report.documents)
    assert any("[domain=civil]" in d.text for d in report.documents)
    # Folder tree preserved in a single semantic unit somewhere
    folder_docs = [
        d
        for d in report.documents
        if "folders_permissions" in d.source_url and "01_WIP" in d.text
    ]
    assert folder_docs
    assert any("Team_" in d.text or "8_BIM" in d.text for d in folder_docs)


def test_corpus_files_exist() -> None:
    expected = [
        "00_hk_cde_spec_index.md",
        "10_buildings_overview_roles.md",
        "11_buildings_folders_permissions.md",
        "20_civil_overview_roles.md",
        "21_civil_folders_permissions.md",
        "24_civil_forms_statutory.md",
    ]
    for name in expected:
        assert (PLAYBOOK_CORPUS_DIR / name).is_file()


def test_no_cross_domain_mixed_chunk_bodies() -> None:
    report = load_playbook_corpus(
        PlaybookCorpusLoadConfig(source_dir=PLAYBOOK_CORPUS_DIR)
    )
    for doc in report.documents:
        if "[domain=buildings]" in doc.text:
            if "landsd completeness" in doc.text.lower():
                raise AssertionError(
                    f"Civil LandsD leaked into buildings: {doc.source_url}"
                )
        if "[domain=civil]" in doc.text and "BD Submission Checklist" in doc.text:
            raise AssertionError(
                f"Buildings BD checklist leaked into civil: {doc.source_url}"
            )
