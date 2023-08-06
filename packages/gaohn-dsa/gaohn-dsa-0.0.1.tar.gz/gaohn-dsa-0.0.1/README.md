<div align="center">
<h1>Data Structures and Algorithm Documentation</a></h1>
by Hongnan Gao
Oct, 2022
<br>
</div>

This is the documentation for various data structures and algorithms concepts.

## Workflow

### Installation

```bash
~/gaohn                  $ git clone https://github.com/gao-hongnan/gaohn-dsa.git gaohn-dsa
~/gaohn                  $ cd gaohn-dsa
~/gaohn/gaohn-dsa        $ python -m venv <venv_name> && <venv_name>\Scripts\activate
~/gaohn/gaohn-dsa (venv) $ python -m pip install --upgrade pip setuptools wheel
~/gaohn/gaohn-dsa (venv) $ pip install -r requirements.txt
~/gaohn/gaohn-dsa (venv) $ pip install myst-nb==0.16.0
```

The reason for manual install of `myst-nb==0.16.0` is because it is not in sync
with the current jupyterbook version, I updated this feature to be able to show
line numbers in code cells.

### Setting up Continuous Integration

```bash
~/gaohn/gaohn-dsa (venv) $ mkdir -p .github/workflows .github/actions
```

```bash
~/gaohn/gaohn-dsa (venv) $ curl -o .github/actions/continuous-integration/action.yaml \
    https://raw.githubusercontent.com/gao-hongnan/common-utils/main/.github/actions/continuous-integration/template.yaml
```

```bash
~/gaohn/gaohn-dsa (venv) $ curl -o .github/workflows/continuous_integration.yaml \
    https://raw.githubusercontent.com/gao-hongnan/common-utils/main/.github/workflows/continuous_integration.yaml
```

Change the environment variable `PACKAGES_TO_CHECK` to `dsa` in
`.github/workflows/continuous_integration.yaml`.

### Building the book

After cloning, you can edit the books source files located in the `content/`
directory.

You run

```bash
~/gaohn (venv) $ jupyter-book build content/
```

to build the book, and

```bash
~/gaohn (venv) $ jupyter-book clean content/
```

to clean the build files.

A fully-rendered HTML version of the book will be built in
`content/_build/html/`.

## MyST NB

See
[config documentation](https://myst-nb.readthedocs.io/en/latest/configuration.html).
