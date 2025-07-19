#!/bin/bash

echo "=== Poblando la base de datos con productos ==="
echo "Copiando el archivo de datos al contenedor..."

# Copiar el archivo de datos al contenedor
docker cp /home/danny/Documentos/cloud_project/bike-backend/sample_products.json bike_backend:/app/

# Ejecutar el comando loaddata dentro del contenedor
echo "Cargando datos en la base de datos..."
docker exec -i bike_backend python manage.py loaddata sample_products.json

echo "=== Proceso completado ==="
echo "Los productos han sido cargados en la base de datos."
