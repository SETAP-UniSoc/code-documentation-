User Login
==========

Overview
--------

The **User Login API** authenticates a user using either their email address
or university (UP) number and returns an authentication token.

This token is required for accessing protected endpoints within the system.

Endpoint
--------

.. code-block:: http

   POST /api/login/

**Django Route**

.. code-block:: python

   path("login/", LoginView.as_view(), name="login")

Authentication
--------------

- **Required**: No (public endpoint)
- **Access Level**: All users

Request Body
------------

.. code-block:: json

   {
     "email": "user@example.com",
     "password": "password123"
   }

OR

.. code-block:: json

   {
     "up_number": "up1234567",
     "password": "password123"
   }

Request Rules
~~~~~~~~~~~~~

- Either ``email`` or ``up_number`` must be provided
- ``password`` is required
- ``up_number`` is case-insensitive
- If ``up_number`` does not start with ``"up"``, it will be automatically prefixed

---

Response
--------

Success Response (200 OK)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "token": "abc123xyz",
     "role": "admin",
     "email": "user@example.com",
     "up_number": "up1234567",
     "society_id": 1,
     "society_name": "Music Society"
   }

Response Fields Explained
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``token``
     - Authentication token used for subsequent requests
   * - ``role``
     - User role (e.g. admin, student)
   * - ``email``
     - User email address
   * - ``up_number``
     - University identifier
   * - ``society_id``
     - ID of the society (only for admins, otherwise null)
   * - ``society_name``
     - Name of the society (only for admins, otherwise null)

Error Responses
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status Code
     - Description
   * - 400
     - Missing required fields (e.g. password or login identifier)
   * - 401
     - Invalid credentials

Example Error:

.. code-block:: json

   {
     "error": "Invalid credentials"
   }

---

Implementation
--------------

.. code-block:: python

   class LoginView(APIView):

       def post(self, request):
           email = request.data.get("email")
           up_number = request.data.get("up_number")
           password = request.data.get("password")

           if not password:
               return Response({"error": "Password required"}, status=400)

           try:
               if email:
                   user = User.objects.get(email__iexact=email)
               elif up_number:
                   up_number = up_number.lower()
                   if not up_number.startswith("up"):
                       up_number = f"up{up_number}"
                   user = User.objects.get(up_number__iexact=up_number)
               else:
                   return Response({"error": "Email or UP number required"}, status=400)

               if user.check_password(password):
                   token, _ = Token.objects.get_or_create(user=user)

                   society_id = None
                   society_name = None

                   if user.role == "admin":
                       try:
                           society = Society.objects.get(admin=user)
                           society_id = society.id
                           society_name = society.name
                       except Society.DoesNotExist:
                           pass

                   return Response({
                       "token": token.key,
                       "role": user.role,
                       "email": user.email,
                       "up_number": user.up_number,
                       "society_id": society_id,
                       "society_name": society_name
                   })

           except User.DoesNotExist:
               pass

           return Response({"error": "Invalid credentials"}, status=401)

Description
-----------

- Authenticates user credentials against stored data
- Supports login via:
  - Email (case-insensitive)
  - University number (UP number)
- Automatically normalises UP numbers
- Generates or retrieves an authentication token
- Returns additional admin-specific data if applicable

Data Flow
---------

1. User submits login credentials
2. System validates input fields
3. User is retrieved via email or UP number
4. Password is verified
5. Token is generated/retrieved
6. Response returned with user details

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Missing password
     - Returns 400
   * - Missing email and UP number
     - Returns 400
   * - Invalid credentials
     - Returns 401
   * - Admin without society
     - Returns null for society fields

Implementation Notes
-------------------

- Uses ``TokenAuthentication`` for session management
- Case-insensitive lookups improve usability
- Gracefully handles missing admin society
- Avoids user enumeration by returning generic error messages

---

Security Considerations
----------------------

- Passwords are securely hashed and verified using Django's authentication system
- Token-based authentication is used for subsequent requests
- No sensitive data (e.g. passwords) is returned in responses
- Generic error messages prevent user enumeration attacks

