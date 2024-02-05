![Website](https://img.shields.io/website?url=https%3A%2F%2Fbargaining-experiment-b57fff22feef.herokuapp.com%2Fdemo&logo=heroku)
[![Checks](https://github.com/stanmart/unstructured-bargaining-experiment/actions/workflows/ci.yml/badge.svg)](https://github.com/stanmart/unstructured-bargaining-experiment/actions/workflows/ci.yml)

# unstructured-bargaining-experiment
An otree experiment for testing unstructured bargaining in a specific context.

## Installation

It is recommended to use a virtual environment for the project (either through `conda` or `venv`):

<details>
<summary>conda (standard)</summary>

Create the environment
```bash
    conda create unstructured-bargaining-experiment
```
Activate the environment:
```bash
    conda activate unstructured-bargaining-experiment
```
Deactivate the environment:
```bash
    conda deactivate
```

</details>

<details>
<summary>conda (local)</summary>

Create the environment
```bash
    conda create --prefix=venv -y
```
Activate the environment:
```bash
    conda activate ./venv
```
Deactivate the environment:
```bash
    conda deactivate
```

</details>

<details>
<summary>venv</summary>

Create the environment
```bash
    python3 -m venv ./venv
```
Activate the environment:
```bash
    source venv/bin/activate  # Linux/Mac
    venv/Script/activate  # Windows
```
Deactivate the environment:
```bash
    deactivate
```

</details>

Then install the requirements in this isolated environment.
We have to use `pip` as `oTree` is not on conda-forge yet.

```bash
    pip install -r requirements.txt
```

## Testing locally

Open a terminal in the project folder and run

```bash
otree devserver
```

Then navigate to http://localhost:8000 in your browser.
You can stop the server by pressing <btn>Ctrl</btn>+<btn>c</btn> in your terminal window.

## Prod deployment

The `Procfile` is set up to start a production server on Heroku. Simply create an app, assign a dyno and a Postgres database, and deploy the app from this repo.

## Automated checks

The project is set up with GitHub Actions to run automated checks on every push and pull request to the main branch. The checks include:
 - `pyright` for Python type checking
 - `ruff check` for Python code style
 - `ruff format` for Python code formatting
 - `codespell` for spell checking

<details>
<summary>Running the checks locally</summary>
You can also run these checks locally. For `pyright`, you need to have the `pyright` package installed. The rest of them are implemented as `pre-commit` hooks.

First, install `pyright` and `pre-commit`, e.g. using `pipx`:

```bash
pipx install pyright
pipx install pre-commit
```

Then, you can install the `pre-commit` hooks by running

```bash
pre-commit install
```
This will install the hooks and run them on every commit automatically.

Finally, you can run the `pyright` checks using

```bash
pyright
```
</details>

Please make sure that all checks pass before merging to the main branch.
