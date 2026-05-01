Admin Events Management
=======================

Overview
--------

Allows administrators to create, update, and delete events
for their society.

Endpoints
---------

.. code-block:: python
    path('events/<int:event_id>/update/', UpdateEventView.as_view(), name='update-event')
    path('events/<int:event_id>/delete/', DeleteEventView.as_view(), name='delete-event')


Authentication
--------------

- Required (Admin only)

Features
--------

- Create events
- Update events
- Delete events
- Associate events with a society

Implementation
--------------

.. code-block:: python

   class SocietyEventView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, society_id):
        
        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response({"error": "Society not found"}, status=404)

        events = Event.objects.filter(society=society)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, society_id):
        
        if request.user.role != "admin":
            return Response({"error": "Admins only"}, status=403)

        try:
            society = Society.objects.get(id=society_id, admin=request.user)
        except Society.DoesNotExist:
            return Response({"error": "Society not found or not admin"}, status=404)

        data = request.data.copy()

        if data.get("capacity_limit") in [0, "0", ""]:
            data["capacity_limit"] = None

        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            event = serializer.save(
                society=society,
                created_by=request.user
            )

            send_event_confirmation(request.user, event)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

API view to retrieve or create events for a specific society.
Only users with the ``admin`` role can create events.
The event is automatically linked to the society managed by the authenticated admin.
raises PermissionDenied: If the authenticated user is not an admin.
 - ``GET``: Returns all events belonging to the given society.
- ``POST``: Allows an admin of the society to create a new event.


.. code-block:: python 
   class UpdateEventView(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get_queryset(self):

        return Event.objects.filter(created_by=self.request.user)

API view to update an event created by the authenticated user.
Admins can only update events they created themselves.
Looks up the event using the ``id`` field.
    
.. code-block:: python 
   class DeleteEventView(generics.DestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get_queryset(self):
        
        return Event.objects.filter(created_by=self.request.user)

API view to delete an event created by the authenticated user.
Admins can only delete events they created themselves.
