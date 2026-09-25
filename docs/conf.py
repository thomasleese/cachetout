"""Sphinx configuration for the cachetout documentation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

project = "cachetout"
copyright = "Thomas Leese"
author = "Thomas Leese <thomas@leese.io>"

release = "0.2.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

autodoc_member_order = "bysource"

html_theme = "alabaster"

htmlhelp_basename = "cachetoutdoc"
