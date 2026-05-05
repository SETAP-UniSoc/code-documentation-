User Homepage
=============

Overview
--------

The **User Homepage API** provides core data required for the user dashboard.
It enables users to view recent events and search for societies.

This endpoint supports dynamic content rendering for the homepage, including
event previews and searchable society listings.

Endpoints
---------

.. code-block:: http

   GET /api/events/all/
   GET /api/search/?q=<query>

**Django Routes**

.. code-block:: python

   path('events/all/', AllEventsView.as_view(), name='all-events')
   path("search/", SocietyListSearchView.as_view(), name="society-search")

Authentication
--------------

- **Required**: Yes
- **Access Level**: Any authenticated user

Features
--------

- View the most recent events
- Search societies by name
- View society summaries (name, category, description, member count)

---

All Events Endpoint
------------------

Retrieves the most recently created events.

Request
~~~~~~~

.. code-block:: http

   GET /api/events/all/

Response
~~~~~~~~

.. code-block:: json

   [
     {
       "id": 1,
       "title": "Welcome Event",
       "date": "2026-05-10",
       "society": 3
     }
   ]

Behaviour
~~~~~~~~~

- Returns the **5 most recent events**
- Events are ordered by descending ID (latest first)
- Includes associated society data via ``select_related``

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class AllEventsView(APIView):

       permission_classes = [IsAuthenticated]

       def get(self, request):

           events = Event.objects.select_related("society").order_by('-id')[:5]
           serializer = EventSerializer(events, many=True)
           return Response(serializer.data)

---

Society Search Endpoint
----------------------

Retrieves a list of active societies, optionally filtered by a search query.

Request
~~~~~~~

.. code-block:: http

   GET /api/search/?q=music

Query Parameters
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Parameter
     - Type
     - Description
   * - q
     - string
     - Optional search term used to filter societies by name

Response
~~~~~~~~

.. code-block:: json

   [
     {
       "id": 1,
       "name": "Music Society",
       "category": "Cultural",
       "description": "A society for music lovers",
       "member_count": 120
     }
   ]

Response Fields Explained
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Unique identifier of the society
   * - ``name``
     - Name of the society
   * - ``category``
     - Society category (e.g. Academic, Cultural)
   * - ``description``
     - Brief description of the society
   * - ``member_count``
     - Number of active members in the society

Behaviour
~~~~~~~~~

- Returns only societies where ``is_active = True``
- If ``q`` is provided:
  - Filters societies using case-insensitive name matching
- Results are:
  - Annotated with active member count
  - Ordered alphabetically by name

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class SocietyListSearchView(APIView):

       permission_classes = [IsAuthenticated]

       def get(self, request):

           query = request.query_params.get("q", "").strip()

           societies = Society.objects.filter(is_active=True)

           if query:
               societies = societies.filter(name__icontains=query)

           societies = societies.annotate(
               active_member_count=Count(
                   'membership',
                   filter=Q(membership__left_at__isnull=True)
               )
           ).order_by('name')

           data = [{
               "id": s.id,
               "name": s.name,
               "category": s.category,
               "description": s.description,
               "member_count": s.active_member_count,
           } for s in societies]

           return Response(data)

---

Data Flow
---------

1. User opens homepage
2. Frontend requests latest events
3. Frontend sends search queries as user types
4. Backend filters and returns matching societies
5. Results displayed dynamically on UI

---

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - No events exist
     - Returns empty list
   * - No societies match search
     - Returns empty list
   * - Missing query parameter
     - Returns all active societies
   * - User not authenticated
     - Returns 401

---

Implementation Notes
-------------------

- ``select_related("society")`` improves query performance
- Membership count uses conditional aggregation
- Search is case-insensitive for better usability
- Results are lightweight for fast frontend rendering

---

Suggested Improvements
----------------------

- Add pagination for large society lists
- Implement debounce/throttling on frontend (already done in your UI)
- Add category-based filtering
- Include society images/logos in response
- Add trending or recommended societies
- Cache frequent search queries for performance