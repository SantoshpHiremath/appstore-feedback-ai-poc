"""
Hand-labeled ground truth for the synthetic reviews and tickets --
required to measure extraction/categorization quality against manual
analysis, so the quality and reliability of AI-generated insights
can be compared against manual analysis.

Each item is labeled by hand with: is this a pain point, a feature
request, or neither (pure praise/neutral) -- and if a pain point, which
category it falls into. This is the "manual analysis" baseline the
automated pipeline is scored against.
"""

from __future__ import annotations

# category values: "connectivity", "notifications", "usability",
# "performance", "setup", "battery", None (not a pain point)
PAIN_POINT_CATEGORY = {
    "r001": "performance",       # crashing
    "r002": "connectivity",      # connection drops
    "r003": None,
    "r004": "notifications",     # delayed notifications
    "r005": "setup",             # QR scanner failure
    "r006": None,                # feature request, not a pain point
    "r007": "usability",         # confusing interface
    "r008": None,
    "r009": "connectivity",      # lost connection after update
    "r010": None,                # feature request (dark mode)
    "r011": "performance",       # crashes on startup
    "r012": None,                # feature request (multi-device scheduling)
    "r013": "battery",           # battery drain
    "r014": None,
    "r015": "notifications",     # notifications late/missing
    "r016": "performance",       # app won't load
    "r017": "connectivity",      # pairing second device impossible
    "r018": None,                # feature request (voice assistant)
    "r019": "usability",         # login timeout
    "r020": None,

    "t001": "connectivity",      # won't connect to washer
    "t002": None,                # feature request (multi-device scheduling)
    "t003": "performance",       # crash on login
    "t004": "notifications",     # delayed notifications
    "t005": "connectivity",      # cannot pair second appliance
    "t006": None,
    "t007": "setup",             # QR setup fails
    "t008": None,                # feature request (dark mode)
    "t009": "battery",           # battery drain
    "t010": None,                # feature request (voice assistant)
}

FEATURE_REQUEST = {
    "r006": True, "r010": True, "r012": True, "r018": True,
    "t002": True, "t008": True, "t010": True,
}

# For every item not listed above (or listed as False), no feature
# request is present.
ALL_IDS = list(PAIN_POINT_CATEGORY.keys())


def is_pain_point(item_id: str) -> bool:
    return PAIN_POINT_CATEGORY.get(item_id) is not None


def is_feature_request(item_id: str) -> bool:
    return FEATURE_REQUEST.get(item_id, False)


def pain_point_category(item_id: str) -> str | None:
    return PAIN_POINT_CATEGORY.get(item_id)
