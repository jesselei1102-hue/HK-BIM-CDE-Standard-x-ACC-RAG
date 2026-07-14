"""合并 pages_index、glossary、retrieval_gaps 生成 KB 候选条目。

用法：
    python scripts/merge_kb_candidates.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

RESEARCH_DIR = PROJECT_ROOT / "knowledge" / "research"

STOP_WORDS = {
    "a", "an", "the", "and", "or", "to", "of", "in", "on", "for", "with",
    "how", "do", "i", "is", "are", "your", "you", "can", "from", "by",
}


def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def title_aliases(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z]+", title.lower())
    filtered = [word for word in words if word not in STOP_WORDS and len(word) > 2]
    aliases: list[str] = []
    if len(filtered) >= 2:
        aliases.append(" ".join(filtered[:3]))
    if filtered:
        aliases.append(filtered[0])
    return aliases


def merge_candidates() -> list[dict]:
    pages = read_jsonl(RESEARCH_DIR / "pages_index.jsonl")
    glossary = read_jsonl(RESEARCH_DIR / "industry_glossary.jsonl")
    gaps = read_jsonl(RESEARCH_DIR / "retrieval_gaps.jsonl")

    pages_by_guid = {page["guid"]: page for page in pages}
    candidates: dict[str, dict] = {}

    def add_candidate(
        entry_id: str,
        *,
        topic: str,
        aliases: list[str],
        canonical_query_zh: str,
        canonical_query_en: str,
        guid: str,
        entry_type: str,
        evidence: str,
        external_sources: list[str],
        source: str,
    ) -> None:
        page = pages_by_guid.get(guid)
        if not page:
            return
        key = entry_id
        if key in candidates:
            existing = candidates[key]
            existing["aliases"] = sorted(set(existing["aliases"] + aliases))
            existing["sources"] = sorted(set(existing.get("sources", []) + [source]))
            return
        candidates[key] = {
            "id": entry_id,
            "topic": topic,
            "aliases": sorted(set(alias for alias in aliases if alias)),
            "canonical_query_zh": canonical_query_zh,
            "canonical_query_en": canonical_query_en,
            "target_title": page["title"],
            "target_url": page["source_url"],
            "target_guid": guid,
            "entry_type": entry_type,
            "evidence": evidence or page.get("evidence", ""),
            "external_sources": external_sources,
            "status": "candidate",
            "sources": [source],
        }

    for term in glossary:
        if term.get("alignment_status") != "matched":
            continue
        guid = term["local_target_guid"]
        aliases = [term["term_zh"], term["term_en"], *term.get("aliases", [])]
        add_candidate(
            f"{term['topic']}_{guid.lower()}",
            topic=term["topic"],
            aliases=aliases,
            canonical_query_zh=f"如何{term['term_zh']}" if term["term_zh"] else "",
            canonical_query_en=f"How do I {term['term_en']}" if term.get("term_en") else "",
            guid=guid,
            entry_type="how_to",
            evidence=term.get("evidence", ""),
            external_sources=term.get("external_sources", []),
            source="glossary",
        )

    for page in pages:
        if page["page_type"] != "how_to":
            continue
        guid = page["guid"]
        entry_id = re.sub(r"[^a-z0-9]+", "_", guid.lower()).strip("_")
        add_candidate(
            entry_id,
            topic=page["topics"][0],
            aliases=title_aliases(page["title"]),
            canonical_query_zh="",
            canonical_query_en=f"How do I {page['title'].lower()}",
            guid=guid,
            entry_type="how_to",
            evidence=page.get("evidence", ""),
            external_sources=[],
            source="pages_index",
        )

    for gap in gaps:
        if not gap.get("needs_kb"):
            continue
        query = gap["query"]
        if len(query) > 16:
            continue
        # 短句失败案例暂不自动挂目标页，保留为研究记录供人工验收
        candidates.setdefault(
            f"gap_{hash(query) & 0xFFFFFFFF:08x}",
            {
                "id": f"gap_{hash(query) & 0xFFFFFFFF:08x}",
                "topic": "unresolved",
                "aliases": [query],
                "canonical_query_zh": query if any("\u4e00" <= ch <= "\u9fff" for ch in query) else "",
                "canonical_query_en": query,
                "target_title": "",
                "target_url": "",
                "target_guid": "",
                "entry_type": "gap",
                "evidence": "",
                "external_sources": [],
                "status": "candidate",
                "sources": ["retrieval_gaps"],
                "gap_reasons": gap.get("gap_reasons", []),
            },
        )

    return list(candidates.values())


def main() -> int:
    rows = merge_candidates()
    output = RESEARCH_DIR / "candidate_entries.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    resolved = sum(1 for row in rows if row.get("target_guid"))
    print(f"候选条目：{len(rows)} 条（含目标页 {resolved} 条）→ {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
