"""行业轨意图信号（委托编排层，保持向后兼容）。"""

from __future__ import annotations

from rag.orchestrator.classify import has_industry_signal


def should_route_industry(query: str) -> bool:
    return has_industry_signal(query)
