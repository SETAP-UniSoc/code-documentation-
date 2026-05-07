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