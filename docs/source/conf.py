import os
import sys

# -- Path setup --------------------------------------------------------------

# Add project root to Python path (so Sphinx can find modules if needed)
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'UniSoc Documentation'
author = 'UniSoc Team'
release = '1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

# Disable autosummary auto-generation to avoid import crashes
autosummary_generate = False

# -- HTML output -------------------------------------------------------------

html_theme = 'alabaster'  # simple and safe (works on ReadTheDocs)

# If you want nicer UI later, you can switch to:
# html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']