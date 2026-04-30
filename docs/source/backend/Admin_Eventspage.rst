Admin Events Management
=======================

Overview
--------

Allows administrators to create, update, and delete events
for their society.

Endpoints
---------

.. code-block:: http

   POST /api/events/
   PATCH /api/events/{id}/
   DELETE /api/events/{id}/

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

   class AddEventView(generics.CreateAPIView):
    """API view to create a new event for the authenticated admin's society.

    Requires authentication. Only users with the ``admin`` role can create events.
    The event is automatically linked to the society managed by the authenticated admin.

    :raises PermissionDenied: If the authenticated user is not an admin.
    """

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the new event, associating it with the admin's society.

        :param serializer: The validated event serializer instance.
        :type serializer: EventSerializer
        :raises PermissionDenied: If the user does not have the admin role.
        """
        if self.request.user.role != "admin":
            raise PermissionDenied("Admins only")

        society = Society.objects.get(admin=self.request.user)

        serializer.save(
            created_by=self.request.user,
            society=society
        )
API view to create a new event for the authenticated admin's society.
Only users with the ``admin`` role can create events.
The event is automatically linked to the society managed by the authenticated admin.
raises PermissionDenied: If the authenticated user is not an admin.

.. code-block:: python 
   class UpdateEventView(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Return only events created by the authenticated user.

        :return: Queryset of Event objects created by the current user.
        :rtype: QuerySet
        """
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
        """Return only events created by the authenticated user.

        :return: Queryset of Event objects created by the current user.
        :rtype: QuerySet
        """
        return Event.objects.filter(created_by=self.request.user)

API view to delete an event created by the authenticated user.
Admins can only delete events they created themselves.

