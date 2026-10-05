# App-Store Feedback AI Proof-of-Concept

A tested Python pipeline that structures app-store reviews and customer tickets, scores sentiment, extracts and categorizes pain points and feature requests, ranks categories by priority, and evaluates its own output against hand-labeled ground truth. It covers the full analysis loop: sifting and structuring feedback, scoring and categorizing it, prioritizing what product teams should act on, and measuring how reliable the automated insights are against manual analysis.

## Scope

**All review and ticket text is hand-written and fictional.** `src/data_sources.py` contains 20 synthetic app-store reviews and 10 synthetic customer tickets, written to read like real, informal user feedback (inconsistent structure, mixed sentiment, some reviews raising multiple issues, some pure praise with no actionable content). None of it reflects a real app, product, or customer.

**Sentiment scoring is a small, transparent, rule-based lexicon scorer, not a trained model or a call to a sentiment-analysis library.** No external sentiment package (e.g. VADER, TextBlob) or LLM API was available with confirmed network access in my sandbox, so `src/sentiment.py` implements a minimal negation-aware keyword scorer. It is enough to demonstrate the evaluation methodology; a fine-tuned transformer model or an LLM prompt could be plugged into the same structure (score → label → evaluate against ground truth).

**Categorization is keyword/pattern-based, not topic modeling.** `src/categorization.py` assigns pain-point categories and detects feature-request phrasing via explicit keyword and pattern matching — a cheap, fully inspectable baseline rather than BERTopic/LDA/embedding-based topic modeling. The same "transparent baseline first" approach is used elsewhere in this portfolio (`underwriting-llm-risk-extraction`'s rule-based extractor, scored the same way against ground truth).

## What it does

- **`src/data_sources.py`** — generates the 20 synthetic reviews and 10 synthetic tickets, covering connectivity, performance, notification, setup, usability, and battery complaints, plus feature requests and pure-praise items.
- **`src/ground_truth.py`** — hand-labeled ground truth for every item: is it a genuine pain point (and which category), is it a feature request, or is it neither — the "manual analysis" baseline the automated pipeline is scored against.
- **`src/sentiment.py`** — the rule-based, negation-aware sentiment scorer.
- **`src/categorization.py`** — pain-point category assignment and feature-request detection, both keyword/pattern-based.
- **`src/prioritization.py`** — ranks pain-point categories by a combined volume-and-severity priority score, so results are actionable for a product team rather than an undifferentiated list.
- **`src/evaluation.py`** — the core of the project, comparing automated insights against manual analysis: computes precision/recall/F1 for pain-point detection and feature-request detection, and category-assignment accuracy, all against the hand-labeled ground truth.
- **`run_pipeline.py`** — runs the full flow end to end and prints a real console report (see sample output below, copied from an actual run).

## Testing

36 automated tests (`tests/`), all passing. One real bug was found and fixed during development: the initial `setup` category keyword list included a bare `"install"` substring, which incorrectly matched review r013 ("Battery drain is insane since I **install**ed this") as a setup complaint instead of a battery complaint. Caught by `test_categorizes_battery`, root-caused to keyword-list ordering and an overly broad substring match, and fixed by narrowing the setup keywords to `"setup"`, `"qr code"`, and `"pairing code"` — removing the bare `"install"` match without weakening detection of the actual setup-failure reviews (r005, t007), which are still caught correctly.

```bash
python3 -m pytest -v      # 36 tests, all passing
python3 run_pipeline.py   # runs the full pipeline end to end
```

## Sample output (from an actual run)

```
Loaded 20 app-store reviews and 10 customer tickets (30 total items).

Sentiment distribution: {'positive': 8, 'neutral': 7, 'negative': 15}

Category priority report (pain points, ranked):
  connectivity   count= 6  avg_sentiment=-0.50  priority=9.00
  notifications  count= 3  avg_sentiment=-0.33  priority=4.00
  performance    count= 3  avg_sentiment=-0.22  priority=3.67
  setup          count= 2  avg_sentiment=-0.50  priority=3.00
  usability      count= 2  avg_sentiment=-0.33  priority=2.67
  battery        count= 1  avg_sentiment=-0.67  priority=1.67

Evaluation vs. hand-labeled ground truth:
  Pain-point detection:     precision=1.0  recall=0.944  F1=0.971  (TP=17, FP=0, FN=1)
  Feature-request detection: precision=1.0  recall=1.0  F1=1.0  (TP=7, FP=0, FN=0)
  Category assignment accuracy: 15/18 = 0.833
```

The 0.944 recall and 0.833 category accuracy are reported as measured. A rule-based baseline missing one item and misclassifying a few others is the kind of result this evaluation is meant to surface, and it would equally show where an LLM- or ML-based approach needs improvement.

## Notes

- All review and ticket data is synthetic; no real app-store data or customer feedback was used.
- Sentiment scoring and categorization are simple, transparent, rule-based baselines — not trained ML models, API calls to an LLM, or topic modeling (LDA/BERTopic/embedding clustering). The value of the project is the evaluation methodology and pipeline structure, which a real sentiment, topic-modeling, or LLM component could be substituted into directly.
- The dataset is small (30 items) by design, to keep the hand-labeling verifiable; a production use would validate the approach against a much larger, real feedback corpus.
