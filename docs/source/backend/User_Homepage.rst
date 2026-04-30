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

.. code-block:: python

    class SocietyListSearchView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        query = request.query_params.get("q", "").strip()

        societies = Society.objects.filter(is_active=True)

        if query:
            societies = societies.filter(name__icontains=query)

        societies = societies.annotate(
            active_member_count=Count(
                'membership',
                filter=Q(membership__left_at__isnull=True)
            )
        ).order_by('name')

        data = [{
            "id": s.id,
            "name": s.name,
            "category": s.category,
            "description": s.description,
            "member_count": s.active_member_count,
        } for s in societies]

        return Response(data)

API view to list and search active societies.
Requires authentication. Supports an optional ``q`` query parameter to filter societies by name. Results include the active member count for each society and are ordered alphabetically by name.

Return a list of active societies, optionally filtered by name.
