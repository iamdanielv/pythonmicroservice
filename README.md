# Python Microservice

A Sample Python Microservice using FastAPI

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.11 or higher
- pip (Python package installer)
- pipenv

## Create a virtual environment

To create an environment from scratch, you can run the following command in your terminal:

```shell
python3 -m venv .venv
```

followed by activating the environment:

```shell
source .venv/bin/activate
```

Alternative way of creating an environment is to use the makefile:

```shell
make env
```

The make file will tell you how to activate the environment. In my case it printed out:

```shell
[i] To activate the virtual environment, type:
  source pythonmicroservice.venv/bin/activate 
```

## Install Application Requirements

### Manual way of installing dependencies

> [!NOTE]  
> You should **activate** your virtual environment before installing dependencies.

Install FastAPI:

```shell
pip install "fastapi[all]"
```

Install all other requirements:

```shell
pip install -r requirements.txt
```

### Using makefile way of installing dependencies

If you used the command:

```shell
make env
```

all of the requirements should already be installed for you. Just make sure that you have activated the environment.

## Start the server

To start the server, you can run the following command in your terminal:

```shell
uvicorn src.main:app --reload
```

Or you can use the makefile target

```shell
make run
```

## View Docs

Documentation is available at:

[docs](http://127.0.0.1:8000/docs)

or

[redocs](http://127.0.0.1:8000/redoc)
