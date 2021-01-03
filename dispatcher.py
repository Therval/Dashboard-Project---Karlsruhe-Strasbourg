# -*- coding: utf-8 -*-
"""Run a dispatcher for the Dash application and D-Tale."""

# TODO D-Tale does not work correctly!

# Run this app with `python dispatcher.py` and
# visit http://localhost:8050/ in your web browser.

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import server as dash_app
from dtale_app import app as dtale_app
from werkzeug.serving import run_simple

# Run Dash app as default and D-Tale under '/dtale'
app = DispatcherMiddleware(dash_app, {'/dtale': dtale_app})

# Run the application, if this python file is executed
if __name__ == '__main__':
    run_simple('localhost', 8050, app, use_reloader=True, use_debugger=True, use_evalex=True)
