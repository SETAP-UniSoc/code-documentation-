User Settings Page
==================

Overview
--------

The **User Settings API** allows authenticated users to manage their account
settings, including password, email, profile information, and notification
preferences.

This module provides secure endpoints for updating sensitive user data and
customising user-specific settings.

Endpoints
---------

.. code-block:: http

   POST  /api/change-password/
   POST  /api/change-email/
   GET   /api/user/profile/
   PATCH /api/user/profile/
   GET   /api/notifications/
   POST  /api/notifications/

**Django Routes**

.. code-block:: python

   path('change-password/', ChangePasswordView.as_view(), name='change-password')
   path('change-email/', ChangeEmailView.as_view(), name='change-email')
   path('user/profile/', UserProfileView.as_view(), name='user-profile')
   path('notifications/', NotificationView.as_view(), name='notifications')

Authentication
--------------

- **Required**: Yes
- **Access Level**: Any authenticated user

Features
--------

- Change password securely
- Update email address
- View and update profile information
- Manage notification preferences per society

---

Change Password Endpoint
-----------------------

Allows a user to update their password.

Request
~~~~~~~

.. code-block:: http

   POST /api/change-password/

.. code-block:: json

   {
     "old_password": "OldPass123!",
     "new_password": "NewPass456!"
   }

Response
~~~~~~~~

.. code-block:: json

   {
     "message": "Password changed successfully"
   }

Behaviour
~~~~~~~~~

- Verifies the current password before updating
- Updates password using Django's secure hashing

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class ChangePasswordView(APIView):

       permission_classes = [IsAuthenticated]

       def post(self, request):

           user = request.user
           old_password = request.data.get("old_password")
           new_password = request.data.get("new_password")

           if not user.check_password(old_password):
               return Response({"error": "Old password is incorrect"}, status=400)

           user.set_password(new_password)
           user.save()

           return Response({"message": "Password changed successfully"})

---

Change Email Endpoint
--------------------

Allows a user to update their email address.

Request
~~~~~~~

.. code-block:: http

   POST /api/change-email/

.. code-block:: json

   {
     "new_email": "new@example.com"
   }

Response
~~~~~~~~

.. code-block:: json

   {
     "message": "Email changed successfully"
   }

Behaviour
~~~~~~~~~

- Requires a valid new email
- Ensures email is unique across users

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class ChangeEmailView(APIView):

       permission_classes = [IsAuthenticated]

       def post(self, request):

           user = request.user
           new_email = request.data.get("new_email")

           if not new_email:
               return Response({"error": "New email is required"}, status=400)

           if User.objects.filter(email=new_email).exists():
               return Response({"error": "Email already in use"}, status=400)

           user.email = new_email
           user.save()

           return Response({"message": "Email changed successfully"})

---

User Profile Endpoint
--------------------

Retrieve and update the authenticated user's profile.

Retrieve Profile (GET)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   GET /api/user/profile/

Response:

.. code-block:: json

   {
     "id": 1,
     "first_name": "John",
     "last_name": "Doe",
     "email": "john@example.com",
     "up_number": "up1234567"
   }

Update Profile (PATCH)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   PATCH /api/user/profile/

Example Request:

.. code-block:: json

   {
     "first_name": "Jane",
     "email": "jane@example.com"
   }

Response:

.. code-block:: json

   {
     "message": "Profile updated successfully",
     "user": { ... }
   }

Behaviour
~~~~~~~~~

- Allows partial updates using ``PATCH``
- Validates email uniqueness
- Updates only provided fields

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class UserProfileView(APIView):

       permission_classes = [IsAuthenticated]

       def get(self, request):
           serializer = UserSerializer(request.user)
           return Response(serializer.data, status=status.HTTP_200_OK)

       def patch(self, request):

           user = request.user
           data = request.data

           if "first_name" in data:
               user.first_name = data["first_name"]

           if "last_name" in data:
               user.last_name = data["last_name"]

           if "email" in data:
               if User.objects.filter(email=data["email"]).exclude(id=user.id).exists():
                   return Response({"error": "Email already in use"}, status=400)
               user.email = data["email"]

           if "up_number" in data:
               user.up_number = data["up_number"]

           user.save()

           return Response({
               "message": "Profile updated successfully",
               "user": UserSerializer(user).data
           }, status=status.HTTP_200_OK)

---

Notification Preferences Endpoint
--------------------------------

Retrieve and update notification preferences for societies.

Retrieve Preferences (GET)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   GET /api/notifications/

Response:

.. code-block:: json

   [
     {
       "society": "Music Society",
       "notify_new_events": true
     }
   ]

Update Preferences (POST)
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: http

   POST /api/notifications/

Example Request:

.. code-block:: json

   {
     "society_id": 1,
     "event_notifications": true
   }

Response:

.. code-block:: json

   {
     "message": "Notification preferences updated",
     "society": "Music Society",
     "notify_new_events": true
   }

Behaviour
~~~~~~~~~

- Users can only update preferences for societies they belong to
- Uses ``update_or_create`` to simplify preference management

Implementation
~~~~~~~~~~~~~~

.. code-block:: python

   class NotificationView(APIView):

       permission_classes = [IsAuthenticated]

       def get(self, request):

           user = request.user
           preferences = NotificationPreference.objects.filter(user=user)

           data = []
           for pref in preferences:
               data.append({
                   "society": pref.society.name,
                   "notify_new_events": pref.notify_new_events,
               })

           return Response(data)

       def post(self, request):

           user = request.user
           society_id = request.data.get("society_id")

           notify_new_events = str(
               request.data.get("event_notifications")
           ).lower() == "true"

           try:
               society = Society.objects.get(id=society_id)
           except Society.DoesNotExist:
               return Response({"error": "Society not found"}, status=404)

           if not Membership.objects.filter(user=user, society=society).exists():
               return Response({"error": "Not a member of this society"}, status=403)

           pref, created = NotificationPreference.objects.update_or_create(
               user=user,
               society=society,
               defaults={
                   "notify_new_events": notify_new_events
               }
           )

           return Response({
               "message": "Notification preferences updated",
               "society": society.name,
               "notify_new_events": pref.notify_new_events
           })

---

Data Flow
---------

1. User accesses settings page
2. System retrieves current profile and preferences
3. User submits updates
4. Backend validates and applies changes
5. Updated data returned to frontend

---

Edge Cases
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Scenario
     - Behaviour
   * - Incorrect old password
     - Returns 400
   * - Email already in use
     - Returns 400
   * - Missing required fields
     - Returns 400
   * - Society not found (notifications)
     - Returns 404
   * - User not a member of society
     - Returns 403

---

Implementation Notes
-------------------

- Uses secure password hashing via ``set_password``
- Email uniqueness enforced at update
- Partial updates handled via ``PATCH``
- Notification preferences stored per society
- ``update_or_create`` simplifies database operations

---

Security Considerations
----------------------

- Password changes require current password verification
- Sensitive data is never exposed
- Access is restricted to authenticated users
- Membership validation prevents unauthorized preference changes

---

Suggested Improvements
----------------------

- Add password strength validation (same as registration)
- Implement email verification on change
- Add profile picture support
- Add notification types (email, push, SMS)
- Log account changes for auditing