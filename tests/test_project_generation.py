# pyright: reportArgumentType=false, reportOptionalMemberAccess=false, reportOptionalOperand=false
"""
Run basic tests for generated projects.

Originally adapted from:
https://github.com/pydanny/cookiecutter-django/blob/master/tests
"""

import os
import re
import subprocess
import sys
import tarfile
import tomllib
import zipfile
from datetime import UTC, datetime
from email import message_from_bytes
from pathlib import Path
from typing import Any, Final

import pytest
from binaryornot.check import is_binary
from cookiecutter.exceptions import FailedHookException
from pytest_cookies.plugin import Cookies, Result


RE_OBJ: Final = re.compile(r"{{(\s?cookiecutter)[.](.*?)}}")


def _build_files_list(root_dir: Path) -> list[Path]:
    """List absolute paths to the generated files."""
    return [Path(dirpath) / file_path for dirpath, _subdirs, files in os.walk(str(root_dir)) for file_path in files]


def _load_pyproject(baked_project: Result) -> dict[str, Any]:
    return tomllib.loads((baked_project.project_path / "pyproject.toml").read_text())


def _assert_variables_replaced(paths: list[Path]) -> None:
    """Check that all generated files have their template variables replaced."""
    assert paths, "No files are generated"

    for path in paths:
        if is_binary(str(path)):
            continue

        file_contents = path.read_text()

        match = RE_OBJ.search(file_contents)
        msg = "cookiecutter variable not replaced in {0} at {1}"

        # Assert that no match is found:
        assert match is None, msg.format(path, match.start())


def _bake_project(cookies: Cookies, context: dict[str, str]) -> Result:
    """Generate a project and check that Cookiecutter succeeds."""
    baked_project = cookies.bake(extra_context=context)

    assert baked_project.exit_code == 0
    assert baked_project.exception is None
    assert baked_project.project_path is not None

    return baked_project


def test_with_default_configuration(
    cookies: Cookies,
    context: dict[str, str],
) -> None:
    """Check the project structure with default prompt values."""
    baked_project = _bake_project(cookies, context)
    project = _load_pyproject(baked_project)["project"]

    assert baked_project.project_path.name == context["project_name"]
    assert baked_project.project_path.is_dir()
    assert project["name"] == context["project_name"]
    assert project["description"] == context["project_description"]
    assert project["license"] == "MIT"
    assert "The MIT License (MIT)" in (baked_project.project_path / "LICENSE").read_text(encoding="utf-8")


@pytest.mark.parametrize("type_lib", ["standard", "django"])
def test_variables_replaced(cookies: Cookies, context: dict[str, str], type_lib: str) -> None:
    """Check that all template variables are replaced in project files."""
    baked_project = _bake_project(cookies, {**context, "type_lib": type_lib})
    paths = _build_files_list(baked_project.project_path)

    _assert_variables_replaced(paths)


def test_standard_library_configuration(
    cookies: Cookies,
    context: dict[str, str],
) -> None:
    """Check that standard libraries omit Django dependencies and settings."""
    baked_project = _bake_project(cookies, context)
    pyproject = _load_pyproject(baked_project)
    groups = pyproject["dependency-groups"]

    assert pyproject["project"]["dependencies"] == []
    assert "pytest-django" not in groups["test"]
    assert "django-stubs[compatible-mypy]" not in groups["typing"]
    assert not (baked_project.project_path / "tests" / "settings.py").exists()


def test_django_library_configuration(cookies: Cookies, context: dict[str, str]) -> None:
    """Check the dependencies, settings, and files of a Django library."""
    baked_project = _bake_project(cookies, {**context, "type_lib": "django"})
    pyproject = _load_pyproject(baked_project)
    groups = pyproject["dependency-groups"]
    tool = pyproject["tool"]
    pytest_options = tool["pytest"]["ini_options"]
    settings_path = baked_project.project_path / "tests" / "settings.py"

    assert any(dependency.startswith("django>=") for dependency in pyproject["project"]["dependencies"])
    assert "pytest-django" in groups["test"]
    assert "django-stubs[compatible-mypy]" in groups["typing"]
    assert tool["mypy"]["plugins"] == ["mypy_django_plugin.main"]
    assert tool["django-stubs"]["django_settings_module"] == "tests.settings"
    assert pytest_options["DJANGO_SETTINGS_MODULE"] == "tests.settings"
    assert settings_path.is_file()
    assert (settings_path.parent / "__init__.py").is_file()


@pytest.mark.parametrize(
    ("license_name", "expected_text"),
    [
        ("MIT", "Permission is hereby granted, free of charge"),
        ("BSD-3-Clause", "Redistribution and use in source and binary forms"),
        ("Apache-2.0", "Apache License"),
    ],
)
def test_license_generation(
    cookies: Cookies,
    context: dict[str, str],
    license_name: str,
    expected_text: str,
) -> None:
    """Check the selected license, copyright notice, and project metadata."""
    holder = 'Example """Équipe""" O\'Reilly \\ Organization'
    started_year = str(datetime.now(UTC).year)
    baked = _bake_project(
        cookies,
        {**context, "license": license_name, "copyright_holder": holder},
    )
    project_path = baked.project_path
    license_text = (project_path / "LICENSE").read_text(encoding="utf-8")
    project = _load_pyproject(baked)["project"]

    assert expected_text in license_text
    assert holder in license_text
    assert any(year in license_text for year in (started_year, str(datetime.now(UTC).year)))
    assert "{{" not in license_text
    assert project["license"] == license_name
    assert project["license-files"] == ["LICENSE"]


@pytest.mark.parametrize("holder", ["", "   "])
def test_empty_copyright_holder(
    cookies: Cookies,
    context: dict[str, str],
    holder: str,
    capfd: pytest.CaptureFixture[str],
) -> None:
    """Reject an empty copyright holder rather than generate an incomplete notice."""
    baked = cookies.bake(extra_context={**context, "copyright_holder": holder})

    assert isinstance(baked.exception, FailedHookException)
    assert baked.exit_code == -1
    assert "copyright_holder must contain the name of a person or organization" in capfd.readouterr().out


@pytest.mark.parametrize(
    ("prompt", "entered_value"),
    [
        ("project_name", "myProject"),
        ("project_name", "43project"),
        ("project_name", "_test"),
        ("project_name", "-test"),
        ("project_name", "test-"),
        ("project_name", "1_test"),
        ("project_name", "test@"),
        ("project_name", "0123456"),
    ],
)
def test_validators_work(
    prompt: str,
    entered_value: str,
    cookies: Cookies,
    context: dict[str, str],
) -> None:
    """Check that invalid project names prevent generation."""
    context.update({prompt: entered_value})
    baked_project = cookies.bake(extra_context=context)

    assert isinstance(baked_project.exception, FailedHookException)
    assert baked_project.exit_code == -1
