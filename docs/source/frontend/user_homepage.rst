User Homepage
=============

Overview
--------

The user homepage (``home_page.dart``) is the main screen for student users after login.
It provides a central hub for discovering societies, searching for content, viewing
featured societies, and browsing upcoming events from societies the user has joined.

The page is composed of two main widgets:

- ``HomePage`` — a stateless scaffold that hosts the page layout.
- ``HomeHeader`` — a stateful widget that handles all data fetching, state management, and UI rendering.

Components
----------

Search Bar
~~~~~~~~~~

A debounced ``TextField`` that queries the ``/search?q=`` endpoint as the user types.
Results appear in a dropdown below the search bar with a 300ms debounce to prevent
excessive API requests. A loading spinner is shown in the suffix of the search field
while results are being fetched.

- **Endpoint**: ``/api/search?q=<query>``
- **Debounce**: 300ms
- **Loading indicator**: Shown while request is in flight

Search Dropdown (``_buildSearchDropdown``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Displays search results beneath the search bar. Each result shows an icon and name.
Tapping a result navigates to ``UserSocietyPage`` for that society and clears the
dropdown.

.. code-block:: dart

   onTap: () {
     setState(() => _searchResults = []);
     Navigator.push(
       context,
       MaterialPageRoute(
         builder: (_) => UserSocietyPage(
           societyId: item['id'],
           societyName: item['name'] ?? '',
           description: item['description'] ?? '',
         ),
       ),
     );
   }

Featured Societies Carousel
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A horizontal ``PageView`` displaying the top 3 societies auto-advancing every 5 seconds.
Each card is a ``_SocietyLogoCard`` widget that navigates to ``UserSocietyPage`` when tapped.

- **Auto-advance interval**: 5 seconds
- **Societies shown**: Top 3 from the full society list
- **Navigation**: Tapping opens ``UserSocietyPage``

All Societies (A–Z) List
~~~~~~~~~~~~~~~~~~~~~~~~

A scrollable list of all societies inside a styled container. Supports:

- **Sort by**: A-Z, Z-A, Most Members, Least Members
- **Filter by**: All, Academic, Cultural, Sports, Religious, Extra-curricular

Tapping any society in the list navigates to ``UserSocietyPage``.

Upcoming Events Carousel
~~~~~~~~~~~~~~~~~~~~~~~~

A horizontal ``ListView`` showing upcoming events from societies the user has joined.
Each event card is wrapped in a ``GestureDetector`` — tapping navigates to the
``UserSocietyPage`` of the society that owns the event.

Event data is fetched via ``ApiService.getEventsForJoinedSocieties()``, which loops
through the user's joined societies and tags each event with ``society_id`` and
``society_name`` at fetch time so navigation is possible without a backend change.

.. code-block:: dart

   GestureDetector(
     onTap: () {
       if (societyId == null) return;
       Navigator.push(
         context,
         MaterialPageRoute(
           builder: (_) => UserSocietyPage(
             societyId: societyId,
             societyName: event['society_name'] ?? '',
             description: '',
           ),
         ),
       );
     },
     child: _EventCard(...),
   )

Data Flow
---------

On initialisation, ``_loadData()`` is called which fetches:

1. All societies via ``ApiService.getSocieties()`` → ``/api/societies/``
2. Upcoming events via ``ApiService.getEventsForJoinedSocieties()`` → loops ``/api/societies/<id>/events/`` per joined society

Both are fetched in parallel and stored in local state. A loading spinner is shown
until both calls complete.

State Variables
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Variable
     - Purpose
   * - ``_societies``
     - Full list of all societies
   * - ``_filteredSocieties``
     - Filtered/sorted subset used in the A-Z list
   * - ``_topSocieties``
     - Top 3 societies shown in the featured carousel
   * - ``_events``
     - Upcoming events from joined societies
   * - ``_searchResults``
     - Live search results shown in the dropdown
   * - ``_loading``
     - Controls loading spinner visibility
   * - ``_isSearching``
     - Controls search field loading indicator
   * - ``selectedCategory``
     - Currently selected filter category
   * - ``sortBy``
     - Currently selected sort option

Navigation
----------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Trigger
     - Destination
   * - Tap society in search dropdown
     - ``UserSocietyPage``
   * - Tap society in featured carousel
     - ``UserSocietyPage``
   * - Tap society in A-Z list
     - ``UserSocietyPage``
   * - Tap event card in upcoming events
     - ``UserSocietyPage`` (of owning society)

API Endpoints Used
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Endpoint
     - Purpose
   * - ``GET /api/societies/``
     - Fetch all societies for the A-Z list and featured carousel
   * - ``GET /api/search?q=<query>``
     - Live search for societies
   * - ``GET /api/my-societies/``
     - Fetch societies the user has joined
   * - ``GET /api/societies/<id>/events/``
     - Fetch events per joined society

Helper Widgets
--------------

``_SocietyLogoCard``
~~~~~~~~~~~~~~~~~~~~

A small card widget displaying a society icon and name. Used in the featured
societies carousel. Accepts an optional ``UserSocietyPage`` widget to navigate
to on tap.

``_EventCard``
~~~~~~~~~~~~~~

A styled card displaying event title, date, and location. Used inside the
upcoming events carousel. Navigation is handled by the parent ``GestureDetector``
in the ``itemBuilder``.