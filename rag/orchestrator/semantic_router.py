"""语义路由器：capability → track 分数聚合，低置信度回退 legacy。"""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter

from rag.config import AppConfig, get_config
from rag.orchestrator.route_index import OrchestratorRouteIndex, RouteMatch

CAPABILITY_LABELS: tuple[str, ...] = (
    "project_template",
    "model_viewer",
    "permissions",
    "naming",
    "workflow",
    "project_create",
    "roles",
    "folder",
)

_CAPABILITY_PRIORITY: tuple[str, ...] = CAPABILITY_LABELS

TRACK_SIGNAL_LABELS: tuple[str, ...] = ("product", "industry", "playbook")


@dataclass(frozen=True)
class LabelScore:
    label: str
    score: float
    margin: float
    matched_text: str
    hint_query: str


@dataclass
class SemanticRouteResult:
    query: str
    capability: str | None = None
    capability_score: float = 0.0
    capability_margin: float = 0.0
    capability_confident: bool = False
    capability_null_score: float = 0.0
    product_score: float = 0.0
    industry_score: float = 0.0
    playbook_score: float = 0.0
    out_of_domain_score: float = 0.0
    track: str | None = None
    track_confident: bool = False
    hint_query: str = ""
    index_available: bool = False
    latency_ms: float = 0.0
    fallback_reason: str | None = None
    top_matches: list[RouteMatch] = field(default_factory=list)
    capability_scores: dict[str, float] = field(default_factory=dict)


def _aggregate_scores(matches: list[RouteMatch]) -> dict[tuple[str, str], LabelScore]:
    """按 (label_type, label) 取最高相似度。"""
    best: dict[tuple[str, str], LabelScore] = {}
    for match in matches:
        key = (match.label_type, match.label)
        current = best.get(key)
        if current is None or match.similarity > current.score:
            best[key] = LabelScore(
                label=match.label,
                score=match.similarity,
                margin=0.0,
                matched_text=match.text,
                hint_query=match.hint_query,
            )
    return best


def _capability_margin(scores: dict[str, float], winner: str) -> float:
    others = [score for label, score in scores.items() if label != winner]
    if not others:
        return scores.get(winner, 0.0)
    return scores[winner] - max(others)


def _pick_capability(
    aggregated: dict[tuple[str, str], LabelScore],
    *,
    min_sim: float,
    min_margin: float,
    null_min_sim: float,
) -> tuple[str | None, bool, dict[str, float], float, float, str]:
    cap_scores: dict[str, float] = {}
    hints: dict[str, str] = {}
    for (label_type, label), item in aggregated.items():
        if label_type != "capability":
            continue
        cap_scores[label] = item.score
        if item.hint_query:
            hints[label] = item.hint_query

    null_score = aggregated.get(("capability_null", "__none__"))
    null_val = null_score.score if null_score else 0.0

    if not cap_scores:
        return None, False, cap_scores, null_val, 0.0, ""

    ranked = sorted(cap_scores.items(), key=lambda pair: pair[1], reverse=True)
    winner, top_score = ranked[0]
    second_score = ranked[1][1] if len(ranked) > 1 else 0.0
    margin = top_score - second_score

    # 裸 WIP / 术语解释：null 簇分数足够高时抑制 folder
    if null_val >= null_min_sim and null_val >= top_score - 0.04:
        return None, True, cap_scores, null_val, margin, hints.get(winner, "")

    if top_score < min_sim or margin < min_margin:
        return None, False, cap_scores, null_val, margin, hints.get(winner, "")

    # 冲突优先级：permissions > folder 等同 legacy
    tied = [label for label, score in cap_scores.items() if score >= top_score - 0.02]
    if len(tied) > 1:
        for preferred in _CAPABILITY_PRIORITY:
            if preferred in tied:
                winner = preferred
                break

    return winner, True, cap_scores, null_val, margin, hints.get(winner, "")


def _signal_score(aggregated: dict[tuple[str, str], LabelScore], label: str) -> float:
    item = aggregated.get(("track_signal", label))
    return item.score if item else 0.0


def _derive_track(
    *,
    product_score: float,
    industry_score: float,
    playbook_score: float,
    out_of_domain_score: float,
    capability: str | None,
    signal_min_sim: float,
) -> tuple[str, bool, str | None]:
    has_product = product_score >= signal_min_sim
    has_industry = industry_score >= signal_min_sim
    has_playbook = playbook_score >= signal_min_sim

    if out_of_domain_score >= signal_min_sim and not has_product:
        return "out_of_domain", True, "semantic_out_of_domain"

    if has_product and has_industry:
        return "hybrid", True, None

    if has_playbook and not has_product and not has_industry:
        return "playbook", True, None

    if has_playbook and has_product and not has_industry:
        return "playbook", True, "semantic_playbook_product"

    if has_industry and not has_product:
        return "hk_cde", True, None

    if has_product and not has_industry:
        return "docs", True, None

    # capability-only fallback hints
    if capability in {
        "project_template",
        "folder",
        "permissions",
        "naming",
        "workflow",
        "project_create",
        "model_viewer",
        "roles",
    }:
        if capability in {"project_template"} and has_playbook:
            return "playbook", False, "capability_playbook_hint"
        if has_industry or has_product:
            if has_product and has_industry:
                return "hybrid", False, "capability_hybrid_hint"
            if has_industry:
                return "hk_cde", False, "capability_industry_hint"
            return "docs", False, "capability_docs_hint"

    return "docs", False, "track_low_confidence"


class SemanticRouter:
    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or get_config()
        self.router_config = self.config.semantic_router
        self._index: OrchestratorRouteIndex | None = None

    @property
    def index(self) -> OrchestratorRouteIndex:
        if self._index is None:
            self._index = OrchestratorRouteIndex(self.config)
        return self._index

    def route(self, query: str) -> SemanticRouteResult:
        started = perf_counter()
        result = SemanticRouteResult(query=query.strip())
        index = self.index
        result.index_available = index.available

        if not index.available:
            result.fallback_reason = "index_missing"
            result.latency_ms = (perf_counter() - started) * 1000
            return result

        matches = index.search(query, top_k=self.router_config.route_top_k)
        result.top_matches = matches
        aggregated = _aggregate_scores(matches)

        cfg = self.router_config
        capability, cap_confident, cap_scores, null_score, cap_margin, hint = _pick_capability(
            aggregated,
            min_sim=cfg.min_capability_sim,
            min_margin=cfg.min_capability_margin,
            null_min_sim=cfg.min_capability_null_sim,
        )
        result.capability = capability
        result.capability_scores = cap_scores
        result.capability_score = cap_scores.get(capability or "", 0.0)
        result.capability_margin = cap_margin
        result.capability_confident = cap_confident
        result.capability_null_score = null_score
        result.hint_query = hint

        result.product_score = _signal_score(aggregated, "product")
        result.industry_score = _signal_score(aggregated, "industry")
        result.playbook_score = _signal_score(aggregated, "playbook")
        ood = aggregated.get(("out_of_domain", "__ood__"))
        result.out_of_domain_score = ood.score if ood else 0.0

        track, track_confident, track_reason = _derive_track(
            product_score=result.product_score,
            industry_score=result.industry_score,
            playbook_score=result.playbook_score,
            out_of_domain_score=result.out_of_domain_score,
            capability=capability,
            signal_min_sim=cfg.min_track_signal_sim,
        )
        result.track = track
        result.track_confident = track_confident
        if track_reason:
            result.fallback_reason = track_reason

        if not cap_confident:
            result.fallback_reason = result.fallback_reason or "capability_low_confidence"
        if not track_confident:
            result.fallback_reason = result.fallback_reason or "track_low_confidence"

        result.latency_ms = (perf_counter() - started) * 1000
        return result


_router: SemanticRouter | None = None


def get_semantic_router(config: AppConfig | None = None) -> SemanticRouter:
    global _router
    if config is not None:
        return SemanticRouter(config)
    if _router is None:
        _router = SemanticRouter()
    return _router
