"""
Runs the full App-Store Feedback AI PoC pipeline end to end: loads
synthetic reviews and tickets, runs sentiment scoring, pain-point/
feature-request categorization, priority ranking, and evaluates the
result against hand-labeled ground truth. Prints a real console report.
"""

from src.data_sources import generate_reviews, generate_tickets
from src.sentiment import score_sentiment, sentiment_label
from src.evaluation import evaluate_pain_point_detection, evaluate_feature_request_detection, evaluate_category_accuracy
from src.prioritization import build_category_priority_report


def main():
    reviews = generate_reviews()
    tickets = generate_tickets()
    items = [{"id": r.review_id, "text": r.text, "star_rating": r.star_rating} for r in reviews]
    items += [{"id": t.ticket_id, "text": t.text, "star_rating": None} for t in tickets]
    print(f"Loaded {len(reviews)} app-store reviews and {len(tickets)} customer tickets ({len(items)} total items).\n")

    sentiments = [sentiment_label(score_sentiment(i["text"])) for i in items]
    counts = {label: sentiments.count(label) for label in ("positive", "neutral", "negative")}
    print(f"Sentiment distribution: {counts}\n")

    print("Category priority report (pain points, ranked):")
    report = build_category_priority_report(items)
    for row in report:
        print(f"  {row['category']:14s} count={row['count']:2d}  avg_sentiment={row['avg_sentiment']:+.2f}  priority={row['priority_score']:.2f}")

    print("\nEvaluation vs. hand-labeled ground truth:")
    pp = evaluate_pain_point_detection(items)
    print(f"  Pain-point detection:     precision={pp.precision}  recall={pp.recall}  F1={pp.f1}  (TP={pp.true_positives}, FP={pp.false_positives}, FN={pp.false_negatives})")
    fr = evaluate_feature_request_detection(items)
    print(f"  Feature-request detection: precision={fr.precision}  recall={fr.recall}  F1={fr.f1}  (TP={fr.true_positives}, FP={fr.false_positives}, FN={fr.false_negatives})")
    cat = evaluate_category_accuracy(items)
    print(f"  Category assignment accuracy: {cat['correct']}/{cat['total']} = {cat['accuracy']}")


if __name__ == "__main__":
    main()
