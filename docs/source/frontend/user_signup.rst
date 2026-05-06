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
