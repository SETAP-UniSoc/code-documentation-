User Signup Page
================
 
Overview
--------
 
The **User Signup** page allows new users to create an account. It collects personal
details, validates all input client-side before submission, and on success redirects the
user to the login screen.
 
The page is implemented as the ``SignupUserPage`` stateful widget, found at
``lib/screens/signup_user_page.dart``.
 
---

Navigation
----------
 
**Route into this page**
 
``SignupUserPage`` is reached by tapping the **Signup** button on the User Login screen.
 
.. code-block:: dart
 
   Navigator.push(
     context,
     MaterialPageRoute(builder: (context) => const SignupUserPage()),
   );
 
**Route out of this page**
 
On successful registration the user is sent to ``LoginScreenUser``. The current route
is replaced so the user cannot navigate back to the signup form.
 
.. code-block:: dart
 
   Navigator.pushReplacement(
     context,
     MaterialPageRoute(builder: (context) => const LoginScreenUser()),
   );
 
---


Widget Structure
----------------
 
``SignupUserPage`` is a ``StatefulWidget``. Its state class ``_SignupUserPageState``
manages the following:
 
**Controllers**
 
One ``TextEditingController`` per input field:
 
.. list-table::
   :widths: 35 65
   :header-rows: 1
 
   * - Controller
     - Field
   * - ``firstNameController``
     - First name text input.
   * - ``lastNameController``
     - Last name text input.
   * - ``upnumberController``
     - UP number digits input (numbers only, max 7 digits).
   * - ``emailController``
     - Email address input.
   * - ``passwordController``
     - Password input (obscured).
   * - ``confirmPasswordController``
     - Confirm password input (obscured).
 
**State fields**
 
.. list-table::
   :widths: 25 15 60
   :header-rows: 1
 
   * - Field
     - Type
     - Description
   * - ``isLoading``
     - ``bool``
     - ``true`` while the signup request is in flight. Replaces the submit button
       with a ``CircularProgressIndicator``.
 
---

Form Fields
-----------
 
The form is rendered inside a ``SingleChildScrollView`` to accommodate smaller screens.
All fields use ``UnderlineInputBorder`` styling.
 
.. list-table::
   :widths: 25 20 55
   :header-rows: 1
 
   * - Label
     - Input type
     - Notes
   * - First Name
     - Text
     - Built with ``_buildField``. No special keyboard or formatter.
   * - Last Name
     - Text
     - Built with ``_buildField``. No special keyboard or formatter.
   * - UP Number
     - Number
     - ``keyboardType: TextInputType.number``. Accepts digits only
       (``FilteringTextInputFormatter.digitsOnly``). Hard-capped at 7 digits
       (``LengthLimitingTextInputFormatter(7)``). Displays a ``prefixText`` of ``"UP"``
       so the user only types the numeric portion.
   * - Email
     - Text
     - Built with ``_buildField``.
   * - Password
     - Text (obscured)
     - Built with ``_buildField(obscure: true)``.
   * - Confirm Password
     - Text (obscured)
     - Built with ``_buildField(obscure: true)``.
 
**``_buildField`` helper**
 
Wraps a ``TextField`` in a ``Padding`` with 12 px bottom spacing.
 
.. code-block:: dart
 
   Widget _buildField(TextEditingController controller, String label,
       {bool obscure = false}) {
     return Padding(
       padding: const EdgeInsets.only(bottom: 12),
       child: TextField(
         controller: controller,
         obscureText: obscure,
         decoration: InputDecoration(
           labelText: label,
           border: const UnderlineInputBorder(),
         ),
       ),
     );
   }
 
---


Client-Side Validation
----------------------
 
All validation runs inside ``_validateFields()`` before any network call is made.
Errors are shown via ``SnackBar`` (see `Error Handling`_). The method returns ``false``
on the first failing rule, stopping further checks.
 
.. list-table::
   :widths: 40 60
   :header-rows: 1
 
   * - Rule
     - Error message shown
   * - All fields non-empty
     - ``"Please fill in all fields"``
   * - UP number matches ``^\d{7}$`` (exactly 7 digits)
     - ``"UP number must be exactly 7 digits"``
   * - Email matches ``^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$``
     - ``"Enter a valid email address"``
   * - Password equals confirm password
     - ``"Passwords do not match"``
   * - Password length ≥ 8 characters
     - ``"Password must be at least 8 characters"``
   * - Password length ≤ 20 characters
     - ``"Password must not exceed 20 characters"``
   * - Password contains at least one uppercase letter (``[A-Z]``)
     - ``"Password must contain one uppercase letter"``
   * - Password contains at least one digit (``\d``)
     - ``"Password must contain one number"``
   * - Password contains at least one special character (``[^\w\s]``)
     - ``"Password must contain one special character"``
 
.. note::
   The UP number field accepts only digits at the keyboard level (``FilteringTextInputFormatter``),
   but the 7-digit exact-length rule is enforced again in ``_validateFields`` as a safety check.
 
---


 
Signup Action
-------------
 
The signup is handled by the async method ``signupUser()``.
 
**Step 1 — validate**
 
Calls ``_validateFields()``. Returns early without a network call if validation fails.
 
**Step 2 — build UP number**
 
Prefixes the user's 7-digit input with ``"UP"`` before sending:
 
.. code-block:: dart
 
   final upnumber = "UP${upnumberController.text.trim()}";
 
**Step 3 — POST to the API**
 
.. code-block:: dart
 
   final response = await http.post(
     Uri.parse("http://10.128.4.160:8000/api/user/register/"),
     headers: {
       "Content-Type": "application/json",
       "Accept": "application/json",
     },
     body: jsonEncode({
       "first_name": firstNameController.text.trim(),
       "last_name":  lastNameController.text.trim(),
       "up_number":  upnumber,
       "email":      emailController.text.trim(),
       "password":   passwordController.text,
       "confirm_password": confirmPasswordController.text,
     }),
   );
 
Endpoint: ``POST /api/user/register/``
 
**Step 4 — handle response**
 
.. list-table::
   :widths: 15 85
   :header-rows: 1
 
   * - Status
     - Behaviour
   * - 200 or 201
     - Shows a green ``SnackBar``: ``"Signup successful"``. Navigates to
       ``LoginScreenUser`` via ``pushReplacement``.
   * - Any other status
     - Attempts to decode the body and read ``error``, ``message``, or ``detail``
       fields. Falls back to ``"Signup failed (<status code>)"`` if none are present.
       Displays the message in a ``SnackBar``.
   * - Network exception
     - Shows ``"Network error: <exception message>"`` in a ``SnackBar``.
 
``isLoading`` is set to ``false`` in a ``finally`` block, and all state updates are
guarded by ``mounted`` checks.
 
---

AppBar
------
 
.. list-table::
   :widths: 25 75
   :header-rows: 1
 
   * - Property
     - Value
   * - ``title``
     - ``"User Signup"``.
   * - Style
     - Default — inherits the app theme.
 
---


Submit Button
-------------
 
While ``isLoading`` is ``false``, the page shows an ``ElevatedButton`` labelled
``"Signup"`` that calls ``signupUser()``.
 
While ``isLoading`` is ``true``, the button is replaced with a
``CircularProgressIndicator``.
 
.. code-block:: dart
 
   isLoading
     ? const CircularProgressIndicator()
     : ElevatedButton(
         onPressed: signupUser,
         child: const Text("Signup"),
       ),
 
---


Error Handling
--------------
 
All user-facing errors are shown through ``_showError``, which displays a ``SnackBar``
in the current context:
 
.. code-block:: dart
 
   void _showError(String message) {
     ScaffoldMessenger.of(context).showSnackBar(
       SnackBar(content: Text(message)),
     );
   }
 
This is used for both validation failures and API error responses.
 
---


Endpoint Used
-------------
 
- ``POST /api/user/register/``
 
No auth token is required — this endpoint is publicly accessible. Headers are set
directly on the request rather than using ``ApiService.headers``.
 
---



Page Flow
---------
 
::
 
   LoginScreenUser
         │
         │  [tap Signup button]
         │
         ▼
   SignupUserPage
         │
         │  User fills in all fields
         │
         │  [tap Signup]
         │
         ├── _validateFields() fails
         │         │
         │         └── SnackBar with validation error
         │             (stays on SignupUserPage)
         │
         └── _validateFields() passes
                   │
                   │  POST /api/user/register/
                   │
                   ├── 200 / 201  →  SnackBar "Signup successful"
                   │                 pushReplacement → LoginScreenUser
                   │
                   ├── 4xx / 5xx  →  SnackBar with error from response body
                   │                 (stays on SignupUserPage)
                   │
                   └── Exception  →  SnackBar "Network error: ..."
                                     (stays on SignupUserPage)
 
---