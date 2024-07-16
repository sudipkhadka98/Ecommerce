from django.db import models
from django.contrib.auth.models import User


class APIKey(models.Model):
    key = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_id=models.AutoField
    image=models.ImageField(upload_to='store_images/', default="")
    product_name=models.TextField(max_length=200)
    description=models.CharField(max_length=200)
    price=models.IntegerField(default="0")
    pub_date=models.DateField()

    def __str__(self):
        return self.product_name
    
class AddToCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
