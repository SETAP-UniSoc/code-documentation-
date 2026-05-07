Admin Events Page
=================
 
Overview
--------
 
The **Admin Events Page** (``admin_events_page.dart``) is a Flutter ``StatefulWidget`` that gives society admins a full calendar-based interface for managing their society's events. It is accessible via the **Events** tab (index 2) of the ``AdminBottomNav`` navigation bar.
 
Admins can:
 
- View all society events plotted on an interactive monthly calendar
- Tap any date to see events scheduled on that day
- Create new events by tapping an empty date
- Edit existing event details (title, description, location)
- Delete events directly from the event list dialog
 
The page lives at ``lib/screens/admin/admin_events_page.dart`` and communicates with the Django REST API via the ``ApiService`` class.
 
.. note::
   ``admin_events_page.dart`` requires ``societyId`` as a mandatory constructor argument. This is always sourced from ``ApiService.societyId`` when navigated to via ``AdminBottomNav``.
 
---


Widget Structure
----------------
 
.. code-block:: text
 
   AdminEventsPage (StatefulWidget)
   └── _AdminEventsPageState (State)
       ├── loadEvents()              → GET /societies/<id>/events/
       ├── onDateTapped()            → Routes to _showEvents or _showCreateDialog
       ├── _showEvents()             → AlertDialog listing events on a date
       ├── _showCreateDialog()       → AlertDialog with event creation form
       ├── _showEditDialog()         → AlertDialog with event edit form
       ├── _createEvent()            → POST /societies/<id>/events/
       ├── _updateEvent()            → PUT /events/<id>/update/
       └── _deleteEvent()            → DELETE /events/<id>/delete/
 
---




 
Constructor Parameters
-----------------------
 
.. list-table::
   :header-rows: 1
   :widths: 25 15 15 45
 
   * - Parameter
     - Type
     - Required
     - Description
   * - ``societyId``
     - ``int``
     - Yes
     - The ID of the admin's society. Used in all API endpoint paths.
   * - ``httpClient``
     - ``http.Client?``
     - No
     - Optional injectable HTTP client. Defaults to ``http.Client()`` if not provided. Used for unit testing.
 
---
 