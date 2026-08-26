from src.categorization import categorize_pain_point, is_feature_request_signal, is_pain_point_signal


def test_categorizes_connectivity():
    assert categorize_pain_point("The app won't connect to my washing machine.") == "connectivity"


def test_categorizes_performance():
    assert categorize_pain_point("App keeps crashing on startup.") == "performance"


def test_categorizes_notifications():
    assert categorize_pain_point("The done-cycle notification arrives too late.") == "notifications"


def test_categorizes_battery():
    assert categorize_pain_point("Battery drain is insane since I installed this.") == "battery"


def test_no_category_returns_none():
    assert categorize_pain_point("This is a completely unrelated sentence about nothing.") is None


def test_feature_request_pattern_detected():
    assert is_feature_request_signal("Would be great if I could set a recipe reminder.") is True


def test_feature_request_via_subject():
    assert is_feature_request_signal("Some body text.", subject="Feature request: dark mode") is True


def test_no_feature_request_signal_on_plain_complaint():
    assert is_feature_request_signal("The app crashes constantly, this is broken.") is False


def test_pain_point_signal_via_keyword():
    assert is_pain_point_signal("App won't connect to the dryer.") is True


def test_pain_point_signal_via_low_star_rating():
    # No tracked keyword present, but a 1-star rating signals a problem.
    assert is_pain_point_signal("This is genuinely disappointing overall.", star_rating=1) is True


def test_pain_point_signal_false_on_high_rating_no_keyword():
    assert is_pain_point_signal("This is genuinely disappointing overall.", star_rating=5) is False


def test_feature_request_overrides_pain_point_signal():
    # A feature request should not also be flagged as a pain point,
    # even if phrased with a low star rating.
    text = "Would be great if you added multi-device scheduling."
    assert is_feature_request_signal(text) is True
    assert is_pain_point_signal(text, star_rating=2) is False
