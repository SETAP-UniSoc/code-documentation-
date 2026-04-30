User Registration
=================

Overview
--------

This endpoint allows a new user to register an account in the system.
It validates user input, enforces password strength rules, and ensures
unique email and university number.

Endpoint
--------

.. code-block:: python

   path("user/register/", RegisterView.as_view(), name="register")

Authentication
--------------

- Not required

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

        # Check required fields
        if not all([first_name, last_name, email, up_number, password, confirm_password]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Password match
        if password != confirm_password:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Password strength
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
        # Normalize UP number
        up_number = up_number.lower()
        if not up_number.startswith("up"):
            up_number = f"up{up_number}"
        # Check duplicates
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=400)

        if User.objects.filter(up_number=up_number).exists():
            return Response({"error": "UP number already exists"}, status=400)
        # Create user
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


API view to handle user registration, accepts user details including first name, last name, email,
    university number (UP number), and password. It validates:
    - All required fields are provided
    - Passwords match
    - Password strength (length, uppercase, number, special character)

    Returns:
    - 201 Created on success
    - 400 Bad Request on validation failure
