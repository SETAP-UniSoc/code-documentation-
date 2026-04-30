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

   git clone https://github.com/your-repo
   cd your-repo

Backend Setup
-------------

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
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