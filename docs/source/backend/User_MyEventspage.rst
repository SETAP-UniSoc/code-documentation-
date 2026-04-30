User My Events Page
===================

Overview
--------

Allows users to view, join, and leave events.

Endpoints
---------

.. code-block:: python

   path('events/my/', MyEventsView.as_view(), name='my-events')
   path('events/<int:event_id>/join/', JoinEventView.as_view(), name='join-event')
   path('events/<int:event_id>/leave/', LeaveEventView.as_view(), name='leave-event')

Authentication
--------------

- Required

Features
--------

- View joined events
- Join events
- Leave events
- Prevent joining past events

Implementation
--------------

.. code-block:: python

   class MyEventsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return events relevant to the authenticated user.

        :param request: The HTTP request.
        :type request: Request
        :return: Serialized list of events.
        :rtype: Response
        """
        if request.user.role == "admin":
            society = Society.objects.get(admin=request.user)
            events = Event.objects.filter(society=society)
        else:
            events = Event.objects.filter(
                society__membership__user=request.user
            ).distinct()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

API view to retrieve events relevant to the authenticated user.
- For **admins**: Returns all events belonging to their managed society.
- For **regular users**: Returns all events from societies they are members of.

.. code-block:: python
   class JoinEventView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        # prevent joining past events
        if event.start_time < timezone.now():
            return Response(
                {"error": "Event has already passed"},
                status=400
            )

        attendance, created = EventAttendance.objects.get_or_create(
            user=request.user,
            event=event,
            defaults={"left_at": None}
        )

        if not created:
            if attendance.left_at is None:
                return Response({"message": "Already attending"}, status=400)
            else:
                attendance.left_at = None
                attendance.joined_at = timezone.now()
                attendance.save()

        attendee_count = EventAttendance.objects.filter(
            event=event,
            left_at__isnull=True
        ).count()

        return Response({
            "message": "Joined event",
            "attendee_count": attendee_count
        })

API view to allow a user to join an event.
Behaviour:
    - Prevents joining past events
    - Creates attendance record if not existing
    - Re-activates attendance if previously left
Returns updated attendee count.

.. code-block:: python
   class LeaveEventView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            attendance = EventAttendance.objects.get(
                user=request.user,
                event_id=event_id,
                left_at__isnull=True
            )
        except EventAttendance.DoesNotExist:
            return Response({"error": "Not attending this event"}, status=400)

        attendance.left_at = timezone.now()
        attendance.save()

        attendee_count = EventAttendance.objects.filter(
            event_id=event_id, 
            left_at__isnull=True).count()

        return Response({"message": "Left event successfully"})

API view to allow a user to leave an event.
Marks attendance as inactive by setting `left_at`.
