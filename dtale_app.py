# -*- coding: utf-8 -*-
"""Run a D-Tale server."""

# Running this requires the dtale package!
# Run this app with `python dtale_app.py` and
# visit http://localhost:8050/ in your web browser.

import pandas as pd
from flask import redirect, request
from dtale.app import build_app
from dtale.views import startup
from dtale.global_state import cleanup
import dtale

DATASET_PATH = 'dataset/papers.parquet'
DATASET_NAME = 'papers'

# Dtale application
app = build_app(reaper_on=False)


@app.route('/reload')
def load_dataset():
    """Load data set and start a dtale instance."""
    df = pd.read_parquet(DATASET_PATH)
    cleanup(DATASET_NAME)
    startup(data_id=DATASET_NAME, data=df, ignore_duplicate=True)
    # Redirect to the data set which was loaded
    return redirect(f'{request.script_root}/dtale/main/{DATASET_NAME}', code=302)


@app.route('/')
@app.route('/instances')
def get_dtale_instances():
    """Get all dtale instances and display them."""
    instances = '<h1>D-Tale Instances</h1>'
    instances += f'<h3><a href="{request.script_root}/reload">Reload Data Set</a></h3>'
    # Iterate all loaded instances
    for data_id in dtale.global_state.get_data().keys():
        data_obj = dtale.get_instance(data_id)
        metadata = dtale.global_state.get_metadata(data_id)
        name = metadata.get('name')
        # Convert pandas timestamp to python dateTime
        time = pd.Timestamp(metadata.get('start'), tz=None).to_pydatetime()
        datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        # Add them to the html list
        instances += f'<a href="{data_obj.main_url()}">{data_id}</a> {datetime}<br>'
    return instances


# Run the application, if this python file is executed
if __name__ == '__main__':
    app.run(host='localhost', port=8050)
