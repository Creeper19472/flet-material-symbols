# flet-material-symbols

A Flet extension that provides [Material Symbols](https://fonts.google.com/icons) icons for use in Flet apps.

Material Symbols is Google's latest icon library, offering outlined, rounded, and sharp variants for over 3,000 icons. The icons support variable font axes: fill, weight, grade, and optical size.

## Usage

```python
import flet as ft
from flet_material_symbols import Symbols

def main(page: ft.Page):
    page.add(
        ft.Icon(Symbols.HOME),
        ft.Icon(Symbols.HOME_ROUNDED),
        ft.Icon(Symbols.HOME_SHARP),
    )

ft.run(main)
```

## Icon variants

Each icon is available in three styles:

- **Outlined** (default): `Symbols.ICON_NAME`
- **Rounded**: `Symbols.ICON_NAME_ROUNDED`
- **Sharp**: `Symbols.ICON_NAME_SHARP`

## Variable font axes

Icons can be customized with variable font axes using the standard `ft.Icon` properties:

```python
ft.Icon(
    Symbols.SETTINGS,
    fill=1,        # 0.0 = outlined, 1.0 = fully filled (continuous 0–1)
    weight=700,    # 100–700
    grade=0.25,    # -50–200
    optical_size=48,  # 20–48
)
```

## Updating icon data

To regenerate the icon data after a `material_symbols_icons` package update, run from the `flet-material-symbols` directory:

```
uv run scripts/generate_icons.py
```
