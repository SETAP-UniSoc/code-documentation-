Admin Events Management
=======================

Overview
--------

The **Admin Events Management API** מאפשר administrators to create, retrieve,
update, and delete events associated with their society.

This module ensures that only authorised admins can manage events and that all
events are correctly linked to the society they oversee.

Endpoints
---------

.. code-block:: http

   GET    /api/societies/<society_id>/events/
   POST   /api/societies/<society_id>/events/
   PUT    /api/events/<event_id>/update/
   PATCH  /api/events/<event_id>/update/
   DELETE /api/events/<event_id>/delete/

**Django Routes**

.. code-block:: python

   path('events/<int:event_id>/update/', UpdateEventView.as_view(), name='update-event')
   path('events/<int:event_id>/delete/', DeleteEventView.as_view(), name='delete-event')

Authentication
--------------

- **Required**: Yes
- **Access Level**: Admin users only

Authorization Rules
~~~~~~~~~~~~~~~~~~~

- User must have ``role = "admin"``
- Admin must own the society to create events
- Admin can only update/delete events they created

Error Responses
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status Code
     - Description
   * - 403
     - User is not authorised (not an admin)
   * - 404
     - Society or event not found
   * - 400
     - Invalid request data

Features
--------

- Create events linked to a society
- Retrieve all events for a society
- Update existing events
- Delete events
- Enforce ownership-based permissions
- Optional event capacity handling

Request Handling
----------------

Create Event (POST)
~~~~~~~~~~~~~~~~~~~

Creates a new event for a society managed by the authenticated admin.

Special Handling:
- ``capacity_limit`` values of ``0``, ``"0"``, or empty string are converted to ``null``

Example Request Body:

.. code-block:: json

   {
     "title": "Welcome Event",
     "description": "Introduction for new members",
     "date": "2026-05-10",
     "location": "Main Hall",
     "capacity_limit": 100
   }

Response (201 Created):

.. code-block:: json

   {
     "id": 1,
     "title": "Welcome Event",
     "capacity_limit": 100
   }

Retrieve Events (GET)
~~~~~~~~~~~~~~~~~~~~

Returns all events associated with a given society.

Response:

.. code-block:: json

   [
     {
       "id": 1,
       "title": "Welcome Event",
       "date": "2026-05-10"
     }
   ]

Update Event (PUT / PATCH)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates an event created by the authenticated admin.

- ``PUT`` replaces the entire resource
- ``PATCH`` updates partial fields

Delete Event (DELETE)
~~~~~~~~~~~~~~~~~~~~

Deletes an event created by the authenticated admin.

- Operation is irreversible
- Returns ``204 No Content`` on success

Response Structure
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Unique identifier for the event
   * - ``title``
     - Event name
   * - ``description``
     - Event details
   * - ``date``
     - Event date
   * - ``location``
     - Event location
   * - ``capacity_limit``
     - Maximum number of attendees (nullable)

Implementation
--------------

Society Event View
~~~~~~~~~~~~~~~~~~

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

Description:

- ``GET`` → Returns all events for a society
- ``POST`` → Creates a new event (admin only)
- Automatically links event to the admin’s society
- Sends confirmation after successful creation

Update Event View
~~~~~~~~~~~~~~~~~

.. code-block:: python

   class UpdateEventView(generics.UpdateAPIView):

       permission_classes = [IsAuthenticated]
       queryset = Event.objects.all()
       serializer_class = EventSerializer
       lookup_field = 'id'

       def get_queryset(self):
           return Event.objects.filter(created_by=self.request.user)

Description:

- Allows admins to update only their own events
- Filters queryset by ``created_by``

Delete Event View
~~~~~~~~~~~~~~~~~

.. code-block:: python

   class DeleteEventView(generics.DestroyAPIView):

       permission_classes = [IsAuthenticated]
       serializer_class = EventSerializer
       lookup_field = 'id'

       def get_queryset(self):
           return Event.objects.filter(created_by=self.request.user)

Description:

- Allows admins to delete only their own events
- Ensures ownership-based access control

Data Flow
---------

1. Admin sends request (authenticated)
2. System verifies admin role
3. System validates society ownership
4. Serializer validates input data
5. Event is created/updated/deleted
6. Response returned to client

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Non-admin user attempts action
     - Returns 403
   * - Society not found
     - Returns 404
   * - Event not found
     - Returns 404
   * - Invalid input data
     - Returns 400
   * - Capacity set to 0
     - Converted to ``null``

Implementation Notes
-------------------

- ``capacity_limit`` normalization improves data consistency
- Ownership filtering prevents unauthorized modifications
- Confirmation email/function triggered on event creation
- Querysets are scoped per user for security

Suggested Improvements
----------------------

- Add pagination for event listings
- Include event IDs in all responses (if not already)
- Add soft delete instead of permanent deletion
- Introduce event status (draft, published, cancelled)
- Add validation for date/time conflicts
- Log admin actions for audit trackingAdmin Events Management
=======================

Overview
--------

The **Admin Events Management API** מאפשר administrators to create, retrieve,
update, and delete events associated with their society.

This module ensures that only authorised admins can manage events and that all
events are correctly linked to the society they oversee.

Endpoints
---------

.. code-block:: http

   GET    /api/societies/<society_id>/events/
   POST   /api/societies/<society_id>/events/
   PUT    /api/events/<event_id>/update/
   PATCH  /api/events/<event_id>/update/
   DELETE /api/events/<event_id>/delete/

**Django Routes**

.. code-block:: python

   path('events/<int:event_id>/update/', UpdateEventView.as_view(), name='update-event')
   path('events/<int:event_id>/delete/', DeleteEventView.as_view(), name='delete-event')

Authentication
--------------

- **Required**: Yes
- **Access Level**: Admin users only

Authorization Rules
~~~~~~~~~~~~~~~~~~~

- User must have ``role = "admin"``
- Admin must own the society to create events
- Admin can only update/delete events they created

Error Responses
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status Code
     - Description
   * - 403
     - User is not authorised (not an admin)
   * - 404
     - Society or event not found
   * - 400
     - Invalid request data

Features
--------

- Create events linked to a society
- Retrieve all events for a society
- Update existing events
- Delete events
- Enforce ownership-based permissions
- Optional event capacity handling

Request Handling
----------------

Create Event (POST)
~~~~~~~~~~~~~~~~~~~

Creates a new event for a society managed by the authenticated admin.

Special Handling:
- ``capacity_limit`` values of ``0``, ``"0"``, or empty string are converted to ``null``

Example Request Body:

.. code-block:: json

   {
     "title": "Welcome Event",
     "description": "Introduction for new members",
     "date": "2026-05-10",
     "location": "Main Hall",
     "capacity_limit": 100
   }

Response (201 Created):

.. code-block:: json

   {
     "id": 1,
     "title": "Welcome Event",
     "capacity_limit": 100
   }

Retrieve Events (GET)
~~~~~~~~~~~~~~~~~~~~

Returns all events associated with a given society.

Response:

.. code-block:: json

   [
     {
       "id": 1,
       "title": "Welcome Event",
       "date": "2026-05-10"
     }
   ]

Update Event (PUT / PATCH)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates an event created by the authenticated admin.

- ``PUT`` replaces the entire resource
- ``PATCH`` updates partial fields

Delete Event (DELETE)
~~~~~~~~~~~~~~~~~~~~

Deletes an event created by the authenticated admin.

- Operation is irreversible
- Returns ``204 No Content`` on success

Response Structure
------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Unique identifier for the event
   * - ``title``
     - Event name
   * - ``description``
     - Event details
   * - ``date``
     - Event date
   * - ``location``
     - Event location
   * - ``capacity_limit``
     - Maximum number of attendees (nullable)

Implementation
--------------

Society Event View
~~~~~~~~~~~~~~~~~~

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

Description:

- ``GET`` → Returns all events for a society
- ``POST`` → Creates a new event (admin only)
- Automatically links event to the admin’s society
- Sends confirmation after successful creation

Update Event View
~~~~~~~~~~~~~~~~~

.. code-block:: python

   class UpdateEventView(generics.UpdateAPIView):

       permission_classes = [IsAuthenticated]
       queryset = Event.objects.all()
       serializer_class = EventSerializer
       lookup_field = 'id'

       def get_queryset(self):
           return Event.objects.filter(created_by=self.request.user)

Description:

- Allows admins to update only their own events
- Filters queryset by ``created_by``

Delete Event View
~~~~~~~~~~~~~~~~~

.. code-block:: python

   class DeleteEventView(generics.DestroyAPIView):

       permission_classes = [IsAuthenticated]
       serializer_class = EventSerializer
       lookup_field = 'id'

       def get_queryset(self):
           return Event.objects.filter(created_by=self.request.user)

Description:

- Allows admins to delete only their own events
- Ensures ownership-based access control

Data Flow
---------

1. Admin sends request (authenticated)
2. System verifies admin role
3. System validates society ownership
4. Serializer validates input data
5. Event is created/updated/deleted
6. Response returned to client

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Non-admin user attempts action
     - Returns 403
   * - Society not found
     - Returns 404
   * - Event not found
     - Returns 404
   * - Invalid input data
     - Returns 400
   * - Capacity set to 0
     - Converted to ``null``

Implementation Notes
-------------------

- ``capacity_limit`` normalization improves data consistency
- Ownership filtering prevents unauthorized modifications
- Confirmation email/function triggered on event creation
- Querysets are scoped per user for security

