from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Status, Product, Pay, Delivery, Orders, OrderDetails
from rest_framework import permissions, viewsets, generics
from .serializers import CategorySerializer, StatusSerializer, ProductSerializer,  PaySerializer, DeliverySerializer, OrdersSerializer, OrderDetailsSerializer, UserSerializer
# Create your views here.
import django_filters.rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header


class GetAuthToken(viewsets.ModelViewSet):
    queryset = User.objects.all()
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
        token = str(get_authorization_header(request).decode('UTF-8'))
        user = Token.objects.get(key=token).user
        return Response({
            'token': token,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username
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

        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.data['email'],
                username=serializer.data['username'],
                password=serializer.data['password']
            )
            user.save()
            token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username
        })

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class CategoryApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StatusApiView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class ProductApiView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['category']


class PayApiView(generics.ListAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer


class DeliveryApiView(generics.ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer


class OrdersApiView(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def delete(self, request, pk=None):
        Orders.objects.all().delete()
        OrderDetails.objects.all().delete()

    def create(self, request, *args, **kwargs):
        token = str(get_authorization_header(request).decode('UTF-8'))
        user = Token.objects.get(key=token).user
        order, created = Orders.objects.get_or_create(
            user=user, delivery_id=request.data['delivery'], pay_id=request.data['pay'], 
            number=request.data['number'], total_sum=request.data['total_sum'])
        order.save()
        for detail in request.data['products']:
            orderdetails = OrderDetails.objects.get_or_create(
                order_id=order, product=Product.objects.get(pk=detail['id']), count=detail['count'])
        return Response({'ok': 'ok'})


class OrderDetailsApiView(generics.ListAPIView):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
