# /// script
# dependencies = [
#   "requests",
#   "Jinja2",
# ]
# ///

"""
Generator script for flet-material-symbols icon data.

Fetches the latest Material Symbols icon definitions from
https://github.com/timmaffett/material_symbols_icons and generates:

- src/flet_material_symbols/symbols.json  - icon name → packed integer map
- src/flet_material_symbols/symbols.pyi   - Python type stubs for IDE support
- src/flutter/flet_material_symbols/lib/src/symbols_icons.dart - Dart icon list

Usage (from the flet-material-symbols package directory):

    uv run scripts/generate_icons.py

or:

    pip install requests Jinja2
    python scripts/generate_icons.py
"""

import json
import re
from pathlib import Path

import requests
from jinja2 import Environment, FileSystemLoader

# Icon set ID 3 is used for Material Symbols in the flet icon encoding scheme.
# Lower 16 bits = sorted index, upper byte = set ID.
# IDs 1 (Material Icons) and 2 (CupertinoIcons) are reserved by flet core.
SET_ID = 3

SYMBOLS_DART_URL = "https://raw.githubusercontent.com/timmaffett/material_symbols_icons/master/lib/symbols.dart"

ICON_VAR_PATTERN = re.compile(
    r"""^\s*static const IconData\s+(\w+)\s*=""", re.MULTILINE
)

PACKAGE_ROOT = Path(__file__).parent.parent

SYMBOLS_JSON_OUT = PACKAGE_ROOT / "src/flet_material_symbols/symbols.json"
SYMBOLS_PYI_OUT = PACKAGE_ROOT / "src/flet_material_symbols/symbols.pyi"
SYMBOLS_DART_OUT = (
    PACKAGE_ROOT
    / "src/flutter/flet_material_symbols/lib/src/symbols_icons.dart"
)

PYI_TEMPLATE = """\
\"\"\"
Flet Material Symbols Icons Stub

To generate/update this file run from the flet-material-symbols directory:

    uv run scripts/generate_icons.py
\"\"\"

from flet.controls.icon_data import IconData

__all__ = ["Symbols"]

class Symbols:
{% for name, code in icons %}    {{ name.upper() }}: IconData
{% endfor %}\
"""

DART_TEMPLATE = """\
import 'package:material_symbols_icons/symbols.dart';

List<IconData> symbolsIcons = [
{% for name, code in icons %}  Symbols.{{ name }},
{% endfor %}];
"""


def fetch_dart_file(url: str) -> str:
    print(f"Fetching {url} ...")
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_icon_names(dart_content: str) -> list[str]:
    names = sorted(set(ICON_VAR_PATTERN.findall(dart_content)))
    print(f"Found {len(names)} unique icon names.")
    return names


def make_icons(names: list[str]) -> list[tuple[str, int]]:
    return [(name, (SET_ID << 16) | i) for i, name in enumerate(names)]


def write_json(icons: list[tuple[str, int]]) -> None:
    payload = {name.upper(): value for name, value in icons}
    SYMBOLS_JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    SYMBOLS_JSON_OUT.write_text(
        json.dumps(payload, separators=(",", ":")), encoding="utf-8"
    )
    print(f"Written: {SYMBOLS_JSON_OUT.relative_to(PACKAGE_ROOT)}")


def write_pyi(icons: list[tuple[str, int]]) -> None:
    env = Environment(keep_trailing_newline=True)
    tmpl = env.from_string(PYI_TEMPLATE)
    SYMBOLS_PYI_OUT.parent.mkdir(parents=True, exist_ok=True)
    SYMBOLS_PYI_OUT.write_text(tmpl.render(icons=icons), encoding="utf-8")
    print(f"Written: {SYMBOLS_PYI_OUT.relative_to(PACKAGE_ROOT)}")


def write_dart(icons: list[tuple[str, int]]) -> None:
    env = Environment(keep_trailing_newline=True)
    tmpl = env.from_string(DART_TEMPLATE)
    SYMBOLS_DART_OUT.parent.mkdir(parents=True, exist_ok=True)
    SYMBOLS_DART_OUT.write_text(tmpl.render(icons=icons), encoding="utf-8")
    print(f"Written: {SYMBOLS_DART_OUT.relative_to(PACKAGE_ROOT)}")


def main() -> None:
    dart_content = fetch_dart_file(SYMBOLS_DART_URL)
    names = parse_icon_names(dart_content)
    icons = make_icons(names)

    write_json(icons)
    write_pyi(icons)
    write_dart(icons)

    print("Done.")


if __name__ == "__main__":
    main()
