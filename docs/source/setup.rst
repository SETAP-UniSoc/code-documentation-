Setup Instructions
==================

This project consists of a Flutter frontend and a Django REST backend.

Requirements
------------

Make sure you have the following installed:

Frontend:
- Flutter SDK (>= 3.x)
- Dart SDK (>= 3.9.0)

Backend:
- Python (>= 3.10)
- PostgreSQL
- Redis (for Celery background tasks)

Tools:
- Git

Installation
------------

Clone the repository:

.. code-block:: bash

   git clone https://github.com/Unisoc
   cd Unisoc

-----------------------------------
Backend Setup (Django REST Framework)
-----------------------------------

1. Create virtual environment:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

2. Install dependencies:

.. code-block:: bash

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

5. Create superuser:

.. code-block:: bash

   python manage.py createsuperuser

6. Run backend server:

.. code-block:: bash

   python manage.py runserver

Backend runs at:
http://127.0.0.1:8000/

-----------------------------------
Frontend Setup (Flutter)
-----------------------------------

1. Navigate to Flutter project:

.. code-block:: bash

   cd frontend   # adjust if different

2. Install dependencies:

.. code-block:: bash

   flutter pub get

3. Run the app:

.. code-block:: bash

   flutter run

-----------------------------------
Celery & Redis (Background Tasks)
-----------------------------------

Start Redis server:

.. code-block:: bash

   redis-server

Start Celery worker:

.. code-block:: bash

   celery -A config worker --loglevel=info

-----------------------------------
Environment Variables (Important)
-----------------------------------

Update email configuration in ``settings.py``:

- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD

⚠️ Do not expose real credentials in production.

-----------------------------------
Notes
-----------------------------------

- Ensure PostgreSQL is running before starting Django
- Ensure Redis is running before starting Celery
- Flutter app communicates with backend via API endpoints