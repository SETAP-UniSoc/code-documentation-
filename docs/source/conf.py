import os
import sys
from unittest.mock import MagicMock

BASE_DIR = r"C:\Users\stuti\OneDrive\SETAP\SETAP CW\TERM 2 CW\UNIsoc"
sys.path.insert(0, BASE_DIR)

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = [
    'django', 'django.db', 'django.db.models', 'django.utils',
    'django.utils.timezone', 'django.core', 'django.core.mail',
    'django.contrib', 'django.contrib.auth', 'django.contrib.auth.models',
    'django.contrib.auth.base_user', 'django.core.validators', 'django.conf',
    'rest_framework', 'rest_framework.views', 'rest_framework.response',
    'rest_framework.permissions', 'rest_framework.exceptions',
    'rest_framework.generics', 'flask',
    'celery', 'config.celery'
]

sys.modules.update((mod, Mock()) for mod in MOCK_MODULES)