from django.contrib import admin
from .models import Task, Journal, Invoice, Merchant, Work_Journal, us_bank
from .models import Marvin_Task, Belle_Task, Ebay, Today_order, Amex

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
admin.site.register(Amex)
admin.site.register(us_bank)