"""Download the full Kaggle CSV or validate an instructor-provided CSV sample."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://www.kaggle.com/api/v1/datasets/download/snap/amazon-fine-food-reviews'
COLUMNS = ['Id', 'ProductId', 'UserId', 'ProfileName', 'HelpfulnessNumerator',
           'HelpfulnessDenominator', 'Score', 'Time', 'Summary', 'Text']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, help='Existing Reviews.csv or instructor sample')
    parser.add_argument('--kind', choices=['full', 'shared'], default='full')
    args = parser.parse_args()
    if args.kind == 'shared' and args.csv is None:
        parser.error('--kind shared requires --csv pointing to the instructor sample')
    raw = ROOT / 'data' / 'raw'
    raw.mkdir(parents=True, exist_ok=True)
    source = args.csv.resolve() if args.csv else raw / 'Reviews.csv'
    if args.csv is None and not source.exists():
        archive = raw / 'amazon-fine-food-reviews.zip'
        if not archive.exists():
            partial = archive.with_suffix('.zip.part')
            print('Downloading full Kaggle archive (~254 MB)...', flush=True)
            with urllib.request.urlopen(URL, timeout=60) as response, partial.open('wb') as target:
                shutil.copyfileobj(response, target)
            partial.replace(archive)
        with zipfile.ZipFile(archive) as bundle:
            candidates = [n for n in bundle.namelist() if Path(n).name == 'Reviews.csv']
            if len(candidates) != 1:
                raise ValueError('Expected exactly one Reviews.csv in the archive')
            partial = source.with_suffix('.csv.part')
            with bundle.open(candidates[0]) as incoming, partial.open('wb') as target:
                shutil.copyfileobj(incoming, target)
            partial.replace(source)
    with source.open('rb') as incoming:
        digest = hashlib.file_digest(incoming, 'sha256').hexdigest()
    with source.open(encoding='utf-8-sig', newline='') as incoming:
        reader = csv.DictReader(incoming)
        missing = set(COLUMNS) - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'Missing CSV columns: {sorted(missing)}')
        count = sum(1 for _ in reader)
    print(json.dumps({'csv': str(source), 'kind': args.kind, 'rows': count,
                      'sha256': digest,
                      'sentiment_mapping': 'NOT SELECTED; Score is the raw star rating'},
                     indent=2), flush=True)



if __name__ == '__main__':
    main()
