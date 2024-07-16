from django.contrib import admin
from .models import Product, Category, AddToCart

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(AddToCart)


