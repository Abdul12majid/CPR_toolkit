from rest_framework import serializers
from task_app.models import Invoice, Ebay, Task
from rely_invoice.models import RelyInvoice, Status


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'name', 'invoiced_amount', 'dispatch_no']


class EbaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebay
        fields = ['id', 'name', 'tracking_number', 'order_number', 'link', 'delivery_time']


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