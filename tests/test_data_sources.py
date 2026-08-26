from src.data_sources import generate_reviews, generate_tickets
from src.ground_truth import ALL_IDS


def test_generates_20_reviews():
    reviews = generate_reviews()
    assert len(reviews) == 20


def test_generates_10_tickets():
    tickets = generate_tickets()
    assert len(tickets) == 10


def test_review_star_ratings_in_range():
    for r in generate_reviews():
        assert 1 <= r.star_rating <= 5


def test_all_ids_unique():
    reviews = generate_reviews()
    tickets = generate_tickets()
    ids = [r.review_id for r in reviews] + [t.ticket_id for t in tickets]
    assert len(ids) == len(set(ids))


def test_ground_truth_covers_all_generated_ids():
    reviews = generate_reviews()
    tickets = generate_tickets()
    generated_ids = {r.review_id for r in reviews} | {t.ticket_id for t in tickets}
    assert generated_ids == set(ALL_IDS)
