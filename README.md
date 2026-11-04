# Group Omega — CSE 3521

Amazon food review sentiment analysis project. Planned deliverables include text
feature engineering, classical and deep/modern model comparisons, and a deployed
Streamlit application. Models and the application are not implemented yet.

## Team

| Member | Primary role |
| --- | --- |
| Aniket Chaudhari | Project Lead |
| Sophiya Khurana | Data Engineer / Writer |
| Ethan Brown | Data Engineer / Writer |
| Lianyu Yang | App Engineer / Writer |
| Shilin | ML Engineer |

## Local data setup

Python 3.11+; no third-party packages needed for data setup.

```powershell
python scripts/setup_data.py
```

See [data setup instructions](data/README.md) for validating the instructor's shared
sample. The full Kaggle download is separate from the required shared sample.

To reproduce the provisional 50,000-review sample and summary statistics:

```powershell
python scripts/prepare_sample.py
```

The sample uses seed 42 and still needs instructor approval. The charter plans
three classes: negative (1–2 stars), neutral (3 stars), and positive (4–5 stars).
The script also produces a separate binary dataset from an earlier exploration;
that file excludes neutral reviews and is not the three-class training dataset.

## Milestone 1

- [Working charter](https://docs.google.com/document/d/1wIlXwJSuGBldoeKHOvrOfHx-uvpAIfMrQg1aW8XH1gY/edit)
- [Draft charter PDF](report/milestone1_draft.pdf)
- [Dataset measurements](report/dataset_summary/SUMMARY.md)
- [Three-class sample chart](report/dataset_summary/sentiment_sample_50000.png)

The PDF is a draft snapshot. Check the working charter for current edits and
remaining placeholders before submission.

Live app URL: pending deployment.
Model training instructions and pinned dependencies: pending implementation.
