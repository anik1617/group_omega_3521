# Dataset summary measurements

**Provisional team-created sample. Confirm permission to use it instead of the instructor shared sample.**

## Sampling

- Source: full Kaggle Reviews.csv (568,454 rows).
- Uniform sample of 50,000 rows without replacement; reservoir sampling with Python random.Random(42).
- Sampled before filtering or deduplication; original source order and text retained.
- Raw sample: data/raw/provisional_sample_50000_seed42.csv
- Clean binary CSV: data/processed/provisional_binary_clean_seed42.csv

## Raw sample

| Star rating | Label | Count | Percent of 50,000 |
| --- | --- | ---: | ---: |
| 1 | Negative | 4,549 | 9.10% |
| 2 | Negative | 2,589 | 5.18% |
| 3 | Neutral | 3,834 | 7.67% |
| 4 | Positive | 7,112 | 14.22% |
| 5 | Positive | 31,916 | 63.83% |

- Average Text length: 80.53 whitespace-separated words.
- Average Summary + Text length: 84.64 words.
- Empty or whitespace-only values: 0 in every column.
- Five Summary entries contain the literal string N/A; seven ProfileName entries contain placeholder-like strings. These are flagged for review, not automatically treated as missing.
- Invalid star ratings: 0.
- Completely identical CSV rows: 0 (identifiers are included in this definition).
- Repeated exact Summary/Text pairs beyond the first: 3,666.
- Repeated Summary/Text pairs after casefolding and whitespace normalization beyond the first: 3,674.

## Binary filtering and cleaning

| Step | Rows |
| --- | ---: |
| Original sample | 50,000 |
| Exclude 3-star reviews | -3,834 |
| Binary rows before deduplication | 46,166 |
| Exclude groups with conflicting binary labels | 0 |
| Remove repeated normalized Summary/Text pairs, retaining first | -3,397 |
| Final binary CSV | 42,769 |

| Sentiment | Count | Percent of cleaned data |
| --- | ---: | ---: |
| Negative | 6,623 | 15.49% |
| Positive | 36,146 | 84.51% |

Average Text length after binary cleaning: 78.70 words.
Majority-class baseline on this complete cleaned CSV: 84.51%. Compute the actual held-out baseline after splitting.

Duplicate counts differ between raw and binary stages because neutral reviews are removed before binary deduplication. These counts do not measure all near-duplicates or repeated Text with different summaries. No train/validation/test splits have been created.

## Files and reproducibility

- statistics.json: measured statistics, cleaning rules, and SHA-256 hashes.
- class_counts.csv: raw and cleaned sentiment distributions.
- distribution.png: raw ratings and cleaned binary sentiment chart.
- Reproduce the CSVs and statistics: python scripts/prepare_sample.py
- CSVs and archives remain excluded from Git.
