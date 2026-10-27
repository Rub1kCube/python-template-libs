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

#### Context7 (optional)

[Context7](https://context7.com/docs/overview) lets a coding agent retrieve documentation for the project's
dependencies. Connect it in your agent or editor using the [official setup guide](https://context7.com/docs/installation).
For a manual remote MCP connection, use `https://mcp.context7.com/mcp` and follow the
[instructions for your client](https://context7.com/docs/resources/all-clients).
Keep authentication in your client's user settings or credential store.

After connecting, reload the client or start a new session if required, and check that its Context7 tools
are available. Try a documentation request such as:

```text
Look up pytest fixture scopes for the pytest version in uv.lock. use context7
```

The project's `AGENTS.md` explains when to consult Context7 and how to fall back to official documentation
or installed sources if the needed documentation is unavailable. Context7 is an optional development aid;
the Python environment, documentation builds, tests, and CI work independently of it.

To make this library discoverable by other agents, follow the separate
[publication steps](#publishing-documentation-to-context7) below.

#### Contributing code

1. Set up the development environment.
2. Create a branch from `main` and make your changes.
3. Run `just format` to apply Ruff fixes and format the code.
4. Run `just check-all` to check dependencies, code, formatting, types, tests, and documentation without
   applying fixes.
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
just docs                             # Build the HTML documentation
just docs-serve                       # Build and serve documentation locally
just docs-check                       # Build docs strictly and run documentation examples
just docs-linkcheck                   # Check external links in the documentation
```

`just lint` and `just format` accept file and directory paths; without paths they process the entire project.
`just test`, `just mypy`, and `just pyright` forward extra arguments to the corresponding tool.

#### Documentation

Documentation sources live in `docs/`. Run `just docs` to rebuild `docs/_build/html` locally. Before opening
a pull request that changes documentation or public APIs, run `just docs-check`. The external link check uses
the network and is intentionally kept separate from `just check-all`.

Run `just docs-serve` to rebuild the HTML documentation and serve it at <http://127.0.0.1:8000>. Pass a
different port when needed, for example `just docs-serve 9000`, and press `Ctrl+C` to stop the server.

The HTML build also generates `llms.txt` and a Markdown version of each documentation page for AI agents.
These files live alongside the HTML pages in `docs/_build/html/`; edit the documentation sources and
docstrings rather than the generated files. `just docs-check` also verifies that `llms.txt` and `index.md`
are nonempty.

Follow the [documentation guidelines](docs/pages/documentation-guidelines.rst) when writing docstrings,
guides, API references, and executable examples.

The project includes `.readthedocs.yml` for publishing with Read the Docs. Repository maintainers must connect
the repository to Read the Docs once before the documentation is published.

#### Publishing documentation to Context7

Once the library has public documentation with meaningful usage examples, maintainers can submit it to
Context7. This project uses the published `llms.txt` as the entry point: its Markdown pages contain the
documentation after Sphinx has processed it, including content generated by `autodoc`.

1. Run `just docs-check`, then publish the documentation with Read the Docs or another static host.
2. Verify that the public `llms.txt` URL and its linked Markdown pages are accessible. A typical Read the Docs
   URL is `https://your-project.readthedocs.io/en/latest/llms.txt`; use the actual domain and version path
   of your documentation site.
3. Open [Add Library](https://context7.com/add-library?tab=llmstxt), select the `llms.txt` source type,
   and submit that public URL. Building or publishing `llms.txt` alone does not register the library.
4. When indexing finishes, use the library ID shown by Context7 to query a documented usage example and
   check the returned content. Keep examples and API documentation up to date in the Sphinx sources.
5. After publishing documentation updates, request a refresh from the library's Context7 page when needed.
   See [Keeping Libraries Fresh](https://context7.com/docs/library-updates) for refresh behavior.

For repository-based indexing, the included [`context7.json`](context7.json) selects `docs/` and excludes
`docs/_build/`, `AGENTS.md`, `CONTRIBUTING.md`, and `documentation-guidelines.rst`. Context7 also includes
root-level Markdown files, so the library's `README.md` remains available. Extend the folder list when
adding user guides or examples outside `docs/`; `excludeFiles` entries must be filenames, not paths.
The generated title and description are included when they meet Context7's length limits
(1–100 and 10–500 characters respectively); otherwise Context7 can infer this metadata.

To use this configuration, commit it to the public repository and submit the repository URL using the
GitHub source type on [Add Library](https://context7.com/add-library). These exclusions apply to repository
indexing; they do not change the published `llms.txt` or its Markdown pages. Prefer the published output
described above when the API reference relies on Sphinx `autodoc`.

The file does not register the library or connect an MCP client automatically. For ownership verification,
add the actual `url` and `public_key` provided by Context7 when following the
[library owner guide](https://context7.com/docs/library-owners).
