# Python Microservice

A Sample Python Microservice using FastAPI

## Create a virtual environment

``` shell
python3 -m venv .venv
```

## Install Requirements

Install FastAPI:

``` shell
pip install "fastapi[all]"
```

Install all other requirements:

``` shell
pip install -r requirements.txt
```

## Start the server

Can now run the server by just running `main.py`:

``` shell
python3 main.py
```

Alternate way of running:

``` shell
uvicorn main:app --reload
```

## View Docs

Documentation is available at:

[docs](http://127.0.0.1:8000/docs)

or

[redocs](http://127.0.0.1:8000/redoc)
