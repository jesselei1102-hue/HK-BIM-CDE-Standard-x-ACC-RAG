#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
帮助文档整站下载工具
将指定帮助文档网站的所有页面抓取并合并为一个完整文件（Markdown 或 HTML）。
支持传统 HTML 站点；对 SPA（如 Autodesk Help）需配合 Playwright 使用。
"""

import argparse
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# 默认请求头，模拟浏览器
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def get_site_name(url: str) -> str:
    """从 URL 提取站点名（用于 output/<name>/<name>_help），用域名生成 slug。"""
    parsed = urlparse(url)
    name = (parsed.netloc or "site").split(":")[0].replace(".", "_").strip("_")
    return name or "site"


def get_output_dir_and_path(url: str, output_format: str) -> tuple[str, str]:
    """返回 (output_dir, output_path)，并创建目录。"""
    name = get_site_name(url)
    out_dir = Path(__file__).resolve().parent / "output" / name
    out_dir.mkdir(parents=True, exist_ok=True)
    ext = "html" if output_format == "html" else "md"
    output_path = str(out_dir / f"{name}_help.{ext}")
    return str(out_dir), output_path


def normalize_url(base: str, link: str, site_base: str) -> str | None:
    """将相对链接转为绝对 URL，并限制在同一站点内。"""
    if not link or link.startswith("#") or link.lower().startswith("javascript:"):
        return None
    full = urljoin(base, link)
    parsed = urlparse(full)
    if parsed.fragment:
        full = full.split("#")[0]
    if not full.startswith(site_base):
        return None
    return full.rstrip("/") or full


def same_domain(url: str, site_base: str) -> bool:
    """判断 url 是否属于 site_base 同站。"""
    return url.startswith(site_base)


def extract_links(soup: BeautifulSoup, page_url: str, site_base: str) -> list[str]:
    """从页面中提取同站内的 a[href] 链接。"""
    seen = set()
    out = []
    for a in soup.find_all("a", href=True):
        href = a.get("href", "").strip()
        u = normalize_url(page_url, href, site_base)
        if u and u not in seen and same_domain(u, site_base):
            seen.add(u)
            out.append(u)
    return out


def extract_main_content(soup: BeautifulSoup, url: str) -> tuple[str, str]:
    """
    从页面提取主内容区域和标题。
    优先使用 main, article, [role="main"], .content 等，否则用 body。
    返回 (title, html_content)。
    """
    title = ""
    if soup.title:
        title = soup.title.get_text(strip=True)
    for tag in soup.find_all(["h1", "h2"]):
        t = tag.get_text(strip=True)
        if t and not title:
            title = t
            break

    content = None
    for selector in ['main', 'article', '[role="main"]', '.content', '.main-content', '#content', '.help-content']:
        content = soup.select_one(selector)
        if content:
            break
    if content is None:
        content = soup.find("body") or soup

    # 移除 script, style, nav 等
    for tag in content.find_all(["script", "style", "nav", "header", "footer", "aside", "iframe"]):
        tag.decompose()
    html = str(content)
    return title, html


def html_to_markdown_basic(html: str) -> str:
    """将 HTML 转为简易 Markdown（仅处理常见标签）。"""
    soup = BeautifulSoup(html, "html.parser")
    lines = []

    def text(elem):
        if elem is None:
            return ""
        return elem.get_text(separator=" ", strip=True)

    for node in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li", "pre", "code", "blockquote", "table", "tr", "td", "th"]):
        name = node.name
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            lines.append("\n" + "#" * level + " " + text(node) + "\n")
        elif name == "p":
            lines.append(text(node) + "\n\n")
        elif name == "li":
            lines.append("- " + text(node) + "\n")
        elif name == "pre":
            lines.append("\n```\n" + text(node) + "\n```\n\n")
        elif name == "code" and node.parent and node.parent.name != "pre":
            lines.append("`" + text(node) + "`")
        elif name == "blockquote":
            for line in text(node).split("\n"):
                lines.append("> " + line + "\n")
        elif name == "tr":
            row = [text(c) for c in node.find_all(["td", "th"])]
            if row:
                lines.append("| " + " | ".join(row) + " |\n")
        elif name == "th" and not node.find_previous_sibling("th"):
            pass  # 表头在 tr 里一起处理
    if not lines:
        lines.append(BeautifulSoup(html, "html.parser").get_text(separator="\n", strip=True))
    return "\n".join(lines).strip()


def fetch_page(session: requests.Session, url: str, timeout: int = 30) -> tuple[int, str]:
    """请求页面，返回 (status_code, text)。"""
    try:
        r = session.get(url, timeout=timeout)
        return r.status_code, r.text
    except Exception as e:
        return -1, str(e)


def crawl(
    start_url: str,
    site_base: str | None = None,
    max_pages: int | None = None,
    delay: float = 0.5,
    output_format: str = "markdown",
    output_path: str | None = None,
    pages_per_file: int = 100,
) -> str:
    """
    从 start_url 开始爬取同站页面，合并为一个或多个文档。
    site_base: 只爬取该前缀下的 URL，默认用 start_url 的 origin。
    max_pages: None 表示不限制页数；pages_per_file>0 时每若干页存一个文件。
    """
    parsed = urlparse(start_url)
    base = site_base or f"{parsed.scheme}://{parsed.netloc}"
    if not base.endswith("/"):
        base = base + "/"
    if not start_url.startswith(base):
        base = start_url.rsplit("/", 1)[0] + "/"

    limit = max_pages if max_pages is not None else 999999
    to_visit = [start_url]
    visited = set()
    session = requests.Session()
    session.headers.update(DEFAULT_HEADERS)

    all_parts = []
    pages_done = 0

    while to_visit and pages_done < limit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)

        status, text = fetch_page(session, url)
        if status != 200:
            continue

        soup = BeautifulSoup(text, "html.parser")
        title, content_html = extract_main_content(soup, url)
        new_links = extract_links(soup, url, base)
        for u in new_links:
            if u not in visited and u not in to_visit:
                to_visit.append(u)

        if output_format == "markdown":
            body = html_to_markdown_basic(content_html)
            part = f"\n\n---\n\n# {title}\n\nSource: {url}\n\n{body}\n"
        else:
            part = f"\n\n<hr>\n<article data-url=\"{url}\">\n<h1>{title}</h1>\n{content_html}\n</article>\n"
        all_parts.append(part)
        pages_done += 1
        print(f"  [{pages_done}] {url[:80]}...", file=sys.stderr)
        time.sleep(delay)

    total = len(all_parts)
    if output_format == "html":
        wrapper_start = "<!DOCTYPE html>\n<html><head><meta charset=\"utf-8\"><title>Help Export</title></head><body>"
        wrapper_end = "</body></html>"
    else:
        wrapper_start = wrapper_end = ""

    if output_path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if pages_per_file <= 0 or total <= pages_per_file:
            doc = wrapper_start + "".join(all_parts) + wrapper_end
            out_path.write_text(doc, encoding="utf-8")
            print(f"已保存到 {output_path}，共 {total} 页", file=sys.stderr)
        else:
            num_files = (total + pages_per_file - 1) // pages_per_file
            for idx in range(num_files):
                start = idx * pages_per_file
                end = min(start + pages_per_file, total)
                chunk = all_parts[start:end]
                chunk_path = out_path.parent / f"{out_path.stem}_{idx + 1:03d}{out_path.suffix}"
                doc = wrapper_start + "".join(chunk) + wrapper_end
                chunk_path.write_text(doc, encoding="utf-8")
                print(f"  已保存 {chunk_path.name}（第 {start + 1}-{end} 页）", file=sys.stderr)
            print(f"共 {total} 页，已拆分到 {num_files} 个文件", file=sys.stderr)
    return wrapper_start + "".join(all_parts) + wrapper_end


def main():
    parser = argparse.ArgumentParser(description="帮助文档整站下载为单个或多个文件")
    parser.add_argument("url", help="起始 URL，例如 https://example.com/docs/")
    parser.add_argument("-o", "--output", default=None, help="输出文件路径（默认 output/<站点名>/<站点名>_help.md）")
    parser.add_argument("-f", "--format", choices=["markdown", "html"], default="markdown", help="输出格式")
    parser.add_argument("-n", "--max-pages", type=int, default=None, help="最多抓取页面数（默认不限制，发现多少爬多少）")
    parser.add_argument("-p", "--pages-per-file", type=int, default=100, help="每多少页存为一个文件（默认 100，0 表示不拆分）")
    parser.add_argument("-d", "--delay", type=float, default=0.5, help="请求间隔（秒）")
    parser.add_argument("--base", default=None, help="限制爬取范围（同站 URL 前缀，建议对大型站如 learn.microsoft.com 指定）")
    args = parser.parse_args()

    if args.output is None:
        _, args.output = get_output_dir_and_path(args.url, args.format)

    crawl(
        start_url=args.url,
        site_base=args.base,
        max_pages=args.max_pages,
        delay=args.delay,
        output_format=args.format,
        output_path=args.output,
        pages_per_file=args.pages_per_file,
    )


if __name__ == "__main__":
    main()
