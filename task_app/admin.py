from django.contrib import admin
from .models import Task, Journal, Invoice, Merchant, Work_Journal
from .models import Marvin_Task, Belle_Task, Ebay, Today_order

# Register your models here.
admin.site.register(Task)
admin.site.register(Marvin_Task)
admin.site.register(Belle_Task)
admin.site.register(Journal)
admin.site.register(Invoice)
admin.site.register(Ebay)
admin.site.register(Today_order)
admin.site.register(Merchant)
admin.site.register(Work_Journal)