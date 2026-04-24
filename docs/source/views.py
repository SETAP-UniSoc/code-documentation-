# from flask import request
# from rest_framework import generics
# from .models import User, Event, Society
# from .serializer import UserSerializer
# from .serializer import SocietySerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import status
# from rest_framework.exceptions import PermissionDenied
# from .serializer import EventSerializer
# from .import serializer
# from django.utils.timezone import now
# from django.db.models import Count, Q
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.core.mail import send_mail
# from django.utils import timezone
# from datetime import timedelta

# from .models import NotificationPreference, Society, Membership, Event


# class UserListView(generics.ListAPIView):
#     serializer_class = UserSerializer

#     def get_queryset(self):
#         queryset = User.objects.all().order_by('name')

#         search = self.request.query_params.get('search')
#         letter = self.request.query_params.get('letter')

#         if search:
#             queryset = queryset.filter(name__icontains=search)

#         if letter:
#             queryset = queryset.filter(name__istartswith=letter)

#         return queryset
    
# # class SocietyListView(generics.ListAPIView):
# #     queryset = Society.objects.all().order_by('name')
# #     serializer_class = SocietySerializer

# class SocietyListSearchView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         query = request.query_params.get("q", "").strip()

#         societies = Society.objects.filter(is_active=True)

#         if query:
#             societies = societies.filter(name__icontains=query)

#         societies = societies.annotate(
#             active_member_count=Count(
#                 'membership',
#                 filter=Q(membership__left_at__isnull=True)
#             )
#         ).order_by('name')

#         data = [{
#             "id": s.id,
#             "name": s.name,
#             "category": s.category,
#             "description": s.description,
#             "member_count": s.active_member_count,  # ✅ fixed
#         } for s in societies]

#         return Response(data)

# class AddEventView(generics.CreateAPIView):
#     serializer_class = EventSerializer
#     permission_classes = [IsAuthenticated]

#     def perform_create(self, serializer):
#         if self.request.user.role != "admin":
#             raise PermissionDenied("Admins only")

#         society = Society.objects.get(admin=self.request.user)

#         serializer.save(
#             created_by=self.request.user,
#             society=society
#         )

# class DeleteEventView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EventSerializer
#     lookup_field = 'id'

#     def get_queryset(self):
#         return Event.objects.filter(created_by=self.request.user)
        

# # class CreateEventView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def post(self, request):

# #         if request.user.role != "admin":
# #             return Response({"error": "Admins only"}, status=403)

# #         try:
# #             society = Society.objects.get(admin=request.user)
# #         except Society.DoesNotExist:
# #             return Response({"error": "No society found"}, status=404)

# #         data = request.data.copy()
# #         data["society"] = society.id
# #         data["created_by"] = request.user.id

# #         serializer = EventSerializer(data=data)

# #         if serializer.is_valid():
# #             event = serializer.save()   # capture the event

# #             send_event_confirmation(request.user, event)

# #             return Response(serializer.data, status=201)

# #         return Response(serializer.errors, status=400)


# # class CreateEventView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def post(self, request):

# #         if request.user.role != "admin":
# #             return Response({"error": "Admins only"}, status=403)

# #         try:
# #             society = Society.objects.get(admin=request.user)
# #         except Society.DoesNotExist:
# #             return Response({"error": "No society found"}, status=404)

# #         data = request.data.copy()

# #         # 🔥 FIX capacity issue
# #         if data.get("capacity_limit") in [0, "0", ""]:
# #             data["capacity_limit"] = None

# #         serializer = EventSerializer(data=data)

# #         if serializer.is_valid():
# #             event = serializer.save(
# #                 society=society,            # ✅ FIXES NULL ERROR
# #                 created_by=request.user     # ✅ GOOD PRACTICE
# #             )

# #             send_event_confirmation(request.user, event)

# #             return Response(serializer.data, status=201)

# #         print(serializer.errors)  # DEBUG
# #         return Response(serializer.errors, status=400)
    
# class SocietyEventView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, society_id):

#         try:
#             society = Society.objects.get(id=society_id)
#         except Society.DoesNotExist:
#             return Response({"error": "Society not found"}, status=404)

#         events = Event.objects.filter(society=society)
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, society_id):
#         if request.user.role != "admin":
#             return Response({"error": "Admins only"}, status=403)

#         try:
#             society = Society.objects.get(id=society_id, admin=request.user)
#         except Society.DoesNotExist:
#             return Response({"error": "Society not found or not admin"}, status=404)

#         data = request.data.copy()

#         # ✅ Fix capacity issue
#         if data.get("capacity_limit") in [0, "0", ""]:
#             data["capacity_limit"] = None

#         serializer = EventSerializer(data=data)

#         if serializer.is_valid():
#             # 🔥 THIS IS THE FIX
#             event = serializer.save(
#                 society=society,
#                 created_by=request.user
#             )

#             send_event_confirmation(request.user, event)

#             return Response(serializer.data, status=201)

#         print("❌ ERRORS:", serializer.errors)
#         return Response(serializer.errors, status=400)

# class EventDetailView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     lookup_field = 'id'

# class UpdateEventView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     lookup_field = 'id'

#     def get_queryset(self):
#         return Event.objects.filter(created_by=self.request.user)
    
# class MyEventsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         if request.user.role == "admin":
#             society = Society.objects.get(admin=request.user)
#             events = Event.objects.filter(society=society)
#         else:
#             events = Event.objects.filter(
#                 society__membership__user=request.user
#             ).distinct()

#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)

# class AllEventsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         events = Event.objects.all().order_by('-id')[:5]  

#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)

#     # def get(self, request):
#     #     events = Event.objects.all().order_by('-created_at')[:5]
#     #     # events = Event.objects.filter(
#     #     #     start_time__gte=now()   # ✅ ONLY FUTURE EVENTS
#     #     # ).order_by('start_time')[:5]  # ✅ SOONEST FIRST

#     #     serializer = EventSerializer(events, many=True)
#     #     return Response(serializer.data)
    
# class MyCreatedEventsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         events = Event.objects.filter(created_by=request.user).order_by('-created_at')
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
    
# class ChangePasswordView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         old_password = request.data.get("old_password")
#         new_password = request.data.get("new_password")

#         if not user.check_password(old_password):
#             return Response({"error": "Old password is incorrect"}, status=400)

#         user.set_password(new_password)
#         user.save()
#         return Response({"message": "Password changed successfully"})
    
# class ChangeEmailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         new_email = request.data.get("new_email")

#         if not new_email:
#             return Response({"error": "New email is required"}, status=400)

#         if User.objects.filter(email=new_email).exists():
#             return Response({"error": "Email already in use"}, status=400)

#         user.email = new_email
#         user.save()
#         return Response({"message": "Email changed successfully"})
    
# class User_ProfileView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(user)
    
#         return Response(serializer.data)    

#     def post(self, request):
#         user = request.user
#         new_name = request.data.get("name")

#         if not new_name:
#             return Response({"error": "New name is required"}, status=400)

#         user.name = new_name
#         user.save()
#         return Response({"message": "Name changed successfully"})

    
# class NotificationView(APIView):
#     permission_classes = [IsAuthenticated]

#     # GET USER PREFERENCES
#     def get(self, request):
#         user = request.user
#         preferences = NotificationPreference.objects.filter(user=user)

#         data = []
#         for pref in preferences:
#             data.append({
#                 "society": pref.society.name,
#                 "notify_new_events": pref.notify_new_events,  # ✅ FIXED
#             })

#         return Response(data)

#     # UPDATE PREFERENCES 
#     def post(self, request):
#         user = request.user
#         society_id = request.data.get("society_id")

#         # safer boolean handling
#         notify_new_events = str(request.data.get("event_notifications")).lower() == "true"

#         try:
#             society = Society.objects.get(id=society_id)
#         except Society.DoesNotExist:
#             return Response({"error": "Society not found"}, status=404)

#         if not Membership.objects.filter(user=user, society=society).exists():
#             return Response({"error": "Not a member of this society"}, status=403)

#         pref, created = NotificationPreference.objects.update_or_create(
#             user=user,
#             society=society,
#             defaults={
#                 "notify_new_events": notify_new_events
#             }
#         )

#         return Response({
#             "message": "Notification preferences updated",
#             "society": society.name,
#             "notify_new_events": pref.notify_new_events
#         })


# # def send_event_confirmation(user, event):
# #     if not NotificationPreference.objects.filter(
# #         user=user,
# #         society=event.society,
# #         notify_new_events=True
# #     ).exists():
# #         return

# #     send_mail(
# #         subject="Event Created Successfully",
# #         message=f"""
# # Your event "{event.title}" has been created successfully.

# # Date: {event.start_time}
# # Location: {event.location}
# # """,
# #         from_email=None,
# #         recipient_list=[user.email],
# #         fail_silently=False,
# #     )

# def send_event_confirmation(admin_user, event):
#     """
#     Send emails to all users in the society who have opted in for new event notifications.
#     """
#     # Get all NotificationPreferences for the society where users want new event emails
#     prefs = NotificationPreference.objects.filter(
#         society=event.society,
#         notify_new_events=True
#     )

#     # Collect user emails
#     recipient_emails = [pref.user.email for pref in prefs if pref.user.email]

#     if not recipient_emails:
#         return  # No one to notify

#     subject = f"New Event: {event.title}"
#     message = f"""
#     Hello,

#     A new event has been created in your society: {event.society.name}

#     Title: {event.title}
#     Description: {event.description}
#     Start: {event.start_time}
#     End: {event.end_time}

#     Please check the portal for more details.
#     """

#     send_mail(
#         subject=subject,
#         message=message,
#         from_email="no-reply@yoursite.com",  # replace with your from email
#         recipient_list=recipient_emails,
#         fail_silently=False,
#     )


# def send_event_reminders():
#     now = timezone.now()
#     upcoming = now + timedelta(hours=24)

#     events = Event.objects.filter(start_time__range=(now, upcoming))

#     for event in events:
#         admins = Membership.objects.filter(
#             society=event.society,
#             role="admin"
#         )

#         for member in admins:
#             user = member.user

#             if not NotificationPreference.objects.filter(
#                 user=user,
#                 society=event.society,
#                 notify_24hr_reminder=True
#             ).exists():
#                 continue

#             send_mail(
#                 subject="Reminder: Event in 24 Hours",
#                 message=f"""
# Reminder: "{event.title}" is in 24 hours.

# Date: {event.start_time}
# Location: {event.location}
# """,
#                 from_email=None,
#                 recipient_list=[user.email],
#                 fail_silently=False,
#             )


###################################################################################
# CODE DOCUMENTATION VIEWS BELOW 
###################################################################################


from rest_framework.authtoken.models import Token
from rest_framework import generics
from .models import EventAttendance, User, Event, Society
from .serializer import UserSerializer
from .serializer import SocietySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .serializer import EventSerializer
from .import serializer
from django.utils.timezone import now
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
import re

from .models import NotificationPreference, Society, Membership, Event


class UserListView(generics.ListAPIView):
    """API view to list all users, with optional search and letter filtering.

    Supports the following query parameters:

    - ``search``: Filter users whose name contains the search string (case-insensitive).
    - ``letter``: Filter users whose name starts with the given letter (case-insensitive).

    Results are ordered alphabetically by name.
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        """Return a filtered and ordered queryset of all users.

        :return: Queryset of User objects filtered by search/letter params.
        :rtype: QuerySet
        """
        queryset = User.objects.all().order_by('name')

        search = self.request.query_params.get('search')
        letter = self.request.query_params.get('letter')

        if search:
            queryset = queryset.filter(name__icontains=search)

        if letter:
            queryset = queryset.filter(name__istartswith=letter)

        return queryset


class SocietyListSearchView(APIView):
    """API view to list and search active societies.

    Requires authentication. Supports an optional ``q`` query parameter
    to filter societies by name. Results include the active member count
    for each society and are ordered alphabetically by name.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return a list of active societies, optionally filtered by name.

        :param request: The HTTP request, optionally containing a ``q`` query param.
        :type request: Request
        :return: A list of society objects with id, name, category, description, and member count.
        :rtype: Response
        """
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


class AddEventView(generics.CreateAPIView):
    """API view to create a new event for the authenticated admin's society.

    Requires authentication. Only users with the ``admin`` role can create events.
    The event is automatically linked to the society managed by the authenticated admin.

    :raises PermissionDenied: If the authenticated user is not an admin.
    """

    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Save the new event, associating it with the admin's society.

        :param serializer: The validated event serializer instance.
        :type serializer: EventSerializer
        :raises PermissionDenied: If the user does not have the admin role.
        """
        if self.request.user.role != "admin":
            raise PermissionDenied("Admins only")

        society = Society.objects.get(admin=self.request.user)

        serializer.save(
            created_by=self.request.user,
            society=society
        )


class DeleteEventView(generics.DestroyAPIView):
    """API view to delete an event created by the authenticated user.

    Requires authentication. Users can only delete events they created themselves.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Return only events created by the authenticated user.

        :return: Queryset of Event objects created by the current user.
        :rtype: QuerySet
        """
        return Event.objects.filter(created_by=self.request.user)


class SocietyEventView(APIView):
    """API view to retrieve or create events for a specific society.

    Requires authentication.

    - ``GET``: Returns all events belonging to the given society.
    - ``POST``: Allows an admin of the society to create a new event.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, society_id):
        """Return all events for the specified society.

        :param request: The HTTP request.
        :type request: Request
        :param society_id: The ID of the society to fetch events for.
        :type society_id: int
        :return: Serialized list of events, or 404 if society not found.
        :rtype: Response
        """
        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response({"error": "Society not found"}, status=404)

        events = Event.objects.filter(society=society)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request, society_id):
        """Create a new event for the specified society.

        Only the admin of the society can create events.

        :param request: The HTTP request containing event data.
        :type request: Request
        :param society_id: The ID of the society to add the event to.
        :type society_id: int
        :return: Serialized event data on success, or an error response.
        :rtype: Response
        """
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


class EventDetailView(generics.RetrieveAPIView):
    """API view to retrieve details of a single event by ID.

    Requires authentication. Looks up the event using the ``id`` field.
    """

    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'


class UpdateEventView(generics.UpdateAPIView):
    """API view to update an event created by the authenticated user.

    Requires authentication. Users can only update events they created themselves.
    Looks up the event using the ``id`` field.
    """

    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'id'

    def get_queryset(self):
        """Return only events created by the authenticated user.

        :return: Queryset of Event objects created by the current user.
        :rtype: QuerySet
        """
        return Event.objects.filter(created_by=self.request.user)


class MyEventsView(APIView):
    """API view to retrieve events relevant to the authenticated user.

    Requires authentication.

    - For **admins**: Returns all events belonging to their managed society.
    - For **regular users**: Returns all events from societies they are members of.
    """

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


class AllEventsView(APIView):
    """API view to retrieve the 5 most recently added events.

    Requires authentication. Returns events ordered by descending ID.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the 5 most recent events.

        :param request: The HTTP request.
        :type request: Request
        :return: Serialized list of up to 5 events.
        :rtype: Response
        """
        events = Event.objects.all().order_by('-id')[:5]
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class MyCreatedEventsView(APIView):
    """API view to retrieve all events created by the authenticated user.

    Requires authentication. Results are ordered by most recently created first.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return all events created by the authenticated user.

        :param request: The HTTP request.
        :type request: Request
        :return: Serialized list of events created by the user.
        :rtype: Response
        """
        events = Event.objects.filter(created_by=request.user).order_by('-created_at')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    """API view to allow an authenticated user to change their password.

    Requires authentication. The user must provide their current password
    to verify their identity before setting a new one.
    """

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


class ChangeEmailView(APIView):
    """API view to allow an authenticated user to change their email address.

    Requires authentication. The new email must not already be in use by another account.
    """

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


class User_ProfileView(APIView):
    """API view to retrieve or update the authenticated user's profile.

    Requires authentication.

    - ``GET``: Returns the current user's profile data.
    - ``POST``: Updates the current user's display name.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the authenticated user's profile.

        :param request: The HTTP request.
        :type request: Request
        :return: Serialized user profile data.
        :rtype: Response
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request):
        """Update the authenticated user's display name.

        :param request: The HTTP request containing ``name``.
        :type request: Request
        :return: Success message, or 400 if the name is missing.
        :rtype: Response
        """
        user = request.user
        new_name = request.data.get("name")

        if not new_name:
            return Response({"error": "New name is required"}, status=400)

        user.name = new_name
        user.save()
        return Response({"message": "Name changed successfully"})


class NotificationView(APIView):
    """API view to retrieve or update the authenticated user's notification preferences.

    Requires authentication.

    - ``GET``: Returns the user's notification preferences for each society they belong to.
    - ``POST``: Updates the notification preference for a specific society.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return the authenticated user's notification preferences.

        :param request: The HTTP request.
        :type request: Request
        :return: List of societies and their notification settings for the user.
        :rtype: Response
        """
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
        """Update the authenticated user's notification preference for a society.

        :param request: The HTTP request containing ``society_id`` and ``event_notifications``.
        :type request: Request
        :return: Updated preference data, or an error if the society is not found or user is not a member.
        :rtype: Response
        """
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


def send_event_confirmation(admin_user, event):
    """Send a new event notification email to all opted-in society members.

    Finds all members of the event's society who have enabled new event
    notifications and sends them an email with the event details.

    :param admin_user: The admin user who created the event.
    :type admin_user: User
    :param event: The newly created event to notify members about.
    :type event: Event
    """
    prefs = NotificationPreference.objects.filter(
        society=event.society,
        notify_new_events=True
    )

    recipient_emails = [pref.user.email for pref in prefs if pref.user.email]

    if not recipient_emails:
        return

    subject = f"New Event: {event.title}"
    message = f"""
    Hello,

    A new event has been created in your society: {event.society.name}

    Title: {event.title}
    Description: {event.description}
    Start: {event.start_time}
    End: {event.end_time}

    Please check the portal for more details.
    """

    send_mail(
        subject=subject,
        message=message,
        from_email="no-reply@yoursite.com",
        recipient_list=recipient_emails,
        fail_silently=False,
    )


def send_event_reminders():
    """Send 24-hour reminder emails to admin members of upcoming events.

    Queries all events starting within the next 24 hours and sends reminder
    emails to admin members of each event's society who have opted in to
    24-hour reminders via their notification preferences.
    """
    now = timezone.now()
    upcoming = now + timedelta(hours=24)

    events = Event.objects.filter(start_time__range=(now, upcoming))

    for event in events:
        admins = Membership.objects.filter(
            society=event.society,
            role="admin"
        )

        for member in admins:
            user = member.user

            if not NotificationPreference.objects.filter(
                user=user,
                society=event.society,
                notify_24hr_reminder=True
            ).exists():
                continue

            send_mail(
                subject="Reminder: Event in 24 Hours",
                message=f"""
Reminder: "{event.title}" is in 24 hours.

Date: {event.start_time}
Location: {event.location}
""",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

class SocietyAdminDetailView(APIView):
    """
    API view to retrieve detailed information about a society,
    including its events.

    Returns:
    - Society details
    - List of associated events

    Does not require admin privileges.
    """
    permission_classes = [IsAuthenticated]

    # GET society details — used by both admin and user society page
    def get(self, request, society_id):
        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response({"error": "Society not found"}, status=404)

        return Response({
            "id": society.id,
            "name": society.name,
            "category": society.category,
            "description": society.description,
        })

    # PATCH update society description — admin only
    def patch(self, request, society_id):
        if request.user.role != "admin":
            return Response({"error": "Admin only"}, status=403)

        try:
            society = Society.objects.get(id=society_id, admin=request.user)
        except Society.DoesNotExist:
            return Response({"error": "Society not found or not your society"}, status=404)

        description = request.data.get("description")
        if description is not None:
            society.description = description
            society.save()

        return Response({
            "id": society.id,
            "name": society.name,
            "category": society.category,
            "description": society.description,
            "message": "Society updated successfully"
        })


class SocietyMembershipCheckView(APIView):
    """
    Check if the authenticated user is an active member of a society.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, society_id):
        # Check active membership (not left)
        is_member = Membership.objects.filter(
            user=request.user,
            society_id=society_id,
            left_at__isnull=True
        ).exists()

        return Response({
            "society_id": society_id,
            "is_member": is_member
        }, status=status.HTTP_200_OK)
    
class SocietyDetailView(APIView):
    """
    Retrieve a society along with its events.
    """
    def get(self, request, society_id):
        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response({"error": "Society not found"}, status=404)

        events = Event.objects.filter(society=society)

        event_data = []
        for event in events:
            event_data.append({
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "location": event.location,
                "start_time": event.start_time,
            })

        return Response({
            "id": society.id,
            "name": society.name,
            "category": society.category,
            "description": society.description,
            "events": event_data
        })   

class RegisterView(APIView):
    '''
    API view to handle user registration.
    Accepts user details including first name, last name, email,
    university number (UP number), and password.

    Validates:
    - All required fields are provided
    - Passwords match
    - Password strength (length, uppercase, number, special character)

    Returns:
    - 201 Created on success
    - 400 Bad Request on validation failure
    '''
    def post(self, request):
        """
        Handle user registration.

        :param request: HTTP request containing user registration data
        :type request: Request
        :return: Success or error response
        :rtype: Response
        """        
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        up_number = request.data.get("up_number")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not all([first_name, last_name, email, up_number, password, confirm_password]):
            return Response(
                {"error": "All fields are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Password strength validation
        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not re.search(r"[A-Z]", password):
            return Response(
                {"error": "Password must contain at least one uppercase letter"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not re.search(r"[0-9]", password):
            return Response(
                {"error": "Password must contain at least one number"},
                status=status.HTTP_400_BAD_REQUEST
            )   

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return Response(
                {"error": "Password must contain at least one special character"},
                status=status.HTTP_400_BAD_REQUEST
         )



class LoginView(APIView):
    """
    API view to authenticate a user and return an auth token.

    Users can log in using either:
    - Email
    - University number (UP number)

    Returns:
    - Auth token and user details on success
    - 401 Unauthorized if credentials are invalid
    """
    def post(self, request):
        """
        Authenticate the user and generate a token.

        :param request: HTTP request containing login credentials
        :type request: Request
        :return: Authentication token and user info
        :rtype: Response
        """
        email = request.data.get("email")
        up_number = request.data.get("up_number")
        password = request.data.get("password")

        if not password:
            return Response({"error": "Password required"}, status=400)

        try:
            if email:
                user = User.objects.get(email__iexact=email)
            elif up_number:
                up_number = up_number.lower()
                if not up_number.startswith("up"):
                    up_number = f"up{up_number}"
                user = User.objects.get(up_number__iexact=up_number)
            else:
                return Response({"error": "Email or UP number required"}, status=400)

            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)

                society_id = None
                society_name = None

                if user.role == "admin":
                    try:
                        society = Society.objects.get(admin=user)
                        society_id = society.id
                        society_name = society.name
                    except Society.DoesNotExist:
                        pass

                return Response({
                    "token": token.key,
                    "role": user.role,
                    "email": user.email,
                    "up_number": user.up_number,
                    "society_id": society_id,      
                    "society_name": society_name   
                })

        except User.DoesNotExist:
            pass

        return Response({"error": "Invalid credentials"}, status=401)
    
class LeaveSocietyView(APIView):
    """
    API view to allow a user to leave a society.

    Sets the `left_at` timestamp on the membership record
    instead of deleting it.

    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, society_id):
        user = request.user

        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response(
                {"error": "Society not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            membership = Membership.objects.get(
                user=user,
                society=society,
                left_at__isnull=True
                
            )
        except Membership.DoesNotExist:
            return Response(
                {"error": "You are not an active member"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        membership.left_at = timezone.now()
        membership.save()

        return Response(
            {"message": "Successfully left society"},
            status=status.HTTP_200_OK,
        )
    
class LeaveEventView(APIView):
    """
    API view to allow a user to leave an event.

    Marks attendance as inactive by setting `left_at`.

    Requires authentication.
    """
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
    
class JoinSocietyView(APIView):
    """
    API view to allow a user to join a society.

    Behaviour:
    - Creates a new membership if none exists
    - Returns 'Already joined' if user is already active
    - Re-activates membership if previously left

    Requires authentication.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, society_id):
        user = request.user

        try:
            society = Society.objects.get(id=society_id)
        except Society.DoesNotExist:
            return Response(
                {"error": "Society not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        membership, created = Membership.objects.get_or_create(
            user=user,
            society=society
        )

        if created:
            return Response(
                {"message": "Joined successfully"},
                status=status.HTTP_201_CREATED
            )

        if membership.left_at is None:
            return Response({"message": "Already joined"}, status=200)

        # Rejoining
        membership.left_at = None
        membership.joined_at = timezone.now()
        membership.save()

        return Response({"message": "Rejoined successfully"}, status=200)
            
class JoinEventView(APIView):
    """
    API view to allow a user to join an event.

    Behaviour:
    - Prevents joining past events
    - Creates attendance record if not existing
    - Re-activates attendance if previously left

    Returns updated attendee count.

    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=404)

        # prevent joining past events
        if event.event_date < timezone.now():
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
    
class AnalyticsView(APIView):
    """
    API view to provide analytics for a society admin.

    Includes:
    - Membership growth over time
    - Total active members
    - Total events
    - Event attendance statistics
    - Most popular event

    Query Parameters:
    - period: 'week', 'month', '6months', 'year'

    Requires:
    - Authenticated admin user
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "admin":
            return Response({"error": "Admins only"}, status=403)

        period = request.query_params.get("period", "week")

        try:
            society = Society.objects.get(admin=request.user)
        except Society.DoesNotExist:
            return Response({"error": "Society not found"}, status=404)

        now = timezone.now()

        # Decide grouping & range
        if period == "week":
            days_range = 7
            delta = timedelta(days=1)
            label_format = "%a"  # Mon Tue Wed
        elif period == "month":
            days_range = 30
            delta = timedelta(days=1)
            label_format = "%d %b"
        elif period == "6months":
            days_range = 26
            delta = timedelta(weeks=1)
            label_format = "Week %W"
        elif period == "year":
            days_range = 12
            delta = timedelta(days=30)
            label_format = "%b"
        else:
            return Response({"error": "Invalid period"}, status=400)

        start_date = now - (delta * days_range)

        labels = []
        totals = []

        current_date = start_date

        for _ in range(days_range):

            total = Membership.objects.filter(
                society=society,
                joined_at__lte=current_date
            ).filter(
                Q(left_at__isnull=True) | Q(left_at__gt=current_date)
            ).count()

            labels.append(current_date.strftime(label_format))
            totals.append(total)

            current_date += delta

        society = Society.objects.get(admin=request.user) # gets admis society
        total_events = society.events.count() # total events in that society
        events_stats = society.events.annotate(
            attendee_count = Count(
                "eventattendance",
                filter = Q(eventattendance__left_at__isnull=True)
            )
        ).values("title", "attendee_count")

        #most popular event
        most_popular = society.events.annotate(
            attendee_count = Count(
                "eventattendance",
                filter = Q(eventattendance__left_at__isnull=True)
            )
        ).order_by("-attendee_count").values("title", "attendee_count").first()

        live_count = Membership.objects.filter(
            society=society,
            left_at__isnull=True
        ).count()

        return Response({
            "labels": labels,
            "totals": totals,
            "live_count": live_count,
            "total_events": total_events,
            "events_stats": list(events_stats),
            "most_popular": most_popular,
            "event_attendance": list(events_stats)
        })

        