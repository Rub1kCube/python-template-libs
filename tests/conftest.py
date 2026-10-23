from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def _isolate_license_settings(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep lice2 settings independent of the developer's configuration."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))


@pytest.fixture
def context() -> dict[str, str]:
    """Provide the default test context."""
    return {
        "project_name": "test-project",
        "project_description": "Custom description",
        "min_version_python": "3.12",
    }
