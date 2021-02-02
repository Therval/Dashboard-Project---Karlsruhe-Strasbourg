# -*- coding: utf-8 -*-
"""Define the layouts of the Dash application."""

import dash_core_components as dcc
import dash_html_components as html

# Local import of the text strings
from app import df
from constants import (LABELS, RESEARCH_CATEGORIES, PANDASPROFILING_REPORT, SWEETVIZ_REPORT,
                       HEADER_INTRO_TXT, DATASET_FEATURES_TXT, PROJECT_DESCRIPTION_TXT)


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
