from rest_framework import serializers
from django.db import models
from .models import Product, Category, Bicycle

# serializers.py
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'image_url', 'stock', 'category']

class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bicycle
        fields = ['bike_type','wheel_size','color','material','weight']

class ProductWithDetailsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    bicycle = BicycleSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'description', 'image_url',
            'stock', 'category', 'type', 'bicycle'
        ]