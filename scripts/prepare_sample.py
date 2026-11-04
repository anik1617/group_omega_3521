"""Create a provisional uniform 50,000-row sample and measured M1 summaries."""
import collections
import csv
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[1]
SEED, SIZE = 42, 50_000


def sha256(path):
    with path.open('rb') as incoming:
        return hashlib.file_digest(incoming, 'sha256').hexdigest()


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def key(row):
    # This same normalized text pair must be used before later data splitting.
    return tuple(' '.join(row[field].split()).casefold() for field in ('Summary', 'Text'))


def main():
    source = ROOT / 'data/raw/Reviews.csv'
    rng = random.Random(SEED)
    sample = []
    with source.open(encoding='utf-8-sig', newline='') as incoming:
        reader = csv.DictReader(incoming)
        fields = reader.fieldnames
        for index, row in enumerate(reader):
            if index < SIZE:
                sample.append((index, row))
            else:
                replacement = rng.randrange(index + 1)
                if replacement < SIZE:
                    sample[replacement] = (index, row)
        source_count = index + 1
    if source_count < SIZE:
        raise ValueError('Source CSV has fewer than 50,000 rows')
    # Retain source order for stable output; selection itself is uniform without replacement.
    sample.sort(key=lambda item: item[0])
    rows = [row for _, row in sample]
    sample_path = ROOT / 'data/raw/provisional_sample_50000_seed42.csv'
    write_csv(sample_path, fields, rows)
    score_counts = collections.Counter(row['Score'] for row in rows)
    missing = {field: sum(not row[field].strip() for row in rows) for field in fields}
    placeholder_like = {field: dict(collections.Counter(
        row[field] for row in rows if row[field].strip().casefold() in {'nan', 'n/a', 'none', 'null'}
    )) for field in fields}
    placeholder_like = {field: counts for field, counts in placeholder_like.items() if counts}
    exact_keys = [(row['Summary'], row['Text']) for row in rows]
    groups = collections.defaultdict(list)
    for row in rows:
        groups[key(row)].append(row)
    binary = [row for row in rows if row['Score'] in {'1', '2', '4', '5'}]
    binary_groups = collections.defaultdict(list)
    for row in binary:
        binary_groups[key(row)].append(row)
    clean = []
    conflict_rows = duplicate_rows = blank_text_rows = 0
    for group in binary_groups.values():
        labels = {'negative' if row['Score'] in {'1', '2'} else 'positive' for row in group}
        if len(labels) > 1:
            conflict_rows += len(group)
            continue
        if not group[0]['Text'].strip():
            blank_text_rows += len(group)
            continue
        duplicate_rows += len(group) - 1
        clean.append({**group[0], 'Sentiment': labels.pop()})
    clean_path = ROOT / 'data/processed/provisional_binary_clean_seed42.csv'
    write_csv(clean_path, fields + ['Sentiment'], clean)
    report = {
        'status': 'PROVISIONAL team-created sample; instructor shared-sample approval unconfirmed',
        'source': 'https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews',
        'source_sha256': sha256(source), 'source_rows': source_count,
        'sampling': {'method': 'uniform reservoir sampling without replacement; sample before filtering',
                     'seed': SEED, 'requested_rows': SIZE, 'sample_sha256': sha256(sample_path)},
        'sample_rows': len(rows), 'score_counts': dict(sorted(score_counts.items())),
        'mean_text_words': sum(len(row['Text'].split()) for row in rows) / len(rows),
        'mean_summary_plus_text_words': sum(len((row['Summary']+' '+row['Text']).split()) for row in rows) / len(rows),
        'missing_or_whitespace_only': missing,
        'placeholder_like_strings_for_review_not_automatically_missing': placeholder_like,
        'duplicate_complete_rows_beyond_first': len(rows) - len({tuple(row[field] for field in fields) for row in rows}),
        'duplicate_exact_summary_text_beyond_first': len(rows) - len(set(exact_keys)),
        'duplicate_normalized_summary_text_beyond_first': len(rows) - len(groups),
        'invalid_score_rows': sum(value for score, value in score_counts.items() if score not in {'1','2','3','4','5'}),
        'binary_before_deduplication': dict(collections.Counter('negative' if row['Score'] in {'1','2'} else 'positive' for row in binary)),
        'neutral_rows_excluded': score_counts['3'],
        'binary_cleaning': {'conflicting_sentiment_group_rows_removed': conflict_rows,
                            'duplicate_rows_removed_after_conflict_exclusion': duplicate_rows,
                            'blank_text_rows_removed': blank_text_rows},
        'binary_clean_rows': len(clean),
        'binary_clean_class_counts': dict(collections.Counter(row['Sentiment'] for row in clean)),
        'binary_clean_mean_text_words': sum(len(row['Text'].split()) for row in clean) / len(clean),
        'binary_clean_sha256': sha256(clean_path),
        'cleaning': 'Exclude 3-star reviews; remove all binary groups with conflicting sentiment; retain first row per casefolded, whitespace-normalized Summary/Text pair. Preserve original CSV text.'
    }
    output = ROOT / 'report/dataset_summary'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'statistics.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
