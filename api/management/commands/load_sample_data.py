from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
from api.models import Product, Category
import os


class Command(BaseCommand):
    help = 'Load sample data for the bike store'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force reload data even if products already exist',
        )

    def handle(self, *args, **options):
        # Verificar si ya existen productos
        if Product.objects.exists() and not options['force']:
            self.stdout.write(
                self.style.WARNING(
                    'Los productos ya existen en la base de datos. '
                    'Usa --force para recargar los datos.'
                )
            )
            return

        # Si se usa --force, limpiar datos existentes
        if options['force']:
            self.stdout.write('Limpiando datos existentes...')
            with transaction.atomic():
                Product.objects.all().delete()
                Category.objects.all().delete()

        # Cargar datos de muestra
        try:
            self.stdout.write('Cargando datos de muestra...')
            
            # Buscar el archivo sample_products.json
            fixture_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                'sample_products.json'
            )
            
            if not os.path.exists(fixture_path):
                self.stdout.write(
                    self.style.ERROR(f'No se encontró el archivo: {fixture_path}')
                )
                return

            # Ejecutar loaddata
            call_command('loaddata', fixture_path, verbosity=2)
            
            # Verificar que se cargaron los datos
            categories_count = Category.objects.count()
            products_count = Product.objects.count()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Datos cargados exitosamente!\n'
                    f'Categorías: {categories_count}\n'
                    f'Productos: {products_count}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al cargar los datos: {str(e)}')
            )
            raise e
