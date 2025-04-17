from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json


class Schedule_App_Member(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    total_amount = models.DecimalField(default=0.0, max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.total_amount}"


class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='events')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    is_recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.title

class Student(models.Model):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    first_field = models.CharField(max_length=200, null=True, blank=True)
    second_field = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Event(models.Model):
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_event')

    def __str__(self):
        return self.name