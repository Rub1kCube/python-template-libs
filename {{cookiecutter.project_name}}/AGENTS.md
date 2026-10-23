# Agent instructions for {{ cookiecutter.project_name }}

Use `just` from the repository root to manage this project. The `justfile` is the
source of truth for commands; run `just` to list the available recipes.

## Project layout

- Python version for development: `{{ cookiecutter.min_version_python }}`.
- Library code: `{{ cookiecutter.project_name.lower().replace('-', '_') }}/`.
- Tests: `tests/`.
- Dependencies and tool configuration: `pyproject.toml`.
- Resolved dependency versions: `uv.lock`.
{% if cookiecutter.type_lib == "django" -%}
- Django tests and the mypy plugin use `tests.settings` from `tests/settings.py`.
{% endif %}
## Environment setup

1. Make sure `just`, `uv`, Git, and Bash are available.
2. For a newly generated project, initialize the repository with `git init`.
3. Run `just doctor` to check the local tools.
4. Run `just install` to pin the development Python version, synchronize all
   dependency groups and extras, and install Git hooks through `prek`.

Run `just install` again after changing dependencies or pulling dependency
updates. Recipes set `UV_NO_SYNC=1`, so checks do not synchronize the environment
automatically. There is no need to activate `.venv` manually.

## Development commands

| Command | Purpose |
| --- | --- |
| `just test` | Run the test suite with pytest and three workers. |
| `just test tests/test_example.py` | Run one test file. |
| `just test -k 'example or smoke'` | Select tests by expression. |
| `just lint` | Check Ruff lint rules and formatting without applying fixes. |
| `just format` | Apply Ruff fixes and format code. |
| `just type-check` | Run both mypy and Pyright. |
| `just mypy` / `just pyright` | Run one type checker. |
| `just package` | Check the lockfile, installed environment, and dependency compatibility. |
| `just check-all` | Run `package`, `lint`, `type-check`, and `test`. |
| `just check` | Run prek hooks on all Git-tracked files, with automatic fixes. |

`just lint` and `just format` accept file or directory paths and default to the
entire project. `just test`, `just mypy`, and `just pyright` forward extra arguments
to their tools. The type-checker aliases also have the names `just type-mypy` and
`just type-pyright`.

While working, run the checks relevant to the change. Use `just format` when
formatting or lint fixes are needed, then run `just check-all` before handing off
code changes. Report the checks run and any failures or checks you could not run.

`just check` may modify files, including `uv.lock`; inspect its changes. Hooks
also run when committing. After dependency changes, run `just install` and repeat
the checks. `just package` validates dependencies; use `uv build` when a task
requires building wheel and source distributions, since there is no build recipe.

## Dependency maintenance and cleanup

- Edit dependency declarations in `pyproject.toml`, then run `just install` to
  update the lockfile and environment. Include the resulting `uv.lock` changes.
- `just lock` updates `uv.lock` without synchronizing the environment.
- `just upgrade` upgrades dependencies, synchronizes the environment, and updates
  hook revisions. Use it when dependency upgrades are part of the task.
- `just clean` removes build artifacts, test and lint caches, and coverage output.
- `just venv-remove` (alias `just destroy`) removes `.venv`.
- `just reinstall` removes `.venv` and generated artifacts, then runs installation.
  Use `just install` for routine synchronization of the existing environment.
