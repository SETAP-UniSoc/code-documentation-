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

   git clone https://github.com/SETAP-UniSoc/UNIsoc.git
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
   python manage.py runserver 0.0.0.0:8000

Frontend Setup
--------------

1. Navigate to the Flutter project directory:

.. code-block:: bash

   cd Unisoc

2. Get dependencies:

.. code-block:: bash

   flutter pub get
   
3. Run the application:

.. code-block:: bash

   flutter run -d emulator-5554


Frontend Dependencies Installed:
- http: ^1.2.2 (API calls)
- fl_chart: ^1.1.1 (Analytics charts)
- pdf: ^3.10.7 (PDF generation)
- printing: ^5.12.0 (PDF printing)
- carousel_slider: 5.1.1 (Carousel sliders)
- permission_handler: ^11.0.0 (Storage permissions)
- cupertino_icons: ^1.0.8 (iOS icons)
- flutter_calenders: ^0.0.7 (Calendar widget)


Notes
-----

- Ensure PostgreSQL and Redis are running
- Update environment variables before deployment
- In order to run the application on a virtual machine, an Android emulator has been used,
 or to you can run the application on a application of you choice through the command line by using the command ``flutter run -d <device_id>``.
You can find the device id by running ``flutter devices`` in the terminal.
