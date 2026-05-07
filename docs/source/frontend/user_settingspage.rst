User Settings Page
==================
 
Overview
--------
 
The **User Settings Page** (``settings_user_page.dart``) is a Flutter ``StatefulWidget`` that allows authenticated users to manage their personal account details. It provides the following functionality:
 
- View and edit their display name
- View their current email address
- Change their email address
- Change their password
- Manage per-society notification preferences
 
The page lives at ``lib/screens/user/settings_user_page.dart`` and communicates with the Django REST API via the ``ApiService`` class.
 
.. note::
   All API calls on this page require an authenticated user. The ``Authorization: Token <token>`` header is automatically included via ``ApiService.headers``.
 
---