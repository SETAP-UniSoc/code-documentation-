"""
Serializers for converting UNIsoc models to JSON.
"""

from unittest.mock import MagicMock

NotificationPreference = Society = User = MagicMock()
Event = Membership = MagicMock()
serializers = MagicMock()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model, returning all fields."""

    class Meta:
        model = Society
        fields = '__all__'


class SocietySerializer(serializers.ModelSerializer):
    """Serializer for the Society model, including active member count.

    :param member_count: Read-only count of active members in the society.
    :type member_count: int
    """

    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Society
        fields = '__all__'

    def get_member_count(self, obj):
        """Return the number of active members in the society.

        :param obj: The society instance.
        :return: Count of memberships where left_at is null.
        :rtype: int
        """
        return obj.membership.filter(left_at__isnull=True).count()


class EventSerializer(serializers.ModelSerializer):
    """Serializer for the Event model, including attendee count.

    :param attendee_count: Read-only count of RSVPs for the event.
    :type attendee_count: int
    """

    attendee_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'location',
            'start_time',
            'end_time',
            'capacity_limit',
            'status',
            'attendee_count',
        ]
        read_only_fields = ['id', 'status', 'attendee_count']

    def get_attendee_count(self, obj):
        """Return the number of RSVPs for this event.

        :param obj: The event instance.
        :return: Count of RSVPs.
        :rtype: int
        """
        return obj.rsvps.count()


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for the NotificationPreference model, returning all fields.

    The ``user`` and ``id`` fields are read-only.
    """

    class Meta:
        model = NotificationPreference
        fields = "__all__"
    read_only_fields = ['user', 'id']

