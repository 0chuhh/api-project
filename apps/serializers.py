from rest_framework import serializers
from .models import Category, Status, Product,Pay, Delivery, Orders, OrderDetails
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
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'category', 'description', 'image')

    
class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = '__all__'


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


        

class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderDetails
        fields = ('id', 'product', 'count')


class OrdersSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True, read_only=True)
    pay = PaySerializer(read_only=True)
    delivery = DeliverySerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    class Meta:
        model = Orders
        fields = ('id', 'address', 'delivery', 'pay', 'number', 'status','total_sum', 'order_details')