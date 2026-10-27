# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

## Usage example

```python
from {{cookiecutter.project_name.lower().replace('-', '_')}}.example import some_function

print(some_function(3, 4))
# => 7
```

## Documentation

The documentation source is available in [`docs/`](docs/index.rst). Build it locally with:

```bash
just docs
```

Run `just docs-check` to perform a clean, strict build and execute documentation examples.
The included `.readthedocs.yml` can be used to publish the documentation on
[Read the Docs](https://readthedocs.org/).

## License

This project is licensed under {{ cookiecutter.license }}. See [LICENSE](LICENSE) for details.
