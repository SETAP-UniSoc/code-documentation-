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