User My Events Page
===================

Overview
--------

The **User My Events API** allows authenticated users to view, join, and leave events.

The endpoint adapts its behaviour based on the user role:

- **Admins** → View all events belonging to their society  
- **Regular users** → View events from societies they have joined  

Endpoints
---------

.. code-block:: http

   GET  /api/events/my/
   POST /api/events/<event_id>/join/
   POST /api/events/<event_id>/leave/

**Django Routes**

.. code-block:: python

   path('events/my/', MyEventsView.as_view(), name='my-events')
   path('events/<int:event_id>/join/', JoinEventView.as_view(), name='join-event')
   path('events/<int:event_id>/leave/', LeaveEventView.as_view(), name='leave-event')

Authentication
--------------

- **Required**: Yes
- **Access Level**: Any authenticated user

Features
--------

- View relevant events based on user role
- Join events
- Leave events
- Prevent joining past events
- Track event attendance dynamically

---

My Events Endpoint
-----------------

Retrieves events relevant to the authenticated user.

Request
~~~~~~~

.. code-block:: http

   GET /api/events/my/

Response
~~~~~~~~

.. code-block:: json

   [
     {
       "id": 1,
       "title": "Welcome Event",
       "date": "2026-05-10",
       "society": 3
     }
   ]

Behaviour
~~~~~~~~~

- If user is **admin**:
  - Returns all events for their society
- If user is **regular user**:
  - Returns events from societies they are members of
- Uses ``distinct()`` to avoid duplicate results

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class MyEventsView(APIView):

       permission_classes = [IsAuthenticated]

       def get(self, request):

           if request.user.role == "admin":
               society = Society.objects.get(admin=request.user)
               events = Event.objects.filter(society=society)
           else:
               events = Event.objects.filter(
                   society__membership__user=request.user
               ).distinct()

           serializer = EventSerializer(events, many=True)
           return Response(serializer.data)

---

Join Event Endpoint
------------------

Allows a user to join an event.

Request
~~~~~~~

.. code-block:: http

   POST /api/events/<event_id>/join/

Response
~~~~~~~~

.. code-block:: json

   {
     "message": "Joined event",
     "attendee_count": 45
   }

Behaviour
~~~~~~~~~

- Prevents joining events that have already started
- Creates a new attendance record if one does not exist
- If the user previously left:
  - Reactivates attendance
- If already attending:
  - Returns an error
- Returns updated attendee count

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class JoinEventView(APIView):

       permission_classes = [IsAuthenticated]

       def post(self, request, event_id):

           try:
               event = Event.objects.get(id=event_id)
           except Event.DoesNotExist:
               return Response({"error": "Event not found"}, status=404)

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

---

Leave Event Endpoint
-------------------

Allows a user to leave an event.

Request
~~~~~~~

.. code-block:: http

   POST /api/events/<event_id>/leave/

Response
~~~~~~~~

.. code-block:: json

   {
     "message": "Left event successfully"
   }

Behaviour
~~~~~~~~~

- Only allows leaving if the user is currently attending
- Marks attendance as inactive by setting ``left_at``
- Updates attendee count internally

Implementation
~~~~~~~~~~~~~~

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
               left_at__isnull=True
           ).count()

           return Response({"message": "Left event successfully"})

---

Data Flow
---------

1. User requests their events
2. System determines user role
3. Relevant events are retrieved
4. User joins or leaves events
5. Attendance records are updated
6. Updated data returned to frontend

---

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Event does not exist
     - Returns 404
   * - User tries to join past event
     - Returns 400
   * - User already attending
     - Returns 400
   * - User tries to leave without joining
     - Returns 400
   * - No events available
     - Returns empty list

---

Implementation Notes
-------------------

- Uses ``get_or_create`` to simplify attendance logic
- Soft delete pattern used via ``left_at`` field
- ``distinct()`` prevents duplicate events in queries
- Time-based validation ensures logical consistency

---


