from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.utils.redis_client import redis_client
from api.models import Product
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user_id = request.user.id
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=404)

    # Redis key por usuario
    cart_key = f"cart:{user_id}"

    # Leer el carrito actual
    current_cart = redis_client.get(cart_key)
    if current_cart:
        cart_data = json.loads(current_cart)
    else:
        cart_data = {}

    # Actualizar o insertar producto con categoría
    cart_data[str(product_id)] = {
        "quantity": quantity,
        "category": product.category.id  # Usar el nombre de la categoría como string
    }

    # Guardar de nuevo en Redis
    redis_client.set(cart_key, json.dumps(cart_data))

    return Response({"message": "Producto agregado al carrito"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    user_id = request.user.id
    cart_key = f"cart:{user_id}"
    
    # Leer el carrito actual
    current_cart = redis_client.get(cart_key)
    if current_cart:
        cart_data = json.loads(current_cart)
        return Response(cart_data)
    else:
        return Response({})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    user_id = request.user.id
    cart_key = f"cart:{user_id}"
    product_id = request.data.get('product_id')
    
    if not product_id:
        return Response({"error": "product_id es requerido"}, status=400)
    
    # Leer el carrito actual
    current_cart = redis_client.get(cart_key)
    if current_cart:
        cart_data = json.loads(current_cart)
        
        # Remover el producto si existe
        if str(product_id) in cart_data:
            del cart_data[str(product_id)]
            
            # Guardar el carrito actualizado
            redis_client.set(cart_key, json.dumps(cart_data))
            return Response({"message": "Producto removido del carrito"})
        else:
            return Response({"error": "Producto no encontrado en el carrito"}, status=404)
    else:
        return Response({"error": "Carrito vacío"}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request):
    user_id = request.user.id
    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))
    
    if not product_id:
        return Response({"error": "product_id es requerido"}, status=400)
    
    if quantity <= 0:
        return Response({"error": "La cantidad debe ser mayor a 0"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=404)

    cart_key = f"cart:{user_id}"
    
    # Leer el carrito actual
    current_cart = redis_client.get(cart_key)
    if current_cart:
        cart_data = json.loads(current_cart)
    else:
        cart_data = {}

    # Actualizar cantidad del producto
    cart_data[str(product_id)] = {
        "quantity": quantity,
        "category": product.category.name  # Usar el nombre de la categoría como string
    }

    # Guardar de nuevo en Redis
    redis_client.set(cart_key, json.dumps(cart_data))

    return Response({"message": "Cantidad actualizada en el carrito"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    user_id = request.user.id
    cart_key = f"cart:{user_id}"
    
    # Eliminar todo el carrito
    redis_client.delete(cart_key)
    
    return Response({"message": "Carrito vaciado completamente"})