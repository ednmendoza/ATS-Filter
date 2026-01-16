"""
Platform heuristic profiles for ATS optimization.
These weights determine how different platforms prioritize resume elements.
"""
from typing import Dict, Any

PLATFORM_PROFILES: Dict[str, Dict[str, float]] = {
    "linkedin": {
        "title_weight": 0.35,
        "recency_weight": 0.25,
        "keyword_weight": 0.40
    },
    "indeed": {
        "title_weight": 0.20,
        "recency_weight": 0.15,
        "keyword_weight": 0.65
    },
    "dice": {
        "title_weight": 0.15,
        "recency_weight": 0.10,
        "keyword_weight": 0.75
    }
}


def get_platform_profile(platform: str) -> Dict[str, float]:
    """Get platform-specific weight profile"""
    return PLATFORM_PROFILES.get(platform.lower(), PLATFORM_PROFILES["indeed"])
