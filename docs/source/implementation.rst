Implementation
==============

Technologies Used
----------------
- Python (backend)
- SQL Database
- Dart/Flutter (frontend)
- GitHub for version control

Example Code
------------

.. code-block:: python

   class User_ProfileView(APIView)

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        """Update the authenticated user's display name.

        user = request.user
        new_name = request.data.get("name")

        if not new_name:
            return Response({"error": "New name is required"}, status=400)

        user.name = new_name
        user.save()
        return Response({"message": "Name changed successfully"})

