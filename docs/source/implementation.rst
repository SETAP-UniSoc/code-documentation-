Implementation
==============

Technologies Used
----------------

- Python (Django REST Framework backend)
- Dart / Flutter (frontend)
- PostgreSQL (database)
- Redis & Celery (background processing)
- GitHub (version control)

System Architecture
-------------------

The system follows a client-server architecture:

- The Flutter frontend communicates with the backend via REST APIs
- The Django backend processes requests and interacts with the database
- Redis and Celery handle asynchronous background tasks

Example API View
----------------

.. code-block:: python

   class User_ProfileView(APIView):

       permission_classes = [IsAuthenticated]

       def get(self, request):
           user = request.user
           serializer = UserSerializer(user)
           return Response(serializer.data)

       def post(self, request):
           user = request.user
           new_name = request.data.get("name")

           if not new_name:
               return Response({"error": "New name is required"}, status=400)

           user.name = new_name
           user.save()

           return Response({"message": "Name changed successfully"})