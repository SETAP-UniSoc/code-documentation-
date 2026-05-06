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


All Societies Mode
~~~~~~~~~~~~~~~~~~
 
When ``societyId`` is ``null``:
 
1. Fetches all societies via ``GET /api/societies/``.
2. For each society, fetches its events via ``GET /api/societies/<societyId>/events/``.
3. For each event, calls ``GET /api/events/<eventId>/attending/`` to check attendance.
4. Collects all attending events and **sorts them ascending by ``start_time``**.
 
.. note::
   All Societies mode makes multiple sequential HTTP requests (one per society, then one
   per event). For users in many societies with many events this may be slow. A loading
   indicator is shown for the full duration.
 
**Event map structure stored in ``_myEvents``**
 
.. list-table::
   :widths: 25 15 60
   :header-rows: 1
 
   * - Key
     - Type
     - Present in
   * - ``id``
     - ``int``
     - Both modes
   * - ``title``
     - ``String``
     - Both modes
   * - ``description``
     - ``String``
     - Both modes
   * - ``location``
     - ``String``
     - Both modes
   * - ``start_time``
     - ``String`` (ISO 8601)
     - Both modes
   * - ``end_time``
     - ``String`` (ISO 8601)
     - Both modes
   * - ``capacity_limit``
     - ``int?``
     - Both modes
   * - ``society_id``
     - ``int``
     - All societies mode only
   * - ``society_name``
     - ``String``
     - All societies mode only
 
**Null-safe fallbacks applied on load**
 
.. code-block:: dart
 
   "title":       event["title"]       ?? "Untitled Event",
   "description": event["description"] ?? "No description",
   "location":    event["location"]    ?? "No location",
 
---


UI States
---------
 
Loading
~~~~~~~
 
Shown while ``_isLoading`` is ``true``.
 
::
 
   ┌──────────────────────────────────┐
   │           My Events              │  ← AppBar
   ├──────────────────────────────────┤
   │                                  │
   │     [CircularProgressIndicator]  │
   │                                  │
   └──────────────────────────────────┘
 
Error
~~~~~
 
Shown when ``_errorMessage`` is not ``null``. Includes a **Try Again** button that
re-calls ``_loadMyAttendingEvents``.
 
::
 
   ┌──────────────────────────────────┐
   │           My Events              │
   ├──────────────────────────────────┤
   │                                  │
   │    [!]  <error message>          │
   │                                  │
   │         [ Try Again ]            │
   │                                  │
   └──────────────────────────────────┘
 
- Error icon: ``Icons.error_outline``, size 64, colour ``Colors.grey``.
- Try Again button background: ``Color(0xFF8B5CF6)`` (purple).
 
Empty State
~~~~~~~~~~~
 
Shown when the request succeeds but the user is not attending any events.
 
::
 
   ┌──────────────────────────────────┐
   │           My Events              │
   ├──────────────────────────────────┤
   │                                  │
   │  [calendar_busy icon]            │
   │                                  │
   │  You're not attending any        │
   │  events yet                      │
   │                                  │
   │  Go to a society page and        │
   │  tap 'Attend Event'              │
   │                                  │
   └──────────────────────────────────┘
 
- Empty icon: ``Icons.event_busy``, size 64, colour ``Colors.grey``.


Populated List
~~~~~~~~~~~~~~
 
Shown when ``_myEvents`` is non-empty. Events are rendered in a ``ListView.builder``
with 16 px padding and 20 px bottom margin between cards.
 
::
 
   ┌──────────────────────────────────┐
   │           My Events              │
   ├──────────────────────────────────┤
   │  ┌────────────────────────────┐  │
   │  │ [Society Header]           │  │  ← Only in all-societies mode
   │  │  📁 Photography Society    │  │
   │  │     1 Jun 2025 at 14:00    │  │
   │  ├────────────────────────────┤  │
   │  │  Macro Workshop            │  │
   │  │  📅  1 Jun 2025 at 14:00   │  │
   │  │  📍  Room 2B               │  │
   │  │                            │  │
   │  │  Learn macro techniques... │  │
   │  │                            │  │
   │  │  👥  Capacity: 30          │  │
   │  │                            │  │
   │  │  [ Leave Event ]           │  │
   │  └────────────────────────────┘  │
   └──────────────────────────────────┘
 
---

Event Card
----------
 
Each card is a ``Container`` with a white background, rounded corners (``16 px``),
a subtle box shadow, and a ``Colors.grey.shade200`` border.



Society Header (all-societies mode only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Rendered when the event map contains the key ``society_name``. Appears at the top of
the card with a light purple background (``Color(0xFF8B5CF6)`` at 10% opacity).
 
.. list-table::
   :widths: 25 75
   :header-rows: 1
 
   * - Element
     - Detail
   * - Society icon
     - ``Icons.business`` in a purple-to-blue gradient ``Container`` (40 × 40 px,
       border radius 10 px).
   * - Society name
     - ``FontWeight.w600``, size 16, colour ``Color(0xFF1F2937)``.
   * - Date line
     - Formatted start time, size 12, colour ``Colors.grey.shade600``.
   * - Past badge
     - Shown when ``start_time`` is before ``DateTime.now()``. Grey pill labelled
       ``"Past"``.