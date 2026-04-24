import os
import sys

# Add project root (VERY IMPORTANT)
sys.path.insert(0, os.path.abspath('..'))

# --- Django setup (preferred over mocking) ---
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.config.settings')
django.setup()

# -- Project information --
project = 'UNIsoc'
author = 'Your Team'
release = '0.1'
version = '0.1.0'

# -- General configuration --
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',    
    'sphinx.ext.viewcode',     
    'sphinx.ext.duration',
]

autosummary_generate = True

# Better autodoc output
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

# Templates
templates_path = ['_templates']

# Theme
html_theme = 'sphinx_rtd_theme'