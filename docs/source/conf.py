import os
import sys

BASE_DIR = r"C:\Users\stuti\OneDrive\SETAP\SETAP CW\TERM 2 CW\UNIsoc"
sys.path.insert(0, BASE_DIR)

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