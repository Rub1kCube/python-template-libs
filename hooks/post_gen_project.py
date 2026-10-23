import json
from datetime import UTC, datetime
from pathlib import Path

from lice2.api import Lice


LIBRARY_TYPE = "{{ cookiecutter.type_lib }}"
LICENSE_TEMPLATES = {
    "MIT": "mit",
    "BSD-3-Clause": "bsd3",
    "Apache-2.0": "apache",
}
LICENSE = "{{ cookiecutter.license }}"
COPYRIGHT_HOLDER: str = json.loads(r""" {{ cookiecutter.copyright_holder | tojson }} """)
PROJECT_NAME: str = json.loads(r""" {{ cookiecutter.project_name | tojson }} """)


def _generate_license() -> None:
    """Write the selected license using lice2's bundled templates."""
    generator = Lice(
        organization=COPYRIGHT_HOLDER.strip(),
        project=PROJECT_NAME,
        year=datetime.now(UTC).year,
    )
    license_text = generator.get_license(LICENSE_TEMPLATES[LICENSE])
    Path("LICENSE").write_text(license_text.rstrip() + "\n", encoding="utf-8")


_generate_license()

if LIBRARY_TYPE == "standard":
    Path("tests/settings.py").unlink()
