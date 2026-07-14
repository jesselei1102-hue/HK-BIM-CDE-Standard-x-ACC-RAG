"""导出 DOCS 语料页面索引、主题聚类与 how-to 页标记。

用法：
    python scripts/research_corpus.py
    python scripts/research_corpus.py --output-dir knowledge/research
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.chunking import estimate_tokens
from rag.ingestion import Document, load_corpus

TOKEN_RE = re.compile(r"[\w\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+", re.UNICODE)

TOPIC_RULES: list[tuple[str, list[str]]] = [
    ("permissions", ["permission", "folder permission", "access", "权限"]),
    ("reviews", ["review", "approval", "workflow", "审阅", "审批"]),
    ("transmittals", ["transmittal", "transmit", "传送", "附函"]),
    ("files_formats", ["supported", "viewable", "file format", "格式", "upload"]),
    ("limitations", ["limitation", "maximum", "限制"]),
    ("markups", ["markup", "标记"]),
    ("sharing", ["share", "public link", "分享", "公开"]),
    ("upload", ["upload", "上传"]),
    ("naming", ["naming standard", "命名"]),
    ("sync", ["sync", "同步", "desktop connector"]),
    ("admin", ["administrator", "activity log", "template", "管理"]),
    ("insight", ["insight", "dashboard", "report"]),
    ("issues", ["issue", "问题"]),
    ("packages", ["package", "handover", "包"]),
    ("mobile", ["mobile", "ios", "android", "移动"]),
]

HOW_TO_PATTERNS = re.compile(
    r"\b(how to|create|manage|set up|configure|upload|export|share|submit)\b",
    re.IGNORECASE,
)
OVERVIEW_PATTERNS = re.compile(
    r"\b(about|overview|what is|introduction|system requirements)\b",
    re.IGNORECASE,
)
LIMITATION_PATTERNS = re.compile(
    r"\b(limitation|limitations|maximum|supported browsers)\b",
    re.IGNORECASE,
)


def extract_guid(source_url: str) -> str:
    query = parse_qs(urlparse(source_url).query)
    guid = query.get("guid", [""])[0]
    return guid or source_url.rsplit("/", 1)[-1]


def first_summary(text: str, max_chars: int = 240) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    body = [line for line in lines if not line.startswith("#")]
    summary = " ".join(body[:3])
    if len(summary) > max_chars:
        return summary[: max_chars - 3] + "..."
    return summary


def classify_page_type(title: str, text: str) -> str:
    combined = f"{title}\n{text[:800]}"
    if LIMITATION_PATTERNS.search(combined):
        return "limitations"
    if HOW_TO_PATTERNS.search(title) or HOW_TO_PATTERNS.search(text[:400]):
        return "how_to"
    if OVERVIEW_PATTERNS.search(title):
        return "overview"
    return "reference"


def classify_topics(title: str, text: str) -> list[str]:
    combined = f"{title} {text[:600]}".lower()
    topics: list[str] = []
    for topic, keywords in TOPIC_RULES:
        if any(keyword.lower() in combined for keyword in keywords):
            topics.append(topic)
    return topics or ["general"]


def build_page_index(documents: list[Document]) -> list[dict]:
    rows: list[dict] = []
    for doc in documents:
        token_count = estimate_tokens(doc.text)
        rows.append(
            {
                "title": doc.title,
                "guid": extract_guid(doc.source_url),
                "source_url": doc.source_url,
                "source_file": doc.source_file,
                "line_start": doc.line_start,
                "page_index": doc.page_index,
                "token_count": token_count,
                "summary": first_summary(doc.text),
                "page_type": classify_page_type(doc.title, doc.text),
                "topics": classify_topics(doc.title, doc.text),
                "evidence": f"{doc.source_file}:{doc.line_start}",
            }
        )
    return rows


def build_topic_clusters(pages: list[dict]) -> dict:
    clusters: dict[str, dict] = defaultdict(lambda: {"pages": [], "how_to_pages": []})
    for page in pages:
        for topic in page["topics"]:
            clusters[topic]["pages"].append(
                {
                    "title": page["title"],
                    "guid": page["guid"],
                    "source_url": page["source_url"],
                    "page_type": page["page_type"],
                }
            )
            if page["page_type"] == "how_to":
                clusters[topic]["how_to_pages"].append(
                    {
                        "title": page["title"],
                        "guid": page["guid"],
                        "source_url": page["source_url"],
                    }
                )

    result: dict[str, dict] = {}
    for topic, data in sorted(clusters.items()):
        how_tos = data["how_to_pages"]
        representative = how_tos[0] if how_tos else (data["pages"][0] if data["pages"] else None)
        result[topic] = {
            "page_count": len(data["pages"]),
            "how_to_count": len(how_tos),
            "representative": representative,
            "how_to_pages": how_tos[:10],
            "sample_titles": [page["title"] for page in data["pages"][:8]],
        }
    return result


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="导出 DOCS 语料研究索引")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "knowledge" / "research",
        help="研究产物输出目录",
    )
    args = parser.parse_args()

    report = load_corpus()
    pages = build_page_index(report.documents)
    clusters = build_topic_clusters(pages)

    output_dir = args.output_dir
    pages_path = output_dir / "pages_index.jsonl"
    clusters_path = output_dir / "topic_clusters.json"

    write_jsonl(pages_path, pages)
    clusters_path.write_text(
        json.dumps(clusters, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    how_to_count = sum(1 for page in pages if page["page_type"] == "how_to")
    print(f"页面索引：{len(pages)} 条 → {pages_path}")
    print(f"主题聚类：{len(clusters)} 个主题 → {clusters_path}")
    print(f"  how-to 页：{how_to_count}")
    print(f"  overview 页：{sum(1 for p in pages if p['page_type'] == 'overview')}")
    print(f"  limitations 页：{sum(1 for p in pages if p['page_type'] == 'limitations')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
