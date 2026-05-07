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



State Variables
---------------
 
.. list-table::
   :header-rows: 1
   :widths: 30 25 45
 
   * - Variable
     - Type
     - Description
   * - ``calendarEvents``
     - ``List<Event>``
     - List of ``Event`` objects consumed by the ``EventBasedCalender`` widget. Each entry represents one calendar day marker.
   * - ``eventData``
     - ``List``
     - Raw event data returned from the API, enriched with a ``normalized_date`` field for local timezone-aware date comparison.
   * - ``isLoading``
     - ``bool``
     - Controls the full-page ``CircularProgressIndicator`` shown while events are being fetched.
 
---



Lifecycle
---------
 
``initState``
~~~~~~~~~~~~~
 
Calls ``loadEvents()`` immediately after the widget is inserted into the tree:
 
.. code-block:: dart
 
   @override
   void initState() {
     super.initState();
     loadEvents();
   }
 
---
 
Helper Method
-------------
 
``getDateOnly(DateTime dt)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Strips the time component from a ``DateTime`` and returns a date-only ``DateTime`` in local timezone. Used internally during event processing.
 
.. code-block:: dart
 
   DateTime getDateOnly(DateTime dt) {
     final local = dt.toLocal();
     return DateTime(local.year, local.month, local.day);
   }
 
---
 



 
API Methods
-----------
 
``loadEvents()``
~~~~~~~~~~~~~~~~
 
**Endpoint:** ``GET /api/societies/<societyId>/events/``
 
Fetches all events for the admin's society and prepares them for calendar display.
 
**Processing pipeline:**
 
1. Fetches raw event list from the API.
2. Converts each event's ``start_time`` from UTC to the device's local timezone.
3. Strips the time component to produce a ``normalized_date`` (date-only ``DateTime``).
4. Groups events by their ``normalized_date`` key (``"YYYY-M-D"``).
5. Maps each date group to a calendar ``Event`` object:
 
   - ``eventName``: ``"N events"`` where N is the count for that day.
   - ``color``: ``Colors.red`` if more than one event falls on the date, ``Color(0xFF8B5CF6)`` (purple) for a single event.
 
6. Updates ``eventData`` and ``calendarEvents`` state.
 
**On failure (non-200):** Sets ``isLoading = false`` with no error message displayed (the calendar simply renders empty).
 
---
 
``_createEvent(...)``
~~~~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``POST /api/societies/<societyId>/events/``
 
**Parameters:**
 
.. list-table::
   :header-rows: 1
   :widths: 25 15 60
 
   * - Parameter
     - Type
     - Description
   * - ``title``
     - ``String``
     - Event title (required).
   * - ``description``
     - ``String``
     - Event description (required).
   * - ``location``
     - ``String``
     - Event location (required).
   * - ``startTime``
     - ``String``
     - ISO 8601 UTC datetime string for the event start.
   * - ``endTime``
     - ``String``
     - ISO 8601 UTC datetime string for the event end.
   * - ``capacity``
     - ``int?``
     - Optional capacity limit. Only included in the request body if non-null and greater than 0.
 
**Request body example:**
 
.. code-block:: json
 
   {
     "title": "Football Tryouts",
     "description": "Open tryouts for new members",
     "location": "Sports Hall",
     "start_time": "2026-05-10T09:00:00Z",
     "end_time": "2026-05-10T11:00:00Z",
     "capacity_limit": 30
   }
 
**Time handling:** The user picks start and end times via ``showTimePicker``. These are combined with the tapped calendar date into local ``DateTime`` objects, then converted to UTC before being serialised to ISO 8601.
 
**On success (201):** Calls ``loadEvents()`` to refresh the calendar and shows a success ``SnackBar``.
 
**On failure:** Shows a ``SnackBar`` with the HTTP status code.
 
---
 
``_updateEvent(int id, Map data)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``PUT /api/events/<id>/update/``
 
**Request body:** A map containing ``title``, ``description``, ``location``, ``start_time``, and ``end_time``. The original ``start_time`` and ``end_time`` are preserved from the existing event — only the text fields are edited.
 
**On success (200):** Calls ``loadEvents()`` and shows a success ``SnackBar``.
 
---
 
``_deleteEvent(int id)``
~~~~~~~~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``DELETE /api/events/<id>/delete/``
 
**On success (204):** Calls ``loadEvents()`` and shows a success ``SnackBar``.
 
.. warning::
   Deletion is immediate and irreversible. There is no confirmation dialog before the ``DELETE`` request is sent — the delete button in ``_showEvents`` triggers deletion directly.
 
---

 

 
User Interaction Flow
---------------------
 
Date Tap Routing — ``onDateTapped(DateTime date)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
The calendar's ``onDateTap`` callback always calls ``onDateTapped``. The method compares the tapped date against all ``normalized_date`` values in ``eventData``:
 
.. code-block:: text
 
   User taps a calendar date
   │
   ├── Events exist on that date?
   │   ├── YES → _showEvents(eventsOnDate)
   │   └── NO  → _showCreateDialog(date)
 
---


Events Dialog — ``_showEvents(List events)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Displayed when the tapped date has one or more events. Shows an ``AlertDialog`` with a scrollable ``ListView`` of ``ListTile`` widgets, one per event.
 
Each ``ListTile`` shows:
 
- **Title:** Event title.
- **Subtitle:** ``HH:MM • location • Cap: N`` (or ``No Cap`` if unlimited).
- **Trailing:** A red delete ``IconButton`` that calls ``_deleteEvent(id)`` after closing the dialog.
- **onTap:** Closes the dialog and opens ``_showEditDialog`` for that event.
 
Dialog actions:
 
- **Close** — Dismisses the dialog.
- **Add Another** — Closes the dialog and opens ``_showCreateDialog`` pre-populated with the date of the first listed event.
 
---
 
Create Dialog — ``_showCreateDialog(DateTime date)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
An ``AlertDialog`` wrapped in a ``StatefulBuilder`` so the time picker selections update the dialog UI without rebuilding the whole page.
 
Fields:
 
.. list-table::
   :header-rows: 1
   :widths: 30 70
 
   * - Field
     - Description
   * - Title
     - Free-text ``TextField``.
   * - Description
     - Free-text ``TextField``.
   * - Location
     - Free-text ``TextField``.
   * - Capacity (optional)
     - Numeric ``TextField``. Left empty for unlimited capacity.
   * - Start Time
     - ``ListTile`` that opens ``showTimePicker``. Defaults to 09:00.
   * - End Time
     - ``ListTile`` that opens ``showTimePicker``. Defaults to 10:00.
 
Dialog actions:
 
- **Cancel** — Dismisses without saving.
- **Create** — Converts picked times to UTC, calls ``_createEvent()``, then closes the dialog.
 
---
 
Edit Dialog — ``_showEditDialog(Map event)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
A simpler ``AlertDialog`` pre-filled with the event's existing ``title``, ``description``, and ``location``.
 
.. note::
   The edit dialog does **not** allow changing ``start_time`` or ``end_time``. The original timestamps are passed through unchanged to ``_updateEvent()``.
 
Dialog actions:
 
- **Cancel** — Dismisses without saving.
- **Save** — Calls ``_updateEvent()`` with the updated fields, then closes.
 
---
 

