Event Details
=============

Overview
--------

Retrieves detailed information about a specific event,
including attendance data.

Endpoint
--------

.. code-block:: http

   GET /api/events/{id}/

Authentication
--------------

- Required

Implementation
--------------

.. code-block:: python

   class EventDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

API view to retrieve details of a single event by ID.
Requires authentication. Looks up the event using the ``id`` field.
