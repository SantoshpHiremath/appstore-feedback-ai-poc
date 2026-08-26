from src.sentiment import score_sentiment, sentiment_label


def test_positive_text_scores_positive():
    score = score_sentiment("Works great, love it, very reliable.")
    assert score > 0


def test_negative_text_scores_negative():
    score = score_sentiment("App keeps crashing, useless, frustrating.")
    assert score < 0


def test_neutral_text_scores_near_zero():
    score = score_sentiment("The weather today is mild.")
    assert score == 0.0


def test_negation_flips_positive_to_negative():
    # "not great" should not score as strongly positive as "great" alone
    plain = score_sentiment("This is great.")
    negated = score_sentiment("This is not great.")
    assert negated < plain


def test_negation_flips_negative_to_positive_direction():
    # "no complaints" contains a negative-flavored construction but is
    # actually positive framing; at minimum it should not score as
    # negatively as an unnegated complaint word would.
    negated = score_sentiment("No complaints, works well.")
    plain_complaint = score_sentiment("Complaints about crashes.")
    assert negated >= plain_complaint


def test_sentiment_label_boundaries():
    assert sentiment_label(0.5) == "positive"
    assert sentiment_label(-0.5) == "negative"
    assert sentiment_label(0.0) == "neutral"
    assert sentiment_label(0.1) == "neutral"


def test_score_bounded_in_range():
    score = score_sentiment("crash crash crash crashing crashes useless nightmare frustrating insane uninstalling")
    assert -1.0 <= score <= 1.0
