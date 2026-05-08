Admin Login Screen
==================

Overview
--------

The **Admin Login Screen** provides a secure authentication interface for
administrators to access the UniSoc admin dashboard. It validates admin credentials
against the backend and ensures that only authorised administrators can log in.

This screen also includes a society selection dropdown to prevent administrators
from logging into the wrong society.

Features
--------

- Society selection dropdown populated from backend
- Email and password authentication
- Society validation against admin assignment
- Loading states for society fetching and login
- Error handling for network failures and invalid credentials
- Navigation links to Forgot Password and Signup screens

Widget Structure
----------------

.. code-block:: dart

   LoginScreenAdmin (StatefulWidget)
   ├── initState() → _fetchSocieties()
   ├── _fetchSocieties()
   ├── loginUser()
   └── build() → UI components

State Variables
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Variable
     - Type
     - Description
   * - ``emailController``
     - TextEditingController
     - Controls email input field
   * - ``passwordController``
     - TextEditingController
     - Controls password input field
   * - ``societies``
     - List<Map<String, dynamic>>
     - List of societies fetched from backend
   * - ``selectedSocietyId``
     - String?
     - ID of the selected society
   * - ``selectedSocietyName``
     - String?
     - Name of the selected society
   * - ``isLoadingSocieties``
     - bool
     - Shows loading indicator while fetching societies
   * - ``isLoggingIn``
     - bool
     - Shows loading indicator during login attempt

Initialisation
--------------

When the screen loads, it fetches all active societies from the backend:

.. code-block:: dart

   @override
   void initState() {
     super.initState();
     _fetchSocieties();
   }

**Behaviour:**
- Societies fetched from ``/societies/`` endpoint (no authentication required)
- Loading indicator shown while fetching
- Error message displayed if fetch fails
- Societies populate the dropdown selector

Society Selection
-----------------

Administrators must select their assigned society before logging in:

.. code-block:: dart

   DropdownButtonFormField<String>(
     value: selectedSocietyId,
     items: societies.map((society) {
       return DropdownMenuItem<String>(
         value: society["id"].toString(),
         child: Text(society["name"]),
       );
     }).toList(),
     onChanged: (value) {
       setState(() {
         selectedSocietyId = value;
         final society = societies.firstWhere(
           (s) => s["id"].toString() == value
         );
         selectedSocietyName = society["name"];
       });
     },
   )

**Features:**
- Dropdown shows all active societies
- Loading spinner shown while fetching
- "No societies found" message if list is empty
- Selected society stored for login validation

Authentication Flow
-------------------

Login Request

When the administrator submits the login form:

.. code-block:: dart

   Future<void> loginUser() async {
     // Frontend validation
     if (email.isEmpty || password.isEmpty) {
       showError("Email and Password are required");
       return;
     }
     
     if (selectedSocietyId == null) {
       showError("Please select a society");
       return;
     }

     // API request
     final response = await http.post(
       Uri.parse("${ApiService.baseUrl}/login/"),
       body: jsonEncode({
         "email": email,
         "password": password,
         "society_id": selectedSocietyId,
       }),
     );
   }

**Request Body:**
- ``email`` – Administrator's email address
- ``password`` – Administrator's password
- ``society_id`` – Selected society ID

Validation
----------

Frontend Validation

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Rule
     - Error Message
   * - Email empty
     - "Email and Password are required"
   * - Password empty
     - "Email and Password are required"
   * - Invalid email format
     - "Enter a valid email address"
   * - No society selected
     - "Please select a society"

Backend Validation

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Rule
     - Behaviour
   * - Email exists
     - 200 OK if found
   * - Password correct
     - 200 OK with token
   * - Society assignment matches
     - Verifies admin belongs to selected society
   * - Invalid credentials
     - 401 Unauthorized
   * - Society mismatch
     - Error: "Selected society does not match your admin assignment"

Society Validation
------------------

After successful login, the backend returns the admin's actual society ID. The
frontend compares it with the selected society:

.. code-block:: dart

   final backendSocietyId = responseData['society_id']?.toString();
   if (backendSocietyId != null && backendSocietyId != selectedSocietyId) {
     showError("Selected society does not match your admin assignment");
     return;
   }

This prevents administrators from logging in with a society they are not assigned to.

Successful Login
----------------

On successful authentication:

.. code-block:: dart

   ApiService.authToken = responseData["token"];
   ApiService.societyId = responseData["society_id"];
   ApiService.societyName = responseData["society_name"];

   Navigator.pushReplacement(
     context,
     MaterialPageRoute(builder: (context) => const AdminHomepage()),
   );

**Stored Data:**
- ``authToken`` – Used for subsequent API requests
- ``societyId`` – Admin's assigned society ID
- ``societyName`` – Admin's society name for display

Error Handling
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Network failure
     - "Unable to connect to server" message
   * - Invalid credentials
     - "Invalid email or password" message
   * - Society fetch fails
     - "Could not load societies. Please try again."
   * - Login timeout (10 seconds)
     - Timeout handled with error message
   * - Server error (4xx/5xx)
     - "Login failed (status code)" message

Loading States
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - State
     - Indicator
   * - Fetching societies
     - CircularProgressIndicator in dropdown area
   * - Logging in
     - CircularProgressIndicator replaces Login button
   * - Login button disabled
     - Button greyed out during request

API Endpoints
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Endpoint
     - Method
     - Purpose
   * - ``/societies/``
     - GET
     - Fetch all active societies for dropdown
   * - ``/login/``
     - POST
     - Authenticate admin and return token

Response Format
---------------

Successful Login (200 OK)

.. code-block:: json

   {
     "token": "auth_token_here",
     "role": "admin",
     "email": "admin@example.com",
     "society_id": 1,
     "society_name": "Football Society"
   }

Failed Login (401 Unauthorized)

.. code-block:: json

   {
     "error": "Invalid credentials"
   }

Society Mismatch (403 Forbidden)

.. code-block:: json

   {
     "error": "Invalid society selection"
   }

Navigation
----------

After successful login, the administrator is redirected to the **Admin Homepage**.
The screen also provides navigation links to:

- **Forgot Password** – ``ForgottenPasswordScreen``
- **Signup** – ``SignupUserPage`` (for regular user registration)

UI Components
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Description
   * - Society Dropdown
     - Form field with border outline, shows all societies
   * - Email Field
     - Underline input with email keyboard type
   * - Password Field
     - Underline input with obscure text
   * - Login Button
     - Elevated button, full width, shows loading spinner when pressed
   * - Signup Button
     - Secondary elevated button for user registration
   * - Forgot Password Link
     - Text button below password field

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
     - Centralised API configuration

Implementation Notes
--------------------

- Societies endpoint does NOT require authentication (allows pre-login fetch)
- Login request includes ``society_id`` for backend validation
- Timeout set to 10 seconds to prevent hanging requests
- All text controllers disposed in ``dispose()`` to prevent memory leaks
- ``mounted`` checks prevent state updates after widget disposal
- Society dropdown validates selection before enabling login
- Backend society ID comparison prevents unauthorised access to wrong society