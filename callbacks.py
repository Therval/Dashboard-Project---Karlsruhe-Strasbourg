# -*- coding: utf-8 -*-
"""Define the callbacks of the Dash application."""

from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np

from app import app, df
from constants import COLOR_MAP, LABELS, RESEARCH_CATEGORIES

# Set alternative color scheme
color_list = px.colors.qualitative.Antique
# Move grey to fifth position
color_list.insert(4, color_list.pop(10))


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
