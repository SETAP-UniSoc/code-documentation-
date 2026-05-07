Admin Events Page
=================
 
Overview
--------
 
The **Admin Events Page** (``admin_events_page.dart``) is a Flutter ``StatefulWidget`` that gives society admins a full calendar-based interface for managing their society's events. It is accessible via the **Events** tab (index 2) of the ``AdminBottomNav`` navigation bar.
 
Admins can:
 
- View all society events plotted on an interactive monthly calendar
- Tap any date to see events scheduled on that day
- Create new events by tapping an empty date
- Edit existing event details (title, description, location)
- Delete events directly from the event list dialog
 
The page lives at ``lib/screens/admin/admin_events_page.dart`` and communicates with the Django REST API via the ``ApiService`` class.
 
.. note::
   ``admin_events_page.dart`` requires ``societyId`` as a mandatory constructor argument. This is always sourced from ``ApiService.societyId`` when navigated to via ``AdminBottomNav``.
 
---