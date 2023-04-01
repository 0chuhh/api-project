from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Status, Product, Pay, Delivery, Orders, OrderDetails
from rest_framework import permissions, viewsets, generics
from .serializers import GroupSerializer, CategorySerializer, StatusSerializer, ProductSerializer,  PaySerializer, DeliverySerializer, OrdersSerializer, OrderDetailsSerializer, UserSerializer
# Create your views here.
import django_filters.rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from .permissions import IsUser, IsManager

class GetAuthToken(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    

    def list(self, request, *args, **kwargs):
        users = User.objects.all()
        users_tokens = []
        for user in users:
            token, created = Token.objects.get_or_create(user=user)
            users_tokens.append({'username': user.username, 'user_id': user.pk,
                                 'email': user.email, 'token': token.key})
        return Response(users_tokens)

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user) 
        groups = GroupSerializer(request.user.groups.all(), many=True)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'roles': groups.data
        })

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            groups = GroupSerializer(user.groups.all(), many=True)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username,
                'roles': groups.data
            })

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class Users(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        permission_classes = permissions.IsAdminUser
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        user_group = Group.objects.get(name='user') 
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.data['email'],
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            user_group.user_set.add(user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username
            })
        return Response('error')

    


class CategoryApiView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            new_category = Category(name=serializer.data['name'], image=request.FILES.get('image'))
            new_category.save()
            category = Category.objects.get(name=serializer.data['name'])
            return Response({
                'id': category.id,
                'name': category.name,
                'image':'http://127.0.0.1:8081'+category.image.url
                
            })
        
        return Response('error')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsUser]
        if self.action == 'create':
            permission_classes = [IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

class StatusApiView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class ProductApiView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category']

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            new_product = Product(name=serializer.data['name'], description=serializer.data['description'], category_id=int(request.data['category']), price=serializer.data['price'], image=request.FILES.get('image'))
            new_product.save()
            product = Product.objects.get(name=serializer.data['name'])
            return Response({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price':product.price,
                'category':{'id':product.category.id, 'name':product.category.name, 'image':product.category.image.url},
                'image':'http://127.0.0.1:8081'+product.image.url
                
            })
        
        return Response('error')

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsUser]
        if self.action == 'create':
            permission_classes = [IsManager]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class PayApiView(generics.ListAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsUser]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]


class DeliveryApiView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsUser]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]


class OrdersApiView(viewsets.ModelViewSet):
    queryset = Orders.objects.none()
    serializer_class = OrdersSerializer
    permission_classes = [IsUser]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def delete(self, request, pk=None):
        Orders.objects.all().delete()
        OrderDetails.objects.all().delete()

    @action(detail=False, methods=['get'], permission_classes=[IsUser]) 
    def my_orders(self, request, pk=None):
        orders = Orders.objects.filter(user=request.user)
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)

    
    
    def create(self, request, *args, **kwargs):
        user = request.user
        order, created = Orders.objects.get_or_create(
            user=user, delivery_id=request.data['delivery'], pay_id=request.data['pay'], 
            number=request.data['number'], total_sum=request.data['total_sum'])
        order.save()
        for detail in request.data['products']:
            orderdetails = OrderDetails.objects.get_or_create(
                order=order, product=Product.objects.get(pk=detail['id']), count=detail['count'])
        return Response({'ok': 'ok'})

