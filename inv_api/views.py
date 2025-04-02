from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer, EbaySerializer, RelyInvoiceSerializer, WoSerializer
from .serializers import TaskSerializer, Today_orderSerializer, BelleTaskSerializer
from .serializers import Work_JournalSerializer, RelyMessageSerializer
from .serializers import OrderUpdateSerializer, MerchantSerializer
from task_app.models import Ebay
from django.utils import timezone

@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def create_invoice_api(request):
    serializer = InvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Invoice created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def create_ebay_api(request):
    serializer = EbaySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def create_merchant_api(request):
    serializer = MerchantSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def create_rely_invoice(request):
    serializer = RelyInvoiceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def create_task_api(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "task added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def today_order_api(request):
    serializer = Today_orderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "data added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def belle_task_api(request):
    serializer = BelleTaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "task added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def work_order_api(request):
    serializer = WoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "WO created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def rely_message_api(request):
    serializer = RelyMessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "message added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([])  
@permission_classes([])  
@api_view(['POST'])
def update_order_details(request):
    # Deserialize and validate the incoming data
    serializer = OrderUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    order_number = validated_data['order_number']
    
    try:
        # Find the existing order
        order = Ebay.objects.get(order_number=order_number)
        
        # Update the fields if they're provided in the request
        if 'tracking_number' in validated_data:
            order.tracking_number = validated_data['tracking_number']
        if 'link' in validated_data:
            order.link = validated_data['link']
        if 'name' in validated_data:
            order.name = validated_data['name']
        if 'delivery_time' in validated_data:
            order.delivery_time = validated_data['delivery_time']

        order.date_updated = timezone.now()
        
        order.save()
        
        # Return the updated order using EbaySerializer
        updated_order_serializer = EbaySerializer(order)
        return Response({
            "message": "Order updated successfully",
            "order": updated_order_serializer.data
        }, status=status.HTTP_200_OK)
    
    except Ebay.DoesNotExist:
        return Response(
            {"error": f"Order with number {order_number} not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@authentication_classes([])  
@permission_classes([])  
def work_journal_api(request):
    serializer = Work_JournalSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "update added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 