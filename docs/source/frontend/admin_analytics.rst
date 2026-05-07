Admin Analytics Page
====================
 
Overview
--------
 
The **Admin Analytics Page** (``AdminAnalyticsPage``) is a Flutter ``StatefulWidget`` that gives society admins a real-time dashboard of their society's membership and event attendance data. It is accessible via the **Analytics** tab (index 1) of the ``AdminBottomNav`` navigation bar.
 
Admins can:
 
- View a membership trend line chart across selectable time periods (1W, 1M, 6M, 1Y)
- See the current live member count updated in real time every 50 seconds
- View per-event attendance as a horizontal bar chart
- Export the full analytics report as a PDF
 
The page lives at ``lib/screens/admin/admin_analytics_page.dart`` and communicates with the Django REST API via the ``ApiService`` class.
 
.. note::
   ``AdminAnalyticsPage`` is admin-only. The backend ``AnalyticsView`` returns ``403 Admins only`` for non-admin users. The ``Authorization: Token <token>`` header is automatically included via ``ApiService.headers``.
 
---



Widget Structure
----------------
 
.. code-block:: text
 
   AdminAnalyticsPage (StatefulWidget)
   └── _AdminAnalyticsPageState (State)
       ├── fetchAnalytics(period)     → GET /my-analytics/?period=<period>
       ├── startLiveUpdates()         → Timer.periodic every 50 seconds
       ├── exportPdf()                → Generates and prints PDF via Printing package
       ├── _buildChart(data)          → LineChart widget (fl_chart)
       ├── _buildEventList(data, names) → Horizontal bar chart (custom ListView)
       └── _buildPeriodButton(value, label) → Period selector tab button
 
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
   * - ``httpClient``
     - ``http.Client?``
     - No
     - Optional injectable HTTP client. Defaults to ``http.Client()`` if not provided. Used for unit testing.
 
---



State Variables
---------------
 
.. list-table::
   :header-rows: 1
   :widths: 30 20 50
 
   * - Variable
     - Type
     - Description
   * - ``selectedPeriod``
     - ``String``
     - The currently active time period. Defaults to ``"year"``. Accepted values: ``"week"``, ``"month"``, ``"6months"``, ``"year"``.
   * - ``labels``
     - ``List<String>``
     - X-axis labels for the membership trend chart (e.g. ``["Jan", "Feb", ...]``).
   * - ``values``
     - ``List<double>``
     - Y-axis data points for the membership trend chart. The last value is overwritten with ``liveCount`` after each fetch.
   * - ``eventValues``
     - ``List<double>``
     - Attendee counts per event, used for the horizontal bar chart.
   * - ``eventNames``
     - ``List<String>``
     - Event title labels corresponding to each value in ``eventValues``.
   * - ``liveCount``
     - ``int``
     - The current active member count. Used as the headline figure and overwrites the last data point in ``values``.
   * - ``isLoading``
     - ``bool``
     - Controls the ``CircularProgressIndicator`` shown inside both chart areas during fetches.
   * - ``liveTimer``
     - ``Timer?``
     - Periodic timer that triggers ``fetchAnalytics`` every 50 seconds. Cancelled in ``dispose()``.
 
---
 
 
Lifecycle
---------
 
``initState``
~~~~~~~~~~~~~
 
Defers the initial data fetch to after the first frame using ``WidgetsBinding.instance.addPostFrameCallback``, then starts the live update timer:
 
.. code-block:: dart
 
   @override
   void initState() {
     super.initState();
     WidgetsBinding.instance.addPostFrameCallback((_) {
       fetchAnalytics(selectedPeriod);
     });
     startLiveUpdates();
   }
 
.. note::
   The post-frame callback is used to ensure the widget tree is fully built before the first API call triggers a ``setState``, avoiding the "setState called during build" assertion error.
 
``dispose``
~~~~~~~~~~~
 
Cancels the live update timer to prevent memory leaks and dangling callbacks:
 
.. code-block:: dart
 
   @override
   void dispose() {
     liveTimer?.cancel();
     super.dispose();
   }
 
---
 
Methods
-------
 
``startLiveUpdates()``
~~~~~~~~~~~~~~~~~~~~~~
 
Creates a ``Timer.periodic`` that calls ``fetchAnalytics(selectedPeriod)`` every 50 seconds. This keeps the live member count and chart data current without requiring manual refresh.
 
.. code-block:: dart
 
   void startLiveUpdates() {
     liveTimer = Timer.periodic(const Duration(seconds: 50), (_) {
       fetchAnalytics(selectedPeriod);
     });
   }
 
.. warning::
   The timer uses the value of ``selectedPeriod`` at the time each tick fires, not the value at the time the timer was created. This means switching period tabs will be reflected in subsequent live updates automatically.
 
---
 
``fetchAnalytics(String period)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``GET /api/my-analytics/?period=<period>``
 
Fetches membership trend data and event attendance statistics for the given period.
 
**Query parameter values:**
 
.. list-table::
   :header-rows: 1
   :widths: 20 20 60
 
   * - Value
     - Label
     - Backend behaviour
   * - ``"week"``
     - 1W
     - Returns 7 daily data points labelled by day abbreviation (Mon, Tue…).
   * - ``"month"``
     - 1M
     - Returns 30 daily data points labelled by date and month (e.g. 01 May).
   * - ``"6months"``
     - 6M
     - Returns 26 weekly data points labelled by week number.
   * - ``"year"``
     - 1Y
     - Returns 12 monthly data points labelled by month abbreviation (Jan, Feb…).
 
**Response structure:**
 
.. code-block:: json
 
   {
     "labels": ["Jan", "Feb", "Mar", "..."],
     "totals": [10, 12, 15, "..."],
     "live_count": 18,
     "events_stats": [
       { "title": "Tryouts", "attendee_count": 12 },
       { "title": "AGM", "attendee_count": 5 }
     ],
     "most_popular": { "title": "Tryouts", "attendee_count": 12 },
     "total_events": 4
   }
 
**Post-fetch state updates:**
 
1. ``labels`` ← ``data["labels"]``
2. ``values`` ← ``data["totals"]`` (cast to ``List<double>``)
3. ``liveCount`` ← ``data["live_count"]``
4. ``eventValues`` ← attendee counts from ``data["events_stats"]``
5. ``eventNames`` ← titles from ``data["events_stats"]``
6. ``values[values.length - 1]`` ← overwritten with ``liveCount`` to ensure the most recent point reflects real-time membership.
 
**On error:** Catches and prints the exception. No error state is shown in the UI — the chart areas simply retain their previous data or remain empty.
 
---
 
``exportPdf()``
~~~~~~~~~~~~~~~
 
Generates an in-memory PDF document using the ``pdf`` package and sends it to the device's print/share dialog via the ``printing`` package.
 
**PDF content:**
 
- Title: ``"Society Analytics"``
- Live member count
- Membership trend table (label → value for each data point)
- Event attendance table (event name → attendee count)
 
**On success:** The system print dialog opens.
 
**On failure:** A ``SnackBar`` is shown with the error message.
 
.. note::
   ``exportPdf`` does not require a network call — it uses the data already held in state from the last ``fetchAnalytics`` call.
 
---
 
 
UI Sections
-----------
 
Period Selector
~~~~~~~~~~~~~~~
 
A horizontal row of four ``_buildPeriodButton`` widgets at the top of the page:
 
.. list-table::
   :header-rows: 1
   :widths: 15 15 70
 
   * - Label
     - Value
     - Behaviour on tap
   * - 1W
     - ``"week"``
     - Sets ``selectedPeriod = "week"`` and calls ``fetchAnalytics("week")``.
   * - 1M
     - ``"month"``
     - Sets ``selectedPeriod = "month"`` and calls ``fetchAnalytics("month")``.
   * - 6M
     - ``"6months"``
     - Sets ``selectedPeriod = "6months"`` and calls ``fetchAnalytics("6months")``.
   * - 1Y
     - ``"year"``
     - Sets ``selectedPeriod = "year"`` and calls ``fetchAnalytics("year")``.
 
The active button is shown in purple with a 2px underline indicator. Inactive buttons are grey with no indicator.
 
---
 