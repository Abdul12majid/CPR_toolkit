from django.contrib import admin
from .models import CalendarEvent, Student, Schedule_App_Member

# Register your models here.
admin.site.register(CalendarEvent)
admin.site.register(Student)
admin.site.register(Schedule_App_Member)