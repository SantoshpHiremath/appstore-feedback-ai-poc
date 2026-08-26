"""
Priority scoring for detected pain points -- the "Priorisierung von
Feedback" half of the posting's categorization/prioritization task.

Combines frequency (how many items fall in a category) with severity
signals (low star rating, negative sentiment) into a single priority
score per category, so results can be ranked for a product team rather
than left as an undifferentiated list.
"""

from __future__ import annotations

from collections import defaultdict

from src.categorization import is_pain_point_signal, categorize_pain_point
from src.sentiment import score_sentiment


def build_category_priority_report(items: list[dict]) -> list[dict]:
    """items: list of {"id": str, "text": str, "star_rating": int|None}
    Returns a list of {"category": str, "count": int, "avg_sentiment": float,
    "priority_score": float}, sorted by priority_score descending."""
    buckets: dict[str, list[dict]] = defaultdict(list)
    for item in items:
        if not is_pain_point_signal(item["text"], item.get("star_rating")):
            continue
        category = categorize_pain_point(item["text"]) or "uncategorized"
        buckets[category].append(item)

    report = []
    for category, bucket_items in buckets.items():
        sentiments = [score_sentiment(i["text"]) for i in bucket_items]
        avg_sentiment = round(sum(sentiments) / len(sentiments), 3)
        count = len(bucket_items)
        # priority = volume weighted by how negative the sentiment is --
        # a high-volume, very-negative category should rank above a
        # low-volume, mildly-negative one.
        severity = max(0.0, -avg_sentiment)
        priority_score = round(count * (1 + severity), 3)
        report.append({
            "category": category,
            "count": count,
            "avg_sentiment": avg_sentiment,
            "priority_score": priority_score,
        })

    report.sort(key=lambda r: r["priority_score"], reverse=True)
    return report
