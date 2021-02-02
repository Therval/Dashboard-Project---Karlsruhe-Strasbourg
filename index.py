# -*- coding: utf-8 -*-
"""Run the Dash application."""

# Run this app with `python index.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Although server and callbacks are not used directly, they are still needed
from app import app, server
from layouts import analyses_layout, dataset_layout, description_layout
import callbacks

app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    """Route to the desired page."""
    if pathname == '/':
        return analyses_layout
    elif pathname == '/dataset':
        return dataset_layout
    elif pathname == '/description':
        return description_layout
    else:
        # the default
        return analyses_layout


# Run the application, if this python file is executed
if __name__ == '__main__':
    app.run_server(debug=True)
