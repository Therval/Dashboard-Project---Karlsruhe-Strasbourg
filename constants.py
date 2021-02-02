# -*- coding: utf-8 -*-
"""Define constant strings."""

DATASET_PATH = 'dataset/papers.parquet'
PANDASPROFILING_REPORT = 'papers_pandas-profiling-report.html'
SWEETVIZ_REPORT = 'papers_sweetviz-report.html'

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
    'Academia': '#3a6186',
    'Company': '#89253e',
    'Collaboration': '#719F78'
}

HEADER_INTRO_TXT = '''
This dashboard shows the diffusion of publications between academia and companies in the field of Deep Learning.
It includes a total of 287544 scientific publications.
These papers were published in the Web of Science Core Collection.
The papers were retrieved through web scraping.
The use of deep learning was identified through keyword search in the title and abstract.
The author metadata was used for classifying the publications into company, academia or collaborations of both.
To learn more about the descriptions of the dashboard graphs and their functions click on "Learn More".
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
Thank you for learning more :)
'''
