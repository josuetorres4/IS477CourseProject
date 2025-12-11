# Income, Listings, and Inequality: A Community Level View of Chicago's Housing Market

## Contributors
- Josue Torres


## Summary
Housing affordability is a central concern in many large U.S. cities, and Chicago is no exception. 
The city’s 77 community areas show wide variation in both income levels and housing markets, 
reflecting historical patterns of segregation, disinvestment, and gentrification. This project 
investigates how housing prices and income distributions relate across Chicago’s community areas, 
with a focus on identifying where homes are relatively more or less affordable given estimated community level incomes.

To address this, I combined a Chicago real estate listings dataset (`real_estate_data_chicago.csv`) with American Community Survey (ACS) 
5-year estimates by community area (`ACS_5_Year_Data_by_Community_Area.csv`). The real estate data provides around 2,000 residential listings 
across the city, including list prices and textual descriptions that contain the community area name. The ACS dataset provides population, race/ethnicity, 
and a breakdown of households by income brackets (example:, “Under $25,000”, “$25,000 to $49,999”, etc.) for each community area.

Because the ACS file does not include a direct median income variable, I created a median income proxy by assigning midpoints to each income bracket 
(e.g., \$12,500 for “Under \$25,000”, \$37,500 for “\$25,000 to \$49,999”, etc.) and computing a weighted average based on the number of households in each 
bracket. This produces an approximate central income value for each community area that can be used in affordability metrics.

On the real estate side, I used regular expressions to extract community area names from the `text` column of the listings data and mapped them to canonical 
names from the ACS file (example:“LOGAN SQUARE”, “ENGLEWOOD”). Each listing was then assigned a `Community Area` and its `listPrice` was cleaned into a numeric 
`float` field by stripping currency symbols and commas. A **many to one merge** between listings and ACS data attached demographic attributes to each listing 
based on its community area.

From this enriched dataset, I collapsed the data to the community level by computing, for each community area, the number of listings, the median listing price, 
and the mean listing price. These summary statistics were then joined with the median income proxy to compute a simple price to income ratio as a proxy for 
affordability. Higher ratios indicate less affordable areas (homes are expensive relative to community income), while lower ratios indicate relatively more affordable areas.

Preliminary results show a clear and intuitive pattern: wealthier community areas generally have higher housing prices, but the relationship is not perfectly uniform. 
Some community areas such as Humboldt Park, Hermosa, Oakland, West Town, and Douglas emerge with very high price to income ratios, suggesting that housing costs are 
especially burdensome relative to local incomes. On the other end of the spectrum, community areas like Fuller Park, Englewood, Greater Grand Crossing, Roseland, and 
West Englewood have low ratios, meaning that median listing prices are lower relative to estimated community income, although these are also areas that face long standing 
disinvestment and other structural barriers.

The analysis highlights that “affordability” is not purely a function of price but it is a relationship between income, price, and broader neighborhood context. 
By integrating real estate and ACS data and summarizing at the community level, this project provides an interpretable view of where housing might be considered 
relatively more or less affordable across Chicago, and it creates a reproducible workflow that can be extended with additional variables or updated data in the future.

## Data Profile
### Real Estate Listings: `real_estate_data_chicago.csv`
- Source: City of Chicago / public real estate data (specifically Realtor.com). But I personally found this dataset on kaggle.
- Format: CSV.  
- Key fields:
  - `text`: Free-text field containing address, community area name, and other details.
  - `listPrice`: Listing price for the property (string with currency formatting).
  - Additional attributes such as property type, bedrooms, bathrooms, and potentially latitude/longitude (not all features used in the final analysis).
 
    This dataset contains approximately 2,000 rows and 16 columns. It represents a snapshot of Chicago residential listings, not a full census of
    all properties. Some rows are duplicated (2 duplicates were identified), and not all listings contain detectable community area information within the
    `text` field. After processing, 67 unique community areas are represented among the listings.

    **Provenance & License:**  
    The data are derived from the **City of Chicago’s open data** infrastructure.
    The City’s data portal and FOIA related resources explicitly note that these datasets are provided under an open data license for
    public reuse, with appropriate attribution. No personally identifiable information about individual property owners is used in this project,
    the analysis is conducted at the community area level. The kaggle owner states "Using an APIFY based API after target state/city selection.
    ethically mined and personal details removed to ensure data privacy."



### ACS 5-Year Community Area Data: `ACS_5_Year_Data_by_Community_Area.csv`
- Source: U.S. Census Bureau, American Community Survey (ACS) 5-Year Estimates, aggregated to Chicago’s 77 community areas. But I personally found this dataset on kaggle.
- Format: CSV.
- Key fields:
  - `ACS Year`: Year of the estimate, 2023 in this dataset.
  - `Community Area`: Name of the community area (examples: “ALBANY PARK”, “LINCOLN PARK”).
  - Income distribution fields: `Under $25,000`, `$25,000 to $49,999`, `$50,000 to $74,999`, `$75,000 to $125,000`, `$125,000 +` (counts of households in each bracket).
  - Demographic breakdowns: `Total Population`, `White`, `Black or African American`, `Asian`, `Hispanic or Latino`, etc.
  - `Record ID`: A unique identifier combining year and community area.

This dataset contains 77 rows (one per community area) and 30 columns. It does not directly include a median income column, so
income distribution is used to derive a proxy. All counts were converted to numeric and checked for missing values.

**Provenance & License:**
The ACS data are provided by the U.S. Census Bureau and are considered public domain. The Bureau’s terms of service permit 
reuse with appropriate attribution. The dataset is fully aggregated and contains no Personally Identifiable Information.

### Ethical, Legal, and Policy Considerations

- **Privacy:** Both datasets are aggregated or public records; no individual level sensitive information is exposed in the analysis.
- **Consent:** Data are collected and published by public agencies (City of Chicago, U.S. Census Bureau) under established legal frameworks.
- **Bias:** ACS and listing data reflect structural inequalities and sampling limitations. Results are interpreted descriptively rather than as causal claims.
- **Sharing:** The processed outputs (example: merged data, summary tables) are shared via a Box folder for grading, with paths documented below.

## Data Quality 
### Real Estate Data Quality

- **Shape:** 2,000 rows and 16 columns.
- **Duplicates:** 2 fully duplicated rows were identified. But they didn't affect the communtiy level meidans but can be dropped if desired
- **Missingness:**   - The `listPrice` column had some non-numeric entries (e.g., currency symbols, commas).
- These were cleaned using a regex replacement and converted to numeric with `errors="coerce"`, which results in `NaN` for unparseable values.
  The `text` field is present for all listings, but not all texts contain a recognizable community area name.
- **Comunity Area Coverage:** 67 unique community areas were successfully mapped from the real estate data but after text extraction
- The ACS data cover all 77 community areas which means that 10 areas have ACS information but no listings.

  The mapping from listings to community areas was implemented by building a list of community area names from
  `ACS_df["Community Area"]`, constructing a case insensitive regex, and searching each `text` field for a match.
  A small number of listings remained unmatched, either because their `text` did not contain a clean community area name or
  used unconventional wording.

  ### ACS Data Quality

- **Shape:** 77 rows and 30 columns.
- **Duplicates:** 0 duplicate rows.
- **Missingness:** Income bracket fields were successfully converted to numeric.
- No critical fields (community area or total population) were missing.
- **Deriving Median Income Proxy:**
- Brackets were assigned midpoints of \$12,500, $37,500, $62,500, $100,000, and $150,000 respectively.
- For each community area, a weighted mean of these midpoints was computed, using the household counts as weights.
- This yielded a continuous `median_income_made` proxy.
- The proxy is an approximation, it assumes relatively uniform distribution within brackets and caps the highest bracket at $150,000.

### Integrated Dataset
- **Listings enriched:** After merging `real_estate_df` and `ACS_df` on `Community Area`, `listings_enriched` contains
- around 2,000 rows one per listing with ACS demographics repeated for each listing in that community.
- **Community level summary:** Grouping by `Community Area` and aggregating created `community_summary`,
- with one row per area and the following fields:
  - `n_listings`
  - `median_listing_price`
  - `mean_listing_price`
  - `median_income` (renamed proxy)
  - `price_to_income` (computed ratio)

Data consistency checks included verifying that all 66–67 communities in `community_summary` are valid ACS community names 
and confirming that price and income fields were numeric and non-negative. Outlier checks suggest that very high median listing prices in a few areas (examples: West Town, Lincoln Park, the Loop) are real reflections of expensive markets rather than data errors.

## Findings 

The main goal of the analysis was to understand how housing prices relate to community level incomes across Chicago, 
and which community areas appear relatively more or less affordable.

### Community Level Price and Income

For each community area with at least one listing, I computed:

- `median_listing_price`: the median list price across all listings in that community.
- `median_income`: the estimated median income proxy derived from ACS income brackets.
- `price_to_income`: a ratio of `median_listing_price / median_income`.

This ratio provides a simple proxy for affordability: a higher ratio suggests that home prices in that community are high relative to the typical income, 
while a lower ratio suggests relatively more affordable housing.

### Least Affordable Communities (Highest Price to Income Ratios)

The top five community areas by price to income ratio were:

1. **Humboldt Park** – median listing price ~ $589,450; median income ~ $68,000; ratio ~ 8.67  
2. **Oakland** –  $454,000 vs ~  $59,000; ratio ~ 7.63  
3. **Hermosa** – ~ $597,500 vs ~ $79,500; ratio ~ 7.51  
4. **West Town** – ~ $850,000 vs ~ $119,800; ratio ~ 7.10  
5. **Douglas** – ~ $517,000 vs ~ $73,300; ratio ~ 7.05  

These areas appear least affordable by this measure: residents would, on average, need several multiples of their annual income to match local 
listing prices. Some of these areas (example: West Town, parts of Humboldt Park) are known to be undergoing gentrification, which may help explain high 
prices relative to existing community income.

### Most Affordable Communities (Lowest Price to Income Ratios)

The bottom five areas by price to income ratio were:

1. **Fuller Park** – median listing ~ $25,000; income ~ $46,540; ratio ~ 0.54  
2. **Englewood** – $55,000; income ~ $51,000; ratio ~ 1.08  
3. **Greater Grand Crossing** – $79,400; income ~ $58,378; ratio ~ 1.36  
4. **Roseland** – $95,000; income ~ $68,879; ratio ~ 1.38  
5. **West Englewood** – $99,900; income ~ $55,827; ratio ~ 1.79  

These communities have low listing prices relative to income, suggesting that homes are more “affordable” in a narrow financial sense. 
However, many of these areas also face high levels of disinvestment, lower access to amenities, and higher exposure to other forms of risk, 
which are not captured in this simple metric.

### Visual Findings
<img width="1190" height="1490" alt="ACS(5-year data)" src="https://github.com/user-attachments/assets/aec6114c-406b-4b31-bcff-d2c0a4e48d33" />
A horizontal bar chart of estimated median income by community area clearly shows a wide spread between high income and low income neighborhoods. 
Overlaying or comparing this with median listing prices by community highlights both alignments (high income = high price) and misalignments 
(relatively low income but elevated prices). Overall, the analysis supports the intuition that income and housing prices are positively related across 
Chicago, but also emphasizes that affordability is uneven, with some communities facing particularly high housing burdens relative to their incomes.

## Future Work
There are several avenues that I can go in to extend and deepen this project such as:

1. **Temporal Dimension:**  
   The current analysis is cross sectional, using a single snapshot of listings and ACS estimates for 2023.
   A natural extension would be to incorporate multiple years of sales or listing data to study trends in affordability over time,
   identifying where prices are rising fastest relative to income.

2. **Spatial Precision:**  
   The current community assignment is based on text extraction of community names. If latitude/longitude are available,
   a more precise spatial join using community polygon boundaries (from the City of Chicago’s GIS datasets possibly)
   would improve matching for listings whose `text` field does not clearly name a community area.

3. **Rental Market and Tenure:**  
  This project focuses on listing prices for ownership. Adding rental data, along with owner versus renter proportions from ACS,
  would provide a more comprehensive picture of housing affordability, especially in renter heavy communities.

4. **Additional Socioeconomic Variables:**  
   The ACS data include race/ethnicity, age structure, and poverty indicators. Future analysis could assess how high price to income
   ratios intersect with demographics, potentially highlighting equity concerns and the uneven impact of housing market pressure across
   different communities.

5. **Robust Affordability Metrics:**  
   More nuanced affordability measures such as the share of households that would be cost burdened by median prices, or debt service ratios using typical mortgage assumptions could provide a more realistic view than a simple price to income ratio.















