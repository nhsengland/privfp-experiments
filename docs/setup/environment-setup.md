# Environment Set-up

## Create a suitable environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Note that a separate Python 3.9 environment is required to run the scispacy notebooks:

```bash
python3.9 -m venv .venv_scispacy
source .venv_scispacy/bin/activate
pip install -r requirements_scispacy.txt
```


## Pre-commit Installation

This repo uses `pre-commit` to ensure `black` and `flake8` has been applied. You will need to make sure your virtual environment has been activated.

```bash 
source .venv/bin/activate
pre-commit install
```