# Retail Profitability & Discount Policy

Reproducible analysis of the public Tableau Sample Superstore order-line extract.

## What this repository actually supports

- 9,994 order lines covering January 2015 through December 2018
- Sales, Discount, and Profit are used as recorded in the source file
- Tables are the largest loss-making sub-category at **-$17,725**
- Bookcases are also negative at **-$3,473**
- 1,166 rows, or **11.7%**, use a discount above 30%
- Among sub-category and discount-band cells with data above 30%, 10 of 11 are negative

The recommendation is a **policy test**, not a claimed causal impact. This public dataset does not contain a counterfactual demand model, shipping cost, inventory data, or a randomized pricing experiment. Therefore the repository does not claim that a 20% cap would automatically convert furniture profit to positive.

## Source and provenance

The raw file is the public Sample Superstore dataset distributed in several public mirrors. The checked copy used here is the 21-column, 9,994-row extract with dates from 2015-01-03 to 2018-12-30.

- Dataset mirror used for reproducibility: `https://gist.githubusercontent.com/nnbphuong/38db511db14542f3ba9ef16e69d3814c/raw/Superstore.csv`
- Public GitHub mirror with the same schema: `https://github.com/leonism/sample-superstore/blob/master/data/superstore.csv`
- Original dataset listing referenced by the portfolio: `https://www.kaggle.com/datasets/vivek468/superstore-dataset-final`

The dataset is commonly called “Sample Superstore” and should not be described as proprietary data from a real retailer.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/analyze.py
```

Outputs are written to `outputs/` as CSV summaries and PNG charts.

## Analysis definition

`profit_margin = sum(Profit) / sum(Sales)`.

Discount bands are:

- `0%`
- `1-20%`
- `21-30%`
- `31-40%`
- `40%+`

Repeat-customer comparisons are descriptive only. They must not be interpreted as evidence that discounts cause or prevent repeat purchase.
