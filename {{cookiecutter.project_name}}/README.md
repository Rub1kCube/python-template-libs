# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

## Usage example

```python
from {{cookiecutter.project_name.lower().replace('-', '_')}}.example import some_function

print(some_function(3, 4))
# => 7
```

## License

This project is licensed under {{ cookiecutter.license }}. See [LICENSE](LICENSE) for details.

### Contributing 📦

#### Environment setup

1. Install [just](https://just.systems/man/en/installation.html),
   [uv](https://docs.astral.sh/uv/getting-started/installation/), Git, and Bash.
2. Clone the repository and enter its directory. For a newly generated project, run `git init`.
3. Run `just doctor` to check that the required tools are available.
4. Run `just install` to install the project, all dependency groups, and Git hooks
   through [`prek`](https://github.com/j178/prek).

Running `just install` again synchronizes the existing environment. `just reinstall` removes
`.venv`, caches, and build artifacts, then installs the project again.
Check commands do not update the environment automatically: after changing dependencies,
run `just install`. Use `just upgrade` to update dependency versions and hooks.

Run `just` to list commands by group.

#### Contributing code

1. Set up the development environment.
2. Create a branch from `main` and make your changes.
3. Run `just format` to apply Ruff fixes and format the code.
4. Run `just check-all` to check dependencies, code, formatting, types, and tests without applying fixes.
5. If needed, run `just check`: this runs prek hooks on Git-tracked files and may modify files,
   including `uv.lock`. These hooks also run when you commit.
   After changing dependencies, repeat `just install` and `just check-all`.
6. Commit your changes and open a pull request. Pull request titles and commit messages should follow
   [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).
   For example: `feat: add a model for working with MySQL`.

Individual checks can be run independently:

```bash
just test                             # All tests
just test tests/test_example.py        # One test file
just test -k 'example or smoke'        # Select tests by expression
just mypy tests/test_example.py        # Type-check one file
just type-check                       # Run mypy and Pyright on the entire project
just lint tests/test_example.py        # Check lint and formatting for one file
just package                          # Check the lockfile and installed environment
```

`just lint` and `just format` accept file and directory paths; without paths they process the entire project.
`just test`, `just mypy`, and `just pyright` forward extra arguments to the corresponding tool.
