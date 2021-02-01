# -*- coding: utf-8 -*-
"""Run the Dash application."""

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
# Local import of the text strings
from texts import HEADER_INTRO_TXT, DATASET_FEATURES_TXT, PROJECT_DESCRIPTION_TXT


# --- SET THE CONSTANTS ---

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
color_list = px.colors.qualitative.Antique
# Move grey to fifth position
color_list.insert(4, color_list.pop(10))


# --- INITIATE THE APP ---

# Create application instance
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Import dataset
df = pd.read_parquet(DATASET_PATH)


# --- CALCULATIONS ---

# Publication year range
py_min = int(df['PY'].min())
py_max = int(df['PY'].max())
# This adds three dicts together to describe the markers of the year range:
# There is marker every year with an empty label,
# every five years there is a marker with the year as label
# and there is the last year with a label
year_range_marks = {
    **{i: '' for i in range(py_min, py_max)},
    **{i: str(i) for i in range(py_min, py_max, 5)},
    **{py_max: str(py_max)}
}


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
                            className='ten columns'
                        ),
                        html.Div([
                                html.A(
                                    'Learn More',
                                    href='/description',
                                    id='learn-more-btn',
                                    role='button',
                                    className='button'
                                ),
                                html.A(
                                    'Explore Dataset',
                                    href='/dataset',
                                    id='explore-dataset-btn',
                                    role='button',
                                    className='button'
                                )
                            ],
                            className='two columns item-column'
                        )
                    ],
                    className='pretty_container'
                ),
            ],
            id='header-description',
            className='row flex-display'
        ),
        html.Div([
                html.Div([
                        html.P(
                            'Filter by research area (overlapping categories):',
                            className='control_label three columns'
                        ),
                        dcc.Dropdown(
                            id='category-filter',
                            options=[{'label': LABELS[category], 'value': category}
                                     for category in RESEARCH_CATEGORIES],
                            multi=True,
                            value=RESEARCH_CATEGORIES,
                            className='dcc_control'
                        )
                    ],
                    className='row flex-display'
                ),
                html.Div([
                        html.P(
                            'Filter by year published:',
                            className='control_label three columns'
                        ),
                        dcc.RangeSlider(
                            id='year-slider',
                            marks=year_range_marks,
                            min=py_min,
                            max=py_max,
                            value=[py_min, py_max],
                            className='dcc_control seven columns'
                        ),
                        html.Button(
                            id='submit-button-state',
                            n_clicks=0,
                            children='Update Charts'
                        )
                    ],
                    className='row flex-display'
                ),
            ],
            className='pretty_container'
        ),
        html.Div([
                dcc.Graph(
                    id='histogram-year',
                    className='pretty_container eight columns'
                ),
                dcc.Graph(
                    id='pie-org',
                    className='pretty_container four columns'
                )
            ],
            className='row flex-display'
        ),
        dcc.Tabs([
                dcc.Tab(label='Company vs Academia w/ Collab.', value='comp-acad-collab'),
                dcc.Tab(label='Company vs Academia', value='comp-acad'),
                dcc.Tab(label='Company vs Collaboration', value='comp-collab'),
                dcc.Tab(label='Collaboration vs Academia', value='collab-acad')
            ],
            id='map-tabs',
            value='comp-acad-collab'
        ),
        html.Div([
                dcc.Graph(
                    id='choropleth-map'
                )
            ],
            className='row pretty_container'
        ),
        html.Div(
            id='map-data',
            style={'display': 'none'}
        ),
        html.Div([
                html.Div([
                        html.H5(
                            'Research Area Distribution',
                            className='center-content flex-display twelve columns'
                        )
                    ],
                    className='row flex-display'
                ),
                html.Div([
                        dcc.Graph(
                            id='pie-cat-all',
                            className='five columns'
                        ),
                        dcc.Graph(
                            id='pie-cat-academia',
                            className='three columns'
                        ),
                        dcc.Graph(
                            id='pie-cat-companies',
                            className='three columns'
                        ),
                        dcc.Graph(
                            id='pie-cat-collaborations',
                            className='three columns'
                        )
                    ],
                    className='row flex-display'
                ),
            ],
            className='pretty_container'
        ),
        html.Div([
                html.A([
                        'Example charts',
                    ],
                    href='/examples',
                    role='button',
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
                className='pretty_container twelve columns flex-display center-content text-container'
            ),
        ],
            className='row flex-display center-content'
        ),
        html.Div([
                html.Div([
                        html.A(
                            'Show Pandas Profiling Report',
                            href=f'/static/{PANDASPROFILING_REPORT}',
                            target='_blank',
                            rel='noopener noreferrer',
                            id='pandas-profiling-btn',
                            role='button',
                            className='button'
                        ),
                        html.A(
                            'Show Sweetviz Profiling Report',
                            href=f'/static/{SWEETVIZ_REPORT}',
                            target='_blank',
                            rel='noopener noreferrer',
                            id='sweetviz-btn',
                            role='button',
                            className='button'
                        ),
                        html.A(
                            'Read the Project Description',
                            href='/description',
                            id='learn-more-btn',
                            role='button',
                            className='button'
                        ),
                        html.A(
                            'Return to the Dashboard',
                            href='/',
                            id='return-dashboard-btn',
                            role='button',
                            className='button'
                        )
                    ],
                    className='pretty_container twelve columns item-column'
                ),
            ],
            className='row flex-display center-content'
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
                    className='pretty_container twelve columns text-container'
                ),
            ],
            className='row flex-display center-content'
        ),
        html.Div([
                html.Div([
                        html.A(
                            'Explore the Dataset',
                            href='/dataset',
                            id='explore-dataset-btn',
                            role='button',
                            className='button'
                        ),
                        html.A(
                            'Return to the Dashboard',
                            href='/',
                            id='return-dashboard-btn',
                            role='button',
                            className='button'
                        )
                    ],
                    className='pretty_container twelve columns item-column'
                ),
            ],
            className='row flex-display center-content'
        )
])


# --- HELPER FUNCTIONS ---

def filter_dataframe(filter_categories, year_range):
    """Init mask with only False values, add selected categories and filter by year range."""
    mask = pd.Series(index=df.index, dtype=bool)
    for category in filter_categories:
        mask = mask | df[category].astype(bool)
    return df[mask & (df['PY'] >= year_range[0]) & (df['PY'] <= year_range[1])]


def calc_country_org_count(dff):
    """Calculate the count of organisation by country."""
    # Count of organisation by country
    counts = dff.groupby(['CountryCode', 'Organisation']).size().unstack()
    # Flatten hierarchical columns
    counts.columns = counts.columns.tolist()
    # Add country names from dataset
    counts = counts.merge(
        dff[['CountryCode', 'Country']],
        how='left',
        on='CountryCode'
    ).drop_duplicates().reset_index(drop=True)
    # Calculate fractions
    counts['CompanyAcademiaFraction'] = 100 / (
            counts['Academia'] / counts['Company'] + 1)
    counts['CompanyCollaborationFraction'] = 100 / (
            counts['Collaboration'] / counts['Company'] + 1)
    counts['CollaborationAcademiaFraction'] = 100 / (
            counts['Academia'] / counts['Collaboration'] + 1)
    counts['CompanyAcademiaCollabFraction'] = 100 / ((
            counts['Academia'] +
            counts['Collaboration']
        ) / (
            counts['Company'] +
            counts['Collaboration']
        ) + 1)
    return counts


def draw_histogram(dff):
    """Draw the histogram chart."""
    # Count of organisation by year
    year_org_count = pd.DataFrame({'Count': dff.groupby(['PY', 'Organisation']).size()}).reset_index()

    fig = px.bar(
        year_org_count,
        x='PY',
        y='Count',
        barmode='group',
        color='Organisation',
        color_discrete_map=COLOR_MAP,
        labels=LABELS,
        title='Published Papers in the Data Set'
    ).update_layout(
        title_x=0.5
    )
    return fig


def draw_pie(dff):
    """Draw the pie chart."""
    # Count of organisation
    org_count = pd.DataFrame({'Count': dff.groupby(['Organisation']).size()}).reset_index()

    fig = px.pie(
        org_count,
        values='Count',
        names='Organisation',
        color='Organisation',
        color_discrete_map=COLOR_MAP,
        title='Distribution of Academia vs Companies'
    ).update_layout(
        title_x=0.5
    )
    return fig


def draw_category_pies(dff):
    """Draw the category pie charts."""
    # Count of organization type for each category
    category_org_count = dff[[
        *RESEARCH_CATEGORIES,
        'Organisation'
    ]].replace(0, np.nan).groupby('Organisation').agg('count').T
    # Flatten categorical columns
    category_org_count.columns = category_org_count.columns.tolist()
    # Set names properly and reset the index
    category_org_count['Total'] = category_org_count.sum(axis='columns')
    category_org_count = category_org_count.reset_index().rename({'index': 'Category'}, axis='columns').replace(LABELS)

    pie_cat_academia = px.pie(
        category_org_count,
        values='Academia',
        names='Category',
        color='Category',
        color_discrete_sequence=color_list,
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
        color_discrete_sequence=color_list,
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
        color_discrete_sequence=color_list,
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
        color_discrete_sequence=color_list,
        labels=LABELS,
        title='Overall'
    ).update_layout(
        title_x=0.5
    )
    return [pie_cat_academia, pie_cat_companies, pie_cat_collaborations, pie_cat_all]


# --- CALLBACKS ---

@app.callback(Output('choropleth-map', 'figure'),
              Input('map-tabs', 'value'),
              Input('map-data', 'children'))
def draw_map(tab, counts_json):
    """Draw the four different choropleth maps."""
    # Import jsonified saved map-data
    country_org_count = pd.read_json(counts_json, orient='split')

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
        title='Company to Academia Publication Fractions',
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
        title='Company to Collaboration Publication Fractions',
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
        title='Collaboration to Academia Publication Fractions',
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
        title='Company to Academia Publication Fractions (Collab. count for both)',
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

    if tab == 'comp-acad-collab':
        return choro_map_comp_acad_collab
    elif tab == 'comp-acad':
        return choro_map_comp_acad
    elif tab == 'comp-collab':
        return choro_map_comp_collab
    elif tab == 'collab-acad':
        return choro_map_collab_acad


@app.callback(Output('histogram-year', 'figure'),
              Output('pie-org', 'figure'),
              Output('map-data', 'children'),
              Output('pie-cat-all', 'figure'),
              Output('pie-cat-academia', 'figure'),
              Output('pie-cat-companies', 'figure'),
              Output('pie-cat-collaborations', 'figure'),
              Input('submit-button-state', 'n_clicks'),
              State('category-filter', 'value'),
              State('year-slider', 'value'))
def create_charts(_n_clicks, filter_categories, year_range):
    """Calls functions for creating/updating charts and outputs them."""
    del _n_clicks  # n_clicks is only used for triggering this function
    dff = filter_dataframe(filter_categories, year_range)
    return (draw_histogram(dff),
            draw_pie(dff),
            calc_country_org_count(dff).to_json(orient='split'),
            *draw_category_pies(dff))


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
    else:
        # the default
        return analyses_layout


# --- START APP ---

# Run the application, if this python file is executed
if __name__ == '__main__':
    app.run_server(debug=True)
