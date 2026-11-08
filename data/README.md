# Dataset setup

Source: https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews

Run from the repository root with Python 3.11 or newer:

```powershell
pip install -r requirements.txt
python scripts/setup_data.py
python scripts/prepare_sample.py
```

`setup_data.py` downloads the complete Kaggle archive into `data/raw/`, extracts
`data/raw/Reviews.csv` (568,454 rows), and prints its row count and SHA-256. It uses
only the standard library and does not modify the CSV.

`prepare_sample.py` builds the team dataset exactly as the instructor's script does:

```python
pd.read_csv("Reviews.csv").sample(n=50000, random_state=46)
```

Seed 46 is Group Omega's assigned seed. Do not resample with a different seed. The
script writes:

- `data/raw/group_sample_seed46.csv`: the 50,000-review team dataset. If the file
  already exists (for example, copied from the instructor-script output in
  Downloads), the script reuses it instead of resampling.
- `data/processed/group_seed46_clean.csv`: three-class labels (1–2 negative,
  3 neutral, 4–5 positive) in a `Sentiment` column, with repeated reviews removed.
- `report/dataset_summary/`: statistics, class counts, and the Figure 1 chart.

To check a sample file someone else made, validate its columns and hash:

```powershell
python scripts/setup_data.py --kind shared --csv data/raw/group_sample_seed46.csv
```

The SHA-256 should be `b850d24da52d97eeeccf04cdc5bbddd73409afdc3d092c096189c9a26af2b89b`.

## Fields

- `Text`: full review; `Summary`: review headline. These are the model inputs.
- `Score`: 1–5 star rating, used only to derive labels. Never use it as an input feature.
- `Id`, `ProductId`, `UserId`, `ProfileName`: identifiers and reviewer information.
- `HelpfulnessNumerator`, `HelpfulnessDenominator`: helpful votes and total votes.
- `Time`: Unix timestamp.

## Repeated reviews

Two rows count as the same review when their `Summary` and `Text` match after
collapsing whitespace and ignoring case (`dedup_key()` in `scripts/prepare_sample.py`).
Use the same key when creating train/validation/test splits so a repeated review
cannot appear in more than one split.

Do not commit raw data, processed CSVs, or downloaded archives.
