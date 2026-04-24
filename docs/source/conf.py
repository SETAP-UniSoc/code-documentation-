import os
import sys

BASE_DIR = r"C:\Users\stuti\OneDrive\SETAP\SETAP CW\TERM 2 CW\UNIsoc"

# Point to backend so Sphinx can import your project
#sys.path.insert(0, os.path.join(BASE_DIR, "backend"))
sys.path.insert(0, BASE_DIR)

# ---- Sphinx extensions (IMPORTANT) ----
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]

autosummary_generate = True

autodoc_mock_imports = [
    "django",
    "django.db",
    "django.utils",
    "django.core",
    "django.contrib",
    "rest_framework",
    "flask",
    "celery",
    "config.celery",
]