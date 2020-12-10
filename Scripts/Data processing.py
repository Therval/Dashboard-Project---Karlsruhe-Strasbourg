"""
Data processing 
"""
# %% -- Load needed librairies
import pandas as pd 
import re 

# %% -- Load dataset
papers = pd.read_csv("/Users/valentinjoly/Documents/Data - Dashboard/DL_PAPER_1990_2018.tsv",
    sep='\t')
"If issue, try to install the 'xlrd' dependency : pip install xlrd"

# %% -- Filter
"First, we remove all the observations where we don't have any information on who published this paper"
papers.dropna(subset = ["C1"], inplace = True, axis = 0)

# Drop duplicates (if exists)
papers.drop_duplicates(subset = ["AB"], inplace = True)

# %% -- Identify pattern in order to get university/firms names for each observations
papers.C1.head(20)
"""
Pattern : name always before the first comma
So, we can extract this information with a more efficient way than regex 
"""
names = []
for obs in papers.C1:
        names.append(obs.split(',', 1)[0]) # add nsplits = 1 for efficiency 
papers.C1 = names
del names, obs
# %% -- Show results 
papers.C1.head(20) # Good!

# %% -- Replace "Univ" by "University" ; "Inst" by "Institude" ; "Acad" by "Academy"
papers.C1 = papers.C1.str.replace("Univ", "University")
papers.C1 = papers.C1.str.replace("UNIV", "University") #In case of issue with the first one

papers.C1 = papers.C1.str.replace("Inst", "Institute")

papers.C1 = papers.C1.str.replace("Acad", "Academy")
# %% -- More informations about firms
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
"Lot of issue with observations where we have a pattern like this : [name"
"A simple solution is to remove them because we cannot now if they work for academia or firms"

filtered_pap = filtered_pap[~filtered_pap.C1.str.startswith("[")]
count = filtered_pap.C1.value_counts()
# %% -- Create new variable
filtered_pap["Organisation"] = "Firms"
# Merge with papers dataset
papers = papers.merge(filtered_pap,
                      how = "left")
# Fill na by "Academia"
papers.Organisation.fillna("Academia", inplace = True)

# %% -- Keep Only interesting variables
papers = papers[["UT", "PY", "SC", "NR", "ArtsHumanities", "LifeSciencesBiomedicine", "PhysicalSciences",
                "SocialSciences", "Technology", "ComputerScience", "Health", "TCperYear", "nb_aut", "Organisation"]]

# %% -- Aggregate country and regions
# - Load 2nd dataset
dl_country = pd.read_csv("/Users/valentinjoly/Documents/Data - Dashboard/DL_COUNTRY_REGION.tsv",
    sep='\t')

# - Drop unneeded variables
cols = [0, 3]
dl_country.drop(dl_country.columns[cols], axis = 1, inplace = True)
del cols
# - Rename variables
dl_country.rename(columns = {"C1":"Country"}, inplace = True)

# %% -- Add Country and Regions
final_df = papers.merge(dl_country, 
                        how = "left")
# - Drop "UT" Variables and "Nb_aut_aff"
cols = [0, 15]
final_df.drop(final_df.columns[cols], axis = 1, inplace = True)
# - Drop_duplicates
final_df.drop_duplicates(inplace = True)

# %% -- Save final dataset
final_df.to_csv("Dataset.csv", index = False)
