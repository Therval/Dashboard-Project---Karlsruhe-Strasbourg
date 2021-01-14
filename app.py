# -*- coding: utf-8 -*-
"""Run the Dash application."""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

DATASET_PATH = 'dataset/papers.parquet'
PANDASPROFILING_REPORT = 'papers_pandas-profiling-report.html'
SWEETVIZ_REPORT = 'papers_sweetviz-report.html'

# Set color scheme
COLOR_MAP = {
    'Academia': '#3a6186',
    'Company': '#89253e',
    'Collaboration': '#719F78'
}
COLOR_SEQU = [(0, COLOR_MAP['Academia']), (1, COLOR_MAP['Company'])]
COLOR_QUAL = px.colors.qualitative.Antique

# Describe some labels
LABELS = {
    'PY': 'Year Published',
    'SC': 'Research Areas',
    'NR': 'Cited Reference Count',
    'TCperYear': 'WoS Core Cited Count per Year',
    'NumAuthors': 'Number of Authors',
    'CountryCode': 'Country Code'
}

# Create application instance
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Import dataset
df = pd.read_parquet(DATASET_PATH)


# --- CALCULATE TABLES FOR CHARTS ---

# Count of organisation
org_count = pd.DataFrame({'Count': df.groupby(['Organisation']).size()}).reset_index()
# Count of organisation by year
year_org_count = pd.DataFrame({'Count': df.groupby(['PY', 'Organisation']).size()}).reset_index()

# Count of organisation by country
country_org_count = df.groupby(['CountryCode', 'Organisation']).size().unstack()
# Flatten hierarchical columns
country_org_count.columns = country_org_count.columns.tolist()
# Calculate company percentage
country_org_count['CompanyPercentage'] = 100 / (country_org_count['Academia'] / country_org_count['Company'] + 1)
# Add country names from dataset
country_org_count = country_org_count.merge(
    df[['CountryCode', 'Country']],
    how='left',
    on='CountryCode'
).drop_duplicates()


# --- DEFINE CHARTS ---

histogram_year = px.histogram(
    df,
    x='PY',
    barmode='group',
    color='Organisation',
    color_discrete_map=COLOR_MAP,
    labels=LABELS,
    title='Published Papers in the Data Set'
).update_layout(
    title_x=0.5
)

pie_org = px.pie(
    org_count,
    values='Count',
    names='Organisation',
    color='Organisation',
    color_discrete_map=COLOR_MAP,
    title='Distribution of Academia vs Companies'
).update_layout(
    title_x=0.5
)

histogram_year_line = px.line(
    year_org_count,
    x='PY',
    y='Count',
    color='Organisation',
    color_discrete_map=COLOR_MAP,
    labels=LABELS,
    title='Published Papers in the Data Set'
).update_layout(
    title_x=0.5
)

choropleth_map = px.choropleth(
    country_org_count,
    locations='CountryCode',
    color='CompanyPercentage',
    hover_name='Country',
    hover_data=['Academia', 'Company'],
    labels=LABELS,
    color_continuous_scale=COLOR_SEQU,
    range_color=[0, 15],
    title='Company to Academia Ratio',
    center={'lat': 20}
).update_layout(
    title_x=0.5,
    height=800,
    coloraxis_colorbar=dict(
        title='Company Ratio',
        ticks='outside',
        ticksuffix='%'
    )
).update_geos(
    visible=False,
    showland=True,
    landcolor='#ccc',
    showcoastlines=True,
    projection_type='natural earth'
)


# --- LAYOUTS ---

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

analyses_layout = html.Div([
        html.Div([
                html.Div([
                        html.H1(
                            'Exploring the Diffusion of Publications Between Academia and Companies',
                            id='main-title'
                        ),
                        html.H3(
                            'in the Field of Deep Learning',
                            id='subtitle'
                        ),
                    ],
                    id='title',
                    className='twelve columns'
                )
            ],
            id='header',
            className='row flex-display'
        ),
        html.Div([
                html.Div([
                        html.H6(
                            '''
This dashboard shows the diffusion of publications between academia and companies in the field of Deep Learning.
It includes a total of 287544 scientific publications.
These papers were published in the Web of Science Core Collection.
The papers were retrieved through web scraping.
The use of deep learning was identified through keyword search in the title and abstract.
The author metadata was used for classifying the publications into company, academia or collaborations of both.
To learn more about the descriptions of the dashboard graphs and their functions click on "Learn More".
                            ''',
                            className="ten columns"
                        ),
                        html.Div([
                                html.A(
                                    "Learn More",
                                    href="/description",
                                    id="learn-more-btn",
                                    role="button",
                                    className="button"
                                ),
                                html.A(
                                    "Explore Dataset",
                                    href="/dataset",
                                    id="explore-dataset-btn",
                                    role="button",
                                    className="button"
                                )
                            ],
                            className="two columns item-column"
                        )
                    ],
                    className="pretty_container twelve columns"
                ),
            ],
            id='header-description',
            className="row flex-display"
        ),
        html.Div([
                dcc.Graph(
                    id='histogram-year',
                    figure=histogram_year,
                    className="pretty_container eight columns"
                ),
                dcc.Graph(
                    id='pie-org',
                    figure=pie_org,
                    className="pretty_container four columns"
                )
            ],
            className="row flex-display"
        ),
        html.Div([
                dcc.Graph(
                    id='choropleth-map',
                    figure=choropleth_map,
                    className="pretty_container twelve columns"
                )
            ],
            className="row flex-display"
        ),
        html.Div([
                html.A([
                        'Example charts',
                    ],
                    href='/examples',
                    role="button",
                    className='button'
                )
            ],
            className='row flex-display'
        )
])

dataset_layout = html.Div([
        html.Div([
                html.Div([
                        html.H1(
                            'Paper Dataset'
                        )
                    ],
                    id='title',
                    className='twelve columns'
                )
            ],
            id='header',
            className='row flex-display'
        ),
        html.Div([
                html.Div([
                        html.A(
                            "Show Pandas Profiling Report",
                            href=f"/static/{PANDASPROFILING_REPORT}",
                            target="_blank",
                            rel="noopener noreferrer",
                            id="pandas-profiling-btn",
                            role="button",
                            className="button"
                        ),
                        html.A(
                            "Show Sweetviz Profiling Report",
                            href=f"/static/{SWEETVIZ_REPORT}",
                            target="_blank",
                            rel="noopener noreferrer",
                            id="sweetviz-btn",
                            role="button",
                            className="button"
                        ),
                        html.A(
                            "Read the Project Description",
                            href="/description",
                            id="learn-more-btn",
                            role="button",
                            className="button"
                        ),
                        html.A(
                            "Return to the Dashboard",
                            href="/",
                            id="return-dashboard-btn",
                            role="button",
                            className="button"
                        )
                    ],
                    className="pretty_container twelve columns item-column"
                ),
            ],
            className="row flex-display center-content"
        ),
        html.Div([
                html.Div([
                        dcc.Markdown('''
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
                        ''')
                    ],
                    className="pretty_container twelve columns flex-display center-content text-container"
                ),
            ],
            className="row flex-display center-content"
        )
])

description_layout = html.Div([
        html.Div([
                html.Div([
                        html.H1(
                            'Exploring the Diffusion of Publications Between Academia and Companies',
                            id='main-title'
                        ),
                        html.H3(
                            'in the Field of Deep Learning',
                            id='subtitle'
                        ),
                    ],
                    id='title',
                    className='twelve columns'
                )
            ],
            id='header',
            className='row flex-display'
        ),
        html.Div([
                html.Div([
                        dcc.Markdown('''
Learn More
                        ''')
                    ],
                    className="pretty_container twelve columns text-container"
                ),
            ],
            className="row flex-display center-content"
        ),
        html.Div([
                html.Div([
                        html.A(
                            "Explore the Dataset",
                            href="/dataset",
                            id="explore-dataset-btn",
                            role="button",
                            className="button"
                        ),
                        html.A(
                            "Return to the Dashboard",
                            href="/",
                            id="return-dashboard-btn",
                            role="button",
                            className="button"
                        )
                    ],
                    className="pretty_container twelve columns item-column"
                ),
            ],
            className="row flex-display center-content"
        )
])

examples_layout = html.Div([
        html.Div([
            dcc.Graph(
                id='histogram-year-line',
                figure=histogram_year_line,
                className="pretty_container twelve columns"
            )
        ],
            className="row flex-display",
        ),
        html.H2('Hello World'),
        dcc.Dropdown(
            id='dropdown',
            options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
            value='LA'
        ),
        html.Div(id='display-value')
])


# --- CALLBACKS ---

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


# --- URL ROUTER ---

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return analyses_layout
    elif pathname == '/dataset':
        return dataset_layout
    elif pathname == '/description':
        return description_layout
    elif pathname == '/examples':
        return examples_layout
    else:
        # the default
        return analyses_layout


# --- START APP ---

# Run the application, if this python file is executed
if __name__ == '__main__':
    app.run_server(debug=True)
