import pandas as pd
import re

real_estate_df = pd.read_csv("real_estate_data_chicago.csv")
real_estate_df


ACS_df = pd.read_csv("ACS_5_Year_Data_by_Community_Area.csv")
ACS_df

areas = ACS_df["Community Area"].dropna().astype(str).str.strip().unique().tolist()
pat = re.compile(r"\b(" + "|".join(map(re.escape, areas)) + r")\b", flags=re.IGNORECASE)
canon = {a.lower(): a for a in areas}

def extract_area(s: str):
    if isinstance(s, str):
        m = pat.search(s)
        if m:
            return canon.get(m.group(1).lower())
    return None


real_estate_df["Community Area"] = real_estate_df["text"].apply(extract_area)


real_estate_df["listPrice"] = (
    real_estate_df["listPrice"]
      .astype(str)
      .str.replace(r"[\$,]", "", regex=True)
      .pipe(pd.to_numeric, errors="coerce")
)




listings_enriched = real_estate_df.merge(ACS_df, on="Community Area", how="left")

print("Rows (listings_enriched):", len(listings_enriched))
print("Price:", listings_enriched["listPrice"].dtype)
print("Mapped areas:", listings_enriched["Community Area"].notna().sum())

PRINTS THIS:
Rows (listings_enriched): 2000
Price: float64
Mapped areas: 886

listings_enriched


community_summary = (
    listings_enriched
      .dropna(subset=["Community Area", "listPrice"])
      .groupby("Community Area", as_index=False)
      .agg(
          n_listings=("listPrice", "size"),
          median_listing_price=("listPrice", "median"),
          mean_listing_price=("listPrice", "mean")
      )
)



final_summary = community_summary.merge(ACS_df, on="Community Area", how="left")

print("Rows (final_summary):", len(final_summary))
print(final_summary.head())

PRINTS THIS:

Rows (final_summary): 66
   Community Area  n_listings  median_listing_price  mean_listing_price  \
0     ALBANY PARK          11              350000.0       553863.636364   
1  ARCHER HEIGHTS           1              349000.0       349000.000000   
2         ASHBURN           5              241000.0       254174.600000   
3  AUBURN GRESHAM           4              149000.0       164450.000000   
4          AUSTIN          14              239450.0       262907.071429   

   ACS Year  Under $25,000  $25,000 to $49,999  $50,000 to $74,999  \
0      2023           1269                1916                1801   
1      2023            223                 752                 441   
2      2023            797                1351                1985   
3      2023           2541                2451                1592   
4      2023           5506                5084                3600   

   $75,000 to $125,000  $125,000 +  ...  White  Black or African American  \
0                 2306        3379  ...  21496                       2228   
1                  795         739  ...   6232                         10   
2                 3014        2735  ...  11297                      18124   
3                 2202        1850  ...    760                      43414   
4                 4047        3725  ...  10447                      73602   

   American Indian or Alaska Native  Asian  \
0                               759   7124   
1                               108    679   
2                               697    436   
3                               119    399   
4                               531    678   

   Native Hawaiian or Pacific Islander  Other Race  Multiracial  \
0                                    1        7888         8334   
1                                    0        3705         3142   
2                                    0        7772         4517   
3                                    0         993          798   
4                                   21        8512         6487   

   White Not Hispanic or Latino  Hispanic or Latino            Record ID  
0                         16115               21108     2023_ALBANY PARK  
1                          2043               11097  2023_ARCHER HEIGHTS  
2                          3774               19917         2023_ASHBURN  
3                           491                1577  2023_AUBURN GRESHAM  
4                          5386               19591          2023_AUSTIN  

[5 rows x 33 columns]

final_summary.head(n=60)

THEN SHOWS THIS

Community Area	n_listings	median_listing_price	mean_listing_price	ACS Year	Under $25,000	$25,000 to $49,999	$50,000 to $74,999	$75,000 to $125,000	$125,000 +	...	White	Black or African American	American Indian or Alaska Native	Asian	Native Hawaiian or Pacific Islander	Other Race	Multiracial	White Not Hispanic or Latino	Hispanic or Latino	Record ID
0	ALBANY PARK	11	350000.0	5.538636e+05	2023	1269	1916	1801	2306	3379	...	21496	2228	759	7124	1	7888	8334	16115	21108	2023_ALBANY PARK
1	ARCHER HEIGHTS	1	349000.0	3.490000e+05	2023	223	752	441	795	739	...	6232	10	108	679	0	3705	3142	2043	11097	2023_ARCHER HEIGHTS
2	ASHBURN	5	241000.0	2.541746e+05	2023	797	1351	1985	3014	2735	...	11297	18124	697	436	0	7772	4517	3774	19917	2023_ASHBURN
3	AUBURN GRESHAM	4	149000.0	1.644500e+05	2023	2541	2451	1592	2202	1850	...	760	43414	119	399	0	993	798	491	1577	2023_AUBURN GRESHAM
4	AUSTIN	14	239450.0	2.629071e+05	2023	5506	5084	3600	4047	3725	...	10447	73602	531	678	21	8512	6487	5386	19591	2023_AUSTIN
5	AVALON PARK	4	294450.0	2.809500e+05	2023	420	489	356	518	630	...	27	8924	0	65	0	265	211	27	48	2023_AVALON PARK
6	AVONDALE	10	432000.0	4.345200e+05	2023	689	1191	1106	1726	3059	...	19289	927	263	1750	15	7809	6297	13718	18606	2023_AVONDALE
7	BELMONT CRAGIN	3	329900.0	3.466000e+05	2023	1585	3843	3031	4588	3299	...	27909	3370	993	1939	23	25743	14011	10782	57511	2023_BELMONT CRAGIN
8	BEVERLY	43	375000.0	4.642163e+05	2023	160	294	355	1074	3255	...	11330	6671	9	176	23	276	1327	10974	1389	2023_BEVERLY
9	BRIDGEPORT	17	559999.0	5.383764e+05	2023	1123	1450	1043	1634	2572	...	13410	991	152	13234	0	2751	2475	11334	6879	2023_BRIDGEPORT
10	BRIGHTON PARK	4	294000.0	2.807250e+05	2023	1685	2564	1889	2138	1531	...	14018	937	850	4391	128	14067	7969	3193	33785	2023_BRIGHTON PARK
11	CALUMET HEIGHTS	9	269900.0	2.507332e+05	2023	353	308	431	906	903	...	130	11470	19	17	0	158	284	28	498	2023_CALUMET HEIGHTS
12	CHATHAM	21	199999.0	2.234972e+05	2023	1530	1427	940	1291	1356	...	414	29714	69	111	0	276	855	336	783	2023_CHATHAM
13	CLEARING	10	334900.0	3.573599e+05	2023	359	997	1002	1677	1913	...	13917	486	479	178	37	4913	4701	8932	14872	2023_CLEARING
14	DOUGLAS	8	517000.0	6.201125e+05	2023	689	571	526	431	737	...	2278	12400	214	2006	0	797	936	2042	1416	2023_DOUGLAS
15	DUNNING	4	344950.0	4.037250e+05	2023	761	1136	1714	3223	4246	...	28488	1273	225	2450	4	5328	4779	23593	14613	2023_DUNNING
16	EAST GARFIELD PARK	6	349000.0	3.804833e+05	2023	1416	1114	462	767	436	...	1537	16911	47	35	13	494	818	1130	1535	2023_EAST GARFIELD PARK
17	EAST SIDE	6	306500.0	8.113167e+05	2023	712	1248	1214	1450	988	...	10892	365	597	146	0	7703	3927	2651	20479	2023_EAST SIDE
18	EDGEWATER	28	262000.0	3.852928e+05	2023	736	1082	909	1984	3751	...	28646	5684	87	5724	90	1724	5529	25939	7756	2023_EDGEWATER
19	EDISON PARK	19	489000.0	5.534046e+05	2023	123	183	109	677	1846	...	9914	50	0	178	0	517	739	9162	1673	2023_EDISON PARK
20	ENGLEWOOD	2	55000.0	5.500000e+04	2023	1501	1264	754	705	321	...	619	19500	20	167	0	515	516	276	1114	2023_ENGLEWOOD
21	FOREST GLEN	2	619950.0	6.199500e+05	2023	162	349	343	953	3439	...	15419	193	0	2190	0	725	1236	14528	2133	2023_FOREST GLEN
22	FULLER PARK	11	25000.0	7.694545e+04	2023	186	113	36	61	34	...	148	1850	7	7	0	22	151	86	232	2023_FULLER PARK
23	GAGE PARK	4	242400.0	2.376500e+05	2023	1007	2038	1582	1619	1240	...	13619	1403	536	264	1	13063	5764	995	31985	2023_GAGE PARK
24	GARFIELD RIDGE	25	375000.0	4.079614e+05	2023	421	1324	1220	2378	3565	...	21939	1183	502	595	40	6073	5932	13879	20235	2023_GARFIELD RIDGE
25	GREATER GRAND CROSSING	3	79400.0	1.074667e+05	2023	1853	1764	1121	1172	747	...	350	27524	184	74	1	531	387	304	756	2023_GREATER GRAND CROSSING
26	HEGEWISCH	6	227450.0	2.331498e+05	2023	213	309	462	560	592	...	4768	1226	10	59	0	2015	818	3236	4331	2023_HEGEWISCH
27	HERMOSA	2	597500.0	5.975000e+05	2023	549	1273	974	1270	1148	...	8318	1087	107	702	11	8182	4793	2866	18578	2023_HERMOSA
28	HUMBOLDT PARK	10	589450.0	6.253699e+05	2023	2099	3124	2632	2200	1901	...	14677	19829	820	1335	0	11664	6691	6488	27389	2023_HUMBOLDT PARK
29	HYDE PARK	46	320000.0	4.438109e+05	2023	301	255	309	731	2078	...	11509	6143	49	3763	0	604	2024	10805	1762	2023_HYDE PARK
30	IRVING PARK	21	549987.0	6.873946e+05	2023	1028	1882	1674	2798	5232	...	31156	2073	205	5083	139	7625	7253	24178	20637	2023_IRVING PARK
31	JEFFERSON PARK	15	399900.0	4.364333e+05	2023	521	751	814	1744	2965	...	17913	695	66	3399	44	2070	2805	15345	6786	2023_JEFFERSON PARK
32	KENWOOD	14	357000.0	5.298857e+05	2023	564	296	116	646	1254	...	2958	9791	18	697	4	124	775	2804	383	2023_KENWOOD
33	LAKE VIEW	7	439000.0	1.025200e+06	2023	627	661	860	1969	10739	...	71631	3913	146	6386	88	2415	6073	67784	8979	2023_LAKE VIEW
34	LINCOLN PARK	96	612500.0	1.673800e+06	2023	309	346	381	1224	8892	...	50933	2283	25	4319	7	1261	3238	49078	4274	2023_LINCOLN PARK
35	LINCOLN SQUARE	20	444950.0	5.480099e+05	2023	576	1022	1173	2162	4410	...	28731	1623	280	4345	0	2662	4539	25776	8311	2023_LINCOLN SQUARE
36	LOGAN SQUARE	30	634450.0	9.508166e+05	2023	1259	1521	1329	2708	7008	...	45894	4355	481	3344	78	5260	11942	36570	24808	2023_LOGAN SQUARE
37	LOOP	93	449500.0	6.772914e+05	2023	138	540	305	1122	4777	...	22509	3120	367	8849	0	1016	2424	20573	4297	2023_LOOP
38	MCKINLEY PARK	4	277500.0	3.037500e+05	2023	320	781	699	779	1039	...	5199	339	256	4282	0	3700	1625	2204	8474	2023_MCKINLEY PARK
39	MONTCLARE	1	379900.0	3.799000e+05	2023	312	464	510	827	1089	...	7066	922	72	446	0	3851	1398	4683	7515	2023_MONTCLARE
40	MORGAN PARK	7	325000.0	2.704286e+05	2023	759	761	571	1180	1767	...	6807	12770	53	211	0	335	1112	6485	981	2023_MORGAN PARK
41	MOUNT GREENWOOD	11	319500.0	3.270909e+05	2023	158	289	270	917	2785	...	17017	344	16	202	0	356	1172	16041	1834	2023_MOUNT GREENWOOD
42	NEW CITY	4	257450.0	3.364500e+05	2023	2266	2142	1432	1622	1440	...	12557	8446	524	991	29	13273	5024	4036	27311	2023_NEW CITY
43	NORTH CENTER	7	650000.0	7.691429e+05	2023	355	271	378	1019	6575	...	28092	906	17	2264	22	1063	3418	26136	4516	2023_NORTH CENTER
44	NORTH LAWNDALE	2	314448.0	3.144480e+05	2023	1772	1538	1171	1454	613	...	2545	24036	155	59	0	2363	1196	1614	4413	2023_NORTH LAWNDALE
45	NORTH PARK	3	560000.0	5.113333e+05	2023	391	835	583	1105	1390	...	10185	532	153	6058	0	904	1426	8578	3398	2023_NORTH PARK
46	NORWOOD PARK	26	409450.0	3.868577e+05	2023	771	972	1140	2459	5263	...	31029	515	144	2809	0	1759	3819	27986	7802	2023_NORWOOD PARK
47	OAKLAND	2	454000.0	4.540000e+05	2023	361	228	144	125	182	...	159	3946	59	51	0	14	143	155	131	2023_OAKLAND
48	OHARE	2	347400.0	3.474000e+05	2023	321	650	1052	1083	1155	...	10624	1079	55	2237	0	1110	1176	9418	3013	2023_OHARE
49	PORTAGE PARK	17	439000.0	4.469053e+05	2023	909	2483	1926	4182	5814	...	38249	1171	1026	3935	9	12068	7743	29957	27520	2023_PORTAGE PARK
50	PULLMAN	12	225000.0	2.128667e+05	2023	287	308	346	478	226	...	1123	5293	0	5	0	244	186	848	559	2023_PULLMAN
51	ROGERS PARK	26	304950.0	3.265615e+05	2023	1038	1986	1477	2460	2802	...	25129	13602	459	2750	0	5278	5951	23158	10599	2023_ROGERS PARK
52	ROSELAND	3	95000.0	1.682667e+05	2023	1535	2186	1379	2244	1160	...	668	35905	56	85	0	209	738	529	700	2023_ROSELAND
53	SOUTH CHICAGO	5	228900.0	2.178800e+05	2023	1499	1522	968	1295	1055	...	2813	21948	123	125	0	2986	1077	947	5604	2023_SOUTH CHICAGO
54	SOUTH SHORE	31	199900.0	2.171806e+05	2023	2299	2082	1681	1798	1563	...	1588	43339	12	160	27	453	698	1066	1463	2023_SOUTH SHORE
55	UPTOWN	8	452500.0	4.215874e+05	2023	1379	1189	971	1500	4119	...	30635	10848	238	5033	17	2275	3626	27437	7558	2023_UPTOWN
56	WASHINGTON HEIGHTS	5	259900.0	2.381600e+05	2023	918	905	1179	1804	1609	...	488	25401	87	24	0	94	216	386	248	2023_WASHINGTON HEIGHTS
57	WASHINGTON PARK	9	335000.0	4.158667e+05	2023	1142	717	274	317	267	...	242	11691	10	0	0	138	281	230	171	2023_WASHINGTON PARK
58	WEST ELSDON	3	319900.0	3.166000e+05	2023	267	921	788	979	1030	...	7800	128	749	688	0	5056	3780	2606	14781	2023_WEST ELSDON
59	WEST ENGLEWOOD	7	99900.0	1.204429e+05	2023	1547	1804	785	932	570	...	1353	20537	279	83	65	2435	1220	262	4674	2023_WEST ENGLEWOOD




# These are the basic shapes
re_shape = real_estate_df.shape
acs_shape = ACS_df.shape

# Duplicates 
re_dupes = real_estate_df.duplicated().sum()
acs_dupes = ACS_df.duplicated().sum()


# Ammount of Community Areas
re_areas = real_estate_df["Community Area"].dropna().nunique()
acs_areas = ACS_df["Community Area"].dropna().nunique()



print("Real estate rows, columns :", re_shape)
print("ACS rows, columns:", acs_shape)
print("Real estate duplicates:", re_dupes)
print("ACS duplicates:", acs_dupes)
print("Listings mapped to a Community Area (unique areas):", re_areas)
print("ACS unique community areas:", acs_areas)

THEN PRINTS THIS: 
Real estate rows, columns : (2000, 16)
ACS rows, columns: (77, 30)
Real estate duplicates: 2
ACS duplicates: 0
Listings mapped to a Community Area (unique areas): 67
ACS unique community areas: 77

income_midpoints = {
    "Under $25,000": 12500,
    "$25,000 to $49,999": 37500,
    "$50,000 to $74,999": 62500,
    "$75,000 to $125,000": 100000,
    "$125,000 +": 150000
}

for col in income_midpoints.keys():
    ACS_df[col] = pd.to_numeric(ACS_df[col], errors="coerce")

numerator = sum(ACS_df[col] * income_midpoints[col] for col in income_midpoints)
denominator = sum(ACS_df[col] for col in income_midpoints)
ACS_df["median_income_made"] = numerator / denominator


import numpy as np

listings_enriched["listPrice"] = (
    listings_enriched["listPrice"].astype(str)
    .str.replace(r"[\$,]", "", regex=True)
    .pipe(pd.to_numeric, errors="coerce")
)

community_summary = (
    listings_enriched
      .dropna(subset=["Community Area", "listPrice"])
      .groupby("Community Area", as_index=False)
      .agg(
          n_listings=("listPrice", "size"),
          median_listing_price=("listPrice", "median"),
          mean_listing_price=("listPrice", "mean")
      )
      .merge(ACS_df[["Community Area", "median_income_made"]], on="Community Area", how="left")
)

community_summary = community_summary.rename(columns={"median_income_made": "median_income"})

community_summary["price_to_income"] = (
    community_summary["median_listing_price"] / community_summary["median_income"]
)

import matplotlib.pyplot as plt
import seaborn as sns

ACS_sorted = ACS_df.sort_values("median_income_made", ascending=False)

plt.figure(figsize=(12, 15))
sns.barplot(
    data=ACS_sorted,
    x="median_income_made",
    y="Community Area",
    color="skyblue"
)

plt.title("Estimated Median Income by Community Area (ACS 5-Year Data)", fontsize=14, pad=15)
plt.xlabel("Estimated Median Income (USD)")
plt.ylabel("Community Area")
plt.tight_layout()
plt.show()

A horizontal bar chart ranking all 77 Chicago community areas by their estimated median income proxy (using the weighted midpoint calculation).


community_summary["price_to_income"] = (
    community_summary["median_listing_price"] / community_summary["median_income"]
)

top5 = community_summary.sort_values("price_to_income", ascending=False).head(5)
bottom5 = community_summary.sort_values("price_to_income", ascending=True).head(5)

print("Top 5 (least affordable):\n", top5[["Community Area","median_listing_price","median_income","price_to_income"]])
print("Top 5 (most affordable):\n", bottom5[["Community Area","median_listing_price","median_income","price_to_income"]])

Top 5 (least affordable):
    Community Area  median_listing_price  median_income  price_to_income
28  HUMBOLDT PARK              589450.0   68002.467380         8.668068
47        OAKLAND              454000.0   59483.173077         7.632411
27        HERMOSA              597500.0   79531.070196         7.512787
64      WEST TOWN              850000.0  119761.357450         7.097448
14        DOUGLAS              517000.0   73307.379824         7.052496
Top 5 (most affordable):
             Community Area  median_listing_price  median_income  \
22             FULLER PARK               25000.0   46540.697674   
20               ENGLEWOOD               55000.0   51031.353135   
25  GREATER GRAND CROSSING               79400.0   58378.398678   
52                ROSELAND               95000.0   68879.350894   
59          WEST ENGLEWOOD               99900.0   55826.534232   

  price_to_income  
22         0.537164  
20         1.077769  
25         1.360092  
52         1.379223  
59         1.789472  



All of this was done on VSCode





