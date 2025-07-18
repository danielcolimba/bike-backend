from django.shortcuts import render
from .models import BicycleSale, Bicycle, Product, UserProfile
from .serializers import ProductWithDetailsSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from decimal import Decimal
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

import redis
from django.http import JsonResponse

# Health check endpoint
class HealthCheckView(APIView):
    """
    Endpoint para verificar el estado de salud del servicio
    """
    def get(self, request):
        return Response({
            'status': 'healthy',
            'service': 'bike-backend',
            'version': '1.0.0'
        }, status=status.HTTP_200_OK)

# Create your views here.
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithDetailsSerializer

class TopDiscountedGearAPIView(generics.ListAPIView): #just send 3 products with discount
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
    

class BuyCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        total = request.data.get('total')
        items = request.data.get('items', [])
        
        print(f"DEBUG: Datos recibidos - Total: {total}, Items: {items}")
        
        if not items:
            return Response(
                {"error": "No se encontraron items para procesar"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not total:
            return Response(
                {"error": "Total de compra es requerido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            total_amount = Decimal(str(total))
        except (ValueError, TypeError):
            return Response(
                {"error": "Total de compra inválido"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener o crear el perfil del usuario
        user_profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'credit': Decimal('1000.00')}
        )
        
        if created:
            print(f"DEBUG: Perfil creado para usuario {user.username} con crédito inicial de $1000.00")
        
        # Verificar que el usuario tenga suficiente crédito
        if user_profile.credit < total_amount:
            return Response(
                {"error": f"Crédito insuficiente. Disponible: ${user_profile.credit}, Requerido: ${total_amount}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                created_sales = []
                
                for item in items:
                    product_id = item.get('product_id')
                    quantity = item.get('quantity')
                    
                    print(f"DEBUG: Procesando item - Product ID: {product_id}, Quantity: {quantity}")
                    
                    if not product_id or not quantity:
                        continue
                    
                    try:
                        # Buscar el producto
                        product = Product.objects.get(id=product_id)
                        
                        print(f"DEBUG: Producto encontrado - ID: {product.id}, Nombre: {product.name}, Tipo: {product.type}, Stock: {product.stock}")
                        
                        # Verificar stock disponible
                        if product.stock < quantity:
                            print(f"DEBUG: ERROR - Stock insuficiente para {product.name}. Disponible: {product.stock}, Solicitado: {quantity}")
                            return Response(
                                {"error": f"Stock insuficiente para {product.name}. Disponible: {product.stock}, Solicitado: {quantity}"}, 
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                        # Manejar diferentes tipos de productos
                        if product.type == 'bicycle':
                            # Para bicicletas, crear registro en BicycleSale
                            try:
                                bicycle = product.bicycle
                                print(f"DEBUG: Bicicleta asociada encontrada")
                                
                                sale = BicycleSale.objects.create(
                                    bicycle=bicycle,
                                    user=user,
                                    quantity=quantity
                                )
                                created_sales.append(sale)
                                print(f"DEBUG: Venta de bicicleta creada - Sale ID: {sale.id}, Producto: {product.name}")
                                
                            except Bicycle.DoesNotExist:
                                print(f"DEBUG: ERROR - No se encontró bicicleta asociada al producto {product.name}")
                                return Response(
                                    {"error": f"Bicicleta asociada al producto {product_id} no encontrada"}, 
                                    status=status.HTTP_404_NOT_FOUND
                                )
                        
                        elif product.type == 'accessory':
                            # Para accesorios, solo registramos la compra (podrías crear un modelo AccessorySale si quieres)
                            print(f"DEBUG: Procesando accesorio - {product.name}")
                            # Por ahora solo reducimos el stock, pero podrías crear un modelo separado para accesorios
                        
                        else:
                            print(f"DEBUG: ERROR - Tipo de producto no soportado: {product.type}")
                            return Response(
                                {"error": f"Tipo de producto no soportado: {product.type}"}, 
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                        # Reducir el stock para todos los tipos de productos
                        product.stock -= quantity
                        product.save()
                        
                        print(f"DEBUG: Stock actualizado para {product.name} - Nuevo stock: {product.stock}")
                        
                    except Product.DoesNotExist:
                        print(f"DEBUG: ERROR - Producto con ID {product_id} no encontrado en la base de datos")
                        return Response(
                            {"error": f"Producto con ID {product_id} no encontrado"}, 
                            status=status.HTTP_404_NOT_FOUND
                        )
                    except Exception as item_error:
                        print(f"DEBUG: ERROR - Error procesando producto {product_id}: {str(item_error)}")
                        return Response(
                            {"error": f"Error procesando producto {product_id}: {str(item_error)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )
                
                # Reducir el crédito del usuario
                user_profile.credit -= total_amount
                user_profile.save()
                
                print(f"DEBUG: Crédito actualizado - Nuevo crédito: ${user_profile.credit}")
                
                # Limpiar el carrito (opcional)
                from api.utils.redis_client import redis_client
                import json
                cart_key = f"cart:{user.id}"
                redis_client.delete(cart_key)
                
                print(f"DEBUG: Carrito limpiado para usuario {user.username}")
                
                return Response({
                    "message": "Compra realizada con éxito",
                    "bicycle_sales_created": len(created_sales),
                    "total_amount": str(total_amount),
                    "remaining_credit": str(user_profile.credit)
                }, status=status.HTTP_200_OK)
                
        except Exception as e:
            print(f"DEBUG: Error en transacción: {str(e)}")
            return Response(
                {"error": f"Error procesando la compra: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # lógica para obtener el carrito del usuario
        return Response({"msg": f"Carrito de {user.username}"})
    
class UserCreditView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Obtener o crear el perfil del usuario
        user_profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'credit': Decimal('1000.00')}
        )
        
        return Response({
            "username": user.username,
            "credit": str(user_profile.credit),
            "is_new_profile": created
        }, status=status.HTTP_200_OK)

class DebugCheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Vista de debug para ver qué datos está enviando el frontend"""
        user = request.user
        
        print(f"=== DEBUG CHECKOUT ===")
        print(f"Usuario: {user.username}")
        print(f"Headers: {dict(request.headers)}")
        print(f"Datos recibidos: {request.data}")
        print(f"Método: {request.method}")
        print(f"Content-Type: {request.content_type}")
        
        return Response({
            "debug_info": {
                "user": user.username,
                "received_data": request.data,
                "headers": dict(request.headers),
                "method": request.method,
                "content_type": request.content_type
            }
        }, status=status.HTTP_200_OK)

class DebugTokenView(APIView):
    def post(self, request):
        """Vista para debuggear tokens JWT"""
        from rest_framework_simplejwt.tokens import UntypedToken
        from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
        from django.conf import settings
        import jwt
        
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return Response({
                "error": "No se encontró token Bearer en el header",
                "auth_header": auth_header
            }, status=400)
        
        token = auth_header.split(' ')[1]
        
        debug_info = {
            "token_received": token[:20] + "..." if len(token) > 20 else token,
            "settings_secret_key": settings.SECRET_KEY[:10] + "..." if len(settings.SECRET_KEY) > 10 else settings.SECRET_KEY,
            "jwt_settings": getattr(settings, 'SIMPLE_JWT', {}),
        }
        
        try:
            # Intentar decodificar el token manualmente
            decoded = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=['HS256'],
                options={"verify_exp": False}  # No verificar expiración por ahora
            )
            debug_info["decoded_token"] = decoded
            debug_info["token_valid"] = True
            
        except jwt.InvalidTokenError as e:
            debug_info["jwt_decode_error"] = str(e)
            debug_info["token_valid"] = False
        
        try:
            # Intentar validar con rest_framework_simplejwt
            UntypedToken(token)
            debug_info["simplejwt_valid"] = True
        except (InvalidToken, TokenError) as e:
            debug_info["simplejwt_error"] = str(e)
            debug_info["simplejwt_valid"] = False
        
        return Response(debug_info, status=200)


class LoginView(APIView):
    """
    Endpoint simple de login para el frontend
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Autenticar usuario
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Generar token JWT
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'success': True,
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)