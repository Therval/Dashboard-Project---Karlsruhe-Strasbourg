# -*- coding: utf-8 -*-
"""Define the Dash application."""

import dash
import pandas as pd

from constants import DATASET_PATH

# Import dataset
df = pd.read_parquet(DATASET_PATH)

# Create application instance
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
