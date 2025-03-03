from rest_framework import serializers
from task_app.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'name', 'invoiced_amount', 'dispatch_no']
