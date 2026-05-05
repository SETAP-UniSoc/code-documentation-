User LoginPage
========================================
 
1. Overview
-----------
 
``LoginScreenUser`` is a ``StatefulWidget`` responsible for authenticating regular
(non-admin) users of the UniSoc application. It presents a form to collect the
user's UP number and password, submits credentials to the backend REST API, and
navigates to the home page upon successful authentication.
 
**Source file:** ``lib/screens/auth/login_screen_user.dart``
 
----
 
2. Imports
----------
 
.. list-table::
   :widths: 35 65
   :header-rows: 1
 
   * - Package / File
     - Purpose
   * - ``dart:convert``
     - JSON encoding/decoding (``jsonEncode``, ``jsonDecode``)
   * - ``dart:async``
     - ``TimeoutException`` handling
   * - ``package:flutter/material.dart``
     - Core Flutter widgets and Material design
   * - ``package:flutter/services.dart``
     - ``FilteringTextInputFormatter``, ``LengthLimitingTextInputFormatter``
   * - ``package:http/http.dart``
     - HTTP client for API requests
   * - ``screens/user/user_home_page.dart``
     - Destination screen after successful login
   * - ``login_screen.admin.dart``
     - Admin login screen (navigation target)
   * - ``forgotten_password_screen.dart``
     - Forgotten password screen (navigation target)
   * - ``signup_user_page.dart``
     - User signup screen (navigation target)
   * - ``services/api_services.dart``
     - ``ApiService`` class — base URL and auth token storage
 
----
 
3. Class Structure
------------------
 
.. list-table::
   :widths: 30 35 35
   :header-rows: 1
 
   * - Class
     - Type
     - Description
   * - ``LoginScreenUser``
     - ``StatefulWidget``
     - Root widget; instantiated with ``const`` constructor
   * - ``_LoginScreenUserState``
     - ``State<LoginScreenUser>``
     - Holds controllers, loading flag, and all business logic
 
----
 
4. State Variables
------------------
 
.. list-table::
   :widths: 30 30 40
   :header-rows: 1
 
   * - Variable
     - Type
     - Purpose
   * - ``upnumberController``
     - ``TextEditingController``
     - Captures the UP number field input
   * - ``passwordController``
     - ``TextEditingController``
     - Captures the password field input
   * - ``isLoading``
     - ``bool``
     - Toggles between the login button and ``CircularProgressIndicator``
 
----
 
5. Methods
----------
 
5.1 ``_showError(String message)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Displays a transient ``SnackBar`` at the bottom of the screen with the given
error message. Guards against calls after widget disposal using a ``mounted``
check.
 
**Signature:**
 
.. code-block:: dart
 
   void _showError(String message)
 
**Behaviour:**
 
- Checks ``mounted`` before accessing ``context`` to avoid calling ``setState``
  on a disposed widget.
- Calls ``ScaffoldMessenger.of(context).showSnackBar`` with a ``SnackBar``
  containing the message text.
 
----
 
5.2 ``loginUser()``
~~~~~~~~~~~~~~~~~~~~
 
Core async method that validates input, sends a ``POST`` request to the login
endpoint, handles the response, and navigates to the home screen on success.
 
**Signature:**
 
.. code-block:: dart
 
   Future<void> loginUser() async
 
**Step-by-step flow:**
 
.. list-table::
   :widths: 8 92
   :header-rows: 1
 
   * - Step
     - Description
   * - 1
     - Read and trim ``upnumberController.text``; read ``passwordController.text``.
   * - 2
     - Validate: if either field is empty, call ``_showError`` and return early.
   * - 3
     - Set ``isLoading = true`` via ``setState`` to show the loading indicator.
   * - 4
     - Build the target URI: ``"${ApiService.baseUrl}/login/"``.
   * - 5
     - ``POST`` JSON body ``{"up_number": upNumber, "password": password}`` with
       ``Content-Type: application/json``. A 10-second timeout is applied.
   * - 6
     - Check ``mounted`` after ``await``; if ``false``, return without touching context.
   * - 7
     - Handle response by status code (see table below).
   * - 8
     - Catch ``TimeoutException`` and generic exceptions, showing appropriate error messages.
   * - 9
     - ``finally``: set ``isLoading = false`` if still mounted.
 
**HTTP response handling:**
 
.. list-table::
   :widths: 20 42 38
   :header-rows: 1
 
   * - Status Code
     - Action
     - User-Facing Message
   * - ``200 OK``
     - Decode token, store in ``ApiService.authToken``, navigate to ``HomePage``
       via ``pushReplacement``
     - *(navigates — no message)*
   * - ``401 Unauthorized``
     - Call ``_showError``
     - ``"Incorrect password"``
   * - ``404 Not Found``
     - Call ``_showError``
     - ``"UP number not found"``
   * - Other
     - Call ``_showError`` with status code
     - ``"Login failed (<status code>)"``
   * - ``TimeoutException``
     - Call ``_showError``; log to console
     - ``"Login request timed out. Check server connection."``
   * - Other exception
     - Call ``_showError``; log to console
     - ``"Network or server error"``
 
----
 
5.3 ``build(BuildContext context)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Constructs and returns the widget tree. Returns a ``Scaffold`` with an
``AppBar`` and a centred, padded ``Column`` containing all form elements.
 
**Signature:**
 
.. code-block:: dart
 
   @override
   Widget build(BuildContext context)
 
----
 
6. UI Components
----------------
 
.. list-table::
   :widths: 28 25 47
   :header-rows: 1
 
   * - Widget
     - Type / Config
     - Description
   * - AppBar
     - ``title: "User Login"``
     - Top application bar
   * - ``"Login"`` label
     - ``Text``, 28pt bold
     - Section heading at top of the form
   * - UP Number field
     - ``TextField`` (numeric)
     - Digits only, max 7 chars, prefixed with ``"UP"``. Bound to
       ``upnumberController``.
   * - Password field
     - ``TextField`` (obscured)
     - Password input, ``obscureText: true``. Bound to ``passwordController``.
   * - ``"Forgot Password?"`` button
     - ``TextButton``
     - Navigates to ``ForgottenPasswordScreen`` via ``push``.
   * - ``"Login"`` button
     - ``ElevatedButton`` / ``CircularProgressIndicator``
     - Full-width. Calls ``loginUser()``. Replaced by spinner when
       ``isLoading`` is ``true``.
   * - ``"Signup"`` button
     - ``ElevatedButton``
     - Full-width. Navigates to ``SignupUserPage`` via ``push``.
   * - ``"Admin"`` button
     - ``ElevatedButton``
     - Full-width. Navigates to ``LoginScreenAdmin`` via ``push``.
 
----
 
7. Input Validation & Formatting
---------------------------------
 
7.1 UP Number Field
~~~~~~~~~~~~~~~~~~~~
 
- ``FilteringTextInputFormatter.digitsOnly`` — rejects any non-digit keystroke.
- ``LengthLimitingTextInputFormatter(7)`` — enforces a maximum of 7 digits.
- The prefix ``"UP"`` is displayed via ``prefixText`` but is **not** part of
  the stored controller value.
- The raw numeric string is sent to the backend; the ``LoginView`` on the
  backend prepends ``"up"`` if absent and lowercases the result.



7.2 Client-Side Pre-submission Check
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 
Both fields must be non-empty; otherwise ``_showError`` is called and the
network request is skipped entirely.


.. note::
 
   No further client-side validation (format, length semantics, password
   strength) is performed. All deeper validation is delegated to the backend.
  
----


8. API Integration
------------------
 
.. list-table::
   :widths: 22 78
   :header-rows: 1

* - Field
  - Value
* - Method
  - ``POST``
* - URL
  - ``${ApiService.baseUrl}/login/`` → ``http://10.128.5.248:8000/api/login/``
* - Headers
  - ``Content-Type: application/json``
* - Request Body
  - ``{"up_number": "<digits>", "password": "<password>"}``
* - Timeout
  - 10 seconds
* - Success Response
  - ``HTTP 200`` — ``{"token": "<auth_token>", "role": ..., "email": ..., ...}``

8.1 Token Storage
~~~~~~~~~~~~~~~~~~
 
On success the token string from ``responseData["token"]`` is written to the
static field ``ApiService.authToken``. This value is then automatically
included as ``Authorization: Token <authToken>`` in the headers map for all
subsequent authenticated requests via ``ApiService.headers``.

----

9. Navigation Map
-----------------
 
.. list-table::
   :widths: 35 30 35
   :header-rows: 1

* - Trigger
  - Destination Screen
  - Method
* - Successful login (``HTTP 200``)
  - ``HomePage``
  - ``Navigator.pushReplacement`` (removes login screen from stack)




