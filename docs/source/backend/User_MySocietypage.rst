User My Societies Page
======================

Overview
--------

Allows users to view and manage societies they are part of.

Endpoints
---------

.. code-block:: python

   path("my-societies/", MySocietiesView.as_view(), name="my-societies")
   path("society/<int:society_id>/join/", JoinSocietyView.as_view(), name="join-society")
   path("society/<int:society_id>/leave/", LeaveSocietyView.as_view(), name="leave-society")

Authentication
--------------

- Required

Features
--------

- View joined societies
- Join new societies
- Leave societies

Implementation
--------------

.. code-block:: python

   class MySocietiesView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        memberships = Membership.objects.filter(
            user=request.user,
            left_at__isnull=True
        ).select_related("society")

        societies = []
        for m in memberships:
            s = m.society
            societies.append({
                "id": s.id,
                "name": s.name,
                "category": s.category,
                "description": s.description,
            })

        return Response(societies)

Returns all societies the user is currently a member of.

.. code-block:: python
   class JoinSocietyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, society_id):
        user = request.user

        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response(
                {"error": "Society not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        membership, created = Membership.objects.get_or_create(
            user=user,
            society=society
        )

        if created:
            return Response(
                {"message": "Joined successfully"},
                status=status.HTTP_201_CREATED
            )

        if membership.left_at is None:
            return Response({"message": "Already joined"}, status=200)

        # Rejoining
        membership.left_at = None
        membership.joined_at = timezone.now()
        membership.save()

        return Response({"message": "Rejoined successfully"}, status=20


API view to allow a user to join a society.
Behaviour:
    - Creates a new membership if none exists
    - Returns 'Already joined' if user is already active
    - Re-activates membership if previously left

.. code-block:: python

   class LeaveSocietyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, society_id):
        user = request.user

        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response(
                {"error": "Society not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            membership = Membership.objects.get(
                user=user,
                society=society,
                left_at__isnull=True
                
            )
        except Membership.DoesNotExist:
            return Response(
                {"error": "You are not an active member"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.left_at = timezone.now()
        membership.save()

        return Response(
            {"message": "Successfully left society"},
            status=status.HTTP_200_OK,
        )

API view to allow a user to leave a society.
Sets the `left_at` timestamp on the membership record instead of deleting it.

