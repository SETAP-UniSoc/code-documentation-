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

1. Create virtual environment:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Configure PostgreSQL database:

Update your database settings in ``settings.py``:

- Database name: unisoc_db
- User: unisoc_user
- Password: strongpassword

4. Apply migrations:

.. code-block:: bash

   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver

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