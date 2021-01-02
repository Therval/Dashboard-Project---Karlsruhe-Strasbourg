# Dashboard-Project - Karlsruhe-Strasbourg

The dashboard is deployed at [dashboard-ka-sb.herokuapp.com](https://dashboard-ka-sb.herokuapp.com/)

## Installation

### Install using PyCharm

- Download and install [PyCharm](https://www.jetbrains.com/pycharm/)
- New Project -> Get from VCS -> Github
- Sign in to your Github account
- Then you can select the repo and clone it
- When PyCharm asks, create a virtual environment in a folder called "env" using python3.9 and the requirements.txt.
- If the virtual environment dialog doesn't appear automatically: Select File -> Settings -> Project -> Python Interpreter -> Add.
Then it is probably also necessary to open the requirements.txt and click on "install requirements".
- On Windows you might need to adjust the 'SDK_HOME' path in `.run/app.run.xml` to match the structure of your `env`
directory (eg. to `$PROJECT_DIR$/env/Scripts/python`).

To run, click the green arrow on the top right.
The app is then running on
[http://127.0.0.1:8050/](http://127.0.0.1:8050/)

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

To run:

(activate the virtual environment again, necessary)

```sh
python app.py
```

The app is then running at
[127.0.0.1:8050](http://127.0.0.1:8050/)

## Deployment

The files `runtime.txt`, `Procfile` and the requirement `gunicorn` are used for
[deployment on Heroku](https://dash.plotly.com/deployment).

## Dependencies

This project mainly uses:

- [Python 3.9](https://www.python.org/)
- [Gunicorn](https://gunicorn.org/)
- [Plotly Dash](https://plotly.com/dash/)
- [D-Tale](https://github.com/man-group/dtale)
- [Flask](https://flask.palletsprojects.com/)
- [Pandas](https://pandas.pydata.org/)

## Dataset

The dataset is a record of 283014 published scientific papers.

- `PY`: Publication Year (integer)
- `SC`: (string/category)
- `NR`: (integer)
- `ArtsHumanities /
  LifeSciencesBiomedicine /
  PhysicalSciences /
  SocialSciences /
  Health /
  ComputerScience`:
  (float between 0 and 1)
- `TCperYear`: (float)
- `NumAuthors`: Number of authors (integer)
- `Organisation`: Either "Academia" or "Company" (string/category)
- `Country`: (string/category)
- `Region`: 9 different Regions (string/category)
