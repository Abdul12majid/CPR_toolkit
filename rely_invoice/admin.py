from django.contrib import admin
from .models import Status, RelyInvoice, RelyProcessed, RelyCompleted, RelyMessage
from .models import RelyPaid, RelyProblem, RelyReassigned, RelyGMMM
# Register your models here.

admin.site.register(Status)
admin.site.register(RelyInvoice)
admin.site.register(RelyProcessed)
admin.site.register(RelyCompleted)
admin.site.register(RelyPaid)
admin.site.register(RelyProblem)
admin.site.register(RelyReassigned)
admin.site.register(RelyGMMM)
admin.site.register(RelyMessage)