# -*- coding: utf-8 -*-
"""Define constant strings."""

DATASET_PATH = 'dataset/papers.parquet'
PANDASPROFILING_REPORT = 'papers_pandas-profiling-report.html'
SWEETVIZ_REPORT = 'papers_sweetviz-report.html'

LOADING_TYPE = 'default'

RESEARCH_CATEGORIES = [
    'ArtsHumanities',
    'LifeSciencesBiomedicine',
    'PhysicalSciences',
    'SocialSciences',
    'Technology'
]

# Describe some of the labels
LABELS = {
    'PY': 'Year Published',
    'SC': 'Research Areas',
    'NR': 'Cited Reference Count',
    'TCperYear': 'WoS Core Cited Count per Year',
    'NumAuthors': 'Number of Authors',
    'CountryCode': 'Country Code',
    'ArtsHumanities': 'Arts & Humanities',
    'LifeSciencesBiomedicine': 'Life Sciences & Biomedicine',
    'PhysicalSciences': 'Physical Sciences',
    'SocialSciences': 'Social Sciences',
    'Technology': 'Technology'
}

# Set color scheme
COLOR_MAP = {
    'Academia': '#E9B254',
    'Company': '#89253E',
    'Collaboration': '#3A6186'
}

HEADER_INTRO_TXT = '''
This dashboard shows the diffusion of publications between academia and companies in the field of Deep Learning.
It includes a total of 287544 scientific publications.
These papers were published in the Web of Science Core Collection.
The use of deep learning was identified through keyword search in the title and abstract.
The author metadata was used for classifying the publications into company, academia or collaborations of both.
Use the links on the right to learn more about the dashboard graphs, their functions and the data set.
'''

DATASET_FEATURES_TXT = '''
| Feature                   | Description                                               | Data Type             |
|---------------------------|-----------------------------------------------------------|-----------------------|
| `PY`                      | Year Published                                            | integer               |
| `SC`                      | Research Areas                                            | string / category     |
| `ArtsHumanities`          | Research Area                                             | float between 0 and 1 |
| `LifeSciencesBiomedicine` | Research Area                                             | float between 0 and 1 |
| `PhysicalSciences`        | Research Area                                             | float between 0 and 1 |
| `SocialSciences`          | Research Area                                             | float between 0 and 1 |
| `Technology`              | Research Area                                             | float between 0 and 1 |
| `ComputerScience`         | A Subset of `Technology`                                  | integer 0 or 1        |
| `Health`                  | A Subset of `LifeSciencesBiomedicine`                     | integer 0 or 1        |
| `NR`                      | Cited Reference Count                                     | integer               |
| `TCperYear`               | Web of Science Core Collection Times Cited Count per Year | float                 |
| `NumAuthors`              | Number of Authors                                         | integer               |
| `Organisation`            | Either "Academia", "Company" or "Collaboration"           | string / category     |
| `Region`                  | 9 Different Regions                                       | string / category     |
| `Country`                 | Country Name of Author                                    | string / category     |
| `CountryCode`             | ISO 3166-1 Alpha-3 Country Code                           | string / category     |

The classification of research areas can be found here:
[webofknowledge.com](https://images.webofknowledge.com/images/help/WOS/hp_research_areas_easca.html)
'''

PROJECT_DESCRIPTION_TXT = '''
## Motivation

Nowadays, it is well understood that the creation and application of new knowledge is the primary factor that drives
economic growth – especially universities depict an important source of new knowledge. Related to quality, both
universities and companies encounter challenges in evolving their innovation processes. Therefore, in recent years,
collaborations between universities and companies have received substantial interest as a source for knowledge
production and new technological advancements to source cutting-edge research. But collaborations between
organizations and academia can be difficult to manage due to a variety of skills including different expectations and
research goals. There is a trend of researchers switching from academic to university research teams and vice versa
(Mendeley, 2017). Companies like Facebook have even started to develop their own research programs to be able to better
address their research demands. As suggested by Bianchini et al. (2020), we use Deep Learning (DL) papers to proxy AI
knowledge. Owning strategic resources makes firms lead users of AI tools and gives them a novel comparative advantage
over universities in researching AI. With this in mind, we identified a research question on the potential divergence
of public and private interests, coupled with resource interdependence of the actors.

## Processing

To derive the organizational information of the papers, we developed a list of keywords to classify them according to
their metadata. Using a bottom-up approach we manually scanned the metadata of various publications of our dataset and
added the keywords of commonly known academic institutions and terms to a list. We then used this list to conclude
whether a publication was developed by a private company, an academic institution, or a collaboration of these two.
To enable the representations of the various dashboard graphs and features (e.g., the countries of the world map, the
aggregation functions when applying filters, and the exploration of the dataset), we processed and transformed the
dataset further.

## Conception and Features of the Dashboard

At the top of the dashboard, the research topic is introduced: The user of the dashboard has the possibility to (1)
learn more about the motivation of the research question and the data processing by clicking on the button
“learn more”, and (2) explore the dataset used by clicking on the button “explore data set”. The next section of the
dashboard contains the filtering area. To provide more interactivity to the dashboard, we decided to add a
click-to-filter function to dissect the data. This feature allows the user to apply two filters on all graphs of the
dashboard (filter of: the area of research + publication year).

In total, the dashboard itself comprises four different graphs. The first graph displays the number of publications
in the dataset by year, starting from 1990 to 2018. The three mentioned organizations (publications from academic
institutes, publications from private companies, and collaborations from academic institutes and private companies)
are represented with three different colors – this coloring scheme is used consistently throughout all graphs, so the
user can orient oneself better. The second graph shows the distribution of the publications between all three
organization types in form of a pie chart. In the third graph, the user can explore all distribution ratios in a
world map where each country is colored according to their publication distribution. The navigation bar on top of the
map graph allows the user to compare all different organization types with each other. And the last section shows four
different pie charts that display the distribution of publications across five different research areas.

An option to zoom in and out enables the viewer to look into the data from different perspectives. Also, to compare
individual areas it is possible to enable or disable them in the graph by clicking on their name in the corresponding
graph legend section – this feature can be found in the first, second, and fourth chart.

## Results

The first graph shows that the number of publications resulting from collaborations between academic institutes and
private companies is increasing almost exponentially after the year 2008 while the number of publications from
companies stagnates at around 200 to 500 publications. But we can also see the number of publications from private
companies is increasing from 351 in 2013 to 930 in the year 2018. The second graph shows that the total distribution
of publications allocates across 3.96% company publications, 45.2% academic publications, and 50.8% collaborations.
The world map graph shows that the collaboration to academia ratio all over the world is mostly between 40% and 58%.
And the last figure shows that in the field of deep learning firms, academies and collaborations especially focus
their research on the research area technology.

## Limitations

The information about the publications was extracted from the research database Web of Science. Therefore, the
dashboard at hand relies heavily on the coverage and distribution of the publications in the Web of Science research
database. It can only provide insights into the trend of the diffusion; the absolute paper numbers have to be
investigated further. The next limitation focuses on the manual natural language processing we used in the data
processing phase. This natural language process approach has its limits, but we could estimate an error rate of 5%
which is acceptable for natural language processing.
'''
