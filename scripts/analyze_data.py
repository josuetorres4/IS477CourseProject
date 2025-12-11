import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    project_root = Path(__file__).resolve().parents[1]
    cleaned_dir = project_root / "data" / "cleaned"
    results_dir = project_root / "results"
    results_dir.mkdir(exist_ok=True)

    summary_path = cleaned_dir / "community_summary.csv"
    print(f"Reading community summary from: {summary_path}")

    df = pd.read_csv(summary_path)
    if "median_income_proxy" in df.columns and "median_income" not in df.columns:
        df = df.rename(columns={"median_income_proxy": "median_income"})

    if "median_income" not in df.columns:
        raise ValueError("No median_income or median_income_proxy column in community_summary.csv")


    df["price_to_income"] = df["median_listing_price"] / df["median_income"]

    corr = df[["median_listing_price", "median_income"]].corr().iloc[0, 1]
    print(f"Correlation (median listing price vs median income): {corr:.3f}")

    top5 = df.sort_values("price_to_income", ascending=False).head(5)
    bottom5 = df.sort_values("price_to_income", ascending=True).head(5)

    print("\nTop 5 least affordable (highest price-to-income):")
    print(top5[["Community Area", "median_listing_price", "median_income", "price_to_income"]])

    print("\nTop 5 most affordable (lowest price-to-income):")
    print(bottom5[["Community Area", "median_listing_price", "median_income", "price_to_income"]])

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df,
        x="median_income",
        y="median_listing_price"
    )
    plt.title("Median Listing Price vs. Median Income by Community Area")
    plt.xlabel("Estimated Median Income (USD)")
    plt.ylabel("Median Listing Price (USD)")
    scatter_path = results_dir / "price_vs_income_scatter.png"
    plt.tight_layout()
    plt.savefig(scatter_path, dpi=150)
    plt.close()
    print(f"Saved scatter plot to: {scatter_path}")


    df_sorted = df.sort_values("price_to_income", ascending=False)

    plt.figure(figsize=(10, 14))
    sns.barplot(
        data=df_sorted,
        x="price_to_income",
        y="Community Area"
    )
    plt.title("Price-to-Income Ratios by Community Area")
    plt.xlabel("Price-to-Income Ratio (higher = less affordable)")
    plt.ylabel("Community Area")
    bar_path = results_dir / "price_to_income_bar.png"
    plt.tight_layout()
    plt.savefig(bar_path, dpi=150)
    plt.close()
    print(f"Saved price-to-income bar chart to: {bar_path}")

    print("analyze_data.py finished successfully.")

if __name__ == "__main__":
    main()
