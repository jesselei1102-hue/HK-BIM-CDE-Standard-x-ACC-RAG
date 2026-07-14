"""香港 CDE 行业知识库：语料、配置、检索。"""

from .config import IndustryHKConfig, get_industry_hk_config
from .intent import should_route_industry

__all__ = [
    "IndustryHKConfig",
    "get_industry_hk_config",
    "should_route_industry",
]
