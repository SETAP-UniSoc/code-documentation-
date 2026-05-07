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
   │    [CircularProgressIndicator]   │
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



AppBar
------
 
.. list-table::
   :widths: 25 75
   :header-rows: 1
 
   * - Property
     - Value
   * - ``title``
     - ``'My Societies'`` in white (``Colors.white``).
   * - ``backgroundColor``
     - ``Color(0xFF4A235A)`` — the app's primary brand purple.
 
---


 
Data Fetching
-------------
 
The page calls a single endpoint on load.
 
.. list-table::
   :widths: 20 80
   :header-rows: 0
 
   * - **Method**
     - ``GET``
   * - **URL**
     - ``/api/my-societies/``
   * - **Auth**
     - Token header — set automatically via ``ApiService.headers``.
 
The service method used is ``ApiService.getMySocieties``:
 
.. code-block:: dart
 
   static Future<List> getMySocieties() async {
     final response = await http.get(
       Uri.parse("$baseUrl/my-societies/"),
       headers: headers,
     );
 
     if (response.statusCode == 200) {
       return jsonDecode(response.body) as List;
     }
 
     throw Exception(
       "Failed to load my societies: ${response.statusCode} ${response.body}",
     );
   }
 
**Expected response shape**
 
Each item in the returned list is a ``Map<String, dynamic>`` with these keys used by the UI:
 
.. list-table::
   :widths: 20 15 65
   :header-rows: 1
 
   * - Key
     - Dart type
     - Used for
   * - ``id``
     - ``int``
     - Passed to ``UserSocietyPage`` as ``societyId``.
   * - ``name``
     - ``String``
     - Card title and passed to ``UserSocietyPage`` as ``societyName``.
   * - ``description``
     - ``String``
     - Card subtitle line 1 and passed to ``UserSocietyPage`` as ``description``.
   * - ``member_count``
     - ``int``
     - Card subtitle line 2 (member count label).
 
Values are accessed with null-safe fallbacks:
 
.. code-block:: dart
 
   final id          = soc['id']           as int?    ?? 0;
   final name        = soc['name']         as String? ?? '';
   final description = soc['description']  as String? ?? '';
   final memberCount = soc['member_count'] as int?    ?? 0;
 
---




Testing
-------
 
``MySocietyPage`` accepts an optional ``mySocietiesFetcher`` parameter so the network call
can be replaced in widget tests without mocking ``http``.
 
**Example: empty state test**
 
.. code-block:: dart
 
   testWidgets('shows empty state when no societies', (tester) async {
     await tester.pumpWidget(
       MaterialApp(
         home: MySocietyPage(
           mySocietiesFetcher: () async => [],
         ),
       ),
     );
     await tester.pumpAndSettle();
     expect(find.text('You have not joined any societies yet.'), findsOneWidget);
   });
 
**Example: populated list test**
 
.. code-block:: dart
 
   testWidgets('renders a card for each society', (tester) async {
     await tester.pumpWidget(
       MaterialApp(
         home: MySocietyPage(
           mySocietiesFetcher: () async => [
             {'id': 1, 'name': 'Chess Club', 'description': 'Weekly chess.', 'member_count': 10},
             {'id': 2, 'name': 'Film Soc',   'description': 'Movie nights.',  'member_count': 5},
           ],
         ),
       ),
     );
     await tester.pumpAndSettle();
     expect(find.text('Chess Club'), findsOneWidget);
     expect(find.text('Film Soc'),   findsOneWidget);
   });
 
**Example: error state test**
 
.. code-block:: dart
 
   testWidgets('shows error message on failure', (tester) async {
     await tester.pumpWidget(
       MaterialApp(
         home: MySocietyPage(
           mySocietiesFetcher: () async => throw Exception('Network error'),
         ),
       ),
     );
     await tester.pumpAndSettle();
     expect(find.textContaining('Error:'), findsOneWidget);
   });
 
---



Page Flow
---------
 
::
 
   [Bottom Nav / Home]
         │
         ▼
   MySocietyPage
         │
         │  GET /api/my-societies/
         │
         ├── Loading  →  CircularProgressIndicator
         ├── Error    →  Error message (centred)
         ├── Empty    →  "You have not joined any societies yet."
         │
         └── [tap card]
                  │
                  ▼
           UserSocietyPage
           (societyId, societyName, description)
 
---