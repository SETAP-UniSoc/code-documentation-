My Events Page
==============
 
Overview
--------
 
The **My Events** page displays all events the authenticated user is currently attending.
It supports two modes: showing events from a single society (when launched from a society
page) or showing all attending events across every society the user is a member of.
 
The page is implemented as the ``MyEventsPage`` stateful widget, found at
``lib/pages/my_events_page.dart``.
 
---


Navigation
----------
 
**Route into this page — single society mode**
 
When navigated to from a society page, a ``societyId`` is passed to scope the list to
events from that society only.
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(
       builder: (_) => MyEventsPage(societyId: societyId),
     ),
   );
 
**Route into this page — all societies mode**
 
When navigated to from the bottom navigation bar or home screen, no ``societyId`` is
passed. The page fetches attending events across all societies.
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(
       builder: (_) => const MyEventsPage(),
     ),
   );
 
**Constructor properties**
 
.. list-table::
   :widths: 25 15 60
   :header-rows: 1
 
   * - Property
     - Type
     - Description
   * - ``societyId``
     - ``int?``
     - Optional. If provided, only events from this society are shown.
       If ``null``, attending events from all societies are fetched.
 
---


Widget Structure
----------------
 
``MyEventsPage`` is a ``StatefulWidget``. Its state class ``_MyEventsPageState`` manages
the following fields:
 
.. list-table::
   :widths: 30 15 55
   :header-rows: 1
 
   * - Field
     - Type
     - Description
   * - ``_myEvents``
     - ``List<Map<String, dynamic>>``
     - The list of events the user is attending. Populated by ``_loadMyAttendingEvents``.
   * - ``_isLoading``
     - ``bool``
     - ``true`` while the network requests are in progress.
   * - ``_errorMessage``
     - ``String?``
     - Holds an error string if any request fails. ``null`` on success.
   * - ``_isMounted``
     - ``bool``
     - Guards all ``setState`` calls after async gaps. Set to ``false`` in ``dispose``
       to prevent calling ``setState`` on an unmounted widget.
 
**Lifecycle**
 
- ``initState`` — calls ``_loadMyAttendingEvents`` immediately on widget creation.
- ``dispose`` — sets ``_isMounted = false`` before calling ``super.dispose()``.
 
---

Data Loading
------------
 
All data fetching is handled by the private method ``_loadMyAttendingEvents``. The method
branches on whether ``widget.societyId`` is set.
 
Single Society Mode
~~~~~~~~~~~~~~~~~~~
 
When ``societyId`` is provided:
 
1. Fetches all events for that society via ``GET /api/societies/<societyId>/events/``.
2. For each event, calls ``GET /api/events/<eventId>/attending/`` to check if
   ``is_attending`` is ``true``.
3. Builds ``_myEvents`` from only the events where the user is attending.