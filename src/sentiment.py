"""
Lightweight, rule-based sentiment scoring -- deliberately simple and
fully inspectable, as a baseline for evaluating
sentiment-analysis approaches.

No external sentiment library (e.g. VADER, TextBlob) was available in
this sandbox with confirmed network access, so this implements a small,
transparent lexicon-based scorer instead -- honestly disclosed as a
simple baseline, not a claim of production-grade sentiment-model
experience. See README for the full disclosure and what a production
version would use instead (e.g. a fine-tuned transformer or an LLM
prompt).
"""

from __future__ import annotations

_NEGATIVE_WORDS = {
    "crash", "crashes", "crashing", "useless", "nightmare", "confusing",
    "frustrating", "insane", "uninstalling", "drop", "drops", "dropped",
    "impossible", "never", "won't", "wont", "constantly", "delayed",
    "late", "lost", "stopped", "fails", "fail", "hurt", "pointless",
}
_POSITIVE_WORDS = {
    "great", "love", "works", "solid", "reliable", "helpful", "useful",
    "genuinely", "simple", "thanks", "good", "nice",
}
_NEGATION_WORDS = {"not", "no", "never", "n't", "without"}


def _tokenize(text: str) -> list[str]:
    return [w.strip(".,!?'\"").lower() for w in text.split()]


def score_sentiment(text: str) -> float:
    """Returns a score in [-1.0, 1.0]. Applies simple negation handling:
    a positive word immediately preceded by a negation word counts as
    negative, and vice versa -- catching "not great" and "no complaints"
    correctly rather than scoring purely on word presence."""
    tokens = _tokenize(text)
    score = 0
    for i, tok in enumerate(tokens):
        negated = i > 0 and tokens[i - 1] in _NEGATION_WORDS
        if tok in _NEGATIVE_WORDS:
            score += 1 if negated else -1
        elif tok in _POSITIVE_WORDS:
            score += -1 if negated else 1
    if score == 0:
        return 0.0
    # normalize into [-1, 1] with a soft cap so a handful of strong
    # words doesn't blow past the range
    return max(-1.0, min(1.0, score / max(3, len(tokens) / 8)))


def sentiment_label(score: float) -> str:
    if score > 0.15:
        return "positive"
    if score < -0.15:
        return "negative"
    return "neutral"
