from src.data_sources import generate_reviews, generate_tickets
from src.prioritization import build_category_priority_report


def _all_items():
    reviews = generate_reviews()
    tickets = generate_tickets()
    items = [{"id": r.review_id, "text": r.text, "star_rating": r.star_rating} for r in reviews]
    items += [{"id": t.ticket_id, "text": t.text, "star_rating": None} for t in tickets]
    return items


def test_report_is_sorted_by_priority_descending():
    report = build_category_priority_report(_all_items())
    scores = [r["priority_score"] for r in report]
    assert scores == sorted(scores, reverse=True)


def test_report_contains_expected_categories():
    report = build_category_priority_report(_all_items())
    categories = {r["category"] for r in report}
    assert "connectivity" in categories
    assert "performance" in categories


def test_report_excludes_feature_requests():
    report = build_category_priority_report(_all_items())
    total_flagged = sum(r["count"] for r in report)
    # feature requests (7 of them) should not be counted as pain points
    assert total_flagged <= len(_all_items()) - 7


def test_report_counts_are_positive():
    report = build_category_priority_report(_all_items())
    assert all(r["count"] > 0 for r in report)


def test_empty_items_returns_empty_report():
    assert build_category_priority_report([]) == []
