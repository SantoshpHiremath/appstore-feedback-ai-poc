"""
Rule-based pain-point categorization and feature-request detection --
the automated categorization of feedback and the extraction of pain
points and feature requests.

Deliberately keyword/pattern-based (not a trained classifier) so the
logic is fully inspectable and its precision/recall can be measured
transparently against the hand-labeled ground truth in
`ground_truth.py` -- a "cheap, transparent baseline first" approach.
"""

from __future__ import annotations

_CATEGORY_KEYWORDS = {
    "connectivity": ["connect", "connection", "pair", "pairing", "wifi", "drop"],
    "notifications": ["notification", "notify", "alert", "reminder"],
    "usability": ["confusing", "interface", "menu", "login", "timeout", "log in"],
    "performance": ["crash", "crashes", "crashing", "freeze", "won't load", "wont load", "slow"],
    "battery": ["battery", "drain"],
    # "setup" keywords last and deliberately narrow: a bare "install"
    # substring previously matched "installed this" in an unrelated
    # battery complaint (a real bug caught by test_categorizes_battery
    # -- see README). Requiring "setup"/"qr code"/"pairing code" or the
    # word "install" as a standalone token avoids that false match.
    "setup": ["setup", "qr code", "pairing code"],
}

_FEATURE_REQUEST_PATTERNS = [
    "would be great", "would love", "wish it", "please add", "any plans to add",
    "feature request", "would appreciate", "would really help",
]


def categorize_pain_point(text: str) -> str | None:
    """Returns the first matching category by keyword, or None if no
    category keyword is found (does not assert the text is a pain point
    at all -- callers should combine with is_pain_point_signal)."""
    lowered = text.lower()
    for category, keywords in _CATEGORY_KEYWORDS.items():
        if any(kw in lowered for kw in keywords):
            return category
    return None


def is_feature_request_signal(text: str, subject: str = "") -> bool:
    """Detects feature-request phrasing via known request patterns, or
    an explicit 'feature request' subject line (as tickets sometimes
    carry)."""
    lowered = (text + " " + subject).lower()
    return any(pattern in lowered for pattern in _FEATURE_REQUEST_PATTERNS)


def is_pain_point_signal(text: str, star_rating: int | None = None) -> bool:
    """A pain-point signal: either a category keyword is present, or
    (for reviews) the star rating is low (<=2) with no feature-request
    phrasing -- catching complaints that don't use one of the tracked
    keywords but are still clearly negative feedback about a problem,
    not a feature suggestion."""
    if is_feature_request_signal(text):
        return False
    if categorize_pain_point(text) is not None:
        return True
    if star_rating is not None and star_rating <= 2:
        return True
    return False
