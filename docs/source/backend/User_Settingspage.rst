User Settings Page
==================

Overview
--------

Allows users to manage their account settings, including profile,
email, password, and notification preferences.

Endpoints
---------

.. code-block:: http

   path('change-password/', ChangePasswordView.as_view(), name='change-password')
   path('change-email/', ChangeEmailView.as_view(), name='change-email')
   GET /api/profile/
   PATCH /api/profile/
   GET /api/notifications/
   POST /api/notifications/

Authentication
--------------

- Required

Features
--------

- Change password
- Change email
- Update profile information
- Manage notification preferences

Implementation
--------------

.. code-block:: python

   class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Change the authenticated user's password.

        :param request: The HTTP request containing ``old_password`` and ``new_password``.
        :type request: Request
        :return: Success message, or 400 if the old password is incorrect.
        :rtype: Response
        """
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password changed successfully"})

API view to allow an authenticated user to change their password.
The user must provide their current password to verify their identity before setting a new one.
    
.. code-block:: python
   class ChangeEmailView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Change the authenticated user's email address.

        :param request: The HTTP request containing ``new_email``.
        :type request: Request
        :return: Success message, or 400 if the email is missing or already in use.
        :rtype: Response
        """
        user = request.user
        new_email = request.data.get("new_email")

        if not new_email:
            return Response({"error": "New email is required"}, status=400)

        if User.objects.filter(email=new_email).exists():
            return Response({"error": "Email already in use"}, status=400)

        user.email = new_email
        user.save()
        return Response({"message": "Email changed successfully"})

API view to allow an authenticated user to change their email address.
The new email must not already be in use by another account.

.. code-block:: python 
   class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user

        data = request.data

     
        if "first_name" in request.data:
            user.first_name = request.data["first_name"]

        if "last_name" in request.data:
            user.last_name = request.data["last_name"]

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

Retrieve and update the authenticated user's profile.

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

        notify_new_events = str(request.data.get("event_notifications")).lower() == "true"

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

API view to retrieve or update the authenticated user's notification preferences.

- ``GET``: Returns the user's notification preferences for each society they belong to.
- ``POST``: Updates the notification preference for a specific society.
Updates the authenticated user's notification preference for a society.

