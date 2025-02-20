from django.contrib import admin
from .models import Task, Journal, Invoice

# Register your models here.
admin.site.register(Task)
admin.site.register(Journal)
admin.site.register(Invoice)