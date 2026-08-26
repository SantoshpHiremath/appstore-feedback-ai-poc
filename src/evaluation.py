"""
Evaluates the automated pipeline's pain-point/feature-request output
against the hand-labeled ground truth -- directly implementing the
posting's own evaluation task: "Bewertung der Qualität und
Zuverlässigkeit der AI-generierten Insights im Vergleich zur manuellen
Analyse."
"""

from __future__ import annotations

from dataclasses import dataclass

from src.categorization import is_pain_point_signal, is_feature_request_signal, categorize_pain_point
from src.ground_truth import is_pain_point, is_feature_request, pain_point_category


@dataclass
class EvaluationResult:
    task: str
    precision: float
    recall: float
    f1: float
    true_positives: int
    false_positives: int
    false_negatives: int


def _prf1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return round(precision, 3), round(recall, 3), round(f1, 3)


def evaluate_pain_point_detection(items: list[dict]) -> EvaluationResult:
    """items: list of {"id": str, "text": str, "star_rating": int|None}"""
    tp = fp = fn = 0
    for item in items:
        predicted = is_pain_point_signal(item["text"], item.get("star_rating"))
        actual = is_pain_point(item["id"])
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
    precision, recall, f1 = _prf1(tp, fp, fn)
    return EvaluationResult("pain_point_detection", precision, recall, f1, tp, fp, fn)


def evaluate_feature_request_detection(items: list[dict]) -> EvaluationResult:
    tp = fp = fn = 0
    for item in items:
        predicted = is_feature_request_signal(item["text"])
        actual = is_feature_request(item["id"])
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
    precision, recall, f1 = _prf1(tp, fp, fn)
    return EvaluationResult("feature_request_detection", precision, recall, f1, tp, fp, fn)


def evaluate_category_accuracy(items: list[dict]) -> dict:
    """Category assignment is a multi-class task -- reports simple
    accuracy among items that are true pain points (category
    assignment is only meaningful for actual pain points), rather than
    forcing it into the same precision/recall shape as the binary
    detection tasks above."""
    correct = 0
    total = 0
    for item in items:
        if not is_pain_point(item["id"]):
            continue
        total += 1
        predicted_category = categorize_pain_point(item["text"])
        actual_category = pain_point_category(item["id"])
        if predicted_category == actual_category:
            correct += 1
    accuracy = round(correct / total, 3) if total else 0.0
    return {"correct": correct, "total": total, "accuracy": accuracy}
