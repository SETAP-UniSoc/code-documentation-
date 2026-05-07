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
 

 