User MySoc Page
======================
 
Overview
--------
 
The **MySoc** page displays all societies the authenticated user is currently an active
member of. It is one of the main navigation destinations for regular (non-admin) users and acts
as the entry point to individual society pages.
 
The page is implemented as the ``MySocietyPage`` stateful widget, found at
``lib/screens/user_mysoc_page.dart``.
 
---



Navigation
----------
 
**Route into this page**
 
``MySoc`` is typically reached from the main bottom navigation bar or home screen.
No arguments are required to construct it.
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(builder: (_) => const MySocietyPage()),
   );


   
   **Route out of this page**
 
Tapping a society card pushes ``UserSocietyPage``, passing three named arguments:
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(
       builder: (_) => UserSocietyPage(
         societyId: id,
         societyName: name,
         description: description,
       ),
     ),
   );
 

.. list-table::
   :widths: 25 15 60
   :header-rows: 1
 
   * - Argument
     - Type
     - Description
   * - ``societyId``
     - ``int``
     - The unique ID of the selected society.
   * - ``societyName``
     - ``String``
     - Display name passed directly to avoid a second network call.
   * - ``description``
     - ``String``
     - Society description passed directly to avoid a second network call.
 
----

Widget Structure
----------------
 
``MySocietyPage`` is a ``StatefulWidget``. Its state class ``_MySocietyPageState`` holds a
single piece of state:
 
.. list-table::
   :widths: 30 70
   :header-rows: 1
 
   * - Field
     - Description
   * - ``_futureMySocieties``
     - A ``Future<List>`` initialised in ``initState`` by calling ``ApiService.getMySocieties``
       (or the injected ``mySocietiesFetcher`` override). Consumed by ``FutureBuilder``.
 
**Constructor properties**
 
.. list-table::
   :widths: 30 15 55
   :header-rows: 1
 
   * - Property
     - Type
     - Description
   * - ``mySocietiesFetcher``
     - ``Future<List> Function()?``
     - Optional. Overrides the default fetch function. Intended for widget testing — pass a
       mock function to return fixture data without hitting the network.
 
---


UI States
---------
 
The page uses a ``FutureBuilder`` to handle three possible states:
 
Loading
~~~~~~~
 
Displayed while the network request is in flight.
 
::
 
   ┌──────────────────────────────────┐
   │          My Societies            │  ← AppBar
   ├──────────────────────────────────┤
   │                                  │
   │        [CircularProgressIndicator]│
   │                                  │
   └──────────────────────────────────┘
 
Error
~~~~~
 
Displayed if the ``Future`` throws an exception (e.g. network failure or non-200 response).
The error message from the exception is shown centred on screen.
 
::
 
   ┌──────────────────────────────────┐
   │          My Societies            │
   ├──────────────────────────────────┤
   │                                  │
   │   Error: Failed to load my       │
   │   societies: 401 Unauthorized    │
   │                                  │
   └──────────────────────────────────┘
 
Empty state
~~~~~~~~~~~
 
Displayed when the request succeeds but the user has not joined any societies.
 
::
 
   ┌──────────────────────────────────┐
   │          My Societies            │
   ├──────────────────────────────────┤
   │                                  │
   │  You have not joined any         │
   │  societies yet.                  │
   │                                  │
   └──────────────────────────────────┘
 
Populated list
~~~~~~~~~~~~~~
 
Displayed when the user has one or more active memberships. Societies are rendered in a
vertically scrolling ``ListView`` with 12 px spacing between cards.
 
::
 
   ┌──────────────────────────────────┐
   │          My Societies            │
   ├──────────────────────────────────┤
   │  ●  Photography Society          │
   │     A community for enthusiasts  │
   │     42 members              >    │
   ├ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┤
   │  ●  Chess Club                   │
   │     Weekly sessions              │
   │     15 members              >    │
   └──────────────────────────────────┘
 
---



Society Card
------------
 
Each list item is a ``ListTile`` with the following layout:
 
.. list-table::
   :widths: 20 80
   :header-rows: 1
 
   * - Slot
     - Content
   * - ``leading``
     - ``CircleAvatar`` with background colour ``Color(0xFF4A235A)`` and a white ``Icons.group`` icon.
   * - ``title``
     - Society name. Font weight ``FontWeight.w600``.
   * - ``subtitle``
     - Two lines: the society description on line one, and the member count on line two
       (e.g. ``42 members`` or ``1 member`` — singular/plural handled automatically).
   * - ``isThreeLine``
     - ``true``, to accommodate the two-line subtitle.
   * - ``onTap``
     - Pushes ``UserSocietyPage`` with the society's ``id``, ``name``, and ``description``.
 
**Member count label logic**
 
.. code-block:: dart
 
   '$memberCount member${memberCount == 1 ? '' : 's'}'
 
---