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
# Rename some labels
LABELS = {
         'PY': 'Publication Year',
         'SC': 'Fields of Science',
         'NumAuthors': 'Number of Authors',
         }

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

df = pd.read_parquet(DATASET_PATH)
df_sample = pd.DataFrame({
    'Fruit': ['Apples', 'Oranges', 'Bananas', 'Apples', 'Oranges', 'Bananas'],
    'Amount': [4, 1, 2, 2, 4, 5],
    'City': ['SF', 'SF', 'SF', 'Montreal', 'Montreal', 'Montreal']
})


# --- DEFINE CHARTS ---

histogram_year = px.histogram(
    df,
    x='PY',
    color='Organisation',
    labels=LABELS,
    title='Histogram of papers in the data set by year'
)

df_group = pd.DataFrame({'Count': df.groupby(['PY', 'Organisation']).size()}).reset_index()
histogram_year_line = px.line(
    df_group,
    x='PY',
    y='Count',
    color='Organisation',
    labels=LABELS,
    title='Histogram of papers in the data set by year (line chart)'
)

fig_sample = px.bar(df_sample, x='Fruit', y='Amount', color='City', barmode='group')


# --- LAYOUTS ---

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

analyses_layout = html.Div(children=[
    html.H1(children='Published Scientific Papers Which Use Deep Learning'),
    html.Div(children='''
        Analyses of 283014 scientific papers which use deep learning.
        The papers are published in the Web of Science core collection.
    '''),
    html.A(
        children='You can examine the whole data set here using D-Tale',
        href='/dtale'
    ),

    dcc.Graph(
        id='histogram-year',
        figure=histogram_year
    ),
    dcc.Graph(
        id='histogram-year-line',
        figure=histogram_year_line
    ),

    html.A(
        children='Example charts',
        href='/examples'
    )
])

examples_layout = html.Div(children=[
    dcc.Graph(
        id='example-graph',
        figure=fig_sample
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
    if pathname == '/dtale':
        return None
    elif pathname == '/examples':
        return examples_layout
    else:
        return analyses_layout


# --- START APP ---

# Run the application, if this python file is executed
if __name__ == '__main__':
    app.run_server(debug=True)
