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



Widget Structure
----------------
 
.. code-block:: text
 
   UserSettingsPage (StatefulWidget)
   └── _UserSettingsPageState (State)
       ├── _loadUserData()           → GET /user/profile/
       ├── _loadNotificationSettings() → GET /notifications/ + GET /my-societies/
       ├── _updateName()             → POST /user/profile/
       ├── _updateEmail()            → POST /change-email/
       ├── _changePassword()         → POST /change-password/
       ├── _updateNotificationSettings() → POST /notifications/
       └── _updateSingleNotification()   → POST /notifications/
 
---





 
State Variables
---------------
 
.. list-table::
   :header-rows: 1
   :widths: 30 15 55
 
   * - Variable
     - Type
     - Description
   * - ``_nameController``
     - ``TextEditingController``
     - Controls the name input field.
   * - ``_newEmailController``
     - ``TextEditingController``
     - Controls the new email input field.
   * - ``_currentPasswordController``
     - ``TextEditingController``
     - Controls the current password input field.
   * - ``_newPasswordController``
     - ``TextEditingController``
     - Controls the new password input field.
   * - ``_confirmPasswordController``
     - ``TextEditingController``
     - Controls the confirm password input field.
   * - ``_isEditingName``
     - ``bool``
     - Toggles between display and edit mode for the name field.
   * - ``_isLoading``
     - ``bool``
     - Controls the full-page loading spinner.
   * - ``_notificationsEnabled``
     - ``bool``
     - Tracks whether the first society's notifications are enabled.
   * - ``_notificationPrefs``
     - ``List<Map<String, dynamic>>``
     - List of per-society notification preference objects.
   * - ``_obscureCurrentPassword``
     - ``bool``
     - Toggles password visibility for the current password field.
   * - ``_obscureNewPassword``
     - ``bool``
     - Toggles password visibility for the new password field.
   * - ``_obscureConfirmPassword``
     - ``bool``
     - Toggles password visibility for the confirm password field.
   * - ``_userName``
     - ``String``
     - The user's display name loaded from the API.
   * - ``_userEmail``
     - ``String``
     - The user's email address loaded from the API.
   * - ``_errorMessage``
     - ``String``
     - Error message shown in the UI when profile loading fails.
 
---




Lifecycle
---------
 
``initState``
~~~~~~~~~~~~~
 
Called once when the widget is first inserted into the tree. Triggers two parallel data loads:
 
.. code-block:: dart
 
   @override
   void initState() {
     super.initState();
     _loadUserData();
     _loadNotificationSettings();
   }
 
``dispose``
~~~~~~~~~~~
 
Disposes all five ``TextEditingController`` instances to free memory when the widget is removed:
 
.. code-block:: dart
 
   @override
   void dispose() {
     _nameController.dispose();
     _newEmailController.dispose();
     _currentPasswordController.dispose();
     _newPasswordController.dispose();
     _confirmPasswordController.dispose();
     super.dispose();
   }
 
---



API Methods
-----------
 
``_loadUserData()``
~~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``GET /api/user/profile/``
 
Fetches the authenticated user's profile. On success, populates ``_userName`` and ``_userEmail``. Falls back to ``first_name`` if ``name`` is absent.
 
**Name resolution logic:**
 
.. code-block:: text
 
   if data["name"] is not null and not empty  → use data["name"]
   else if data["first_name"] is not null and not empty → use data["first_name"]
   else → use "User"
 
**Error handling:**
 
- ``statusCode != 200`` → sets ``_errorMessage`` with the status code.
- Network exception → sets ``_errorMessage`` to ``"Connection error: Unable to load profile"``.
- Always sets ``_isLoading = false`` in the ``finally`` block.
 
---




``_loadNotificationSettings()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
**Endpoints:**
 
- ``GET /api/notifications/`` — fetches existing notification preferences.
- ``GET /api/my-societies/`` — fetches the user's joined societies as a fallback.
 
**Logic:**
 
1. Fetches notification preferences from ``/notifications/``.
2. Fetches joined societies from ``/my-societies/`` to build a ``societyNameToId`` lookup map.
3. If notification preferences exist, maps each preference to include the resolved ``society_id``.
4. If no preferences exist, falls back to joined societies with ``notify_new_events: true`` as the default.
5. If the notifications endpoint fails entirely, still attempts to load joined societies.
 
.. note::
   A society's ``id`` is resolved from its ``name`` using the ``societyNameToId`` map. If the name is not found, ``society_id`` defaults to ``-1``.
 
---
 
``_updateName()``
~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``POST /api/user/profile/``
 
**Request body:**
 
.. code-block:: json
 
   { "name": "<new_name>" }
 
**Validation:** Rejects empty name strings before making the API call.
 
**On success:** Updates ``_userName`` and exits edit mode (``_isEditingName = false``).
 
**On failure:** Displays the HTTP status code in a ``SnackBar``.
 
---



``_updateEmail()``
~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``POST /api/change-email/``
 
**Request body:**
 
.. code-block:: json
 
   { "new_email": "<new_email>" }
 
**Validation:** Rejects empty email strings before making the API call.
 
**On success:** Updates ``_userEmail`` and clears the input field.
 
**On failure:** Parses ``error`` from the response body if available, otherwise shows a generic message.
 
**Common error responses from the backend:**
 
.. list-table::
   :header-rows: 1
   :widths: 20 80
 
   * - Status
     - Meaning
   * - ``400``
     - Email already in use, or new email field is missing.
   * - ``401``
     - User is not authenticated.
 
---
 
``_changePassword()``
~~~~~~~~~~~~~~~~~~~~~
 
**Endpoint:** ``POST /api/change-password/``
 
**Request body:**
 
.. code-block:: json
 
   {
     "old_password": "<current_password>",
     "new_password": "<new_password>"
   }
 
**Client-side validation (in order):**
 
1. Both ``currentPassword`` and ``newPassword`` must be non-empty.
2. ``newPassword`` must be at least 8 characters.
3. ``newPassword`` must match ``confirmPassword``.
 
If any check fails, a descriptive ``SnackBar`` is shown and no API call is made.
 
**On success:** Clears all three password fields.
 
**Common error responses from the backend:**
 
.. list-table::
   :header-rows: 1
   :widths: 20 80
 
   * - Status
     - Meaning
   * - ``400``
     - Old password incorrect, or new password too short.
   * - ``401``
     - User is not authenticated.
 
---