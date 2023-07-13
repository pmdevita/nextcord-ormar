# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import pathlib
import sys
from tomlkit import parse
from datetime import datetime
project_root = pathlib.Path(__file__).parents[2]
sys.path.insert(0, project_root.resolve().as_posix())

with open(project_root / "pyproject.toml") as f:
    pyproject = parse(f.read())

project = 'Nextcord-Ormar'
copyright = f"{datetime.now().year}, Peter DeVita"
author = 'Peter DeVita'
release = pyproject["tool"]["poetry"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'releases',
    'sphinxarg.ext'
]

templates_path = ['_templates']
exclude_patterns = []

releases_github_path = "pmdevita/nextcord-ormar"
releases_unstable_prehistory = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
