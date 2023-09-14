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
