#!/bin/bash

# Script de inicio para el contenedor de producción
set -e

echo "Iniciando aplicación Django en modo producción..."

# Esperar a que PostgreSQL esté disponible
DB_HOST=${DB_HOST:-localhost}
DB_PORT=${DB_PORT:-5432}
echo "Esperando PostgreSQL en $DB_HOST:$DB_PORT..."
# Instalar netcat si no está disponible
if ! [ -x "$(command -v nc)" ]; then
  apt-get update && apt-get install -y netcat-traditional
fi
timeout=30
counter=0
while ! nc -z $DB_HOST $DB_PORT; do
  counter=$((counter+1))
  if [ $counter -gt $timeout ]; then
    echo "Timeout esperando a PostgreSQL, continuando..."
    break
  fi
  sleep 1
done
echo "PostgreSQL está disponible!"

# Esperar a que Redis esté disponible (solo si REDIS_HOST está definido)
if [ ! -z "$REDIS_HOST" ] && [ "$REDIS_HOST" != "redis" ]; then
  REDIS_PORT=${REDIS_PORT:-6379}
  echo "Esperando Redis en $REDIS_HOST:$REDIS_PORT..."
  counter=0
  while ! nc -z $REDIS_HOST $REDIS_PORT 2>/dev/null; do
    counter=$((counter+1))
    if [ $counter -gt $timeout ]; then
      echo "Timeout esperando a Redis, continuando..."
      break
    fi
    sleep 1
  done
  echo "Redis está disponible o timeout alcanzado!"
else
  echo "Saltando verificación de Redis (no está configurado o es el servicio por defecto)"
fi

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate --settings=royalbike.settings_prod

# Crear superusuario si no existe
echo "Verificando superusuario..."
python manage.py shell --settings=royalbike.settings_prod << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superusuario {username} creado')
else:
    print(f'Superusuario {username} ya existe')
EOF

# Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --settings=royalbike.settings_prod

# Iniciar el servidor con Gunicorn
echo "Iniciando servidor Gunicorn..."
exec gunicorn royalbike.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 30 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --log-level info \
    --access-logfile - \
    --error-logfile -
