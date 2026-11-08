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
| Lianyu Yang | App Engineer |
| Shilin | ML Engineer |

## Local data setup

Python 3.11+.

```powershell
pip install -r requirements.txt
python scripts/setup_data.py
python scripts/prepare_sample.py
```

`setup_data.py` downloads the full Kaggle `Reviews.csv`. `prepare_sample.py` draws
Group Omega's 50,000-review sample with the instructor's method and our assigned
seed, 46 (`df.sample(n=50000, random_state=46)`), then writes the cleaned
three-class dataset and the summary statistics. Labels: negative (1–2 stars),
neutral (3 stars), positive (4–5 stars). See [data setup instructions](data/README.md).

## Milestone 1

- [Working charter](https://docs.google.com/document/d/1wIlXwJSuGBldoeKHOvrOfHx-uvpAIfMrQg1aW8XH1gY/edit)
- [Draft charter PDF](report/milestone1_draft.pdf)
- [Dataset measurements](report/dataset_summary/SUMMARY.md)
- [Sentiment chart](report/dataset_summary/sentiment_seed46.png)

The PDF is a draft snapshot. Check the working charter for current edits and
remaining placeholders before submission.

Live app URL: pending deployment.
Model training instructions: pending implementation.
