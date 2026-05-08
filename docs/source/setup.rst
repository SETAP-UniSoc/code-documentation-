Setup Instructions
==================

This project consists of a Flutter frontend and a Django REST backend.

Requirements
------------

Frontend:
- Flutter SDK (>= 3.x)
- Dart SDK (>= 3.9.0)

Backend:
- Python (>= 3.10)
- PostgreSQL
- Redis

Tools:
- Git

Installation
------------

.. code-block:: bash

   git clone https://github.com/Unisoc
   cd Unisoc

-----------------------------------
Backend Setup (Django REST Framework)
-----------------------------------

1. Create virtual environment

.. code-block:: bash

   python -m venv venv

Windows:

.. code-block:: bash

   venv\Scripts\activate

Mac/Linux:

.. code-block:: bash

   source venv/bin/activate


2. Install dependencies

.. code-block:: bash

   pip install django
   pip install djangorestframework
   pip install djangorestframework-authtoken
   pip install psycopg2-binary
   pip install django-cors-headers
   pip install celery
   pip install redis
   pip install django-filter
   pip install python-dotenv

Or install all requirements:

.. code-block:: bash

   pip install -r requirements.txt


3. Configure PostgreSQL database

Create a PostgreSQL database:

- Database name: unisoc_db
- User: unisoc_user
- Password: strongpassword

Update ``settings.py``:

.. code-block:: python

   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'unisoc_db',
           'USER': 'unisoc_user',
           'PASSWORD': 'strongpassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }


4. Configure Django apps

Add to ``INSTALLED_APPS``:

.. code-block:: python

   INSTALLED_APPS = [
       ...
       'rest_framework',
       'rest_framework.authtoken',
       'corsheaders',
       'authentication',
   ]


5. Configure CORS for Flutter frontend

Add middleware in ``settings.py``:

.. code-block:: python

   MIDDLEWARE = [
       'corsheaders.middleware.CorsMiddleware',
       ...
   ]

Allow frontend requests:

.. code-block:: python

   CORS_ALLOW_ALL_ORIGINS = True

For production, replace with specific origins.


6. Configure REST Framework authentication

.. code-block:: python

   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }


7. Configure Redis and Celery

Install and run Redis locally.

Redis default:

.. code-block:: text

   redis://127.0.0.1:6379/0

Create ``backend/celery.py``:

.. code-block:: python

   import os
   from celery import Celery

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

   app = Celery('backend')

   app.config_from_object('django.conf:settings', namespace='CELERY')

   app.autodiscover_tasks()


Update ``backend/__init__.py``:

.. code-block:: python

   from .celery import app as celery_app

   __all__ = ('celery_app',)

Add Celery config in ``settings.py``:

.. code-block:: python

   CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'


8. Configure email backend

Example Gmail SMTP configuration:

.. code-block:: python

   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your_email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your_app_password'


9. Apply migrations

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate


10. Create superuser

.. code-block:: bash

   python manage.py createsuperuser


11. Run Django development server

.. code-block:: bash

   python manage.py runserver 0.0.0.0:8000


12. Start Celery worker

Open another terminal:

.. code-block:: bash

   celery -A backend worker --loglevel=info


13. Start Redis server

Windows (Redis installed):

.. code-block:: bash

   redis-server

Mac/Linux:

.. code-block:: bash

   redis-server

Frontend Setup
--------------

.. code-block:: bash

   cd frontend
   flutter pub get
   flutter run

Notes
-----

- Ensure PostgreSQL and Redis are running
- Update environment variables before deployment