from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "superstore.csv"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def main():
    orders = pd.read_csv(DATA_PATH)
    numeric_cols = ["Sales", "Discount", "Profit", "Quantity"]
    orders[numeric_cols] = orders[numeric_cols].apply(pd.to_numeric, errors="coerce")
    orders["Order Date"] = pd.to_datetime(orders["Order Date"], errors="coerce")

    orders["discount_band"] = pd.cut(
        orders["Discount"],
        bins=[-0.001, 0, 0.2, 0.3, 0.4, 1],
        labels=["0%", "1-20%", "21-30%", "31-40%", "40%+"],
        include_lowest=True,
    )

    by_subcategory = (
        orders.groupby("Sub-Category", as_index=False)
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            order_lines=("Row ID", "count"),
        )
    )
    by_subcategory["margin_pct"] = 100 * by_subcategory["profit"] / by_subcategory["sales"]
    by_subcategory.sort_values("profit").to_csv(
        OUTPUT_DIR / "profitability_by_subcategory.csv", index=False
    )

    by_band = (
        orders.groupby(["Sub-Category", "discount_band"], observed=True, as_index=False)
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            order_lines=("Row ID", "count"),
        )
    )
    by_band["margin_pct"] = 100 * by_band["profit"] / by_band["sales"]
    by_band.to_csv(OUTPUT_DIR / "profitability_by_discount_band.csv", index=False)

    ax = by_subcategory.sort_values("profit").plot.barh(
        x="Sub-Category", y="profit", legend=False, color="#b45309", figsize=(9, 6)
    )
    ax.set_title("Profit by sub-category")
    ax.set_xlabel("Profit")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "profit_by_subcategory.png", dpi=160)
    plt.close()

    print(f"rows={len(orders)}")
    print(f"date_min={orders['Order Date'].min().date()}")
    print(f"date_max={orders['Order Date'].max().date()}")
    print(f"discount_above_30_pct={100 * (orders['Discount'] > 0.30).mean():.2f}")
    print(by_subcategory.sort_values("profit").head(5).to_string(index=False))


if __name__ == "__main__":
    main()
