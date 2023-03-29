from django.contrib import admin
from .models import Category, Status, Product, Pay, Delivery, Orders, OrderDetails

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
