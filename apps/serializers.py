from rest_framework import serializers
from .models import Category, Status, Product, Cart, CartDetails, Pay, Delivery, Orders, OrderDetails
from django.contrib.auth.models import User

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetails
        fields = '__all__'

    
class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

