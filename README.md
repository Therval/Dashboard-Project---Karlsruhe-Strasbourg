# Dashboard-Project - Karlsruhe-Strasbourg

The dashboard is deployed at [diffusion.herokuapp.com](https://diffusion.herokuapp.com/)

## Installation

### Install using PyCharm

- Download and install [PyCharm](https://www.jetbrains.com/pycharm/)
- New Project -> Get from VCS -> Github
- Sign in to your Github account
- Then you can select the repo and clone it
- When PyCharm asks, create a virtual environment in a folder called "env" using python3.8 and the requirements.txt.
- If the virtual environment dialog doesn't appear automatically: Select File -> Settings -> Project -> Python Interpreter -> Add.
Then it is probably also necessary to open the requirements.txt and click on "install requirements".
  If you have problems installing `pyarrow`, make sure you are using python 3.8 or try installing the nightly:
  `pip install --extra-index-url https://pypi.fury.io/arrow-nightlies/ --pre pyarrow`.

### Install using the terminal

Clone the repo:

```sh
git clone https://github.com/Therval/Dashboard-Project---Karlsruhe-Strasbourg.git
cd Dashboard-Project---Karlsruhe-Strasbourg
```

Set up the environment on macOS and Linux:

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Set up the environment on Windows:

```sh
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

### Run as development server

(activate the virtual environment again, necessary)

```sh
python app.py
# To run a dtale application with the data set:
python dtale_app.py
```

The app is then running at
[127.0.0.1:8050](http://127.0.0.1:8050/)

On Windows you might need to adjust the 'SDK_HOME' path in the `.run` files to match the structure of your `env`
directory (eg. to `$PROJECT_DIR$/env/Scripts/python`).

To run in PyCharm, select the app on the top right and click the green arrow.

## Deployment

The files `runtime.txt`, `Procfile` and the requirement `gunicorn` are used for
[deployment on Heroku](https://dash.plotly.com/deployment).

## Dependencies

This project mainly uses:

- [Python 3.8](https://www.python.org/)
- [Gunicorn](https://gunicorn.org/)
- [PyArrow](https://arrow.apache.org/docs/python/)
- [Plotly Dash](https://plotly.com/dash/)
- [D-Tale](https://github.com/man-group/dtale)
- [Flask](https://flask.palletsprojects.com/)
- [Werkzeug](https://palletsprojects.com/p/werkzeug/)
- [Pandas](https://pandas.pydata.org/)

## Dataset

This dataset includes a total of 287544 scientific publications which use deep learning.
These papers were published in the Web of Science Core Collection.
The papers were retrieved through web scraping.
The use of deep learning was identified through keyword search in the title and abstract.
The author metadata was used The author metadata was used for classifying the publications
into company, academia or collaborations of both.

The classification of research areas can be found here:
[webofknowledge.com](https://images.webofknowledge.com/images/help/WOS/hp_research_areas_easca.html)

- `PY`: Year Published (integer)
- `SC`: Research Areas (string/category)
- `ArtsHumanities /
  LifeSciencesBiomedicine /
  PhysicalSciences /
  SocialSciences /
  Health /
  ComputerScience`:
  (float between 0 and 1)
- `NR`: Cited Reference Count (integer)
- `TCperYear`: Web of Science Core Collection Times Cited Count per Year (float)
- `NumAuthors`: Number of Authors (integer)
- `Organisation`: Either "Academia", "Company" or "Collaboration" (string/category)
- `Region`: 9 Different Regions (string/category)
- `Country`: Country Name of Author (string/category)
- `CountryCode`: ISO 3166-1 Alpha-3 Country Code (string/category)
