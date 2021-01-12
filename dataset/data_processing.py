"""
Data processing
"""
# %% -- Load needed libraries
print("In order to run this script you need pandas, numpy, pycountry and pyarrow installed")
import pandas as pd
import re
from tqdm import tqdm_notebook
import numpy as np
import pycountry

# %% -- Load dataset
papers = pd.read_csv("DL_PAPER_1990_2018.tsv", sep='\t')
"In case of an issue, try to install the 'xlrd' dependency : pip install xlrd"

# %% -- Filter
"First, we remove all the observations where we don't have any information on who published this paper"
papers.dropna(subset=["C1"], inplace=True, axis=0)
# Drop duplicates, if they exist
papers.drop_duplicates(subset=["AB"], inplace=True)
papers = papers.reset_index()

# %%
"Lot of issue with observations where we have a pattern like this: [name"
papers.C1 = [re.sub("[\(\[].*?[\)\]]", "", sentence).lstrip() for sentence in tqdm_notebook(papers.C1)]

# %% 
"""
Pattern: name always before the first comma
So, we can extract this information with a more efficient way than regex
"""
names_1 = []
names_2 = []
for obs in papers.C1:
    sentence = obs.split(';', 1)[0]
    names_1.append(sentence.split(',', 1)[0])
    try:
        sentence = obs.split(';', 1)[1]
        names_2.append(sentence.split(',', 1)[0])
    except IndexError:
        names_2.append(np.nan)

papers.C1 = names_1
papers["C2"] = names_2
del names_1, names_2, obs, sentence

# %% -- Show results
print(papers.C1.head(20), papers.C2.head(20))  # Good!

# %% -- Replace "Univ" by "University" ; "Inst" by "Institute" ; "Acad" by "Academy"
papers.C1 = papers.C1.str.replace("Univ", "University")
papers.C1 = papers.C1.str.replace("UNIV", "University")  # In case we have an issue with the first one
papers.C1 = papers.C1.str.replace("Inst", "Institute")
papers.C1 = papers.C1.str.replace("Acad", "Academy")
papers.C1 = papers.C1.str.replace("Coll", "College")

papers.C2 = papers.C2.str.replace("Univ", "University")
papers.C2 = papers.C2.str.replace("UNIV", "University") 
papers.C2 = papers.C2.str.replace("Inst", "Institute")
papers.C2 = papers.C2.str.replace("Acad", "Academy")
papers.C2 = papers.C2.str.replace("Coll", "College")

# %% -- More information about firms
# First, isolate which not contains "University"
stopwords = ["Ecole", "University", "MIT", "CNR", "CNRS", "UMIST", "Institute", "ESCPI", "ENSCP",
             "Academy", "UNR", "USA", "ESCPI", "INSA", "NASA", "UCL", "RIKEN", "LORIA", "IPN", "CSIC", "CHU"
             "ETIS", "USAF", "Politecn", "Kings Coll London", "London Coll", "NYU", "IDSIA", "Coll Canada",
             "UNICAMP", "UTBM", "CSIRO", "Commiss European", "OECD", "USTHB", "UFRJ", "CEA", "UPC", "INRA",
             "US FDA", "NOAA", "UNESP", "ENEA", "IIT", "SISSA", "IDIAP", "CUNY", "INSERM", "INRIA", "College",
             "UNESCO", "INOAE", "NIST", "CERN", "CSIR", "Polytech", "EPFL", "MITS", "NIMH", "IFREMER"]
pat = r"({})".format('|'.join(stopwords))
filtered_pap = papers[~papers.C1.str.contains(pat, case=False, na=False)]

# %% Create separation between company only and joint paper 
firms_stopwords = pd.unique(filtered_pap.C1.values)

joined = filtered_pap[["C1","C2"]].values.tolist()

types = []
for obs in tqdm_notebook(joined):
    if obs[1] is np.nan:
        types.append("Company")
    else:
        if all(words in " ".join(firms_stopwords) for words in obs):
            types.append("Company")
        else:
            types.append("Joint paper")

filtered_pap["Organisation"] = types

papers = papers.merge(filtered_pap, how="left")

# %% Redo the manipulation for other papers (i.e., academia)
filtered_pap = papers[papers.Organisation.isna()]
academic_stopwords = pd.unique(filtered_pap.C1.values)

joined = filtered_pap[["C1","C2"]].values.tolist()

types = []
for obs in tqdm_notebook(joined):
    if obs[1] is np.nan:
        types.append("Academia")
    else:
        if all(word in " ".join(academic_stopwords) for word in obs):
            types.append("Academia")
        else:
            types.append("Joint paper")

filtered_pap["Organisation_bis"] = types

papers = papers.merge(filtered_pap, how="left")
papers.Organisation.fillna(papers.Organisation_bis, inplace=True)

# %% -- Keep Only interesting variables
papers = papers[["UT", "PY", "SC", 
                 "ArtsHumanities", "LifeSciencesBiomedicine", "PhysicalSciences", "SocialSciences",
                 "Technology", "ComputerScience", "Health", "NR", "TCperYear", "nb_aut", "Organisation"]]

# %% -- Aggregate country and regions
# - Load 2nd dataset
dl_country = pd.read_csv("DL_COUNTRY_REGION.tsv", sep='\t')
# - Drop unneeded variables
dl_country.drop(["aff", "PY"], axis=1, inplace=True)
# - Rename some regions
dl_country["Region"].replace({
        "WesternEurope": "Western Europe",
        "Eastern Europe Central Asia": "Eastern Europe to Central Asia",
        "MiddleEast North Africa": "MiddleEast and North Africa",
        "SouthEast Asia Pacific": "SouthEast Asia and Pacific",
        "Latin America Caribbean": "Latin America and Caribbean"
    },
    inplace=True
)
dl_country["Region"].value_counts(normalize=True)

# %% -- Improve country names
# - Rename US states: Country values with only two letters are US states
dl_country["C1"] = dl_country["C1"].apply(lambda country: "USA" if len(country) == 2 else country)
# - Improve some country names
dl_country["C1"].replace({
        "Iran (Islamic Republic of)": "Iran, Islamic Republic of",
        "The former Yugoslav Republic of Macedonia": "North Macedonia",
        "Libyan Arab Jamahiriya": "Libya",
        "Trinid & Tobago": "Trinidad and Tobago",
        "Fr Polynesia": "French Polynesia",
        "Laos": "Lao People's Democratic Republic",
        "Swaziland": "Eswatini",
        "Western Samoa": "Samoa",
        "W Ind Assoc St": "United Kingdom",
        "Ankara": "Turkey",
        "Arizona": "USA",
        "Democratic Republic of the Congo": "Congo, The Democratic Republic of the",
        "Miaoli": "Taiwan",
        "St Vincent": "Saint Vincent and the Grenadines",
        "Uae": "United Arab Emirates",
        "Serbia Monteneg": "Serbia and Montenegro",
        "*": np.nan
    },
    inplace=True
)
# - Create a list of used countries
ct = dl_country["C1"].value_counts().to_frame().reset_index()
ct.rename({"index": "Country"}, axis='columns', inplace=True)
ct.drop(["C1"], axis="columns", inplace=True)

# %% -- Identify countries
def getCountryCode(country):
    try:
        return pycountry.countries.search_fuzzy(country)[0].alpha_3
    except:
        return np.nan
ct["CountryCode"] = ct["Country"].apply(getCountryCode)
# - Correct some country codes manually
ct["CountryCode"].mask(ct["Country"] == "Guadeloupe", "GLP", inplace=True)
ct["CountryCode"].mask(ct["Country"] == "Niger", "NER", inplace=True)
ct["CountryCode"].mask(ct["Country"] == "Kosovo", "UNK", inplace=True)
# - Add historic country codes
ct["CountryCode"].mask(ct["Country"] == "Yugoslavia", "YUG", inplace=True)
ct["CountryCode"].mask(ct["Country"] == "Serbia and Montenegro", "SCG", inplace=True)
ct["CountryCode"].mask(ct["Country"] == "Ussr", "SUN", inplace=True)
ct["CountryCode"].mask(ct["Country"] == "Czechoslovakia", "CSK", inplace=True)
print("Finished identifying countries")
# - Add country code column using the new table
dl_country = dl_country.merge(ct, how="left", left_on="C1", right_on="Country")

# %% -- Add Country and Regions
final_df = papers.merge(dl_country, how="inner")
# - Drop "UT" features and "Nb_aut_aff"
final_df.drop(["UT", "nb_aut_aff", "C1"], axis="columns", inplace=True)
# - Rename features
final_df.rename({"nb_aut": "NumAuthors"}, axis="columns", inplace=True)
# - Drop duplicates
final_df.drop_duplicates(inplace=True)
# - Re-index
final_df.reset_index(drop=True, inplace=True)

# %% -- Save final dataset to CSV
final_df.to_csv("papers.csv", index=False)

# %% -- Show column and memory info
final_df.info(memory_usage="deep")
final_df.memory_usage(deep=True)
final_df.agg(["size", "count", "nunique", "std", "min",  "median", "max"])

# %% -- Optimize data types
opt_df = final_df.copy()
# - Convert to categories
opt_df["SC"] = final_df["SC"].astype("category")
opt_df["Organisation"] = final_df["Organisation"].astype("category")
opt_df["Region"] = final_df["Region"].astype("category")
opt_df["Country"] = final_df["Country"].astype("category")
opt_df["CountryCode"] = final_df["CountryCode"].astype("category")
# - Downcast integers
opt_df[
    ["PY", "NR", "NumAuthors", "ComputerScience", "Health"]
    ] = final_df[
    ["PY", "NR", "NumAuthors", "ComputerScience", "Health"]
    ].apply(pd.to_numeric, downcast="unsigned")

# %% -- Check optimized dataframe
opt_df.info(memory_usage="deep")
print("Memory reduction: ", round(100 - 100
                                  * opt_df.memory_usage(deep=True).sum()
                                  / final_df.memory_usage(deep=True).sum()
                                  ), '%')

# %% -- Save as a Parquet file
# - Parquet: a compressed file that memorizes dtypes
# - Requires pyarrow: 'conda install -c conda-forge pyarrow' or 'pip install pyarrow'
opt_df.to_parquet("papers.parquet", compression="gzip")

# %% -- Create pandas profiling report
# - https://github.com/pandas-profiling/pandas-profiling
from pandas_profiling import ProfileReport
pp_report = ProfileReport(opt_df, title="Papers - Pandas Profiling Report")
pp_report.to_file("papers_pandas-profiling-report.html")

# %% -- Create Sweetviz profiling report
# - https://github.com/fbdesignpro/sweetviz
import sweetviz
sv_report = sweetviz.analyze(opt_df)
sv_report.show_html(filepath="papers_sweetviz-report.html", open_browser=False)
