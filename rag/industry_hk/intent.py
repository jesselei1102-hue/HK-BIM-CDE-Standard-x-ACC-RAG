"""行业意图：兼容封装 + 多类路由。"""

from __future__ import annotations

from rag.orchestrator.classify import (
    classify_intent,
    has_industry_signal,
    has_out_of_domain_signal,
)


def should_route_industry(query: str) -> bool:
    decision = classify_intent(query)
    if decision.track in {"hk_cde", "hybrid"}:
        return True
    if decision.track == "out_of_domain":
        return False
    return has_industry_signal(query) and decision.track != "docs"


def route_track(query: str) -> str:
    """Return docs | industry | hybrid | playbook | out_of_domain."""
    decision = classify_intent(query)
    if decision.track == "hk_cde":
        return "industry"
    return decision.track


def is_out_of_domain(query: str) -> bool:
    return has_out_of_domain_signal(query) or route_track(query) == "out_of_domain"
