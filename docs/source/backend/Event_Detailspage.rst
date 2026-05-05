Event Details
=============

Overview
--------

The **Event Details API** retrieves comprehensive information about a specific event,
including its metadata and associated attendance data.

This endpoint is primarily used to display detailed event pages within the application.

Endpoint
--------

.. code-block:: http

   GET /api/events/<event_id>/

**Django Route**

.. code-block:: python

   path('events/<int:event_id>/', EventDetailView.as_view(), name='event-detail')

Authentication
--------------

- **Required**: Yes
- **Access Level**: Any authenticated user

Authorization Rules
~~~~~~~~~~~~~~~~~~~

- User must be authenticated
- No admin privileges required
- Access is not restricted by event ownership

Error Responses
~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Status Code
     - Description
   * - 404
     - Event not found
   * - 401
     - Authentication credentials missing or invalid

Response Structure
------------------

.. code-block:: json

   {
     "id": 1,
     "title": "Welcome Event",
     "description": "Introduction for new members",
     "date": "2026-05-10",
     "location": "Main Hall",
     "capacity_limit": 100,
     "society": 3,
     "created_by": 5
   }

Response Fields Explained
------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Field
     - Description
   * - ``id``
     - Unique identifier of the event
   * - ``title``
     - Name of the event
   * - ``description``
     - Detailed event information
   * - ``date``
     - Scheduled date of the event
   * - ``location``
     - Event location
   * - ``capacity_limit``
     - Maximum number of attendees (nullable)
   * - ``society``
     - ID of the associated society
   * - ``created_by``
     - ID of the user who created the event

Attendance Data
---------------

If included in the serializer, attendance-related fields may also be returned:

- Total number of attendees
- List of attendees (optional)
- Attendance status for the current user

(Implementation depends on ``EventSerializer`` configuration.)

Implementation
--------------

.. code-block:: python

   class EventDetailView(generics.RetrieveAPIView):

       permission_classes = [IsAuthenticated]
       queryset = Event.objects.all()
       serializer_class = EventSerializer
       lookup_field = 'id'

Description:

- Retrieves a single event using the ``id`` field
- Uses Django REST Framework's ``RetrieveAPIView``
- Returns serialized event data
- Requires authentication for access

Data Flow
---------

1. Client sends authenticated request with ``event_id``
2. System queries database for matching event
3. Serializer formats event data
4. Response returned to client

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Event does not exist
     - Returns 404
   * - User not authenticated
     - Returns 401
   * - Event has no attendees
     - Attendance fields return empty or zero values

Implementation Notes
-------------------

- Uses DRF generic view for simplicity and consistency
- Relies on ``EventSerializer`` for response structure
- Can be extended to include nested relationships (e.g. society details, attendees)

Suggested Improvements
----------------------

- Include nested society details instead of only ID
- Add attendee count directly in response
- Include user-specific attendance status (joined/not joined)
- Add caching for frequently accessed events
- Support public/private event visibility rules