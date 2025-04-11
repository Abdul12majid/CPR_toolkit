from rest_framework import serializers
from task_app.models import Invoice, Ebay, Task, Today_order, Belle_Task
from task_app.models import Amex, Merchant, Work_Journal, us_bank
from datetime import datetime
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

class AmexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amex
        fields = ['id', 'order_number', 'amount', 'transaction_date']

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


class USBankListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        instances = []
        for item in validated_data:
            # Create a new child serializer for each item
            serializer = self.child.__class__(data=item, context=self.child.context)
            serializer.is_valid(raise_exception=True)
            instances.append(serializer.save())
        return instances

class USBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = us_bank
        fields = ['amount', 'transaction_type', 'transaction_date']
        list_serializer_class = USBankListSerializer
    
    def validate(self, data):
        transaction_date_str = data.get('transaction_date')
        
        if transaction_date_str:
            try:
                if '(' in transaction_date_str:
                    # Format: "Thu, 03 Apr 2025 13:02:10 +0000 (UTC)"
                    date_str = transaction_date_str.split(' (')[0]
                    parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                elif '/' in transaction_date_str:
                    # Format: "03/26/2025"
                    parsed_date = datetime.strptime(transaction_date_str, '%m/%d/%Y')
                else:
                    # Format: "2025-04-03 13:02:10"
                    parsed_date = datetime.strptime(transaction_date_str, '%Y-%m-%d %H:%M:%S')
                
                data['parsed_date'] = parsed_date
            except (ValueError, AttributeError) as e:
                raise serializers.ValidationError({
                    'transaction_date': f"Invalid date format. Accepted formats: 'Thu, 03 Apr 2025...', '03/26/2025', or '2025-04-03 13:02:10'. Error: {str(e)}"
                })
        
        return data
    
    def create(self, validated_data):
        # Get the parsed date from validated_data instead of context
        parsed_date = validated_data.pop('parsed_date', None)
        instance = super().create(validated_data)
        
        if parsed_date:
            instance.date_sent = parsed_date.date()
            instance.save()
        
        return instance