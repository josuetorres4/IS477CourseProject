# (MS3): Status Report

## 1. Project Overview 
The goal of this project is to explore how housing listing prices vary across Chicago community areas and how those differences relate to income distributions by community area. The working research question is:
**How do housing listing prices vary across Chicago community areas, and how do those patterns relate to income distributions (ACS) across the same areas?**

At this milestone, I have successfully loaded both datasets, extracted community area labels for a subset of listings, cleaned and standardized listing price values, and generated a community level summary table with pricing statistics. I have also built an estimated income proxy from ACS income brackets to enable affordability style metrics (price to income ratio). All work so far was developed and executed in VSCode.

Key outputs at this stage:
- Listing level data cleaned and enriched with community areas (partial coverage)
- Community level summary of listing counts and median/mean listing prices by area
- Income proxy created from ACS bracket counts
- Early affordability proxy using price to income ratio
- One exploratory visualization (income proxy by community area)

## 2. Data Sources and Current Data Handling
1) **Real estate listings dataset**
- File: `real_estate_data_chicago.csv`
- Size: 2000 rows, 16 columns
- Key fields used: `text` (listing description), `listPrice` (listing price)

2) **ACS 5-Year dataset by Chicago community area**
- File: `ACS_5_Year_Data_by_Community_Area.csv` 
- Size: 77 rows, 30 columns
- Key fields used: `Community Area`, income bracket columns such as:
  - `Under $25,000`, `$25,000 to $49,999`, `$50,000 to $74,999`, `$75,000 to $125,000`, `$125,000 +`

### Storage and Organization 
At this milestone, the project was still being developed primarily through interactive exploration in VSCode. Data files were stored locally and referenced via relative paths. The organization plan was being prepared but not fully implemented (example: separating `/data/raw` and `/data/cleaned` folders and moving code into scripts).

## 3. Progress on Project Plan Tasks (with evidence/artifacts)
This section maps progress to major tasks described in the Project Plan.

### Task A — Data Acquisition & Loading (Complete)
I successfully loaded both datasets using pandas:
- `real_estate_data_chicago.csv`
- `ACS_5_Year_Data_by_Community_Area.csv`

Evidence: code cells in `IS477CourseProject.ipynb` show data loading with `pd.read_csv()` and inspection of dataframes.

Current dataset shapes:
- Real estate: **(2000, 16)**
- ACS: **(77, 30)**

### Task B — Data Cleaning (In Progress)
Cleaning actions completed so far:
- Standardized `listPrice` to numeric:
  - removed `$` and `,`
  - coerced non numeric values to NaN
- Basic dataset checks:
  - duplicates counted
  - community area coverage counted

Quality checks performed:
- Real estate duplicates: **2**
- ACS duplicates: **0**

Evidence: printed outputs and cleaning logic in the notebook.

Remaining cleaning work:
- Decide how to handle missing/invalid prices
- Standardize any other key numeric fields used later
- Add explicit missingness profile table for report

### Task C — Data Integration / Joining Datasets (In Progress)
The integration challenge was that the ACS dataset includes a clean `Community Area` column, but the real estate dataset does not include a direct community area field. Instead, real estate listings have a `text` column that sometimes contains the community area name.

I implemented a regex based extraction approach:
- created a list of all community areas from ACS
- compiled a case insensitive regex pattern
- extracted the first community area name found in each listing’s `text`

Result:
- Listings mapped to a community area: **886 listings**
- Unique mapped community areas: **67**
- Total ACS community areas: **77**

This means the join works for a subset of listings where the community area name appears in text. It also means that 114 of the 2000 listings were matched in text, and 10 community areas do not appear in the matched listings at all.

Evidence:
- `listings_enriched = real_estate_df.merge(ACS_df, on="Community Area", how="left")`
- printed output:
  - Rows (listings_enriched): **2000**
  - Mapped areas: **886**
 
Remaining integration work:
- Improve the mapping coverage (e.g., handle alternate spellings or add a fallback method)
- Ensure the extraction logic does not incorrectly match partial names or irrelevant text strings

### Task D — Data Enrichment: Income Proxy (Complete)
The ACS dataset does not include a single “median income” column. To support affordability style comparisons, I created an **income proxy** from the bracket counts using midpoints:

- Under $25k → 12,500  
- $25k–$49,999 → 37,500  
- $50k–$74,999 → 62,500  
- $75k–$125k → 100,000  
- $125k+ → 150,000

Then computed:
`median_income_made = (sum(count_i * midpoint_i)) / (sum(count_i))`

This produces a community-level estimated income proxy for every one of the 77 community areas.

Evidence:
- `ACS_df["median_income_made"]` column created in notebook.

### Task E — Analysis / Early Findings (In Progress)
Using the matched and cleaned listings, I created a community level summary:

- `n_listings`
- `median_listing_price`
- `mean_listing_price`

This produced **66 community areas** with at least one listing and valid price.

I also computed a price to income ratio proxy:
`price_to_income = median_listing_price / median_income`

Preliminary result examples:
- **Least affordable (highest ratio):**
  - Humboldt Park (~8.67)
  - Oakland (~7.63)
  - Hermosa (~7.51)
  - West Town (~7.10)
  - Douglas (~7.05)

- **Most affordable (lowest ratio):**
  - Fuller Park (~0.54)
  - Englewood (~1.08)
  - Greater Grand Crossing (~1.36)
  - Roseland (~1.38)
  - West Englewood (~1.79)

This is a preliminary metric and should be treated carefully. It depends on (1) correct community matching in text and (2) income proxy assumptions.

Evidence:
- printed “Top 5 least affordable” and “Top 5 most affordable” tables
- community summary dataframe shown in notebook output

### Task F — Visualization (Started)
I generated a bar chart showing estimated income proxy by community area:

- Figure output: `CommunityAndSalary.png` 

Evidence:
- seaborn barplot code and generated plot

Remaining visualization work:
- Add a scatter plot of median listing price vs income proxy
- Improve readability (top/bottom subsets)

## 4. Changes to Project Plan (and response to feedback)
The original plan assumed a straightforward join on community area. After examining the datasets, I learned that the real estate file does not include community area as a structured field. The only usable location reference for community area was embedded in free text. This required changing the integration strategy.

**Plan changes:**
- Added a new integration step: community area extraction from listing text using regex
- Added a derived variable step: compute income proxy from income brackets because ACS does not provide a single median income column
- Reprioritized analysis to first build community level aggregates after mapping rather than attempting listing-level modeling immediately

**Feedback response (Milestone 2):**
Based on feedback, I focused on improving reproducibility and clarity by:
- explicitly reporting mapping coverage (886 mapped listings across 67 areas)
- explicitly reporting data shapes and duplicates
- documenting that the “median income” is a proxy derived from brackets rather than a direct ACS column

## 5. Updated Timeline (Milestone 3 → Final)
| Task | Status (now) | Planned completion |
| Data acquisition & loading | Complete | Done |
| Cleaning (prices, missingness profile) | Complete |
| Integration (improve mapping coverage) | Complete |
| Community-level analysis + correlation | Complete |
| Visualizations (price vs income, affordability plots) | Complete |
| Workflow automation / scripts | Complete |
| Final README report writing | Complete |
| Final submission (tag + release) | Complete |

## 6. Contributions
**Josue Torres:**  
- Everything. Loaded both datasets, cleaned listing prices, built income proxy from ACS. 





