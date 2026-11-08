"""Build Group Omega's course sample (seed 46) and the M1 dataset summary.

Sampling follows the instructor's script exactly:
    pd.read_csv(Reviews.csv).sample(n=50000, random_state=46)

Outputs:
    data/raw/group_sample_seed46.csv        the team dataset (do not resample)
    data/processed/group_seed46_clean.csv   three-class labels, repeats removed
    report/dataset_summary/statistics.json  measured statistics and hashes
    report/dataset_summary/class_counts.csv sentiment counts before/after cleaning
    report/dataset_summary/sentiment_seed46.png  Figure 1 for the charter
"""
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SEED, SIZE = 46, 50_000
SOURCE = ROOT / 'data/raw/Reviews.csv'
SAMPLE = ROOT / f'data/raw/group_sample_seed{SEED}.csv'
CLEAN = ROOT / f'data/processed/group_seed{SEED}_clean.csv'
OUT = ROOT / 'report/dataset_summary'
LABELS = ['negative', 'neutral', 'positive']


def sha256(path):
    with path.open('rb') as incoming:
        return hashlib.file_digest(incoming, 'sha256').hexdigest()


def sentiment(score):
    return 'negative' if score <= 2 else 'neutral' if score == 3 else 'positive'


def dedup_key(df):
    # Reuse this exact key when splitting so repeated reviews stay in one split.
    def norm(column):
        return df[column].fillna('').astype(str).str.split().str.join(' ').str.casefold()
    return norm('Summary') + '\x1f' + norm('Text')


def counts(series):
    return {label: int((series == label).sum()) for label in LABELS}


def main():
    if not SAMPLE.exists():
        sample = pd.read_csv(SOURCE).sample(n=SIZE, random_state=SEED)
        sample.to_csv(SAMPLE, index=False)
    # Read back from disk so statistics describe the file teammates will load.
    df = pd.read_csv(SAMPLE)
    if len(df) != SIZE:
        raise ValueError(f'Expected {SIZE} rows, found {len(df)}')

    df['Sentiment'] = df['Score'].map(sentiment)
    key = dedup_key(df)
    labels_per_key = df.groupby(key)['Sentiment'].nunique()
    conflicting = key.map(labels_per_key) > 1
    kept = df[~conflicting & ~key.duplicated(keep='first') & df['Text'].notna()]
    CLEAN.parent.mkdir(parents=True, exist_ok=True)
    kept.to_csv(CLEAN, index=False)

    text_words = df['Text'].fillna('').str.split().str.len()
    stats = {
        'group': 'Omega', 'seed': SEED,
        'method': 'pd.read_csv(Reviews.csv).sample(n=50000, random_state=46), per instructor script',
        'source': 'https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews',
        'source_sha256': sha256(SOURCE), 'sample_sha256': sha256(SAMPLE),
        'sample_rows': len(df),
        'score_counts': {str(k): int(v) for k, v in df['Score'].value_counts().sort_index().items()},
        'sentiment_counts': counts(df['Sentiment']),
        'mean_text_words': float(text_words.mean()),
        'median_text_words': float(text_words.median()),
        'missing_values_as_read_by_pandas': {c: int(v) for c, v in df.isna().sum().items() if v},
        'invalid_score_rows': int((~df['Score'].isin([1, 2, 3, 4, 5])).sum()),
        'duplicate_rows_ignoring_id': int(df.drop(columns=['Id', 'Sentiment']).duplicated().sum()),
        'repeated_summary_text_beyond_first': int(key.duplicated().sum()),
        'rows_in_conflicting_label_groups_removed': int(conflicting.sum()),
        'clean_rows': len(kept),
        'clean_sentiment_counts': counts(kept['Sentiment']),
        'clean_mean_text_words': float(kept['Text'].str.split().str.len().mean()),
        'clean_sha256': sha256(CLEAN),
        'cleaning': 'Labels: 1-2 negative, 3 neutral, 4-5 positive. Drop every row whose '
                    'normalized Summary+Text has conflicting labels; keep the first row of '
                    'other repeats; drop rows with missing Text.',
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'statistics.json').write_text(json.dumps(stats, indent=2) + '\n', encoding='utf-8')

    rows = []
    for stage, data in [('sample', stats['sentiment_counts']), ('clean', stats['clean_sentiment_counts'])]:
        total = sum(data.values())
        rows += [{'stage': stage, 'sentiment': k, 'count': v, 'percent': round(100 * v / total, 2)}
                 for k, v in data.items()]
    pd.DataFrame(rows).to_csv(OUT / 'class_counts.csv', index=False)

    values = list(stats['sentiment_counts'].values())
    fig, ax = plt.subplots(figsize=(7, 3), layout='constrained')
    bars = ax.bar(['Negative (1–2 stars)', 'Neutral (3 stars)', 'Positive (4–5 stars)'], values,
                  color=['#b34b48', '#929292', '#3d7c68'], width=0.55)
    ax.bar_label(bars, labels=[f'{v:,} ({v / SIZE:.2%})' for v in values], padding=4, fontsize=10)
    ax.set_ylim(0, max(values) * 1.18)
    ax.set_ylabel('Reviews')
    ax.set_title(f'Sentiment distribution: Group Omega sample (seed {SEED}, 50,000 reviews)')
    ax.spines[['top', 'right']].set_visible(False)
    fig.savefig(OUT / f'sentiment_seed{SEED}.png', dpi=180)

    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
