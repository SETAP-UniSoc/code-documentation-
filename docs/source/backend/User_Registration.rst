User Registration
=================

Overview
--------

The **User Registration API** allows new users to create an account in the system.

It validates user input, enforces password strength requirements, and ensures
that both email and university (UP) number are unique.

Endpoint
--------

.. code-block:: http

   POST /api/user/register/

**Django Route**

.. code-block:: python

   path("user/register/", RegisterView.as_view(), name="register")

Authentication
--------------

- **Required**: No
- **Access Level**: Public

---

Request Body
------------

.. code-block:: json

   {
     "first_name": "John",
     "last_name": "Doe",
     "email": "john@example.com",
     "up_number": "up1234567",
     "password": "SecurePass1!",
     "confirm_password": "SecurePass1!"
   }

Request Rules
~~~~~~~~~~~~~

- All fields are required
- ``password`` and ``confirm_password`` must match
- ``up_number`` is case-insensitive
- If ``up_number`` does not start with ``"up"``, it will be automatically prefixed

---

Validation Rules
----------------

Password Requirements
~~~~~~~~~~~~~~~~~~~~~

- Minimum 8 characters
- At least one uppercase letter
- At least one number
- At least one special character

Uniqueness Constraints
~~~~~~~~~~~~~~~~~~~~~~

- Email must be unique
- UP number must be unique

---

Response
--------

Success Response (201 Created)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

   {
     "message": "User registered successfully"
   }

Error Responses
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status Code
     - Description
   * - 400
     - Missing fields or validation failure

Example Errors:

.. code-block:: json

   { "error": "All fields are required" }

.. code-block:: json

   { "error": "Passwords do not match" }

.. code-block:: json

   { "error": "Password must contain at least one uppercase letter" }

.. code-block:: json

   { "error": "Email already exists" }

---

Implementation
--------------

.. code-block:: python

   class RegisterView(APIView):

       def post(self, request):

           first_name = request.data.get("first_name")
           last_name = request.data.get("last_name")
           email = request.data.get("email")
           up_number = request.data.get("up_number")
           password = request.data.get("password")
           confirm_password = request.data.get("confirm_password")

           if not all([first_name, last_name, email, up_number, password, confirm_password]):
               return Response(
                   {"error": "All fields are required"},
                   status=status.HTTP_400_BAD_REQUEST
               )

           if password != confirm_password:
               return Response(
                   {"error": "Passwords do not match"},
                   status=status.HTTP_400_BAD_REQUEST
               )

           if len(password) < 8:
               return Response(
                   {"error": "Password must be at least 8 characters long"},
                   status=status.HTTP_400_BAD_REQUEST
               )

           if not re.search(r"[A-Z]", password):
               return Response(
                   {"error": "Password must contain at least one uppercase letter"},
                   status=status.HTTP_400_BAD_REQUEST
               )

           if not re.search(r"[0-9]", password):
               return Response(
                   {"error": "Password must contain at least one number"},
                   status=status.HTTP_400_BAD_REQUEST
               )

           if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
               return Response(
                   {"error": "Password must contain at least one special character"},
                   status=status.HTTP_400_BAD_REQUEST
               )

           up_number = up_number.lower()
           if not up_number.startswith("up"):
               up_number = f"up{up_number}"

           if User.objects.filter(email=email).exists():
               return Response({"error": "Email already exists"}, status=400)

           if User.objects.filter(up_number=up_number).exists():
               return Response({"error": "UP number already exists"}, status=400)

           user = User.objects.create_user(
               first_name=first_name,
               last_name=last_name,
               email=email,
               up_number=up_number,
               password=password
           )

           return Response(
               {"message": "User registered successfully"},
               status=status.HTTP_201_CREATED
           )

---

Data Flow
---------

1. User submits registration form
2. System validates all required fields
3. Password rules are enforced
4. UP number is normalised
5. System checks for duplicate email and UP number
6. User account is created
7. Success response returned

---

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Missing required fields
     - Returns 400
   * - Passwords do not match
     - Returns 400
   * - Weak password
     - Returns 400
   * - Email already exists
     - Returns 400
   * - UP number already exists
     - Returns 400

---

Implementation Notes
-------------------

- Uses Django's ``create_user`` for secure password hashing
- Input validation handled manually in the view
- UP number normalisation ensures consistent storage
- Prevents duplicate user records

---

Security Considerations
----------------------

- Passwords are never stored in plain text
- Strong password policy enforced
- Duplicate checks prevent account conflicts
- No sensitive data is returned in responses

---
