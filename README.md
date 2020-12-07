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

The app is then running on
[127.0.0.1:8050](http://127.0.0.1:8050/)

## Deployment

`Procfile` and the requirement `gunicorn` are necessary for
[deployment on Heroku](https://dash.plotly.com/deployment).

## Dependencies

This project mainly uses:

- [Python 3.9](https://www.python.org/)
- [Gunicorn](https://gunicorn.org/)
- [Plotly Dash](https://plotly.com/dash/)
- [Pandas](https://pandas.pydata.org/)

# TODO

- Create a general presentation of the project with the subject, needed Python librairies and so on.
