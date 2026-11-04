# Dataset setup

Source: https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews

Run from the repository root with Python 3.11 or newer (standard library only):

```powershell
python scripts/setup_data.py
```

This downloads the complete Kaggle archive into `data/raw/` and extracts
`data/raw/Reviews.csv`. Existing CSV files are validated without downloading again.
The script reports the row count and SHA-256; it does not clean or modify the CSV.
The full dataset is for exploration, separate from the instructor's shared
50,000-review sample. No sentiment mapping or train/test split is selected.

Once the instructor sample is available, save it as
`data/raw/instructor_sample.csv` and validate it:

```powershell
python scripts/setup_data.py --kind shared --csv data/raw/instructor_sample.csv
```

The sample must retain the original ten CSV columns. Confirm its source/version
and expected row count with the instructor. The script does not create a substitute
sample or copy a CSV passed through `--csv`. Read CSVs directly during analysis
and model training; no database service is required.

## Fields to inspect

- `Text`: full review; `Summary`: review headline. These are the intended text inputs.
- `Score`: 1–5 star rating, used to derive labels. Never include it as an input feature.
- `Id`, `ProductId`, `UserId`, `ProfileName`: identifiers and reviewer information.
- `HelpfulnessNumerator`, `HelpfulnessDenominator`: helpful votes and total votes.
- `Time`: Unix timestamp.

Before reporting M1 facts, inspect the SHARED sample for missing/blank text, class
counts, average whitespace-token review length, and repeated Summary/Text pairs.
Agree on label mapping and duplicate handling before creating shared data splits.
Do not commit raw data or downloaded archives.

## Provisional team-created sample

Run python scripts/prepare_sample.py to create a uniform 50,000-row sample with seed 42 and a separate cleaned binary CSV. The raw sample is data/raw/provisional_sample_50000_seed42.csv; the binary file is data/processed/provisional_binary_clean_seed42.csv. Measured statistics and provenance are saved in report/dataset_summary/statistics.json. See report/dataset_summary/SUMMARY.md for the summary and chart. Confirm with the instructor before using this sample in place of the shared course sample.
