from django.shortcuts import render
from .models import Category, Status, Product, Cart, CartDetails, Pay, Delivery, Orders, OrderDetails
from rest_framework import permissions, viewsets, generics
from .serializers import CategorySerializer, StatusSerializer, ProductSerializer, CartSerializer, CartDetailsSerializer, PaySerializer, DeliverySerializer, OrdersSerializer, OrderDetailsSerializer
# Create your views here.


class CategoryApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    
class StatusApiView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    
class ProductApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    
class CartApiView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    
class CartDetailsApiView(generics.ListAPIView):
    queryset = CartDetails.objects.all()
    serializer_class = CartDetailsSerializer

    
class PayApiView(generics.ListAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer

    
class DeliveryApiView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    
class OrdersApiView(generics.ListAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    
class OrderDetailsApiView(generics.ListAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer

    