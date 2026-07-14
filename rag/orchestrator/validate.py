"""Hybrid 输出轻量校验：结构、编号归属、产品来源相关性。"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from rag.orchestrator.merge import MergedContexts, TrackedChunk


_SECTION_FLEX = (
    re.compile(r"标准要求|標準要求|Standards?\s+Requirements?", re.I),
    re.compile(r"实施建议|實施建議|Implementation\s+(?:Guidance|Advice)", re.I),
    re.compile(r"产品操作|產品操作|Product\s+(?:Steps|Operations|Guidance)", re.I),
    re.compile(r"对齐与缺口|對齊與缺口|Alignment\s*(?:&|and)?\s*Gaps?", re.I),
)

_CITATION_RE = re.compile(r"\[(\d+)\]")
_GAP_RE = re.compile(r"缺口|Gap\s*[:：]", re.I)

# 能力 → 产品 Docs 页应匹配的关键词（title+url+text 前缀）
_CAPABILITY_DOCS_KEYWORDS: dict[str, tuple[str, ...]] = {
    "folder": (
        "folder",
        "folders",
        "subfolder",
        "files",
        "template",
        "organize",
        "文件夹",
        "目录",
    ),
    "project_create": (
        "project",
        "projects",
        "create",
        "template",
        "项目",
    ),
    "naming": (
        "naming",
        "name",
        "standard",
        "命名",
    ),
    "workflow": (
        "review",
        "approval",
        "workflow",
        "approver",
        "审批",
        "审阅",
        "工作流",
    ),
}

# 几乎从不该出现在能力相关产品段的 Docs 噪声页
_DOCS_NOISE_PATTERNS = (
    re.compile(r"navigation\s*basics", re.I),
    re.compile(r"getting_started_navigation", re.I),
    re.compile(r"autodesk\s*profile", re.I),
    re.compile(r"product\s*picker", re.I),
    re.compile(r"regional\s*(data|offerings|faq)", re.I),
    re.compile(r"welcome\s+to\s+the\s+autodesk\s+docs\s+help", re.I),
    re.compile(r"access_assistant|autodesk\s*assistant", re.I),
)


@dataclass
class ValidationIssue:
    code: str
    message: str
    severity: str  # hard | soft
    drop_docs_indices: tuple[int, ...] = ()


@dataclass
class ValidationResult:
    ok: bool
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def hard_issues(self) -> list[ValidationIssue]:
        return [item for item in self.issues if item.severity == "hard"]

    @property
    def warnings(self) -> list[str]:
        return [f"[{item.severity}] {item.code}: {item.message}" for item in self.issues]


def _split_sections(answer: str) -> dict[str, str]:
    """按四段标题切分；找不到则返回空段。"""
    text = answer or ""
    markers: list[tuple[int, str]] = []
    for key, pattern in (
        (
            "standards",
            re.compile(
                r"^#{0,3}\s*(标准要求|標準要求|Standards?\s+Requirements?)\s*$",
                re.M | re.I,
            ),
        ),
        (
            "playbook",
            re.compile(
                r"^#{0,3}\s*(实施建议|實施建議|Implementation\s+(?:Guidance|Advice)|Playbook)\s*$",
                re.M | re.I,
            ),
        ),
        (
            "product",
            re.compile(
                r"^#{0,3}\s*(产品操作|產品操作|Product\s+(?:Steps|Operations|Guidance))\s*$",
                re.M | re.I,
            ),
        ),
        (
            "alignment",
            re.compile(
                r"^#{0,3}\s*(对齐与缺口|對齊與缺口|Alignment\s*(?:&|and)?\s*Gaps?)\s*$",
                re.M | re.I,
            ),
        ),
    ):
        match = pattern.search(text)
        if match:
            markers.append((match.start(), key))
    markers.sort()
    sections = {"standards": "", "playbook": "", "product": "", "alignment": ""}
    if not markers:
        return sections
    for index, (start, key) in enumerate(markers):
        header_end = text.find("\n", start)
        body_start = header_end + 1 if header_end != -1 else start
        end = markers[index + 1][0] if index + 1 < len(markers) else len(text)
        sections[key] = text[body_start:end].strip()
    return sections


def _citations(text: str) -> set[int]:
    return {int(match) for match in _CITATION_RE.findall(text or "")}


def _docs_identity_blob(item: TrackedChunk) -> str:
    """仅 title + url，用于噪声页判断（正文可能顺带提到 product picker 等）。"""
    chunk = item.chunk
    return f"{chunk.title}\n{chunk.source_url}".lower()


def _docs_blob(item: TrackedChunk) -> str:
    chunk = item.chunk
    return f"{chunk.title}\n{chunk.source_url}\n{chunk.text[:800]}".lower()


def _docs_is_noise(item: TrackedChunk) -> bool:
    blob = _docs_identity_blob(item)
    return any(pattern.search(blob) for pattern in _DOCS_NOISE_PATTERNS)


def _docs_matches_capability(item: TrackedChunk, capability: str | None) -> bool:
    if _docs_is_noise(item):
        return False
    if not capability:
        return True
    keywords = _CAPABILITY_DOCS_KEYWORDS.get(capability)
    if not keywords:
        return True
    blob = _docs_blob(item)
    return any(keyword.lower() in blob for keyword in keywords)


def validate_hybrid_answer(
    answer: str,
    merged: MergedContexts,
    *,
    capability: str | None = None,
) -> ValidationResult:
    issues: list[ValidationIssue] = []
    sections = _split_sections(answer)

    header_hits = sum(1 for pattern in _SECTION_FLEX if pattern.search(answer or ""))
    # 兼容旧三段答案：至少标准/产品/对齐；有 playbook 资料时期望四段
    required = 4 if merged.playbook_indices else 3
    if header_hits < required:
        issues.append(
            ValidationIssue(
                code="missing_sections",
                message=f"答案缺少完整标题（命中 {header_hits}/{required}）",
                severity="hard",
            )
        )

    hk_ids = set(merged.industry_indices)
    playbook_ids = set(merged.playbook_indices)
    docs_ids = set(merged.docs_indices)

    std_cites = _citations(sections["standards"])
    pb_cites = _citations(sections["playbook"])
    prod_cites = _citations(sections["product"])
    align_cites = _citations(sections["alignment"])

    bad_std = sorted(std_cites - hk_ids)
    if bad_std and hk_ids:
        issues.append(
            ValidationIssue(
                code="standards_wrong_track",
                message=f"标准要求段引用了非 HK 编号：{bad_std}",
                severity="hard",
            )
        )

    bad_pb = sorted(pb_cites - playbook_ids)
    if bad_pb and playbook_ids and sections["playbook"]:
        issues.append(
            ValidationIssue(
                code="playbook_wrong_track",
                message=f"实施建议段引用了非 Playbook 编号：{bad_pb}",
                severity="hard",
            )
        )

    bad_prod = sorted(prod_cites - docs_ids)
    if bad_prod and docs_ids:
        issues.append(
            ValidationIssue(
                code="product_wrong_track",
                message=f"产品操作段引用了非 Docs 编号：{bad_prod}",
                severity="hard",
            )
        )

    drop_indices: list[int] = []
    cited_docs = prod_cites & docs_ids
    index_to_item = {item.display_index: item for item in merged.tracked}
    for doc_id in sorted(cited_docs):
        item = index_to_item.get(doc_id)
        if item is None or item.track != "docs":
            continue
        if not _docs_matches_capability(item, capability):
            drop_indices.append(doc_id)
            issues.append(
                ValidationIssue(
                    code="irrelevant_docs_citation",
                    message=(
                        f"产品段引用了弱相关 Docs 页 [{doc_id}] "
                        f"{item.chunk.title!r}"
                    ),
                    severity="hard",
                    drop_docs_indices=(doc_id,),
                )
            )

    for item in merged.tracked:
        if item.track != "docs":
            continue
        if item.display_index in drop_indices:
            continue
        if _docs_is_noise(item) or (
            capability and not _docs_matches_capability(item, capability)
        ):
            drop_indices.append(item.display_index)
            issues.append(
                ValidationIssue(
                    code="irrelevant_docs_context",
                    message=(
                        f"上下文含弱相关 Docs 页 [{item.display_index}] "
                        f"{item.chunk.title!r}，将在重试时剔除"
                    ),
                    severity="soft",
                    drop_docs_indices=(item.display_index,),
                )
            )

    # 对齐段：有多轨资料时，应有缺口或至少两轨编号
    active_tracks = sum(1 for ids in (hk_ids, playbook_ids, docs_ids) if ids)
    if active_tracks >= 2 and sections["alignment"]:
        has_gap = bool(_GAP_RE.search(sections["alignment"]))
        track_hits = sum(
            1
            for ids in (hk_ids, playbook_ids, docs_ids)
            if ids and (align_cites & ids)
        )
        if not has_gap and track_hits < 2:
            issues.append(
                ValidationIssue(
                    code="alignment_weak",
                    message="对齐段既无「缺口」也未引用至少两轨编号",
                    severity="soft",
                )
            )

    hard = [item for item in issues if item.severity == "hard"]
    return ValidationResult(ok=not hard, issues=issues)


def drop_docs_indices(merged: MergedContexts, drop: set[int]) -> MergedContexts:
    """去掉指定 Docs 编号后重新编号合并。"""
    from rag.orchestrator.merge import merge_triple_contexts

    keep_docs = [
        item.chunk
        for item in merged.tracked
        if item.track == "docs" and item.display_index not in drop
    ]
    keep_industry = [
        item.chunk for item in merged.tracked if item.track == "hk_cde"
    ]
    keep_playbook = [
        item.chunk for item in merged.tracked if item.track == "playbook"
    ]
    return merge_triple_contexts(
        docs_chunks=keep_docs,
        industry_chunks=keep_industry,
        playbook_chunks=keep_playbook,
        docs_top_k=len(keep_docs) or 0,
        industry_top_k=len(keep_industry) or 0,
        playbook_top_k=len(keep_playbook) or 0,
    )


def collect_drop_indices(result: ValidationResult) -> set[int]:
    drops: set[int] = set()
    for issue in result.issues:
        drops.update(issue.drop_docs_indices)
    return drops


def prefilter_docs_for_capability(
    merged: MergedContexts,
    capability: str | None,
) -> tuple[MergedContexts, set[int]]:
    """生成前剔除噪声/弱相关 Docs 页。若会剔光 Docs，则保留原样。"""
    drop: set[int] = set()
    for item in merged.tracked:
        if item.track != "docs":
            continue
        if not _docs_matches_capability(item, capability):
            drop.add(item.display_index)
    if not drop:
        return merged, set()
    remaining_docs = sum(
        1
        for item in merged.tracked
        if item.track == "docs" and item.display_index not in drop
    )
    if remaining_docs == 0:
        return merged, set()
    return drop_docs_indices(merged, drop), drop
