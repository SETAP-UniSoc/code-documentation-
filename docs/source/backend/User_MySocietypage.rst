User My Societies Page
======================

Overview
--------

The **User My Societies API** allows authenticated users to view and manage
their society memberships.

Users can join new societies, leave existing ones, and retrieve a list of
societies they are currently part of.

Endpoints
---------

.. code-block:: http

   GET  /api/my-societies/
   POST /api/society/<society_id>/join/
   POST /api/society/<society_id>/leave/

**Django Routes**

.. code-block:: python

   path("my-societies/", MySocietiesView.as_view(), name="my-societies")
   path("society/<int:society_id>/join/", JoinSocietyView.as_view(), name="join-society")
   path("society/<int:society_id>/leave/", LeaveSocietyView.as_view(), name="leave-society")

Authentication
--------------

- **Required**: Yes
- **Access Level**: Any authenticated user

Features
--------

- View currently joined societies
- Join societies
- Leave societies
- Rejoin previously left societies
- Soft-delete memberships using timestamps

---

My Societies Endpoint
--------------------

Retrieves all societies the user is currently a member of.

Request
~~~~~~~

.. code-block:: http

   GET /api/my-societies/

Response
~~~~~~~~

.. code-block:: json

   [
     {
       "id": 1,
       "name": "Music Society",
       "category": "Cultural",
       "description": "A society for music lovers"
     }
   ]

Behaviour
~~~~~~~~~

- Returns only active memberships (``left_at IS NULL``)
- Uses ``select_related`` for efficient querying
- Returns simplified society data

Implementation
~~~~~~~~~~~~~~

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

---

Join Society Endpoint
--------------------

Allows a user to join a society.

Request
~~~~~~~

.. code-block:: http

   POST /api/society/<society_id>/join/

Response
~~~~~~~~

.. code-block:: json

   {
     "message": "Joined successfully"
   }

Behaviour
~~~~~~~~~

- Creates a new membership if none exists
- If already a member:
  - Returns ``Already joined``
- If previously left:
  - Reactivates membership
  - Updates ``joined_at`` timestamp

Implementation
~~~~~~~~~~~~~~

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

           membership.left_at = None
           membership.joined_at = timezone.now()
           membership.save()

           return Response({"message": "Rejoined successfully"}, status=200)

---

Leave Society Endpoint
---------------------

Allows a user to leave a society.

Request
~~~~~~~

.. code-block:: http

   POST /api/society/<society_id>/leave/

Response
~~~~~~~~

.. code-block:: json

   {
     "message": "Successfully left society"
   }

Behaviour
~~~~~~~~~

- Only allows leaving if the user is an active member
- Uses soft delete by setting ``left_at``
- Membership record is preserved for history

Implementation
~~~~~~~~~~~~~~

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
                   status=status.HTTP_404_NOT_FOUND
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
                   status=status.HTTP_400_BAD_REQUEST
               )

           membership.left_at = timezone.now()
           membership.save()

           return Response(
               {"message": "Successfully left society"},
               status=status.HTTP_200_OK
           )

---

Data Flow
---------

1. User requests their societies
2. System retrieves active memberships
3. User joins or leaves societies
4. Membership records are created or updated
5. Response returned to frontend

---

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Society does not exist
     - Returns 404
   * - User already joined
     - Returns message without duplication
   * - User rejoins after leaving
     - Membership reactivated
   * - User leaves without being a member
     - Returns 400
   * - No societies joined
     - Returns empty list

---

Implementation Notes
-------------------

- Uses ``get_or_create`` for efficient membership handling
- Soft delete pattern implemented via ``left_at``
- ``select_related`` improves database performance
- Prevents duplicate memberships

---

Suggested Improvements
----------------------

- Add pagination for large society lists
- Include member count in response
- Add role within society (e.g. member, admin)
- Add notifications when joining/leaving
- Prevent joining inactive societies
- Add audit logging for membership changes