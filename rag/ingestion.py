"""解析并清洗 Autodesk Docs Markdown 语料。

本模块只读取源文件，不修改 Markdown，也不生成向量。可先运行下面的
命令检查语料质量：

    python -m rag.ingestion
"""

from __future__ import annotations

import argparse
import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .config import CorpusConfig, get_config


PAGE_START_RE = re.compile(
    r"(?m)^---[ \t]*\r?\n(?:[ \t]*\r?\n)+(?=# )"
)
SOURCE_RE = re.compile(r"^Source:\s*(https?://\S+)\s*$")
SHARE_BLOCK = ("Share", "Email", "Facebook", "Twitter", "LinkedIn")
FOOTER_MARKERS = ("Parent page:", "Pages in this section", "Get Social")
PLACEHOLDER_TITLES = {"Help", "Untitled"}


@dataclass(frozen=True)
class Document:
    title: str
    source_url: str
    text: str
    source_file: str
    page_index: int
    line_start: int
    product: str
    content_hash: str


@dataclass(frozen=True)
class RejectedPage:
    source_file: str
    page_index: int
    line_start: int
    title: str
    source_url: str
    reason: str


@dataclass
class IngestionReport:
    scanned_files: int = 0
    total_pages: int = 0
    accepted_pages: int = 0
    documents: list[Document] = field(default_factory=list)
    rejected: list[RejectedPage] = field(default_factory=list)

    @property
    def rejection_reasons(self) -> Counter[str]:
        return Counter(page.reason for page in self.rejected)


@dataclass(frozen=True)
class _RawPage:
    content: str
    page_index: int
    line_start: int


def _trim_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def _split_pages(markdown: str) -> list[_RawPage]:
    matches = list(PAGE_START_RE.finditer(markdown))
    pages: list[_RawPage] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        content = markdown[match.end() : end]
        line_start = markdown.count("\n", 0, match.end()) + 1
        pages.append(_RawPage(content, index + 1, line_start))
    return pages


def _title_from_url(source_url: str, fallback: str) -> str:
    query = parse_qs(urlparse(source_url).query)
    guid_values = query.get("guid")
    if not guid_values:
        return fallback
    guid = guid_values[0]
    if guid.startswith("topicid="):
        guid = guid.removeprefix("topicid=")
    return re.sub(r"[_-]+", " ", guid).strip() or fallback


def _clean_body(lines: list[str], title: str) -> str:
    lines = _trim_blank_lines(lines)

    if tuple(line.strip() for line in lines[:5]) == SHARE_BLOCK:
        lines = _trim_blank_lines(lines[5:])

    if lines and lines[0].strip() == title:
        lines = _trim_blank_lines(lines[1:])

    footer_indexes = [
        index
        for index, line in enumerate(lines)
        if line.strip() in FOOTER_MARKERS
    ]
    if footer_indexes:
        lines = _trim_blank_lines(lines[: min(footer_indexes)])

    text = "\n".join(line.rstrip() for line in lines).strip()
    return re.sub(r"\n{3,}", "\n\n", text)


def _reject(
    raw: _RawPage,
    source_file: Path,
    reason: str,
    title: str = "",
    url: str = "",
) -> RejectedPage:
    return RejectedPage(
        source_file=source_file.name,
        page_index=raw.page_index,
        line_start=raw.line_start,
        title=title,
        source_url=url,
        reason=reason,
    )


def _parse_page(
    raw: _RawPage,
    source_file: Path,
    product: str,
) -> Document | RejectedPage:
    lines = _trim_blank_lines(raw.content.splitlines())
    if not lines or not lines[0].startswith("# "):
        return _reject(raw, source_file, "missing_title")

    title = lines[0][2:].strip()
    source_index = next(
        (index for index, line in enumerate(lines[:10]) if SOURCE_RE.match(line)),
        None,
    )
    if source_index is None:
        return _reject(raw, source_file, "missing_source", title=title)

    source_match = SOURCE_RE.match(lines[source_index])
    assert source_match is not None
    source_url = source_match.group(1)
    body = _clean_body(lines[source_index + 1 :], title)

    if not body:
        return _reject(
            raw,
            source_file,
            "empty_body",
            title=title,
            url=source_url,
        )

    if not title or title in PLACEHOLDER_TITLES:
        title = _title_from_url(source_url, title or "Untitled")

    return Document(
        title=title,
        source_url=source_url,
        text=body,
        source_file=source_file.name,
        page_index=raw.page_index,
        line_start=raw.line_start,
        product=product,
        content_hash=hashlib.sha256(body.encode("utf-8")).hexdigest(),
    )


def load_corpus(config: CorpusConfig | None = None) -> IngestionReport:
    """读取配置范围内的全部 Markdown，返回文档与质量报告。"""

    corpus = config or get_config().corpus
    report = IngestionReport()
    seen_urls: set[str] = set()

    for source_file in sorted(corpus.source_dir.glob(corpus.file_glob)):
        report.scanned_files += 1
        markdown = source_file.read_text(encoding="utf-8")
        raw_pages = _split_pages(markdown)
        report.total_pages += len(raw_pages)

        for raw in raw_pages:
            parsed = _parse_page(raw, source_file, corpus.product)
            if isinstance(parsed, RejectedPage):
                report.rejected.append(parsed)
                continue
            if parsed.source_url in seen_urls:
                report.rejected.append(
                    _reject(
                        raw,
                        source_file,
                        "duplicate_source",
                        title=parsed.title,
                        url=parsed.source_url,
                    )
                )
                continue
            seen_urls.add(parsed.source_url)
            report.documents.append(parsed)

    report.accepted_pages = len(report.documents)
    return report


def _print_report(report: IngestionReport) -> None:
    print("DOCS Markdown 检查")
    print(f"  文件：{report.scanned_files}")
    print(f"  页面：{report.total_pages}")
    print(f"  可索引：{report.accepted_pages}")
    print(f"  已跳过：{len(report.rejected)}")
    for reason, count in sorted(report.rejection_reasons.items()):
        print(f"    - {reason}: {count}")
    if report.rejected:
        print("\n跳过页面：")
        for page in report.rejected:
            location = f"{page.source_file}:{page.line_start}"
            label = page.title or "(无标题)"
            print(f"  - {location} [{page.reason}] {label} {page.source_url}")


def export_cleaned_markdown(report: IngestionReport, output_path: Path) -> None:
    """导出便于人工检查的清洗结果，不修改原始 Markdown。"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sections = []
    for document in report.documents:
        origin = f"{document.source_file}:{document.line_start}"
        sections.append(
            "\n".join(
                (
                    "---",
                    "",
                    f"# {document.title}",
                    "",
                    f"Source: {document.source_url}",
                    f"Original: {origin}",
                    "",
                    document.text,
                )
            )
        )
    output_path.write_text("\n\n".join(sections) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="检查并清洗 DOCS Markdown")
    parser.add_argument(
        "--export",
        type=Path,
        help="将清洗后的有效页面导出为一个 Markdown 文件",
    )
    args = parser.parse_args()

    report = load_corpus()
    _print_report(report)
    if args.export:
        export_cleaned_markdown(report, args.export)
        print(f"\n清洗结果已导出：{args.export.resolve()}")
    return 0 if report.accepted_pages else 1


if __name__ == "__main__":
    raise SystemExit(main())
