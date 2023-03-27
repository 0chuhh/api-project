from django.urls import include, path, re_path
from .views import CategoryApiView, GetAuthToken,Users, StatusApiView, ProductApiView, CartApiView, CartDetailsApiView, PayApiView, DeliveryApiView, OrdersApiView, OrderDetailsApiView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'cart', CartApiView)
router.register(r'sign-up', Users)
urlpatterns = [
    path('products/categories/', CategoryApiView.as_view()),
    path('cart/statuses/', StatusApiView.as_view()),
    path('products/', ProductApiView.as_view()),
    path('', include(router.urls)),
    path('cart/details/', CartDetailsApiView.as_view()),
    path('pay/', PayApiView.as_view()),
    path('delivery/', DeliveryApiView.as_view()),
    path('orders/', OrdersApiView.as_view()),
    path('orders/details/', OrderDetailsApiView.as_view()),
    path('token-auth/', GetAuthToken.as_view())
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)