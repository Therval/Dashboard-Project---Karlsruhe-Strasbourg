"""
Data processing
"""
# %% -- Load needed libraries
import pandas as pd

# %% -- Load dataset
papers = pd.read_csv("DL_PAPER_1990_2018.tsv", sep='\t')
"In case of an issue, try to install the 'xlrd' dependency : pip install xlrd"

# %% -- Filter
"First, we remove all the observations where we don't have any information on who published this paper"
papers.dropna(subset=["C1"], inplace=True, axis=0)
# Drop duplicates, if they exist
papers.drop_duplicates(subset=["AB"], inplace=True)

# %% -- Identify pattern in order to get university/firms names for each observation
papers.C1.head(20)
"""
Pattern: name always before the first comma
So, we can extract this information with a more efficient way than regex
"""
names = []
for obs in papers.C1:
    names.append(obs.split(',', 1)[0])  # add nsplits = 1 for efficiency
papers.C1 = names
del names

# %% -- Show results
papers.C1.head(20)  # Good!

# %% -- Replace "Univ" by "University" ; "Inst" by "Institute" ; "Acad" by "Academy"
papers.C1 = papers.C1.str.replace("Univ", "University")
papers.C1 = papers.C1.str.replace("UNIV", "University")  # In case of an issue with the first one
papers.C1 = papers.C1.str.replace("Inst", "Institute")
papers.C1 = papers.C1.str.replace("Acad", "Academy")

# %% -- More information about firms
# First, isolate which not contains "University"
stopwords = ["Ecole", "University", "MIT", "CNR", 'CNRS', "UMIST", "Institute", "ESCPI", "ENSCP",
             "Academy", "UNR", "USA", "ESCPI", "INSA", "NASA", "UCL", "RIKEN", "LORIA", "IPN", "CSIC",
             "ETIS", "USAF", "Politecn", "Kings Coll London", "London Coll", "NYU", "IDSIA", "Coll Canada",
             "UNICAMP", "UTBM", "CSIRO", "Commiss European", "OECD", "USTHB", "UFRJ", "CEA", "UPC", "INRA",
             "US FDA", "NOAA", "UNESP", "ENEA", "IIT", "SISSA", "IDIAP", "CUNY", "INSERM", "INRIA",
             "UNESCO", "INOAE", "NIST", "CERN", "CSIR", "Polytech", "EPFL", "MITS", "NIMH", "IFREMER"]
pat = r'({})'.format('|'.join(stopwords))
filtered_pap = papers[~papers.C1.str.contains(pat, case=False, na=False)]

# %% -- Sort by C1 and show unique value
count = filtered_pap.C1.value_counts()
"Lot of issue with observations where we have a pattern like this: [name"
"A simple solution is to remove them, because we cannot now if they work for academia or company"
filtered_pap = filtered_pap[~filtered_pap.C1.str.startswith("[")]
count = filtered_pap.C1.value_counts()

# %% -- Create new variable
filtered_pap["Organisation"] = "Company"
# Merge with papers dataset
papers = papers.merge(filtered_pap, how="left")
# Fill na by "Academia"
papers.Organisation.fillna("Academia", inplace=True)

# %% -- Keep Only interesting variables
papers = papers[["UT", "PY", "SC", "ArtsHumanities", "LifeSciencesBiomedicine", "PhysicalSciences", "SocialSciences",
                 "Technology", "ComputerScience", "Health", "NR", "TCperYear", "nb_aut", "Organisation"]]

# %% -- Aggregate country and regions
# - Load 2nd dataset
dl_country = pd.read_csv("DL_COUNTRY_REGION.tsv", sep='\t')
# - Drop unneeded variables
dl_country.drop(["aff", "PY"], axis=1, inplace=True)
# - Rename some regions
dl_country['Region'].replace({'WesternEurope': 'Western Europe',
                              'Eastern Europe Central Asia': 'Eastern Europe to Central Asia',
                              'MiddleEast North Africa': 'MiddleEast and North Africa',
                              'SouthEast Asia Pacific': 'SouthEast Asia and Pacific',
                              'Latin America Caribbean': 'Latin America and Caribbean'}, inplace=True)
dl_country['Region'].value_counts(normalize=True)

# %% -- Add Country and Regions
final_df = papers.merge(dl_country, how="inner")
# - Drop "UT" features and "Nb_aut_aff"
final_df.drop(["UT", "nb_aut_aff"], axis=1, inplace=True)
# - Rename features
final_df.rename(columns={"C1": "Country", "nb_aut": "NumAuthors"}, inplace=True)
# - Drop duplicates
final_df.drop_duplicates(inplace=True)
# - Re-index
final_df.reset_index(drop=True, inplace=True)

# %% -- Save final dataset to CSV
final_df.to_csv("papers.csv", index=False)

# %% -- Show column and memory info
final_df.info(memory_usage='deep')
final_df.memory_usage(deep=True)
final_df.agg(['size', 'count', 'nunique', 'std', 'min',  'median', 'max'])

# %% -- Optimize data types
opt_df = final_df.copy()
# - Convert to categories
opt_df['SC'] = final_df['SC'].astype('category')
opt_df['Organisation'] = final_df['Organisation'].astype('category')
opt_df['Country'] = final_df['Country'].astype('category')
opt_df['Region'] = final_df['Region'].astype('category')
# - Downcast integers
opt_df[
    ['PY', 'NR', 'NumAuthors', 'ComputerScience', 'Health']
    ] = final_df[
    ['PY', 'NR', 'NumAuthors', 'ComputerScience', 'Health']
    ].apply(pd.to_numeric, downcast='unsigned')

# %% -- Check optimized dataframe
opt_df.info(memory_usage='deep')
print('Memory reduction: ', round(100 - 100
                                  * opt_df.memory_usage(deep=True).sum()
                                  / final_df.memory_usage(deep=True).sum()
                                  ), '%')

# %% -- Save as a Parquet file
# - Parquet: a compressed file that memorizes dtypes
# - Requires pyarrow: 'conda install -c conda-forge pyarrow' or 'pip install pyarrow'
opt_df.to_parquet('papers.parquet', compression='gzip')
