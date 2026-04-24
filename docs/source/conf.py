import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# Mock all Django/DRF dependencies so Sphinx can import your code
from unittest.mock import MagicMock

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = [
    'django', 'django.db', 'django.db.models', 'django.utils',
    'django.utils.timezone', 'django.core', 'django.core.mail',
    'rest_framework', 'rest_framework.views', 'rest_framework.response',
    'rest_framework.permissions', 'rest_framework.exceptions',
    'rest_framework.generics', 'rest_framework', 'flask',
    'authentication', 'authentication.models',
]
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

autosummary_generate = True

# -- Project information
project = 'UNIsoc'
copyright = '2024'
author = 'Your Team'
release = '0.1'
version = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.duration',
]

templates_path = ['_templates']
html_theme = 'sphinx_rtd_theme'