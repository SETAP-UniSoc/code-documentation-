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
 

Headline Member Count
~~~~~~~~~~~~~~~~~~~~~
 
Displays the last value in ``values`` (which is always ``liveCount`` after a fetch) as a large bold number above the chart. Falls back to ``liveCount.toString()`` if ``values`` is empty.
 
---
 
Membership Trend Chart — ``_buildChart(List<double> data)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Rendered using ``LineChart`` from the ``fl_chart`` package.
 
**Chart properties:**
 
- **Curve:** Smooth (``isCurved: true``)
- **Bar width:** 3px
- **Dots:** Hidden (``FlDotData(show: false)``)
- **Gradient:** Purple → deep purple line
- **Fill area:** Purple with opacity fade from 0.4 to 0.05
- **Y-axis max:** ``maxValue * 1.2`` to provide breathing room
- **Grid:** Hidden
- **Border:** Hidden
 
**Empty state:** Shows ``"No data yet"`` centred in the chart area.
 
**Loading state:** Shows a ``CircularProgressIndicator`` in place of the chart.
 
---
 
Event Attendance Chart — ``_buildEventList(List<double> data, List<String> names)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
A custom horizontal bar chart built with a ``ListView.builder`` scrolling horizontally. Each item is a ``Column`` containing:
 
1. Attendee count label (purple, bold)
2. A purple ``Container`` bar whose height is proportional to the event's attendee count relative to the maximum value across all events. Clamped between 10px and 150px.
3. Event name label (truncated to 2 lines)
 
**Bar height formula:**
 
.. code-block:: text
 
   barHeight = (attendeeCount / maxValue) * 150
   barHeight = barHeight.clamp(10.0, 150.0)
 
**Empty state:** Shows a grey bar chart icon, ``"No event attendance data yet"``, and a hint explaining that data appears when users attend events.
 
**Loading state:** Shows a ``CircularProgressIndicator``.
 
---



Export Button
~~~~~~~~~~~~~
 
A ``TextButton`` labelled ``"Export as PDF"`` that calls ``exportPdf()``. Positioned between the live member count and the event attendance chart.
 
---
 
Build Method
------------
 
.. code-block:: text
 
   Scaffold
   ├── AppBar: "My Analytics" (no back button)
   ├── body: SingleChildScrollView
   │   ├── Period selector row (1W / 1M / 6M / 1Y)
   │   ├── Headline member count text
   │   ├── Membership trend LineChart (height: 250)
   │   ├── "Live Members: N" label
   │   ├── "Export as PDF" TextButton
   │   ├── "Event Attendance" heading
   │   └── Event attendance bar chart (height: 300)
   └── bottomNavigationBar: AdminBottomNav(currentIndex: 1)
 
---




API Endpoints Summary
---------------------
 
.. list-table::
   :header-rows: 1
   :widths: 10 45 45
 
   * - Method
     - Endpoint
     - Purpose
   * - ``GET``
     - ``/api/my-analytics/?period=<period>``
     - Fetch membership trend data, live count, and event attendance stats.
 
---
 
Error Handling Summary
-----------------------
 
.. list-table::
   :header-rows: 1
   :widths: 35 65
 
   * - Scenario
     - Handling
   * - Analytics fetch returns non-200
     - State is not updated; previous chart data is retained. No error shown.
   * - Network exception during fetch
     - Caught and printed. UI retains previous state silently.
   * - PDF export fails
     - ``SnackBar`` shown with the exception message.
   * - Non-admin user accesses the page
     - Backend returns 403. Fetch silently fails (no error shown in UI).
   * - ``values`` is empty on render
     - Headline falls back to ``liveCount.toString()``; chart shows ``"No data yet"``.
   * - ``eventValues`` / ``eventNames`` empty on render
     - Event attendance section shows empty state with icon and hint text.
 
---
 

Live Update Behaviour
---------------------
 
.. list-table::
   :header-rows: 1
   :widths: 30 70
 
   * - Behaviour
     - Detail
   * - Update interval
     - Every 50 seconds via ``Timer.periodic``.
   * - What updates
     - Full re-fetch of ``fetchAnalytics(selectedPeriod)`` — all chart data, live count, and event stats are refreshed.
   * - Timer lifecycle
     - Started in ``initState``, cancelled in ``dispose``. Safe against memory leaks.
   * - Period awareness
     - The timer always uses the current value of ``selectedPeriod``, so switching tabs is reflected in the next tick.
 
---
 