from django.contrib import admin
from .models import Category, Status, Product, Cart, CartDetails, Pay, Delivery, Orders, OrderDetails

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
