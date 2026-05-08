Admin Homepage
==============

Overview
--------

The **Admin Homepage** serves as the main dashboard for authenticated administrators.
It provides a comprehensive interface for browsing societies, viewing upcoming events,
and managing society-related content. The page includes a searchable society list,
category filtering, sorting options, and a carousel displaying top societies.

This page is the default landing screen after an administrator successfully logs into
the application.

Features
--------

- Display top societies in an auto-scrolling carousel
- Browse all societies with category filtering
- Sort societies by name or member count
- Search for societies via debounced search bar
- View upcoming events from all societies
- Navigate to individual society profile pages
- View admin's own society name in the welcome header

Widget Structure
----------------

.. code-block:: dart

   AdminHomepage (StatefulWidget)
   ├── _buildHeader()
   ├── _buildSearchBar()
   ├── _buildSearchDropdown()
   ├── _buildTopSocietiesCarousel()
   ├── _buildBrowseSocietiesSection()
   └── _buildEventsSection()

State Variables
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Variable
     - Type
     - Description
   * - ``societies``
     - List
     - Complete list of all societies
   * - ``filteredSocieties``
     - List
     - Societies after filtering and sorting
   * - ``events``
     - List
     - Upcoming events from all societies
   * - ``searchResults``
     - List
     - Results from search bar
   * - ``selectedCategory``
     - String
     - Currently selected filter category
   * - ``sortBy``
     - String
     - Current sorting method (A-Z, Z-A, Most Members, Least Members)
   * - ``showingCategories``
     - bool
     - Toggle between category grid and society list view
   * - ``isLoading``
     - bool
     - Controls loading indicator visibility

Initialisation
--------------

The page loads data immediately after the first frame is rendered:

.. code-block:: dart

   @override
   void initState() {
     super.initState();
     WidgetsBinding.instance.addPostFrameCallback((_) {
       loadData();
     });
   }

   Future<void> loadData() async {
     await loadSocieties();
     await loadEvents();
     setState(() => isLoading = false);
   }

This ensures:
- Society data is fetched from the backend
- Event data is fetched from the backend
- Loading state is cleared once both requests complete

Top Societies Carousel
----------------------

Displays the five societies with the highest member counts in an auto-scrolling
carousel.

**Features:**
- Auto-scrolls every 4 seconds
- Manual navigation via arrow buttons
- Each card shows society name, category, and member count
- Tapping a card navigates to the society profile page

**Implementation:**

.. code-block:: dart

   Widget _buildTopSocietiesCarousel() {
     final topSocieties = [...societies]
       ..sort((a, b) => (b["member_count"] ?? 0).compareTo(a["member_count"] ?? 0));
     final top5 = topSocieties.take(5).toList();

     return CarouselSlider(
       options: CarouselOptions(
         height: 180,
         autoPlay: true,
         autoPlayInterval: const Duration(seconds: 4),
       ),
       items: top5.map((society) => ...).toList(),
     );
   }

Browse Societies Section
------------------------

Provides two view modes for exploring societies:

**1. Category Grid View (Default)**

Displays societies grouped by category (Academic, Cultural, Sports, Religious,
Extra-curricular). Tapping a category applies filtering and switches to list view.

**2. List View with Filtering and Sorting**

When a category is selected or a filter/sort option is applied, the grid is
replaced with a scrollable list of matching societies.

**Filter Options:**
- All (default)
- Academic
- Cultural
- Sports
- Religious
- Extra-curricular

**Sort Options:**
- A-Z (alphabetical ascending)
- Z-A (alphabetical descending)
- Most Members (highest member count first)
- Least Members (lowest member count first)

**Implementation:**

.. code-block:: dart

   void applyFilters() {
     List result = [...societies];

     if (selectedCategory != "All") {
       result = result.where((s) => s["category"] == selectedCategory).toList();
     }

     if (sortBy == "A-Z") {
       result.sort((a, b) => a["name"].compareTo(b["name"]));
     } else if (sortBy == "Z-A") {
       result.sort((a, b) => b["name"].compareTo(a["name"]));
     } else if (sortBy == "Most Members") {
       result.sort((a, b) => (b["member_count"] ?? 0).compareTo(a["member_count"] ?? 0));
     } else if (sortBy == "Least Members") {
       result.sort((a, b) => (a["member_count"] ?? 0).compareTo(b["member_count"] ?? 0));
     }

     setState(() {
       filteredSocieties = result;
       showingCategories = false;
     });
   }

Search Bar
----------

Provides real-time society search with debounced requests to prevent excessive
API calls.

**Features:**
- 300ms debounce delay
- Loading indicator while searching
- Results displayed in dropdown below search field
- Tapping a result navigates to the society profile page

**Implementation:**

.. code-block:: dart

   onChanged: (query) {
     if (debounce?.isActive ?? false) debounce!.cancel();

     debounce = Timer(const Duration(milliseconds: 300), () async {
       if (query.isEmpty) {
         setState(() => searchResults = []);
         return;
       }

       setState(() => isSearching = true);

       final response = await client.get(
         Uri.parse("${ApiService.baseUrl}/societies/?q=$query"),
         headers: ApiService.headers,
       );

       if (response.statusCode == 200) {
         setState(() {
           searchResults = json.decode(response.body);
           isSearching = false;
         });
       }
     });
   }

Upcoming Events Section
-----------------------

Displays a horizontal carousel of upcoming events from all societies.

**Features:**
- Auto-scrolls every 4 seconds
- Manual navigation via arrow buttons
- Each card shows event title, date, location, and capacity (if set)
- Tapping an event navigates to the society profile page

**Data Requirements:**
- Events must include: ``title``, ``start_time``, ``location``, ``society_id``
- Capacity displayed only if ``capacity_limit`` is present

Navigation
----------

Tapping any society card (carousel, list view, or search result) navigates to the
society profile page with the correct admin context:

.. code-block:: dart

   void navigateToSociety(int societyId, String societyName) {
     final bool isOwnSociety = ApiService.societyId != null && societyId == ApiService.societyId;

     Navigator.push(
       context,
       MaterialPageRoute(
         builder: (_) => SocietyProfilePage(
           societyId: societyId,
           isAdmin: true,
           isOwnSociety: isOwnSociety,
         ),
       ),
     );
   }

**Behaviour:**
- ``isAdmin`` is always ``true`` (user is admin)
- ``isOwnSociety`` is ``true`` only if the society belongs to the logged-in admin

This ensures:
- Admin sees edit controls on their own society profile
- Admin sees read-only view for other societies

Error Handling
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - API request fails
     - Error printed to console, loading state cleared
   * - No societies exist
     - "No societies yet" message displayed
   * - No events exist
     - "No upcoming events" message displayed
   * - No search results
     - Dropdown remains empty

Data Flow
---------

1. Page loads → ``loadData()`` fetches societies and events
2. User applies filter → ``applyFilters()`` updates displayed list
3. User sorts → ``applyFilters()`` resorts the list
4. User searches → Debounced request to ``/societies/?q=``
5. User taps society → Navigates to ``SocietyProfilePage``

Dependencies
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Package
     - Purpose
   * - ``carousel_slider``
     - Auto-scrolling carousel for top societies and events
   * - ``http``
     - API requests to backend
   * - ``ApiService``
     - Centralised API communication

Implementation Notes
--------------------

- The ``httpClient`` parameter allows dependency injection for testing
- Debounced search reduces unnecessary API calls during typing
- Null-safe checks prevent crashes when data fields are missing
- Member count sorting uses null coalescing (``?? 0``) to handle missing values
- Category colours use a predefined map for consistent UI styling
- The page uses ``SafeArea`` to avoid system UI overlaps