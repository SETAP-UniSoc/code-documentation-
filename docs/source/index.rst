UniSoc Documentation
===================

UniSoc is a full-stack university society management system designed to improve
student engagement and simplify the management of societies and events.

The system enables students to discover societies, join events, and receive
notifications, while providing administrators with tools to manage societies,
track attendance, and analyse engagement.

Project Architecture
--------------------

The system is composed of:

- A Flutter frontend (mobile/web interface)
- A Django REST API backend
- A PostgreSQL database
- Redis and Celery for background processing

Contents
========

.. toctree::
   :maxdepth: 2
   :caption: Documentation

   scope
   requirements
   implementation
   setup


Backend
=======

.. toctree::
   :maxdepth: 1
   :caption: Backend Pages

   backend/Admin_Analyticspage
   backend/Admin_Eventspage
   backend/Event_Detailspage
   backend/User_Homepage
   backend/User_Login
   backend/User_MyEventspage
   backend/User_MySocietypage
   backend/User_Registration
   backend/User_Settingspage


API
===

.. toctree::
   :maxdepth: 1

   api