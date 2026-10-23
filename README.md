# Python Library Template

A [Cookiecutter](https://github.com/cookiecutter/cookiecutter) template for Python libraries.

## Motivation

This project scaffolds Python libraries with development tools and conventions already configured,
building on the workflow provided by `uv init` or `poetry new`.

## Features

- [uv](https://github.com/astral-sh/uv) for dependency management.
- [just](https://just.systems/man/en/) with ready-to-use project commands.
- [mypy](https://github.com/python/mypy) and [Pyright](https://github.com/microsoft/pyright) for optional static type checking.
- [pytest](https://github.com/pytest-dev/pytest) for testing.
- [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.
- Preconfigured [prek](https://github.com/j178/prek) hooks, a faster alternative to [pre-commit](https://github.com/pre-commit/pre-commit).
- MIT, BSD-3-Clause, or Apache-2.0 license generation with [lice2](https://github.com/seapagan/lice2).

## Installation

Install the template dependencies:

```bash
pip install cookiecutter jinja2-git lice2
```

Then create a project:

```bash
cookiecutter git@github.com:Rub1kCube/python-template-libs.git
```

Alternatively, use a single command with [uvx](https://docs.astral.sh/uv/guides/tools/):

```bash
uvx --with jinja2-git --with lice2 cookiecutter git@github.com:Rub1kCube/python-template-libs.git
```

Enter the generated library directory and initialize Git:

```bash
cd <path-to-lib>
git init
```

Install [just](https://just.systems/man/en/installation.html),
[uv](https://docs.astral.sh/uv/getting-started/installation/), and Bash, then run `just install`.
This installs dependencies and Git hooks while preserving the existing environment.
Use `just reinstall` to recreate the environment and remove generated artifacts.

Run `just` to list available commands. `just check-all` checks dependencies, code, formatting,
types, and tests without applying fixes. Use `just format` to format code and `just check`
to run prek hooks with automatic fixes.
After changing dependencies, run `just install`: check commands do not synchronize the environment
automatically. Use `just upgrade` to update dependency versions and hooks.

## Library type

The `type_lib` prompt offers two options:

- `standard` (default): a regular Python library.
- `django`: a Django 5.2 library with `Django>=5.2,<5.3`, `pytest-django` for testing,
  and `django-stubs[compatible-mypy]` for type checking.

For example, from a local template checkout:

```bash
cookiecutter . --no-input project_name=my-django-lib type_lib=django copyright_holder='Your Name'
```

For Django libraries, pytest and the mypy plugin use `tests.settings`. The `tests/settings.py`
file contains a test-only `SECRET_KEY` and an `INSTALLED_APPS` entry for the library package.
Extend it as needed, for example by adding `DATABASES` for tests that need a database.
The `standard` variant omits this file and the Django settings.

## License selection

Choose `MIT` (default), `BSD-3-Clause`, or `Apache-2.0` at the `license` prompt.
Set `copyright_holder` to the person or organization that owns the copyright; its default is
`Your Name`, so override it when generating a real project, including with `--no-input`.

```bash
cookiecutter . --no-input project_name=my-library license=Apache-2.0 copyright_holder='Example Organization'
```

The post-generation hook writes `LICENSE` with the current year and the supplied copyright holder.
The generated `pyproject.toml` declares the SPDX license identifier and includes the license file
in both wheel and source distributions. License generation uses templates bundled with `lice2`
and does not require a network connection.

## Developing the template

The root `.github/workflows/test.yml` runs these checks on Python 3.13 and 3.14. It also generates
both library types, installs their dependencies, runs their checks, and builds their packages.
Renovate checks the root Python dependencies, `uv.lock`, and GitHub Actions for updates weekly.
Its configuration is in `.github/renovate.json`; the Cookiecutter source directory is excluded
because its `pyproject.toml` contains Jinja syntax. To enable automatic pull requests,
install the [Renovate GitHub App](https://github.com/apps/renovate) and grant it access to this repository.

## Template license

This template is licensed under the MIT License. See [LICENSE](LICENSE) for details.
Generated libraries use the license selected during generation.
