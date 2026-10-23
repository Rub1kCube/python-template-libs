import json
import re
import sys
from typing import Final


MODULE_REGEX: Final = r"^[a-z][a-z0-9\-\_]+[a-z0-9]$"
MODULE_NAME: Final[str] = json.loads(r""" {{ cookiecutter.project_name | tojson }} """)
COPYRIGHT_HOLDER: Final[str] = json.loads(r""" {{ cookiecutter.copyright_holder | tojson }} """)


def _validate_project_name() -> None:
    """
    This validator is used to ensure that `project_name` is valid.

    Valid inputs starts with the lowercase letter.
    Followed by any lowercase letters, numbers or hyphens.
    Ends with a lowercase letter or number.

    Valid example: `school_project3`.
    """
    if not re.match(MODULE_REGEX, MODULE_NAME):
        # Validates project's module name:
        message = [
            "ERROR: The project slug {0} is not a valid Python module name.",
            "Start with a lowercase letter.",
            "Followed by any lowercase letters, numbers or hyphens (-).",
            "End with a lowercase letter or number.",
        ]
        if "_" in MODULE_NAME:
            message.append("Do not use underscores (_) in your project name.")
        raise ValueError(" ".join(message).format(MODULE_NAME))


def _validate_deps() -> None:
    """Ensure that all deps are installed."""
    try:
        from lice2.api import Lice  # noqa: F401, PLC0415
    except ImportError:
        msg = "License generation requires lice2. Install it with: pip install lice2."
        raise RuntimeError(msg) from None

    try:
        import jinja2_git  # noqa: F401, PLC0415
    except ImportError:
        msg = "jinja2-git is not installed. Install it with: pip install jinja2-git."
        raise RuntimeError(msg) from None


def _validate_copyright_holder() -> None:
    """Require a nonempty name for the license copyright notice."""
    if not COPYRIGHT_HOLDER.strip():
        msg = "copyright_holder must contain the name of a person or organization."
        raise ValueError(msg)


validators = (
    _validate_project_name,
    _validate_copyright_holder,
    _validate_deps,
)

for validator in validators:
    try:
        validator()
    except (ValueError, RuntimeError) as ex:
        print(ex)  # noqa: T201
        sys.exit(1)
