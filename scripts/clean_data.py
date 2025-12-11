import pandas as pd
import re
from pathlib import Path


def main():

    project_root = Path(__file__).resolve().parents[1]

    raw_dir = project_root / "data" / "raw"
    cleaned_dir = project_root / "data" / "cleaned"
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    real_estate_path = raw_dir / "real_estate_data_chicago.csv"
    acs_path = raw_dir / "ACS_5_Year_Data_by_Community_Area.csv"

    print(f"Reading real estate from: {real_estate_path}")
    print(f"Reading ACS from:          {acs_path}")


    real_estate_df = pd.read_csv(real_estate_path)
    ACS_df = pd.read_csv(acs_path)

    print(f"Real estate shape: {real_estate_df.shape}")
    print(f"ACS shape:         {ACS_df.shape}")

    income_midpoints = {
        "Under $25,000": 12500,
        "$25,000 to $49,999": 37500,
        "$50,000 to $74,999": 62500,
        "$75,000 to $125,000": 100000,
        "$125,000 +": 150000,
    }

    for col in income_midpoints.keys():
        if col not in ACS_df.columns:
            raise KeyError(f"Expected income column '{col}' not found in ACS data.")
        ACS_df[col] = pd.to_numeric(ACS_df[col], errors="coerce")

    numerator = sum(ACS_df[col] * income_midpoints[col] for col in income_midpoints)
    denominator = sum(ACS_df[col] for col in income_midpoints)
    ACS_df["median_income_proxy"] = numerator / denominator

    print("Added ACS column: median_income_proxy")

    if "text" not in real_estate_df.columns:
        raise KeyError("Expected a 'text' column in real_estate_df for address/community extraction.")

    areas = (
        ACS_df["Community Area"]
        .dropna()
        .astype(str)
        .str.strip()
        .unique()
        .tolist()
    )

    areas_sorted = sorted(areas, key=len, reverse=True)

    pat = re.compile(
        r"\b(" + "|".join(map(re.escape, areas_sorted)) + r")\b",
        flags=re.IGNORECASE,
    )
    canon = {a.lower(): a for a in areas}

    def extract_area(s: str):
        if isinstance(s, str):
            m = pat.search(s)
            if m:
                return canon.get(m.group(1).lower())
        return None

    real_estate_df["Community Area"] = real_estate_df["text"].apply(extract_area)

    mapped_rows = real_estate_df["Community Area"].notna().sum()
    unique_areas = real_estate_df["Community Area"].dropna().nunique()
    print(f"Mapped community area for {mapped_rows} listings "
          f"across {unique_areas} unique community areas.")

    if "listPrice" not in real_estate_df.columns:
        raise KeyError("[ERROR] Expected 'listPrice' column in real_estate_df.")

    real_estate_df["listPrice"] = (
        real_estate_df["listPrice"]
        .astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .pipe(pd.to_numeric, errors="coerce")
    )

    print(f"listPrice dtype after cleaning: {real_estate_df['listPrice'].dtype}")

    real_clean_path = cleaned_dir / "real_estate_clean.csv"
    acs_clean_path = cleaned_dir / "ACS_clean.csv"

    real_estate_df.to_csv(real_clean_path, index=False)
    ACS_df.to_csv(acs_clean_path, index=False)

    print(f"Saved cleaned real estate data to: {real_clean_path}")
    print(f"Saved cleaned ACS data to:         {acs_clean_path}")
    print("clean_data.py finished successfully.")


if __name__ == "__main__":
    main()

