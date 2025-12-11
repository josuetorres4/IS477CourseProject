
import pandas as pd
from pathlib import Path


def main():
    base_dir = Path(__file__).resolve().parents[1]

    cleaned_dir = base_dir / "data" / "cleaned"

    real_estate_clean_path = cleaned_dir / "real_estate_clean.csv"
    acs_clean_path = cleaned_dir / "ACS_clean.csv"

    if not real_estate_clean_path.exists():
        raise FileNotFoundError(f"Missing cleaned real estate file: {real_estate_clean_path}")
    if not acs_clean_path.exists():
        raise FileNotFoundError(f"Missing cleaned ACS file: {acs_clean_path}")

    print(f"Reading cleaned real estate from: {real_estate_clean_path}")
    print(f"Reading cleaned ACS from:         {acs_clean_path}")

    real_estate_df = pd.read_csv(real_estate_clean_path)
    ACS_df = pd.read_csv(acs_clean_path)

    print(f"Real estate shape (cleaned): {real_estate_df.shape}")
    print(f"ACS shape (cleaned):         {ACS_df.shape}")

    listings_enriched = real_estate_df.merge(ACS_df, on="Community Area", how="left")

    print(f"Listings enriched shape: {listings_enriched.shape}")
    mapped = listings_enriched["Community Area"].notna().sum()
    print(f"Listings with mapped community area: {mapped}")

    community_summary = (
        listings_enriched
        .dropna(subset=["Community Area", "listPrice"])
        .groupby("Community Area", as_index=False)
        .agg(
            n_listings=("listPrice", "size"),
            median_listing_price=("listPrice", "median"),
            mean_listing_price=("listPrice", "mean"),
        )
    )

    if "median_income_proxy" in ACS_df.columns:
        community_summary = community_summary.merge(
            ACS_df[["Community Area", "median_income_proxy"]],
            on="Community Area",
            how="left"
        )
        community_summary = community_summary.rename(
            columns={"median_income_proxy": "median_income"}
        )

    listings_enriched_path = cleaned_dir / "listings_enriched.csv"
    community_summary_path = cleaned_dir / "community_summary.csv"

    listings_enriched.to_csv(listings_enriched_path, index=False)
    community_summary.to_csv(community_summary_path, index=False)

    print(f"Saved listings_enriched to: {listings_enriched_path}")
    print(f"Saved community_summary to: {community_summary_path}")
    print("integrate_data.py finished successfully.")


if __name__ == "__main__":
    main()

