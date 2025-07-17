"""
Comando para limpiar carritos corruptos en Redis
"""
from django.core.management.base import BaseCommand
from api.utils.redis_client import redis_client


class Command(BaseCommand):
    help = 'Limpia todos los carritos corruptos en Redis'

    def handle(self, *args, **options):
        # Buscar todas las claves de carrito
        cart_keys = redis_client.keys('cart:*')
        
        corrupted_keys = []
        fixed_keys = []
        
        for key in cart_keys:
            try:
                # Intentar obtener como string
                value = redis_client.get(key)
                if value:
                    # Si es un string válido, no hacer nada
                    import json
                    json.loads(value)
                    self.stdout.write(f"Carrito {key} está correcto")
                else:
                    # Si no es string, es hash - eliminar
                    redis_client.delete(key)
                    corrupted_keys.append(key)
                    self.stdout.write(f"Eliminado carrito corrupto: {key}")
            except Exception as e:
                # Si hay error, eliminar la clave
                redis_client.delete(key)
                corrupted_keys.append(key)
                self.stdout.write(f"Eliminado carrito corrupto: {key} - Error: {str(e)}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Proceso completado. '
                f'Carritos corruptos eliminados: {len(corrupted_keys)}'
            )
        )
