from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductListAPIView
from .views import TopSellingBicyclesAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('top-bicycles/', TopSellingBicyclesAPIView.as_view(), name='top-bicycles'),
    # path('', include(router.urls)),
]