from django.shortcuts import render
from .models import BicycleSale, Bicycle, Product
from .serializers import ProductWithDetailsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated


import redis
from django.http import JsonResponse

# Create your views here.
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithDetailsSerializer

class TopDiscountedGearAPIView(generics.ListAPIView): 
    serializer_class = ProductWithDetailsSerializer
    def get_queryset(self):
        return Product.objects.filter(discount__gt=0).order_by('-discount')[:3]
    

class TopSellingBicyclesAPIView(APIView):
    def get(self, request):
        # Agrupa por bicicleta y suma las cantidades vendidas
        top_bicycles = (
            BicycleSale.objects
            .values('bicycle')  # agrupar por ID de bicicleta
            .annotate(total_sold=Sum('quantity'))  # sumar las ventas
            .order_by('-total_sold')[:3]  # top 3
        )

        # Obtener los objetos reales de Bicycle a partir de los IDs
        top_bicycle_ids = [item['bicycle'] for item in top_bicycles]
        top_bicycles_instances = Bicycle.objects.filter(product_id__in=top_bicycle_ids)

        # Serializar productos relacionados
        serializer = ProductWithDetailsSerializer(
            [b.product for b in top_bicycles_instances], many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # lógica para obtener el carrito del usuario
        return Response({"msg": f"Carrito de {user.username}"})