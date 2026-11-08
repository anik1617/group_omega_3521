# Dataset summary: Group Omega sample (seed 46)

## Sampling

- Source: full Kaggle `Reviews.csv` (568,454 rows).
- Drawn with the instructor's script: `pd.read_csv(Reviews.csv).sample(n=50000, random_state=46)`. Seed 46 is Group Omega's assigned seed. Do not resample with another seed.
- Team dataset: `data/raw/group_sample_seed46.csv` (SHA-256 `b850d24d…`, full hash in `statistics.json`). A fresh run of the instructor's script reproduces this file byte for byte.

## Sample before cleaning

| Star rating | Count |
| --- | ---: |
| 1 | 4,634 |
| 2 | 2,708 |
| 3 | 3,660 |
| 4 | 7,164 |
| 5 | 31,834 |

| Sentiment | Count | Percent |
| --- | ---: | ---: |
| Negative (1–2 stars) | 7,342 | 14.68% |
| Neutral (3 stars) | 3,660 | 7.32% |
| Positive (4–5 stars) | 38,998 | 78.00% |

- Average `Text` length: 80.30 whitespace-separated words (median 56).
- Missing values when read with pandas: 2 `Summary`, 1 `ProfileName`. Every row has `Text` and a valid star rating.
- Rows identical apart from `Id`: 2.
- Repeated `Summary` + `Text` pairs (casefolded, whitespace collapsed) beyond the first copy: 3,656. None has conflicting sentiment labels.

## Cleaned three-class dataset

`data/processed/group_seed46_clean.csv` keeps the first copy of each repeated review.

| Sentiment | Count | Percent |
| --- | ---: | ---: |
| Negative | 6,837 | 14.75% |
| Neutral | 3,394 | 7.32% |
| Positive | 36,113 | 77.92% |
| Total | 46,344 | |

Average `Text` length after cleaning: 79.81 words. Always predicting positive would score 77.92% accuracy on the cleaned data, so report macro-F1 and per-class scores alongside accuracy. Train/validation/test splits have not been created yet.

## Files

- `statistics.json`: all measurements, cleaning rule, and SHA-256 hashes.
- `class_counts.csv`: sentiment counts before and after cleaning.
- `sentiment_seed46.png`: Figure 1 for the charter.
- Regenerate everything with `python scripts/prepare_sample.py`.
