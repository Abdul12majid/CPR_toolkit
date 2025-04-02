from rest_framework import serializers
from task_app.models import Invoice, Ebay, Task, Today_order, Belle_Task, Merchant, Work_Journal
from rely_invoice.models import RelyInvoice, Status, Work_Order, RelyMessage


class InvoiceSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Invoice
        fields = ['id', 'name', 'invoiced_amount', 'dispatch_no']


class EbaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebay
        fields = ['id', 'name', 'transaction_date', 'amount', 'tracking_number', 'order_number', 'link', 'delivery_time']


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['id', 'name', 'transaction_date', 'amount', 'tracking_number', 'order_number', 'link', 'delivery_time']

class Today_orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Today_order
        fields = ['id', 'name', 'tracking_number', 'order_number', 'link']


class RelyInvoiceSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)  # Display status name
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())  # Accept status ID

    class Meta:
        model = RelyInvoice
        fields = ['id', 'dispatch_number', 'status', 'status_name', 'customer', 'note', 'amount']
        extra_kwargs = {'status': {'required': False}}  # Make status optional in request

    def create(self, validated_data):
        validated_data['status'] = Status.objects.get(id=4)  # Set default status to ID 1
        return super().create(validated_data)  


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description']


class BelleTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Belle_Task
        fields = ['id', 'description']


class WoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Order
        fields = ['id', 'customer', 'dispatch_number']


class RelyMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelyMessage
        fields = ['id', 'message']


class OrderUpdateSerializer(serializers.Serializer):
    order_number = serializers.CharField(required=True)
    tracking_number = serializers.CharField(required=False, allow_null=True)
    link = serializers.URLField(required=False, allow_null=True)
    name = serializers.CharField(required=False, allow_null=True)
    delivery_time = serializers.CharField(required=False, allow_null=True)

    def validate_order_number(self, value):
        return value


class Work_JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work_Journal
        fields = ['id', 'description']