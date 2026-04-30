Event Details
=============

Overview
--------

Retrieves detailed information about a specific event,
including attendance data.

Endpoint
--------

.. code-block:: python

   path('events/<int:event_id>/', EventDetailView.as_view(), name='event-detail')

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
