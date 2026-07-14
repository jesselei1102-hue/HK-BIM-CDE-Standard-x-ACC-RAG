"""回答语言与 hybrid 输出润色。"""

from __future__ import annotations

import re

AnswerLanguage = str  # auto | en | zh-Hans | zh-Hant

_CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
_TRAD_HINTS = re.compile(r"設置|資料|無法|確認|實施|對齊|產品|標準|文件夾|權限|審批|發布|歸檔|賬戶")

_LEAD_CANNOT_RE = re.compile(
    r"^(?:根据现有资料无法确认|根據現有資料無法確認)"
    r"(?:[（(][^）)]*[）)])?\s*",
    re.I,
)
_CITATION_RE = re.compile(r"\[\d+\]")


def resolve_answer_language(question: str, lang: str | None) -> AnswerLanguage:
    choice = (lang or "auto").strip()
    if choice in {"en", "zh-Hans", "zh-Hant"}:
        return choice
    text = question.strip()
    if not text:
        return "zh-Hans"
    cjk = len(_CJK_RE.findall(text))
    if cjk / max(len(text), 1) < 0.08:
        return "en"
    if _TRAD_HINTS.search(text):
        return "zh-Hant"
    return "zh-Hans"


def language_instruction(lang: AnswerLanguage) -> str:
    if lang == "en":
        return "Answer language: English only for the entire response."
    if lang == "zh-Hant":
        return "回答语言：全文必须使用繁体中文。"
    if lang == "zh-Hans":
        return "回答语言：全文必须使用简体中文。"
    return "回答语言：与提问语言一致（英文问英文答，中文问中文答）。"


# hybrid 四段标题：随回答语言切换
HYBRID_SECTION_HEADERS: dict[str, tuple[str, str, str, str]] = {
    "zh-Hans": ("标准要求", "实施建议", "产品操作", "对齐与缺口"),
    "zh-Hant": ("標準要求", "實施建議", "產品操作", "對齊與缺口"),
    "en": (
        "Standards Requirements",
        "Implementation Guidance",
        "Product Steps",
        "Alignment & Gaps",
    ),
}


def hybrid_section_headers(lang: AnswerLanguage) -> tuple[str, str, str, str]:
    if lang in HYBRID_SECTION_HEADERS:
        return HYBRID_SECTION_HEADERS[lang]
    return HYBRID_SECTION_HEADERS["zh-Hans"]


_HEADER_ALIASES: dict[str, tuple[str, ...]] = {
    "standards": (
        "标准要求",
        "標準要求",
        "Standards Requirements",
        "Standard Requirements",
        "Standards",
    ),
    "playbook": (
        "实施建议",
        "實施建議",
        "Implementation Guidance",
        "Implementation Advice",
        "Playbook",
    ),
    "product": (
        "产品操作",
        "產品操作",
        "Product Steps",
        "Product Operations",
        "Product Guidance",
    ),
    "alignment": (
        "对齐与缺口",
        "對齊與缺口",
        "Alignment & Gaps",
        "Alignment and Gaps",
        "Alignment",
    ),
}


def localize_hybrid_section_headers(answer: str, lang: AnswerLanguage) -> str:
    """把四段标题改成目标语言（LLM 常仍输出中文标题）。"""
    if not answer or not answer.strip():
        return answer
    headers = hybrid_section_headers(lang)
    key_to_target = {
        "standards": headers[0],
        "playbook": headers[1],
        "product": headers[2],
        "alignment": headers[3],
    }
    # 宽松匹配：标题里含关键字即可（兼容「## 1. 标准要求」等）
    fuzzy: list[tuple[str, re.Pattern[str]]] = [
        ("standards", re.compile(r"标准要求|標準要求|standards?\s+requirements?", re.I)),
        ("playbook", re.compile(r"实施建议|實施建議|implementation\s+(guidance|advice)", re.I)),
        ("product", re.compile(r"产品操作|產品操作|product\s+(steps|operations|guidance)", re.I)),
        ("alignment", re.compile(r"对齐与缺口|對齊與缺口|alignment\s*(&|and)?\s*gaps?", re.I)),
    ]
    lines = answer.splitlines()
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        match = re.match(r"^(#{1,3})\s+(.+?)\s*$", stripped)
        if not match:
            out.append(line)
            continue
        level, title = match.group(1), match.group(2).strip()
        replaced = False
        for key, aliases in _HEADER_ALIASES.items():
            if title in aliases or title.lower() in {a.lower() for a in aliases}:
                out.append(f"{level} {key_to_target[key]}")
                replaced = True
                break
        if not replaced:
            for key, pattern in fuzzy:
                if pattern.search(title):
                    out.append(f"{level} {key_to_target[key]}")
                    replaced = True
                    break
        if not replaced:
            out.append(line)
    return "\n".join(out)


def polish_hybrid_answer(answer: str, *, lang: AnswerLanguage | None = None) -> str:
    """去掉「无法确认」与正文引用自相矛盾的开头，并压缩对齐段过长嵌套。"""
    text = answer or ""
    if not text.strip():
        return text

    parts = re.split(r"(?=^##\s)", text, flags=re.M)
    polished: list[str] = []
    for part in parts:
        if not part.strip():
            continue
        lines = part.splitlines()
        if not lines:
            polished.append(part)
            continue
        header = lines[0]
        body = "\n".join(lines[1:]).strip()
        if body and _CITATION_RE.search(body):
            body = _LEAD_CANNOT_RE.sub("", body)
            # 段内若仍以无法确认独占首句且后面有实质内容，删掉首句
            body = re.sub(
                r"^(?:根据现有资料无法确认|根據現有資料無法確認)[。.]?\s*",
                "",
                body,
                count=1,
                flags=re.I,
            )
        if header.strip().startswith("##") and (
            "对齐" in header or "對齊" in header or "Alignment" in header
        ):
            body = _compact_alignment(body)
        polished.append(header + ("\n" + body if body else ""))

    text = "\n\n".join(polished).strip()
    if lang:
        text = localize_hybrid_section_headers(text, lang)
    return text


def empty_hybrid_answer(lang: AnswerLanguage) -> str:
    h = hybrid_section_headers(lang)
    if lang == "en":
        cannot = "Cannot confirm from available materials."
        gap = "Gap: no usable materials were retrieved on any track."
    elif lang == "zh-Hant":
        cannot = "根據現有資料無法確認。"
        gap = "缺口：各軌均未檢索到可用資料。"
    else:
        cannot = "根据现有资料无法确认。"
        gap = "缺口：各轨均未检索到可用资料。"
    return (
        f"## {h[0]}\n{cannot}\n\n"
        f"## {h[1]}\n{cannot}\n\n"
        f"## {h[2]}\n{cannot}\n\n"
        f"## {h[3]}\n{gap}"
    )

def _compact_alignment(body: str) -> str:
    """对齐段保留前 4 条 bullet + 缺口句。"""
    if not body:
        return body
    bullets = re.findall(r"^[-*]\s+.+$", body, flags=re.M)
    gap = ""
    gap_match = re.search(r"(?:缺口|Gap)\s*[:：].+", body)
    if gap_match:
        gap = gap_match.group(0).strip()
    if len(bullets) <= 4 and (not gap or gap in body):
        # 仍过长则截断
        if len(body) > 600:
            kept = bullets[:3]
            lines = kept + ([f"- {gap}"] if gap else [])
            return "\n".join(lines) if lines else body[:600]
        return body
    kept = bullets[:3]
    lines = list(kept)
    if gap:
        lines.append(f"- {gap}" if not gap.startswith("-") else gap)
    elif "缺口" not in body and "Gap" not in body:
        lines.append("- 缺口：见实施手册与标准资料中的声明。")
    return "\n".join(lines)
