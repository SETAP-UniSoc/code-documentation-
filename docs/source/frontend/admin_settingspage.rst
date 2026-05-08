Admin Settings Page
===================

Overview
--------

The **Admin Settings Page** provides administrators with a dedicated interface to
manage their personal account settings. It allows admins to update their profile
information, change email address, reset password, and configure notification
preferences.

This page is accessible from the admin dashboard and ensures that authenticated
administrators can maintain their account details securely.

Features
--------

- View current profile information (name and email)
- Edit and update display name
- Change email address with current email verification
- Change password with validation rules
- Toggle email notifications for society events
- Real-time form validation
- Secure password visibility toggles

Widget Structure
----------------

.. code-block:: dart

   AdminSettingsPage (StatefulWidget)
   ├── _loadUserData()
   ├── _loadNotificationSettings()
   ├── _updateName()
   ├── _updateEmail()
   ├── _changePassword()
   └── _updateNotificationSettings()

State Variables
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Variable
     - Type
     - Description
   * - ``_nameController``
     - TextEditingController
     - Controls name input field
   * - ``_currentEmailController``
     - TextEditingController
     - Stores current email for verification
   * - ``_newEmailController``
     - TextEditingController
     - Stores new email address
   * - ``_currentPasswordController``
     - TextEditingController
     - Stores current password for verification
   * - ``_newPasswordController``
     - TextEditingController
     - Stores new password
   * - ``_confirmPasswordController``
     - TextEditingController
     - Stores password confirmation
   * - ``_isEditingName``
     - bool
     - Toggles name edit mode
   * - ``_isLoading``
     - bool
     - Controls loading indicator and button states
   * - ``_notificationsEnabled``
     - bool
     - Current notification preference state
   * - ``_userName``
     - String
     - Current display name
   * - ``_userEmail``
     - String
     - Current email address
   * - ``_errorMessage``
     - String
     - Stores error messages for display
   * - ``_obscure*Password``
     - bool
     - Controls password visibility toggles

Initialisation
--------------

When the page loads, two parallel operations fetch user data and notification
preferences:

.. code-block:: dart

   @override
   void initState() {
     super.initState();
     _loadUserData();
     _loadNotificationSettings();
   }

**Behaviour:**
- User profile fetched from ``/user/profile/``
- Notification preferences fetched from ``/notifications/``
- Loading indicator shown until both requests complete
- Error messages displayed if requests fail

Profile Management
------------------

### Load User Profile

Retrieves the administrator's current profile information:

.. code-block:: dart

   Future<void> _loadUserData() async {
     final response = await client.get(
       Uri.parse("${ApiService.baseUrl}/user/profile/"),
       headers: ApiService.headers,
     );

     if (response.statusCode == 200) {
       final data = jsonDecode(response.body);
       setState(() {
         _userName = data["name"] ?? data["first_name"] ?? "Admin";
         _userEmail = data["email"] ?? "";
       });
     }
   }

**Response Fields:**
- ``name`` or ``first_name`` – Display name
- ``email`` – Registered email address

### Update Display Name

Allows administrators to change their display name with inline editing:

.. code-block:: dart

   Row(
     children: [
       Expanded(
         child: _isEditingName
             ? TextField(controller: _nameController)
             : Container(child: Text(_userName)),
       ),
       IconButton(
         icon: Icon(_isEditingName ? Icons.save : Icons.edit),
         onPressed: () {
           if (_isEditingName) {
             _updateName();
           } else {
             setState(() => _isEditingName = true);
           }
         },
       ),
     ],
   )

**Validation Rules:**
- Name cannot be empty
- Error message displayed if validation fails
- Success message confirms update

Email Management
----------------

### Change Email Address

Requires current email verification before updating to a new address:

.. code-block:: dart

   Future<void> _updateEmail() async {
     final response = await client.post(
       Uri.parse("${ApiService.baseUrl}/change-email/"),
       body: jsonEncode({
         "current_email": currentEmail,
         "new_email": newEmail,
       }),
     );

     if (response.statusCode == 200) {
       _userEmail = newEmail;
     }
   }

**Validation Rules:**
- Both current and new email fields must be filled
- Email format validation performed by backend
- Error message displayed for invalid or already used emails
- Fields cleared on successful update

Password Management
-------------------

### Change Password

Secure password update with multiple validation checks:

.. code-block:: dart

   Future<void> _changePassword() async {
     // Validation
     if (currentPassword.isEmpty || newPassword.isEmpty) {
       showError("Please fill in both password fields");
       return;
     }

     if (newPassword.length < 8) {
       showError("Password must be at least 8 characters");
       return;
     }

     if (newPassword != confirmPassword) {
       showError("New passwords don't match");
       return;
     }

     // API call
     final response = await client.post(
       Uri.parse("${ApiService.baseUrl}/change-password/"),
       body: jsonEncode({
         "old_password": currentPassword,
         "new_password": newPassword,
       }),
     );
   }

**Validation Rules:**
- Both current and new password fields required
- New password minimum length: 8 characters
- New password and confirmation must match
- Current password verified against backend

**Security Features:**
- Password visibility toggle (show/hide)
- All password fields start obscured
- Independent toggles for each password field

Notification Preferences
------------------------

### Toggle Email Notifications

Administrators can enable or disable email notifications for society events:

.. code-block:: dart

   Future<void> _updateNotificationSettings(bool enabled) async {
     final response = await client.post(
       Uri.parse("${ApiService.baseUrl}/notifications/"),
       body: jsonEncode({
         "society_id": ApiService.societyId,
         "event_notifications": enabled,
       }),
     );

     if (response.statusCode == 200) {
       setState(() => _notificationsEnabled = enabled);
       showSnackBar(enabled ? "Notifications enabled" : "Notifications disabled");
     }
   }

**Behaviour:**
- Switch toggles without page reload
- Success/failure feedback via SnackBar
- Preference persists across sessions

Form Validation Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Validation Rules
   * - Name
     - Cannot be empty
   * - Email
     - Both current and new fields required; must be valid format
   * - Current Password
     - Required; must match backend record
   * - New Password
     - Minimum 8 characters; must match confirmation
   * - Confirm Password
     - Must match new password

API Endpoints
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Endpoint
     - Method
     - Purpose
   * - ``/user/profile/``
     - GET
     - Retrieve user profile data
   * - ``/user/profile/``
     - POST
     - Update display name
   * - ``/change-email/``
     - POST
     - Change email address
   * - ``/change-password/``
     - POST
     - Update password
   * - ``/notifications/``
     - GET
     - Fetch notification preferences
   * - ``/notifications/``
     - POST
     - Update notification preferences

Error Handling
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Network failure
     - Error banner displayed; page remains functional
   * - Invalid current password
     - SnackBar error message shown
   * - Password mismatch
     - SnackBar error message shown
   * - Password too short
     - SnackBar error message shown
   * - Email already in use
     - Error message from backend displayed
   * - API server error
     - Error message displayed; user can retry

Loading States
--------------

- **Initial page load:** CircularProgressIndicator shown in body
- **Form submission:** Loading indicator within button; button disabled during request
- **Error display:** Error message appears at top of page, can be dismissed

UI Components
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Description
   * - Edit Icon
     - Pencil icon for name field; changes to save icon in edit mode
   * - Visibility Toggles
     - Eye icons next to password fields to show/hide text
   * - Read-only Email
     - Current email displayed in grey container; not editable directly
   * - Notification Switch
     - Modern toggle switch with purple accent colour
   * - Action Buttons
     - Purple elevated buttons for all form submissions

Dependencies
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Package
     - Purpose
   * - ``http``
     - API requests to backend
   * - ``ApiService``
     - Centralised API configuration and headers

Implementation Notes
--------------------

- The ``httpClient`` parameter allows dependency injection for testing
- All text controllers disposed in ``dispose()`` to prevent memory leaks
- ``setState()`` only called when widget is mounted to prevent errors
- Password fields use obscure text for security by default
- Form submission buttons disabled during async operations to prevent duplicates
- Error messages displayed consistently using SnackBar
- Notification preferences tied to admin's specific society using ``ApiService.societyId``