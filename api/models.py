from django.contrib.auth.models import AbstractUser, User
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    
    def __str__(self):
        return f"{self.user.username} - Credit: ${self.credit}"


class Category(models.Model):
    name = models.CharField(max_length=50)

class Product(models.Model):
    PRODUCT_TYPES = [
        ('bicycle', 'Bicycle'),
        ('accessory', 'Accessory'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    stock = models.IntegerField(default=0)
    type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    discount = models.IntegerField(default=0)

class Bicycle(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    bike_type = models.CharField(max_length=50)  # montaña, urbana, etc.
    wheel_size = models.IntegerField()
    color = models.CharField(max_length=50)
    material = models.CharField(max_length=50)  # e.g., Aluminum, Carbon Fiber
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True )  # in kg    

class BicycleSale(models.Model):
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    sale_date = models.DateTimeField(auto_now_add=True)