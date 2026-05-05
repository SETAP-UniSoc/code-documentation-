Admin Analytics
===============

Overview
--------

The **Admin Analytics API** provides analytical insights for society administrators.
It aggregates membership trends, event engagement, and overall activity into a
single endpoint for dashboard visualisation.

This endpoint is designed to support admin dashboards with time-series data and
summary statistics.

Endpoint
--------

.. code-block:: http

   GET /api/my-analytics/

**Django Route**

.. code-block:: python

   path("my-analytics/", AnalyticsView.as_view(), name="analytics")

Authentication
--------------

- **Required**: Yes
- **Access Level**: Admin users only

Authorization Rules
~~~~~~~~~~~~~~~~~~~

- User must have ``role = "admin"``
- User must be associated with a society

Error Responses
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status Code
     - Description
   * - 403
     - User is not an admin
   * - 404
     - No society found for admin

Query Parameters
----------------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Parameter
     - Type
     - Default
     - Description
   * - period
     - string
     - week
     - Time range for analytics aggregation

Allowed Values
~~~~~~~~~~~~~~

- ``week`` → Last 7 days (daily breakdown)
- ``month`` → Last 30 days (daily breakdown)
- ``6months`` → Last 6 months (weekly breakdown)
- ``year`` → Last 12 months (monthly breakdown)

Example Request
~~~~~~~~~~~~~~~

.. code-block:: http

   GET /api/my-analytics/?period=month

Response Structure
------------------

.. code-block:: json

   {
     "labels": ["Mon", "Tue", "Wed"],
     "totals": [10, 15, 18],
     "live_count": 120,
     "total_events": 25,
     "events_stats": [
       { "title": "Welcome Event", "attendee_count": 50 }
     ],
     "most_popular": {
       "title": "Welcome Event",
       "attendee_count": 50
     },
     "event_attendance": [
       { "title": "Welcome Event", "attendee_count": 50 }
     ]
   }

Response Fields Explained
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``labels``
     - Time intervals (e.g. days, weeks, months)
   * - ``totals``
     - Membership count at each interval
   * - ``live_count``
     - Current active members
   * - ``total_events``
     - Total number of events created
   * - ``events_stats``
     - Attendance count per event
   * - ``most_popular``
     - Event with highest attendance (or null)
   * - ``event_attendance``
     - Duplicate of ``events_stats`` (for frontend compatibility)

Data Flow & Logic
-----------------

Membership Growth
~~~~~~~~~~~~~~~~~

Membership totals are calculated using:

- ``joined_at <= current_date``
- ``left_at IS NULL OR left_at > current_date``

This ensures historical accuracy and correct handling of users who have left.

Time Bucketing Strategy
~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Period
     - Interval
     - Data Points
     - Label Format
   * - week
     - Daily
     - 7
     - Mon, Tue
   * - month
     - Daily
     - 30
     - 01 Jan
   * - 6months
     - Weekly
     - 26
     - Week 12
   * - year
     - Monthly
     - 12
     - Jan

Event Analytics
~~~~~~~~~~~~~~~

.. code-block:: python

   Count("eventattendance", filter=Q(eventattendance__left_at__isnull=True))

Only active attendees are counted.

Most Popular Event
~~~~~~~~~~~~~~~~~~

- Determined by highest attendee count
- Returns a single event
- Returns ``null`` if no events exist

Implementation Notes
--------------------

Duplicate Query
~~~~~~~~~~~~~~~

.. code-block:: python

   society = Society.objects.get(admin=request.user)

This appears twice and should be reused to avoid unnecessary database calls.

Redundant Field
~~~~~~~~~~~~~~~

.. code-block:: json

   "event_attendance": list(events_stats)

Duplicates ``events_stats`` and may be removed unless required by the frontend.

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~

- Membership calculation runs one query per time interval
- Event annotations are executed multiple times
- Consider optimisation using aggregation or caching

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - No society exists
     - Returns 404
   * - No events
     - ``most_popular = null``
   * - No members
     - ``totals`` contains zeros
   * - Invalid period
     - Returns 400

Use Cases
---------

- Admin dashboard visualisation
- Membership growth tracking
- Event engagement analysis
- Identifying popular events

Suggested Improvements
----------------------

- Remove duplicate fields
- Optimise database queries
- Add optional date range filters
- Implement caching (e.g. Redis)
- Include event IDs in responses