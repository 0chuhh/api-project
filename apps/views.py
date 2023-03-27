from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Status, Product, Cart, CartDetails, Pay, Delivery, Orders, OrderDetails
from rest_framework import permissions, viewsets, generics
from .serializers import CategorySerializer, StatusSerializer, ProductSerializer, CartSerializer, CartDetailsSerializer, PaySerializer, DeliverySerializer, OrdersSerializer, OrderDetailsSerializer, UserSerializer
# Create your views here.
import django_filters.rest_framework
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.response import Response


class GetAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.username
        })

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
            'name': user.username
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
    
class CartApiView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def delete(self, request, pk=None):
        Cart.objects.all().delete()

    @action(detail=True, methods=['get'])
    def me(self, request, pk=None):
        self.request.session[0] = 'barr'
        sessionid = self.request.COOKIES.get('sessionid')
        current_cart, created = Cart.objects.get_or_create(guest_session_id=sessionid)
        current_cart.save()
        carts = CartDetails.objects.filter(cart_id=current_cart.id)
        total = 0
        for cart in carts:
            total += cart.count * cart.product.price
        # return Response(
        #     {'product': [dict(map(lambda kv: (kv[0], str(kv[1])), model_to_dict(cart).items())) for cart in carts],
        #      'total': total}, safe=False)
        return Response({'products':carts, 'total':total})
        
        
    
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

    