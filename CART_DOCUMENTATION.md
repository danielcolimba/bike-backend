# Documentación de las funciones del carrito mejoradas

## Funciones disponibles

### 1. `view_cart()` - Carrito básico enriquecido
**Endpoint:** `GET /api/cart/`

**Respuesta:**
```json
{
    "items": [
        {
            "id": 1,
            "name": "Bicicleta Mountain Pro",
            "image_url": "https://example.com/bike1.jpg",
            "price": "599.99",
            "quantity": 2,
            "category": "Bicicletas",
            "type": "bicycle",
            "subtotal": "1199.98"
        }
    ],
    "total_items": 1,
    "total_amount": "1199.98"
}
```

### 2. `view_cart_detailed()` - Carrito con información detallada
**Endpoint:** `GET /api/cart/detailed/`

**Respuesta:**
```json
{
    "items": [
        {
            "id": 1,
            "name": "Bicicleta Mountain Pro",
            "image_url": "https://example.com/bike1.jpg",
            "price": "599.99",
            "description": "Bicicleta de montaña profesional con marco de aluminio",
            "quantity": 2,
            "category": "Bicicletas",
            "type": "bicycle",
            "stock": 15,
            "subtotal": "1199.98",
            "bicycle_details": {
                "bike_type": "Montaña",
                "wheel_size": 26,
                "color": "Rojo",
                "material": "Aluminio",
                "weight": "12.5"
            }
        }
    ],
    "total_items": 1,
    "total_amount": "1199.98"
}
```

## Campos disponibles por producto

### Campos básicos (en ambas funciones):
- `id`: ID del producto
- `name`: Nombre del producto
- `image_url`: URL de la imagen
- `price`: Precio unitario (string)
- `quantity`: Cantidad en el carrito
- `category`: Nombre de la categoría
- `type`: Tipo de producto ('bicycle' o 'accessory')
- `subtotal`: Precio total (precio × cantidad)

### Campos adicionales (solo en `view_cart_detailed()`):
- `description`: Descripción del producto
- `stock`: Stock disponible
- `bicycle_details`: Detalles específicos de bicicletas (solo si type='bicycle')

### Campos de `bicycle_details`:
- `bike_type`: Tipo de bicicleta (ej: "Montaña", "Urbana")
- `wheel_size`: Tamaño de rueda en pulgadas
- `color`: Color de la bicicleta
- `material`: Material del marco
- `weight`: Peso en kg (puede ser null)

## Ventajas de la nueva implementación

1. **Datos completos**: Ya no necesitas hacer consultas adicionales para obtener información del producto
2. **Cálculos automáticos**: Subtotales y total general calculados en el backend
3. **Información de stock**: Puedes validar disponibilidad antes de checkout
4. **Detalles específicos**: Información adicional para bicicletas
5. **Manejo de errores**: Productos eliminados son omitidos automáticamente
6. **Dos niveles de detalle**: Básico para listados rápidos, detallado para páginas de carrito

## Ejemplo de uso en frontend

```javascript
// Carrito básico para mostrar contador
const basicCart = await viewCart();
document.getElementById('cart-count').textContent = basicCart.total_items;

// Carrito detallado para página de carrito
const detailedCart = await viewCartDetailed();
displayDetailedCart(detailedCart);
```

## Consideraciones de rendimiento

- La función básica es más rápida (menos consultas a BD)
- La función detallada incluye joins con tabla de bicicletas
- Para contadores simples, usar la función básica
- Para páginas de carrito completas, usar la función detallada
