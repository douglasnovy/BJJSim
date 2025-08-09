from __future__ import annotations

import os
import sys
from typing import Final

# Add project source to path when API docs are added later
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project: Final[str] = "BJJSim"
author: Final[str] = "BJJSim Contributors"
copyright = "2025, BJJSim"

# -- General configuration ---------------------------------------------------

extensions: list[str] = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    # "sphinx.ext.linkcheck",  # optional; disabled to avoid env issues
    "sphinx.ext.doctest",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_static_path: list[str] = ["_static"]

# -- MyST configuration ------------------------------------------------------

myst_heading_anchors = 3
myst_enable_extensions = [
    "deflist",
    "dollarmath",
    "fieldlist",
    "tasklist",
    "colon_fence",
    "attrs_block",
]

# -- Autodoc / type hints ----------------------------------------------------

autodoc_typehints = "description"
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "inherited-members": True,
    "show-inheritance": True,
}
autosummary_generate = True

# -- Intersphinx -------------------------------------------------------------

# Explicitly annotate the mapping so static type checking passes under strict mypy.
# The empty dictionaries are intentionally created with explicit type parameters
# to satisfy invariance of dict types in mypy.
intersphinx_mapping: dict[str, tuple[str, dict[str, str]]] = {
    "python": ("https://docs.python.org/3", dict[str, str]()),
    "numpy": ("https://numpy.org/doc/stable/", dict[str, str]()),
}

# -- Todo --------------------------------------------------------------------

todo_include_todos = True
