from django.contrib import admin
from .models import Status, RelyInvoice, RelyProcessed, RelyCompleted, RelyPaid, RelyProblem
# Register your models here.

admin.site.register(Status)
admin.site.register(RelyInvoice)
admin.site.register(RelyProcessed)
admin.site.register(RelyCompleted)
admin.site.register(RelyPaid)
admin.site.register(RelyProblem)