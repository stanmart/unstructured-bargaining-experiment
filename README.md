[![Website](https://img.shields.io/website?url=https%3A%2F%2Fbargaining-experiment-b57fff22feef.herokuapp.com%2Fdemo&logo=heroku)](https://bargaining-experiment-b57fff22feef.herokuapp.com/demo)
[![Checks](https://github.com/stanmart/unstructured-bargaining-experiment/actions/workflows/ci.yml/badge.svg)](https://github.com/stanmart/unstructured-bargaining-experiment/actions/workflows/ci.yml)
[![oTree](https://img.shields.io/badge/powered_by-oTree-blue?logo=python)](https://www.otree.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org/licenses/MIT)

# unstructured-bargaining-experiment
An otree experiment for testing unstructured bargaining in a specific context.

## Installation

### pixi (recommended)

The recommended way to install the project is using [pixi](https://pixi.sh/), which manages both conda and pip dependencies across all platforms.

Install pixi following the [installation instructions](https://pixi.sh/latest/#installation), then simply run:

```bash
pixi install
```

That's it! All dependencies will be installed automatically.

<details>
<summary>uv</summary>

Alternatively, you can use [uv](https://docs.astral.sh/uv/) for a fast Python package manager.

Create the environment with Python 3.12:
```bash
    uv venv --python 3.12
```
Activate the environment:
```bash
    source .venv/bin/activate  # Linux/Mac
    .venv/Scripts/activate  # Windows
```

Then install the requirements:
```bash
    uv pip install -r requirements.txt
```

</details>

### pre-commit

To set up pre-commit hooks for code quality checks:

```bash
pixi run pre-commit-install
```

This will run linting and formatting checks automatically on every commit.

<details>
<summary>Without pixi</summary>

You'll need to install pre-commit manually (e.g., with pip or your package manager) and then run:

```bash
pre-commit install
```

</details>

## Running a development server

Open a terminal in the project folder and run:

```bash
pixi run dev
```

<details>
<summary>Without pixi</summary>

```bash
otree devserver
```

</details>

Then navigate to http://localhost:8000 in your browser.
You can stop the server by pressing <btn>Ctrl</btn>+<btn>c</btn> in your terminal window.

## Prod deployment

The `Procfile` is set up to start a production server on Heroku. Simply create an app, assign a dyno and a Postgres database, and deploy the app from this repo.

## Testing and code quality

The project has a number of tests and code quality checks. **Please make sure that all checks pass before merging to the main branch.**

**Running tests locally:**
```bash
pixi run test  # Run oTree tests with bots
```

**Running linting and type checks locally:**
```bash
pixi run -e lint lint  # Run all linting checks (ruff, codespell, pyright)
```

<details>
<summary>Without pixi</summary>

Make sure that `pre-commit` and `pyright` are installed and available in your PATH.

Then run:

```bash
otree test  # Run oTree tests
pre-commit run --all-files  # Run ruff and codespell
pyright  # Run type checking
```

</details>

### Continuous Integration (CI)

The project is set up with GitHub Actions to run these checks automatically on every push and pull request to the main branch.

<details>
<summary>Checks performed by CI</summary>

 - `otree test` for playing the experiment with automated bots
 - `pyright` for Python type checking
 - `ruff check` for Python code style
 - `ruff format` for Python code formatting
 - `codespell` for spell checking

</details>
