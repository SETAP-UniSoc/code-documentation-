Society Profile Page
====================

Overview
--------

The **Society Profile Page** displays detailed information about a specific society,
including its description, upcoming events, and membership options. The page
behavior differs based on the user's role (admin vs regular user) and whether the
user is a member of the society.

This page serves as the main interface for users to interact with a society,
allowing them to join/leave, attend events, and for admins to manage society
content.

Features
--------

- Display society logo, name, category, and description
- View upcoming events in a horizontal carousel
- Join or leave the society (regular users only)
- Attend or leave events (regular users only)
- Edit society description (admin only for their own society)
- Manage events via calendar icon (admin only for their own society)
- Real-time capacity tracking with progress bar
- Automatic polling for event updates (regular users)

Widget Structure
----------------

.. code-block:: dart

   SocietyProfilePage (StatefulWidget)
   ├── loadData()
   │   ├── loadSociety()
   │   ├── loadEvents()
   │   └── checkMembership() [regular users only]
   ├── checkEventAttendance() [regular users only]
   ├── toggleEventAttendance()
   ├── toggleJoinSociety()
   ├── saveDescription() [admin only]
   └── build()
       ├── Society header (logo, name, category)
       ├── About section (with edit button for admin)
       ├── Join/Leave button [regular users only]
       └── Upcoming Events carousel

State Variables
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Variable
     - Type
     - Description
   * - ``societyData``
     - Map
     - Society details (name, description, category, image_url)
   * - ``events``
     - List
     - Upcoming events for the society
   * - ``attendingStatus``
     - Map<int, bool>
     - Tracks whether user is attending each event
   * - ``isLoading``
     - bool
     - Controls loading indicator visibility
   * - ``isEditing``
     - bool
     - Toggles description edit mode (admin only)
   * - ``isMember``
     - bool
     - Indicates if user is a society member
   * - ``descController``
     - TextEditingController
     - Controls description text field
   * - ``pollingTimer``
     - Timer?
     - Periodic timer for event updates (regular users only)

Parameter Reference
-------------------

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - Parameter
     - Type
     - Description
   * - ``societyId``
     - int
     - Unique identifier of the society
   * - ``isAdmin``
     - bool
     - True if user is an administrator
   * - ``isOwnSociety``
     - bool
     - True if this is the admin's own society
   * - ``httpClient``
     - http.Client?
     - Optional client for dependency injection (testing)

Initialisation
--------------

When the page loads, three parallel operations occur:

.. code-block:: dart

   Future<void> loadData() async {
     await Future.wait([
       loadSociety(),
       loadEvents(),
       if (!widget.isAdmin) checkMembership(),
     ]);
     setState(() => isLoading = false);
   }

**Behaviour:**
- Society details are fetched from the backend
- Events for the society are fetched
- Membership status is checked (regular users only)
- Loading indicator shown until all requests complete
- For regular users, a 5-second polling timer updates events

---

Endpoint Selection
------------------

The page uses different endpoints based on user role:

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - User Role
     - Endpoint
   * - Admin
     - ``/societies/{id}/admin/``
   * - Regular User
     - ``/societies/{id}/``

Role-Based Views
----------------

### Admin View (Own Society)

When an admin views their own society (``isOwnSociety = true``):

- **Edit button** appears next to "About" section
- **Calendar icon** appears in AppBar to manage events
- **No Join/Leave button**
- **No Attend button** on events

### Admin View (Other Society)

When an admin views another society (``isOwnSociety = false``):

- **No edit button**
- **No calendar icon**
- **No Join/Leave button**
- **No Attend button** on events
- Read-only view

### Regular User View

When a regular user views any society (``isAdmin = false``):

- **Join/Leave button** appears below description
- **Attend/Leave button** appears on each event card
- **No edit button**
- **No calendar icon**

---

Society Details
---------------

### Society Header

Displays the society logo, name, and category:

- If ``image_url`` is provided, shows network image
- Otherwise, shows gradient placeholder with business icon
- Category chip appears if category exists

### About Section

.. code-block:: dart

   Row(
     children: [
       const Text("About"),
       if (isOwnSocietyDirect) ...[
         IconButton(
           icon: Icon(isEditing ? Icons.save : Icons.edit),
           onPressed: () { ... },
         ),
       ],
     ],
   )

**Behaviour:**
- Displays society description
- Admin can tap edit icon to modify description
- Save icon appears during editing
- Description updates via PATCH request

---

Join/Leave Society
------------------

Regular users can join or leave the society:

.. code-block:: dart

   if (!widget.isAdmin)
     SizedBox(
       width: double.infinity,
       child: ElevatedButton(
         onPressed: toggleJoinSociety,
         child: Text(isMember ? "Leave Society" : "Join Society"),
       ),
     )

**Behaviour:**
- Button shows "Join Society" when user is not a member
- Button shows "Leave Society" when user is a member
- API call to ``/society/{id}/join/`` or ``/society/{id}/leave/``
- Membership status updates after successful request

---

Upcoming Events Carousel
------------------------

Displays society events in a horizontal scrollable carousel.

**Event Card Components:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Description
   * - Title
     - Event name (bold, white text)
   * - Date
     - Formatted as day/month/year
   * - Time
     - Formatted as hour:minute
   * - Location
     - Event venue or online link
   * - Description
     - Brief event description (max 2 lines)
   * - Capacity
     - Shows limit and current attendees (if set)
   * - Progress Bar
     - Visual representation of capacity usage
   * - Attend Button
     - Green button for non-attendees, red for attendees

**Capacity Display:**

When an event has a capacity limit:

.. code-block:: dart

   Row(
     children: [
       Icon(Icons.people),
       Expanded(
         child: Text("Capacity: ${event["capacity_limit"]}"),
       ),
       Text("${currentAttendees} / ${event["capacity_limit"]}"),
     ],
   ),
   LinearProgressIndicator(
     value: currentAttendees / capacityLimit,
     color: isFull ? Colors.red : Colors.green,
   )

**Button States:**

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - State
     - Button Appearance
   * - Not attending, not full
     - Green, "Attend Event"
   * - Attending
     - Red, "Leave Event"
   * - Event full
     - Grey, "Event Full" (disabled)
   * - Event passed
     - Grey, "Event Passed" (disabled)

---

Event Attendance
----------------

Regular users can attend or leave events:

.. code-block:: dart

   Future<void> toggleEventAttendance(int eventId) async {
     final isAttending = attendingStatus[eventId] ?? false;
     final endpoint = isAttending
         ? "/events/$eventId/leave/"
         : "/events/$eventId/join/";

     final response = await client.post(...);
   }

**Behaviour:**
- Tracks attendance status locally
- Updates UI immediately on success
- Shows snackbar confirmation
- Prevents joining full or past events

---

Polling Mechanism
-----------------

For regular users, events automatically refresh every 5 seconds:

.. code-block:: dart

   void startPolling() {
     pollingTimer = Timer.periodic(const Duration(seconds: 5), (_) {
       loadEvents();
     });
   }

**Purpose:**
- Keeps event list up-to-date
- Reflects attendance changes from other users
- Updates capacity limits in real-time
- Cancelled in ``dispose()`` to prevent memory leaks

---

Description Editing (Admin Only)
--------------------------------

Admins can edit their own society's description:

.. code-block:: dart

   Future<void> saveDescription() async {
     final response = await client.patch(
       Uri.parse("${ApiService.baseUrl}/societies/${widget.societyId}/admin/"),
       body: jsonEncode({"description": descController.text}),
     );
   }

**Behaviour:**
- PATCH request to admin endpoint
- Success shows snackbar confirmation
- Edit mode closes on success
- Error shows appropriate message

---

API Endpoints
-------------

.. list-table::
   :header-rows: 1
   :widths: 40 20 40

   * - Endpoint
     - Method
     - Purpose
   * - ``/societies/{id}/``
     - GET
     - Fetch society details
   * - ``/societies/{id}/admin/``
     - GET
     - Fetch society details (admin)
   * - ``/societies/{id}/admin/``
     - PATCH
     - Update society description
   * - ``/societies/{id}/events/``
     - GET
     - Fetch society events
   * - ``/societies/{id}/check-membership/``
     - GET
     - Check user membership status
   * - ``/society/{id}/join/``
     - POST
     - Join society
   * - ``/society/{id}/leave/``
     - POST
     - Leave society
   * - ``/events/{id}/attending/``
     - GET
     - Check event attendance
   * - ``/events/{id}/join/``
     - POST
     - Attend event
   * - ``/events/{id}/leave/``
     - POST
     - Leave event

---

Error Handling
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Network failure
     - Error printed to console, loading state cleared
   * - Society not found
     - Empty state displayed
   * - No events
     - "No upcoming events yet" message
   * - Event full
     - Button disabled, "Event Full" text
   * - Already attending
     - Button shows "Leave Event"
   * - Unauthorised action
     - Redirect to login or show error message

Loading States
--------------

- **Initial page load:** CircularProgressIndicator in body
- **Event updates:** Carousel refreshes with new data
- **Description save:** Button shows loading state
- **Join/Leave society:** Button disabled during request

Dependencies
------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Package
     - Purpose
   * - ``http``
     - API requests to backend
   * - ``ApiService``
     - Centralised API configuration
   * - ``carousel_slider``
     - Horizontal event carousel
   * - ``flutter_calenders`` (AdminEventsPage)
     - Calendar widget for event management

Implementation Notes
--------------------

- The ``httpClient`` parameter allows dependency injection for testing
- Polling timer is cancelled in ``dispose()`` to prevent memory leaks
- ``isOwnSocietyDirect`` computed from ``isAdmin`` and ``societyId`` comparison
- Capacity display uses ``Expanded`` to prevent overflow
- Null-safe checks prevent crashes when data fields are missing
- ``attendingStatus`` map tracks attendance per event
- Event buttons are disabled for past events
- Join/Leave buttons only shown for regular users
- Edit/Calendar buttons only shown for admin's own society
- Bottom navigation bar only appears for admin users