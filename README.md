# Ticker-Analysis

## Setup

Create virtual environment:

```sh
conda create -n san-env python=3.11
```

Activate the environment:

```sh
conda activate san-env
```

Install packages:

```sh
pip install -r requirements.txt
```

## Usage

Run the script:

```sh
python app/trend_chart.py

# equivalent:
python -m app.trend_chart
```

Run Flask:

Run the web app (then view in the browser at http://localhost:5000/):

```sh
# Mac OS:
FLASK_APP=web_app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=web_app
flask run
```

## Testing

Run Tests:

```sh
pytest
```