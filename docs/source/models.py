"""
Database models for the UNIsoc application.
""" 

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  


    email = models.EmailField(unique=True)

    up_number = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        default='user'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Society(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'admin'},
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def member_count(self):
        return self.membership.filter(left_at__isnull=True).count()

    def __str__(self):
        return self.name
    
# class SocietyAdmin(models.Model):
#     ROLE_CHOICES = [
#         ('president', 'President'),
#         ('vice_president', 'Vice President'),
#         ('treasurer', 'Treasurer'),
#         ('moderator', 'Moderator'),
#     ]

#     society = models.ForeignKey(
#         Society,
#         on_delete=models.CASCADE,
#         related_name='admins'
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='admin_societies'
#     )

    # class Meta:
    #     unique_together = ('society', 'user')

    # def __str__(self):
    #     return f"{self.user.email} - {self.role}"


class Membership(models.Model):
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('admin', 'Admin'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    society = models.ForeignKey(
        Society,
        on_delete=models.CASCADE,
        related_name="membership"
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')

    class Meta:
        unique_together = ('user', 'society')

    def __str__(self):
        return f"{self.user} -> {self.society}"

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    society = models.ForeignKey(
        Society,
        on_delete=models.CASCADE,
        related_name='events'
    )

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    capacity_limit = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)]
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_events'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='upcoming'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def __str__(self):
        return self.title


class EventRSVP(models.Model):
    RSVP_CHOICES = [ 
        ('attending', 'Attending'),
        ('not_attending', 'Not Attending'),
    ]

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_rsvps'
    )

    rsvp_status = models.CharField(
        max_length=20,
        choices=RSVP_CHOICES,
        default='attending'
    )

    rsvp_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user} - {self.event}"

class NotificationPreference(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )

    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    # 👤 USER EMAIL SETTINGS
    notify_new_events = models.BooleanField(default=True)
    notify_cancellations = models.BooleanField(default=True)

    # 👑 ADMIN EMAIL SETTINGS
    notify_event_created = models.BooleanField(default=True)
    notify_24hr_reminder = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'society')

    def __str__(self):
        return f"{self.user} prefs for {self.society}"

class Message(models.Model):
    society = models.ForeignKey(
        Society,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    content = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender}"

class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action


class EventAttendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "event")

#run in terminal 
#python manage.py makemigrations
#python manage.py migrate
