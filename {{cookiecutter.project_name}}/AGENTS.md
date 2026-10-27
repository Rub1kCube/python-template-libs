# Agent instructions for {{ cookiecutter.project_name }}

Use `just` from the repository root to manage this project. The `justfile` is the
source of truth for commands; run `just` to list the available recipes.

## Project layout

- Python version for development: `{{ cookiecutter.min_version_python }}`.
- Library code: `{{ cookiecutter.project_name.lower().replace('-', '_') }}/`.
- Tests: `tests/`.
- Documentation: `docs/`.
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
| `just docs` | Build the HTML documentation. |
| `just docs-check` | Build documentation strictly and run its doctests. |
| `just docs-linkcheck` | Check external links in the documentation. |
| `just check-all` | Run `package`, `lint`, `type-check`, `test`, and `docs-check`. |
| `just check` | Run prek hooks on all Git-tracked files, with automatic fixes. |

`just lint` and `just format` accept file or directory paths and default to the
entire project. `just test`, `just mypy`, and `just pyright` forward extra arguments
to their tools. The type-checker aliases also have the names `just type-mypy` and
`just type-pyright`.

## Code verification

Run verification commands from the repository root:

- Tests: `just test`.
- Linting and formatting check: `just lint`.
- Formatting and automatic fixes: `just format`.
- Static type analysis: `just type-check`.
- Documentation: `just docs-check`.
- Full verification: `just check-all`.

After changing code:

1. Run `just format`.
2. Run the checks relevant to the changed code.
3. Run `just check-all` before committing or handing off the change.
4. Report which checks were run and whether they passed. Include any failures or
   checks that could not be run.

`just check` may modify files, including `uv.lock`; inspect its changes. Hooks
also run when committing. After dependency changes, run `just install` and repeat
the checks. Unlike `just format` and `just check`, `just check-all` is intended to
verify the project without applying fixes. `just package` validates dependencies;
use `uv build` when a task requires building wheel and source distributions, since
there is no build recipe.

## External dependency documentation

- When a task needs documentation for a dependency's API, behavior, or
  configuration, use Context7 if its tools are available.
- Identify the dependency version in `uv.lock` and request documentation for that
  version when available. Before the first lockfile is generated, use the
  constraints in `pyproject.toml` and state any uncertainty about the exact version.
- Resolve the library's Context7 ID before querying its documentation, unless a
  verified ID is already available. Check that examples apply to the project's
  dependency version before using them.
- If Context7 is unavailable or lacks the required library or version, consult
  official versioned documentation or the installed package's source and
  docstrings. Context7 availability must not block development or verification.
- Use this repository's code and documentation to understand the library being
  developed; an external index may lag behind local changes.

See [Context7 setup](CONTRIBUTING.md#context7-optional) for optional client setup
and the separate process for indexing this library's published documentation.

## Documentation rules

A change to public behavior is incomplete until its docstrings, guides, and API
reference are updated and `just docs-check` passes. Follow the complete
[documentation guidelines](docs/pages/documentation-guidelines.rst).

- Document every new or changed public module, class, function, method, and
  attribute. Do not document private implementation details unless they explain
  an important constraint.
- Use Google-style docstrings. Keep types in Python annotations instead of
  repeating them in docstrings.
- Include `Args`, `Returns`, `Yields`, and `Raises` only when applicable. Explain
  behavior, constraints, side effects, and exceptions rather than restating names.
- Use Sphinx roles such as `:class:`, `:func:`, `:meth:`, `:attr:`, and `:doc:`
  for internal references. Prefer fully qualified targets when a reference could
  be ambiguous.
- Put stable, executable examples in `.. doctest::` blocks. Use `.. code-block::`
  for illustrative examples that require network access, nondeterministic values,
  external services, or extensive setup.
- Add public modules and objects to `docs/pages/api-reference.rst`; add conceptual
  or task-oriented documentation to the appropriate guide and to a `toctree`.
- Never edit generated files under `docs/_build/`.
- Run `just docs-check` after changing public APIs or documentation. Run
  `just docs-linkcheck` when adding or changing external links.

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
