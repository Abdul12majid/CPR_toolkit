from rest_framework import serializers
from task_app.models import Invoice, Ebay


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'name', 'invoiced_amount', 'dispatch_no']


class EbaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebay
        fields = ['id', 'name', 'order_number', 'link', 'delivery_time']
