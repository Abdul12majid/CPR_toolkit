from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer, EbaySerializer, RelyInvoiceSerializer, WoSerializer
from .serializers import TaskSerializer, Today_orderSerializer, BelleTaskSerializer

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