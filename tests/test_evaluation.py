from src.data_sources import generate_reviews, generate_tickets
from src.evaluation import (
    evaluate_pain_point_detection, evaluate_feature_request_detection, evaluate_category_accuracy,
)


def _all_items():
    reviews = generate_reviews()
    tickets = generate_tickets()
    items = [{"id": r.review_id, "text": r.text, "star_rating": r.star_rating} for r in reviews]
    items += [{"id": t.ticket_id, "text": t.text, "star_rating": None} for t in tickets]
    return items


def test_pain_point_evaluation_returns_valid_metrics():
    result = evaluate_pain_point_detection(_all_items())
    assert 0.0 <= result.precision <= 1.0
    assert 0.0 <= result.recall <= 1.0
    assert 0.0 <= result.f1 <= 1.0
    assert result.true_positives + result.false_negatives > 0  # some real pain points exist


def test_pain_point_evaluation_reasonable_recall():
    # The rule-based detector should catch a meaningful majority of the
    # hand-labeled pain points, not just get lucky on one or two.
    result = evaluate_pain_point_detection(_all_items())
    assert result.recall >= 0.7


def test_feature_request_evaluation_returns_valid_metrics():
    result = evaluate_feature_request_detection(_all_items())
    assert 0.0 <= result.precision <= 1.0
    assert 0.0 <= result.recall <= 1.0


def test_feature_request_evaluation_perfect_on_known_patterns():
    # All 7 hand-labeled feature requests in the synthetic set use one
    # of the tracked request phrases by construction, so recall should
    # be perfect on this synthetic set specifically.
    result = evaluate_feature_request_detection(_all_items())
    assert result.recall == 1.0


def test_category_accuracy_returns_valid_structure():
    result = evaluate_category_accuracy(_all_items())
    assert "correct" in result and "total" in result and "accuracy" in result
    assert 0.0 <= result["accuracy"] <= 1.0
    assert result["total"] > 0


def test_category_accuracy_reasonable():
    result = evaluate_category_accuracy(_all_items())
    assert result["accuracy"] >= 0.7


def test_empty_items_do_not_crash():
    result = evaluate_pain_point_detection([])
    assert result.precision == 0.0
    assert result.recall == 0.0
    assert result.f1 == 0.0
