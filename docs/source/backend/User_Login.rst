User Login
==========

Overview
--------

Authenticates a user and returns a token.

Endpoint
--------

.. code-block:: http

   POST /api/login/

Response
--------

- Returns authentication token
- Returns user role and details

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


API view to authenticate a user and return an auth token.
Users can log in using either:
    - Email
    - University number (UP number)
Returns:
    - Auth token and user details on success
    - 401 Unauthorized if credentials are invalid
    