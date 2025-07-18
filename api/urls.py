from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductListAPIView, TopSellingBicyclesAPIView, TopDiscountedGearAPIView, BuyCheckoutView, UserCreditView, DebugCheckoutView, DebugTokenView, HealthCheckView, LoginView
from api.utils import cart_views

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('login/', LoginView.as_view(), name='login'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('top-bicycles/', TopSellingBicyclesAPIView.as_view(), name='top-bicycles'),
    path('gear-discounts/', TopDiscountedGearAPIView.as_view(), name='gear-discounts'),
    path('buy/checkout/', BuyCheckoutView.as_view(), name='buy-checkout'),
    path('buy/debug/', DebugCheckoutView.as_view(), name='debug-checkout'),
    path('debug/token/', DebugTokenView.as_view(), name='debug-token'),
    path('user/credit/', UserCreditView.as_view(), name='user-credit'),
    path('cart/view/', cart_views.view_cart),
    path('cart/detailed/', cart_views.view_cart_detailed),
    path('cart/add/', cart_views.add_to_cart),
    path('cart/remove/', cart_views.remove_from_cart),
    path('cart/update/', cart_views.update_cart_quantity),
    path('cart/clear/', cart_views.clear_cart),
    # path('', include(router.urls)),
]