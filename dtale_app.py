# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# import os
import pandas as pd
from flask import redirect
from dtale.app import build_app
from dtale.views import startup

DATASET_PATH = 'dataset/papers.parquet'

if __name__ == '__main__':
    app = build_app(reaper_on=False)

    @app.route("/dtale")
    def run_dtale():
        df = pd.read_parquet(DATASET_PATH)
        # dtale.cleanup("1")
        # dtale.views.startup(data_id="1", data=df, ignore_duplicate=True)
        # return redirect(f"/dtale/main/1", code=302)
        instance = startup(data=df, ignore_duplicate=True)
        return redirect(f"/dtale/main/{instance._data_id}", code=302)


    @app.route("/")
    def hello_world():
        return 'Hi there, load data using <a href="/dtale">dtale</a>'

    app.run(host="0.0.0.0", port=8080)
