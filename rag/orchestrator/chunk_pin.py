"""从 chunks.jsonl 按 URL/GUID 硬加载段落（不依赖向量排序）。"""

from __future__ import annotations

import json
from pathlib import Path

from rag.orchestrator.merge import MergedContexts
from rag.orchestrator.playbook_pin import (
    CONCEPT_URL_MARKER,
    load_wip_folder_chunk,
    playbook_chunk_needs_folder_pin,
    pin_folder_playbook_in_merged,
)
from rag.retrieval import RetrievedChunk

DOCS_FOLDER_GUID = "Organize_files_With_Folders"
DOCS_FILES_GUID = "Files"
DOCS_NAMING_GUID = "File_Naming_Standard"
DOCS_SETUP_NAMING_GUID = "Set_Up_Naming_Standard"
DOCS_MODEL_BROWSER_GUID = "Model_Browser"
DOCS_VIEWER_SETTINGS_GUID = "Viewer_Settings_Files"
DOCS_PERMISSIONS_GUID = "Folder_Permissions"
DOCS_PERMISSION_LEVELS_GUID = "Folder_Permission_Levels"
DOCS_PROJECT_CREATE_GUID = "Create_Project"
DOCS_PROJECT_MANAGE_GUID = "Create_Manage_Projects"
DOCS_TEMPLATES_DOCS_GUID = "Configure_Templates_Docs"
DOCS_TEMPLATES_CREATE_GUID = "Templates_Create"
DOCS_REVIEWS_CREATE_GUID = "Reviews_Create_Edit"
DOCS_REVIEWS_WORKFLOW_GUID = "Reviews_Workflow"

# 港标命名：优先 Information Identification / Harmonisation 命名附录
HK_NAMING_URL_PARTS = (
    "cicbims_2024_4_4_6_model_and_document_references",
    "cicbims_2024_4_4_8_revision",
    "devb_harmonisation_v3_federation_and_bim_model_naming",
    "devb_harmonisation_v3_appendix_viii_federation_strategy_diagrams_and_naming",
    "devb_harmonisation_v3_appendix_ix_sample_project_specific_codes_for_naming",
)

PLAYBOOK_NAMING_URL_PARTS = (
    "03_naming/2_cicbims_2024_命名規範結構",
    "03_naming/3_在_acc_配置_naming_standard",
    "03_naming/1_命名規範層級",
)


def _chunk_from_record(record: dict) -> RetrievedChunk:
    return RetrievedChunk(
        chunk_id=record["chunk_id"],
        title=record["title"],
        source_url=record["source_url"],
        source_file=record["source_file"],
        page_index=int(record["page_index"]),
        line_start=int(record["line_start"]),
        product=record["product"],
        chunk_index=int(record["chunk_index"]),
        chunk_count=int(record["chunk_count"]),
        token_count=int(record["token_count"]),
        text=record["text"],
        score=1.0,
        vector_similarity=0.99,
    )


def load_chunk_by_url_part(chunks_path: Path, url_part: str) -> RetrievedChunk | None:
    if not chunks_path.is_file():
        return None
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if url_part in record.get("source_url", ""):
                return _chunk_from_record(record)
    return None


def load_chunk_by_guid(chunks_path: Path, guid: str) -> RetrievedChunk | None:
    """按 Docs guid= 精确匹配，避免 Viewer_Settings_Files 命中 _PDF 变体。"""
    if not chunks_path.is_file() or not guid:
        return None
    needle = f"guid={guid}"
    with chunks_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            url = record.get("source_url", "")
            idx = url.find(needle)
            if idx < 0:
                continue
            end = idx + len(needle)
            if end < len(url) and url[end] not in "&?#":
                continue
            return _chunk_from_record(record)
    return None


def load_docs_by_guids(
    chunks_path: Path, guids: tuple[str, ...], limit: int = 2
) -> list[RetrievedChunk]:
    found: list[RetrievedChunk] = []
    seen: set[str] = set()
    for guid in guids:
        chunk = load_chunk_by_guid(chunks_path, guid)
        if chunk and chunk.chunk_id not in seen:
            found.append(chunk)
            seen.add(chunk.chunk_id)
        if len(found) >= limit:
            break
    return found


def prefer_docs_chunks(
    preferred: list[RetrievedChunk],
    retrieved: list[RetrievedChunk],
    *,
    limit: int,
) -> list[RetrievedChunk]:
    """优先保留 preferred GUID 页，再用检索结果补齐；不做无证据硬替换。"""
    if limit <= 0:
        return []
    out: list[RetrievedChunk] = []
    seen: set[str] = set()
    for chunk in preferred + retrieved:
        if chunk.chunk_id in seen:
            continue
        out.append(chunk)
        seen.add(chunk.chunk_id)
        if len(out) >= limit:
            break
    return out


def load_docs_folder_chunks(chunks_path: Path, limit: int = 2) -> list[RetrievedChunk]:
    """folder 类 hybrid 优先用 Files 工具操作页，而非泛化 About 页。"""
    order = (DOCS_FOLDER_GUID, DOCS_FILES_GUID, DOCS_NAMING_GUID)
    found: list[RetrievedChunk] = []
    seen: set[str] = set()
    for part in order:
        chunk = load_chunk_by_guid(chunks_path, part) or load_chunk_by_url_part(
            chunks_path, part
        )
        if chunk and chunk.chunk_id not in seen:
            found.append(chunk)
            seen.add(chunk.chunk_id)
        if len(found) >= limit:
            break
    return found


def load_docs_permissions_chunks(
    chunks_path: Path, limit: int = 2
) -> list[RetrievedChunk]:
    return load_docs_by_guids(
        chunks_path,
        (DOCS_PERMISSIONS_GUID, DOCS_PERMISSION_LEVELS_GUID),
        limit=limit,
    )


def load_docs_project_create_chunks(
    chunks_path: Path, limit: int = 2
) -> list[RetrievedChunk]:
    return load_docs_by_guids(
        chunks_path,
        (DOCS_PROJECT_CREATE_GUID, DOCS_PROJECT_MANAGE_GUID),
        limit=limit,
    )


def load_docs_project_template_chunks(
    chunks_path: Path, limit: int = 2
) -> list[RetrievedChunk]:
    return load_docs_by_guids(
        chunks_path,
        (DOCS_TEMPLATES_DOCS_GUID, DOCS_TEMPLATES_CREATE_GUID),
        limit=limit,
    )


def load_docs_workflow_chunks(
    chunks_path: Path, limit: int = 2
) -> list[RetrievedChunk]:
    return load_docs_by_guids(
        chunks_path,
        (DOCS_REVIEWS_CREATE_GUID, DOCS_REVIEWS_WORKFLOW_GUID),
        limit=limit,
    )


def prefer_docs_for_capability(
    capability: str | None,
    retrieved: list[RetrievedChunk],
    *,
    chunks_path: Path,
    limit: int,
) -> list[RetrievedChunk]:
    """弱能力：优先插入目标 GUID，保留检索结果作为第二来源。"""
    loaders = {
        "permissions": load_docs_permissions_chunks,
        "project_create": load_docs_project_create_chunks,
        "project_template": load_docs_project_template_chunks,
        "workflow": load_docs_workflow_chunks,
    }
    loader = loaders.get(capability or "")
    if loader is None:
        return retrieved
    preferred = loader(chunks_path, limit=limit)
    if not preferred:
        return retrieved
    return prefer_docs_chunks(preferred, retrieved, limit=limit)


def pin_folder_docs_in_merged(
    merged: MergedContexts,
    *,
    chunks_path: Path,
    docs_top_k: int = 2,
) -> tuple[MergedContexts, bool]:
    """folder 类 hybrid：若 Docs 未召回 Organize Files，硬换产品操作页。"""
    from rag.orchestrator.merge import merge_triple_contexts

    current_docs = [t for t in merged.tracked if t.track == "docs"]
    if current_docs and any(
        DOCS_FOLDER_GUID in t.chunk.source_url for t in current_docs
    ):
        return merged, False

    replacement = load_docs_folder_chunks(chunks_path, limit=docs_top_k)
    if not replacement:
        return merged, False

    industry = [t.chunk for t in merged.tracked if t.track == "hk_cde"]
    playbook = [t.chunk for t in merged.tracked if t.track == "playbook"]
    new_merged = merge_triple_contexts(
        docs_chunks=replacement,
        industry_chunks=industry,
        playbook_chunks=playbook,
        docs_top_k=len(replacement),
        industry_top_k=len(industry) or 0,
        playbook_top_k=len(playbook) or 0,
    )
    return new_merged, True


def load_docs_naming_chunks(chunks_path: Path, limit: int = 2) -> list[RetrievedChunk]:
    order = (DOCS_NAMING_GUID, DOCS_SETUP_NAMING_GUID, "Apply_Naming_Standard_To_Project")
    found: list[RetrievedChunk] = []
    seen: set[str] = set()
    for part in order:
        chunk = load_chunk_by_url_part(chunks_path, part)
        if chunk and chunk.chunk_id not in seen:
            found.append(chunk)
            seen.add(chunk.chunk_id)
        if len(found) >= limit:
            break
    return found


def load_hk_naming_chunk(chunks_path: Path) -> RetrievedChunk | None:
    fallback: RetrievedChunk | None = None
    for part in HK_NAMING_URL_PARTS:
        chunk = load_chunk_by_url_part(chunks_path, part)
        if not chunk:
            continue
        text_l = chunk.text.lower()
        if "naming" in text_l or "originator" in text_l or "container" in text_l:
            return chunk
        fallback = fallback or chunk
    return fallback


def load_playbook_naming_chunks(
    chunks_path: Path, limit: int = 1
) -> list[RetrievedChunk]:
    found: list[RetrievedChunk] = []
    for part in PLAYBOOK_NAMING_URL_PARTS:
        chunk = load_chunk_by_url_part(chunks_path, part)
        if chunk:
            found.append(chunk)
        if len(found) >= limit:
            break
    return found


def pin_naming_docs_in_merged(
    merged: MergedContexts,
    *,
    chunks_path: Path,
    docs_top_k: int = 2,
) -> tuple[MergedContexts, bool]:
    from rag.orchestrator.merge import merge_triple_contexts

    current_docs = [t for t in merged.tracked if t.track == "docs"]
    if current_docs and any(
        DOCS_NAMING_GUID in t.chunk.source_url
        or DOCS_SETUP_NAMING_GUID in t.chunk.source_url
        for t in current_docs
    ):
        return merged, False

    replacement = load_docs_naming_chunks(chunks_path, limit=docs_top_k)
    if not replacement:
        return merged, False

    industry = [t.chunk for t in merged.tracked if t.track == "hk_cde"]
    playbook = [t.chunk for t in merged.tracked if t.track == "playbook"]
    new_merged = merge_triple_contexts(
        docs_chunks=replacement,
        industry_chunks=industry,
        playbook_chunks=playbook,
        docs_top_k=len(replacement),
        industry_top_k=len(industry) or 0,
        playbook_top_k=len(playbook) or 0,
    )
    return new_merged, True


def load_docs_model_viewer_chunks(
    chunks_path: Path, limit: int = 2
) -> list[RetrievedChunk]:
    """model_viewer：优先 Model Browser，其次 Viewer Settings。"""
    order = (DOCS_MODEL_BROWSER_GUID, DOCS_VIEWER_SETTINGS_GUID)
    found: list[RetrievedChunk] = []
    seen: set[str] = set()
    for guid in order:
        chunk = load_chunk_by_guid(chunks_path, guid)
        if chunk and chunk.chunk_id not in seen:
            found.append(chunk)
            seen.add(chunk.chunk_id)
        if len(found) >= limit:
            break
    return found


def pin_model_viewer_docs_in_merged(
    merged: MergedContexts,
    *,
    chunks_path: Path,
    docs_top_k: int = 2,
) -> tuple[MergedContexts, bool]:
    from rag.orchestrator.merge import merge_triple_contexts

    current_docs = [t for t in merged.tracked if t.track == "docs"]
    if current_docs and any(
        DOCS_MODEL_BROWSER_GUID in t.chunk.source_url for t in current_docs
    ):
        return merged, False

    replacement = load_docs_model_viewer_chunks(chunks_path, limit=docs_top_k)
    if not replacement:
        return merged, False

    industry = [t.chunk for t in merged.tracked if t.track == "hk_cde"]
    playbook = [t.chunk for t in merged.tracked if t.track == "playbook"]
    new_merged = merge_triple_contexts(
        docs_chunks=replacement,
        industry_chunks=industry,
        playbook_chunks=playbook,
        docs_top_k=len(replacement),
        industry_top_k=len(industry) or 0,
        playbook_top_k=len(playbook) or 0,
    )
    return new_merged, True


def ensure_model_viewer_hybrid_merged(
    merged: MergedContexts,
    *,
    capability: str | None,
    docs_chunks_path: Path,
    docs_top_k: int = 2,
) -> tuple[MergedContexts, list[str]]:
    if capability != "model_viewer":
        return merged, []

    docs_pinned, did_docs = pin_model_viewer_docs_in_merged(
        merged,
        chunks_path=docs_chunks_path,
        docs_top_k=docs_top_k or 2,
    )
    if not did_docs:
        return merged, []
    return docs_pinned, [
        "[soft] model_viewer_docs_pin: prefer Model Browser / Viewer Settings"
    ]


def pin_naming_hk_in_merged(
    merged: MergedContexts,
    *,
    chunks_path: Path,
) -> tuple[MergedContexts, bool]:
    from rag.orchestrator.merge import merge_triple_contexts

    current = [t for t in merged.tracked if t.track == "hk_cde"]
    if current and any(
        any(part in t.chunk.source_url for part in HK_NAMING_URL_PARTS)
        for t in current
    ):
        return merged, False

    replacement = load_hk_naming_chunk(chunks_path)
    if replacement is None:
        return merged, False

    docs = [t.chunk for t in merged.tracked if t.track == "docs"]
    playbook = [t.chunk for t in merged.tracked if t.track == "playbook"]
    new_merged = merge_triple_contexts(
        docs_chunks=docs,
        industry_chunks=[replacement],
        playbook_chunks=playbook,
        docs_top_k=len(docs) or 0,
        industry_top_k=1,
        playbook_top_k=len(playbook) or 0,
    )
    return new_merged, True


def pin_naming_playbook_in_merged(
    merged: MergedContexts,
    *,
    chunks_path: Path,
) -> tuple[MergedContexts, bool]:
    from rag.orchestrator.merge import merge_triple_contexts

    current = [t for t in merged.tracked if t.track == "playbook"]
    if current and any("03_naming" in t.chunk.source_url for t in current):
        # 已有命名章但可能只命中配置段；若无结构段且有结构 chunk，可再换
        if any("命名規範結構" in t.chunk.source_url or "2_cicbims" in t.chunk.source_url for t in current):
            return merged, False

    replacement = load_playbook_naming_chunks(chunks_path, limit=1)
    if not replacement:
        return merged, False

    docs = [t.chunk for t in merged.tracked if t.track == "docs"]
    industry = [t.chunk for t in merged.tracked if t.track == "hk_cde"]
    new_merged = merge_triple_contexts(
        docs_chunks=docs,
        industry_chunks=industry,
        playbook_chunks=replacement,
        docs_top_k=len(docs) or 0,
        industry_top_k=len(industry) or 0,
        playbook_top_k=1,
    )
    return new_merged, True


def ensure_naming_hybrid_merged(
    merged: MergedContexts,
    *,
    capability: str | None,
    playbook_chunks_path: Path,
    docs_chunks_path: Path,
    industry_chunks_path: Path,
    docs_top_k: int = 2,
) -> tuple[MergedContexts, list[str]]:
    if capability != "naming":
        return merged, []

    warnings: list[str] = []
    pb_pinned, did_pb = pin_naming_playbook_in_merged(
        merged, chunks_path=playbook_chunks_path
    )
    if did_pb:
        merged = pb_pinned
        warnings.append("[soft] naming_playbook_pin: prefer CICBIMS structure section")

    hk_pinned, did_hk = pin_naming_hk_in_merged(
        merged, chunks_path=industry_chunks_path
    )
    if did_hk:
        merged = hk_pinned
        warnings.append("[soft] naming_hk_pin: prefer CIC/DEVB naming sections")

    docs_pinned, did_docs = pin_naming_docs_in_merged(
        merged,
        chunks_path=docs_chunks_path,
        docs_top_k=docs_top_k or 2,
    )
    if did_docs:
        merged = docs_pinned
        warnings.append(
            "[soft] naming_docs_pin: replaced weak docs with File Naming Standard"
        )

    return merged, warnings


def ensure_folder_hybrid_merged(
    merged: MergedContexts,
    *,
    question: str,
    capability: str | None,
    playbook_chunks_path: Path,
    docs_chunks_path: Path,
    docs_top_k: int = 2,
) -> tuple[MergedContexts, list[str]]:
    """folder 类 hybrid：检索/生成前统一硬钉 Playbook WIP + Docs Files 页。"""
    from rag.orchestrator.classify import is_folder_question

    if not is_folder_question(question, capability):
        return merged, []

    warnings: list[str] = []
    pinned, did_pin = pin_folder_playbook_in_merged(
        merged,
        chunks_path=playbook_chunks_path,
    )
    if did_pin:
        merged = pinned
        warnings.append(
            "[soft] playbook_pin: replaced concept chunk with WIP folder tree"
        )
    else:
        playbook_items = [t for t in merged.tracked if t.track == "playbook"]
        if playbook_items and playbook_chunk_needs_folder_pin(playbook_items[0].chunk):
            if not playbook_chunks_path.is_file():
                warnings.append(
                    "[hard] playbook_chunks_missing: "
                    f"未找到 {playbook_chunks_path}，请运行 "
                    "python scripts/ingest_playbook_acc_hk.py --rebuild"
                )
            else:
                warnings.append(
                    "[hard] playbook_pin_failed: Playbook 仍为概念段，"
                    f"请检查 {playbook_chunks_path} 是否含 2_wip_容器配置"
                )

    docs_pinned, did_docs = pin_folder_docs_in_merged(
        merged,
        chunks_path=docs_chunks_path,
        docs_top_k=docs_top_k or 2,
    )
    if did_docs:
        merged = docs_pinned
        warnings.append(
            "[soft] docs_pin: replaced weak docs with Organize Files / Files"
        )

    return merged, warnings


def playbook_chunk_is_concept(chunk: RetrievedChunk) -> bool:
    return CONCEPT_URL_MARKER in chunk.source_url
