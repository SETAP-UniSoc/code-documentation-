User HomePage 
==========

Overview
--------

Displays key information for the user dashboard, including recent events
and searchable societies.

Endpoint
--------

.. code-block:: http

   POST /api/login/

Authentication 
--------------

- Required 

Features
--------

- View latest events
- Search societies
- View society details

Implementation
--------------

.. code-block:: python

   class AllEventsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        events = Event.objects.select_related("society").order_by('-id')[:5]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

API view to retrieve the 5 most recently added events. 
Requires authentication. Returns events ordered by descending ID.
Returns the 5 most recent events.


