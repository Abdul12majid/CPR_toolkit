from django.contrib import admin
from .models import Status, RelyInvoice, RelyProcessed
# Register your models here.

admin.site.register(Status)
admin.site.register(RelyInvoice)
admin.site.register(RelyProcessed)