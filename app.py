# -*- coding: utf-8 -*-
"""Run the Dash application."""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
# Local import of the text strings
from texts import HEADER_INTRO_TXT, DATASET_FEATURES_TXT, PROJECT_DESCRIPTION_TXT


# --- SET THE CONSTANTS ---

DATASET_PATH = 'dataset/papers.parquet'
PANDASPROFILING_REPORT = 'papers_pandas-profiling-report.html'
SWEETVIZ_REPORT = 'papers_sweetviz-report.html'

# Set color scheme
COLOR_MAP = {
    'Academia': '#3a6186',
    'Company': '#89253e',
    'Collaboration': '#719F78'
}
COLOR_QUAL = px.colors.qualitative.Antique

# Describe some labels
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
    'SocialSciences': 'Social Sciences'
}


# --- INITIATE THE APP ---

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
# Add country names from dataset
country_org_count = country_org_count.merge(
    df[['CountryCode', 'Country']],
    how='left',
    on='CountryCode'
).drop_duplicates().reset_index(drop=True)
# Calculate fractions
country_org_count['CompanyAcademiaFraction'] = 100 / (
        country_org_count['Academia'] / country_org_count['Company'] + 1)
country_org_count['CompanyCollaborationFraction'] = 100 / (
        country_org_count['Collaboration'] / country_org_count['Company'] + 1)
country_org_count['CollaborationAcademiaFraction'] = 100 / (
        country_org_count['Academia'] / country_org_count['Collaboration'] + 1)
country_org_count['CompanyAcademiaCollabFraction'] = 100 / ((
        country_org_count['Academia'] + country_org_count['Collaboration']
    ) / (
        country_org_count['Company'] + country_org_count['Collaboration']
    ) + 1)

# Count of organization type for each category
category_org_count = df[[
        'ArtsHumanities',
        'LifeSciencesBiomedicine',
        'PhysicalSciences',
        'SocialSciences',
        'Technology',
        'Organisation'
]].replace(0, np.nan).groupby('Organisation').agg('count').T
# Flatten categorical columns
category_org_count.columns = category_org_count.columns.tolist()
# Set names properly and reset the index
category_org_count['Total'] = category_org_count.sum(axis='columns')
category_org_count = category_org_count.reset_index().rename({'index': 'Category'}, axis='columns').replace(LABELS)


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

choro_map_comp_acad = px.choropleth(
    country_org_count,
    locations='CountryCode',
    color='CompanyAcademiaFraction',
    hover_name='Country',
    hover_data=['Academia', 'Company', 'Collaboration'],
    labels=LABELS,
    color_continuous_scale=[
        (0, COLOR_MAP['Academia']),
        (1, COLOR_MAP['Company'])
    ],
    range_color=[0, 20],
    title='Company to Academia Paper Fraction',
    center={'lat': 20}
).update_layout(
    title_x=0.5,
    height=800,
    coloraxis_colorbar=dict(
        title='Company Fraction',
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

choro_map_comp_collab = px.choropleth(
    country_org_count,
    locations='CountryCode',
    color='CompanyCollaborationFraction',
    hover_name='Country',
    hover_data=['Academia', 'Company', 'Collaboration'],
    labels=LABELS,
    color_continuous_scale=[
        (0, COLOR_MAP['Collaboration']),
        (1, COLOR_MAP['Company'])
    ],
    range_color=[0, 16],
    title='Company to Collaboration Paper Fraction',
    center={'lat': 20}
).update_layout(
    title_x=0.5,
    height=800,
    coloraxis_colorbar=dict(
        title='Company Fraction',
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

choro_map_collab_acad = px.choropleth(
    country_org_count,
    locations='CountryCode',
    color='CollaborationAcademiaFraction',
    hover_name='Country',
    hover_data=['Academia', 'Company', 'Collaboration'],
    labels=LABELS,
    color_continuous_scale=[
        (0, COLOR_MAP['Academia']),
        (1, COLOR_MAP['Collaboration'])
    ],
    range_color=[40, 100],
    title='Collaboration to Academia Paper Fraction',
    center={'lat': 20}
).update_layout(
    title_x=0.5,
    height=800,
    coloraxis_colorbar=dict(
        title='Collabor. Fraction',
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

choro_map_comp_acad_collab = px.choropleth(
    country_org_count,
    locations='CountryCode',
    color='CompanyAcademiaCollabFraction',
    hover_name='Country',
    hover_data=['Academia', 'Company', 'Collaboration'],
    labels=LABELS,
    color_continuous_scale=[
        (0, COLOR_MAP['Academia']),
        (1, COLOR_MAP['Company'])
    ],
    range_color=[30, 50],
    title='Company to Academia Paper Fraction (Collab. counts for both)',
    center={'lat': 20}
).update_layout(
    title_x=0.5,
    height=800,
    coloraxis_colorbar=dict(
        title='Company Fraction',
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

pie_cat_academia = px.pie(
    category_org_count,
    values='Academia',
    names='Category',
    color='Category',
    color_discrete_sequence=COLOR_QUAL,
    labels=LABELS,
    title='Academia'
).update_layout(
    showlegend=False,
    title_x=0.5
)

pie_cat_companies = px.pie(
    category_org_count,
    values='Company',
    names='Category',
    color='Category',
    color_discrete_sequence=COLOR_QUAL,
    labels=LABELS,
    title='Companies'
).update_layout(
    showlegend=False,
    title_x=0.5
)

pie_cat_collaborations = px.pie(
    category_org_count,
    values='Collaboration',
    names='Category',
    color='Category',
    color_discrete_sequence=COLOR_QUAL,
    labels=LABELS,
    title='Collaborations'
).update_layout(
    showlegend=False,
    title_x=0.5
)

pie_cat_all = px.pie(
    category_org_count,
    values='Total',
    names='Category',
    color='Category',
    color_discrete_sequence=COLOR_QUAL,
    labels=LABELS,
    title='Overall'
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


# --- LAYOUTS ---

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# --- ANALYSES ---

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
                            HEADER_INTRO_TXT,
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
                    className="pretty_container"
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
        dcc.Tabs(id="map-tabs", value='comp-acad-collab', children=[
            dcc.Tab(label='Company vs Academia w/ Collab.', value='comp-acad-collab'),
            dcc.Tab(label='Company vs Academia', value='comp-acad'),
            dcc.Tab(label='Company vs Collaboration', value='comp-collab'),
            dcc.Tab(label='Collaboration vs Academia', value='collab-acad')
        ]),
        html.Div(
            id='map-container',
            className="row pretty_container"
        ),
        html.Div([
                dcc.Graph(
                    id='pie-cat-academia',
                    figure=pie_cat_academia,
                    className="three columns"
                ),
                dcc.Graph(
                    id='pie-cat-companies',
                    figure=pie_cat_companies,
                    className="three columns"
                ),
                dcc.Graph(
                    id='pie-cat-collaborations',
                    figure=pie_cat_collaborations,
                    className="three columns"
                ),
                dcc.Graph(
                    id='pie-cat-all',
                    figure=pie_cat_all,
                    className="five columns"
                ),
            ],
            className="pretty_container row flex-display"
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


# --- DATASET ---

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
                dcc.Markdown(DATASET_FEATURES_TXT)
            ],
                className="pretty_container twelve columns flex-display center-content text-container"
            ),
        ],
            className="row flex-display center-content"
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
        )
])


# --- DESCRIPTION ---

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
                        dcc.Markdown(PROJECT_DESCRIPTION_TXT)
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

@app.callback(Output('map-container', 'children'), Input('map-tabs', 'value'))
def render_map_content(tab):
    if tab == 'comp-acad-collab':
        return dcc.Graph(id='choro-map-comp-acad-collab', figure=choro_map_comp_acad_collab)
    elif tab == 'comp-acad':
        return dcc.Graph(id='choro-map-comp-acad', figure=choro_map_comp_acad)
    elif tab == 'comp-collab':
        return dcc.Graph(id='choro-map-comp-collab', figure=choro_map_comp_collab)
    elif tab == 'collab-acad':
        return dcc.Graph(id='choro-map-collab-acad', figure=choro_map_collab_acad)


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
