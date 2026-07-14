#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autodesk 帮助文档（Revit、DOCS、COLLAB、BUILD 等）下载工具
SPA 站点，需用 Playwright 渲染后抓取目录与正文。默认每 100 页一个文件，输出为 <产品名>_help.md。
安装: pip install playwright && playwright install chromium
"""

import argparse
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("请先安装: pip install playwright && playwright install chromium", file=sys.stderr)
    sys.exit(1)


def get_site_base(url: str) -> str:
    parts = url.rstrip("/").split("/")
    if len(parts) >= 5:
        return "/".join(parts[:7])
    return url.split("?")[0].rstrip("/")


def get_product_name(url: str) -> str:
    parts = url.rstrip("/").replace("?", "/").split("/")
    try:
        i = parts.index("view")
        product = parts[i + 1]
        if i + 2 < len(parts) and parts[i + 2].isdigit():
            product = f"{product}_{parts[i + 2]}"
        return product
    except (ValueError, IndexError):
        return "help"


def get_output_dir_and_name(url: str) -> str:
    product = get_product_name(url)
    out_dir = Path(__file__).resolve().parent / "output" / product
    out_dir.mkdir(parents=True, exist_ok=True)
    return str(out_dir)


def run_autodesk_help_crawler(
    start_url: str,
    output_path: str,
    output_format: str = "markdown",
    max_pages: int | None = None,
    pages_per_file: int = 100,
    wait_content: float = 1.5,
    headless: bool = True,
) -> None:
    site_base = get_site_base(start_url)
    if "?" in site_base:
        site_base = site_base.split("?")[0]

    all_links = []
    seen_urls = set()
    collected = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        def collect_links_from_page():
            return page.evaluate(
                """() => {
                    const base = window.location.origin + window.location.pathname;
                    const hrefs = new Set();
                    document.querySelectorAll('a[href]').forEach(a => {
                        let h = a.href;
                        if (h && (h.includes('guid=') || h.includes(base)) && h.startsWith('https://help.autodesk.com/')) {
                            hrefs.add(h.split('#')[0]);
                        }
                    });
                    return Array.from(hrefs);
                }"""
            )

        print("正在加载首页并收集目录链接...", file=sys.stderr)
        page.goto(start_url, wait_until="networkidle", timeout=60000)
        time.sleep(wait_content)

        max_expand_rounds = 80
        last_link_count = 0
        stable_rounds = 0

        for round_num in range(max_expand_rounds):
            for u in collect_links_from_page():
                if u not in seen_urls and site_base in u:
                    seen_urls.add(u)
                    all_links.append(u)
            page.evaluate(
                """() => {
                    const sidebar = document.querySelector('nav') || document.querySelector('[role="navigation"]') || document.querySelector('[class*="sidebar"]') || document.querySelector('[class*="toc"]') || document.querySelector('aside');
                    if (sidebar) { sidebar.scrollTop = sidebar.scrollHeight; setTimeout(() => { sidebar.scrollTop = 0; }, 100); }
                }"""
            )
            time.sleep(0)
            clicked = page.evaluate(
                """() => {
                    const selectors = ['[aria-expanded="false"]', 'button[aria-expanded="false"]', '[class*="expand"]', '[class*="tree"] [aria-expanded="false"]'];
                    const seen = new Set();
                    let clicked = 0;
                    for (const sel of selectors) {
                        document.querySelectorAll(sel).forEach(el => {
                            const key = (el.getBoundingClientRect ? el.getBoundingClientRect().top + ',' + el.textContent.slice(0,30) : el.innerHTML);
                            if (seen.has(key)) return;
                            seen.add(key);
                            try { el.scrollIntoView({ block: 'nearest', behavior: 'instant' }); el.click(); clicked++; } catch (e) {}
                        });
                    }
                    return clicked;
                }"""
            )
            time.sleep(0)
            for u in collect_links_from_page():
                if u not in seen_urls and site_base in u:
                    seen_urls.add(u)
                    all_links.append(u)
            current_count = len(all_links)
            if current_count == last_link_count:
                stable_rounds += 1
                if stable_rounds >= 3:
                    print(f"  TOC 已完全展开（共 {current_count} 个链接）", file=sys.stderr)
                    break
            else:
                stable_rounds = 0
            last_link_count = current_count
            if clicked == 0 and stable_rounds >= 1:
                break
            if round_num % 10 == 0 and round_num > 0:
                print(f"  展开中... 已发现 {current_count} 个链接", file=sys.stderr)

        for u in collect_links_from_page():
            if u not in seen_urls and site_base in u:
                seen_urls.add(u)
                all_links.append(u)

        to_fetch = all_links if max_pages is None else all_links[:max_pages]
        print(f"共发现 {len(all_links)} 个链接，开始抓取正文（共 {len(to_fetch)} 页）...", file=sys.stderr)

        for i, url in enumerate(to_fetch):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                if wait_content > 0:
                    time.sleep(wait_content)
                data = page.evaluate(
                    """() => {
                        const titleEl = document.querySelector('h1') || document.querySelector('[class*="title"]') || document.querySelector('title');
                        const title = titleEl ? titleEl.innerText.trim() : document.title || '';
                        const main = document.querySelector('main') || document.querySelector('article') || document.querySelector('[role="main"]') || document.querySelector('.content') || document.querySelector('#content') || document.body;
                        return { title, html: main ? main.innerHTML : '' };
                    }"""
                )
                title = (data.get("title") or "Untitled").strip()
                html = data.get("html") or ""
                if output_format == "markdown":
                    from bs4 import BeautifulSoup
                    s = BeautifulSoup(html, "html.parser")
                    for tag in s.find_all(["script", "style"]):
                        tag.decompose()
                    body = s.get_text(separator="\n", strip=True)
                    part = f"\n\n---\n\n# {title}\n\nSource: {url}\n\n{body}\n"
                else:
                    part = f'\n\n<hr>\n<article data-url="{url}">\n<h1>{title}</h1>\n{html}\n</article>\n'
                collected.append(part)
                print(f"  [{i+1}/{len(to_fetch)}] {title[:50]}...", file=sys.stderr)
            except Exception as e:
                print(f"  Skip {url}: {e}", file=sys.stderr)

        browser.close()

    if output_format == "html":
        wrapper_start = '<!DOCTYPE html>\n<html><head><meta charset="utf-8"><title>Autodesk Help Export</title></head><body>'
        wrapper_end = "</body></html>"
    else:
        wrapper_start = wrapper_end = ""

    out_path = Path(output_path)
    total = len(collected)
    if pages_per_file <= 0 or total <= pages_per_file:
        doc = wrapper_start + ("".join(collected) if output_format == "html" else "\n".join(collected)) + wrapper_end
        out_path.write_text(doc, encoding="utf-8")
        print(f"已保存到 {output_path}，共 {total} 页", file=sys.stderr)
    else:
        num_files = (total + pages_per_file - 1) // pages_per_file
        for idx in range(num_files):
            start = idx * pages_per_file
            end = min(start + pages_per_file, total)
            chunk = collected[start:end]
            chunk_path = out_path.parent / f"{out_path.stem}_{idx + 1:03d}{out_path.suffix}"
            doc = wrapper_start + ("".join(chunk) if output_format == "html" else "\n".join(chunk)) + wrapper_end
            chunk_path.write_text(doc, encoding="utf-8")
            print(f"  已保存 {chunk_path.name}（第 {start + 1}-{end} 页）", file=sys.stderr)
        print(f"共 {total} 页，已拆分到 {num_files} 个文件", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Autodesk 帮助文档下载（Playwright）")
    parser.add_argument("url", nargs="?", default="https://help.autodesk.com/view/RVT/2022/ENU/", help="帮助首页 URL")
    parser.add_argument("-o", "--output", default=None, help="输出文件（默认 output/<产品名>/<产品名>_help.md）")
    parser.add_argument("-f", "--format", choices=["markdown", "html"], default="markdown")
    parser.add_argument("-n", "--max-pages", type=int, default=None, help="最多抓取页数（默认不限制）")
    parser.add_argument("-p", "--pages-per-file", type=int, default=100, help="每多少页存为一个文件（默认 100，0 表示不拆分）")
    parser.add_argument("--wait", type=float, default=1.5, help="每页加载后等待秒数（默认 1.5）")
    parser.add_argument("--show-browser", "-B", action="store_true", help="显示浏览器窗口")
    args = parser.parse_args()

    if args.output is None:
        out_dir = get_output_dir_and_name(args.url)
        product = get_product_name(args.url)
        ext = "html" if args.format == "html" else "md"
        args.output = str(Path(out_dir) / f"{product}_help.{ext}")

    run_autodesk_help_crawler(
        start_url=args.url,
        output_path=args.output,
        output_format=args.format,
        max_pages=args.max_pages,
        pages_per_file=args.pages_per_file,
        wait_content=args.wait,
        headless=not args.show_browser,
    )


if __name__ == "__main__":
    main()
