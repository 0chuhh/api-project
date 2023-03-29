from django.urls import include, path, re_path
from .views import CategoryApiView, GetAuthToken,Users, StatusApiView, ProductApiView,  PayApiView, DeliveryApiView, OrdersApiView, OrderDetailsApiView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'sign-up', Users)
router.register(r'orders', OrdersApiView)
router.register(r'auth-token', GetAuthToken)
urlpatterns = [
    path('products/categories/', CategoryApiView.as_view()),
    path('statuses/', StatusApiView.as_view()),
    path('products/', ProductApiView.as_view()),
    path('', include(router.urls)),
    path('pay/', PayApiView.as_view()),
    path('delivery/', DeliveryApiView.as_view()),
    path('orders/details/', OrderDetailsApiView.as_view()),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)