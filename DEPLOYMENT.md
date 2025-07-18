# Royal Bike Backend - Guía de Deployment

## Archivos de Producción Creados

### 1. Configuración Docker
- **Dockerfile**: Imagen optimizada para producción con Python 3.10
- **docker-compose.yml**: Orquestación de servicios (PostgreSQL, Redis, Django)
- **.dockerignore**: Optimización de imagen excluyendo archivos innecesarios

### 2. Configuración Django
- **royalbike/settings_prod.py**: Configuración específica para producción
- **requirements.txt**: Dependencias actualizadas con JWT, Redis, etc.

### 3. Scripts y Variables
- **entrypoint.sh**: Script de inicio con migraciones y configuración automática
- **.env.example**: Plantilla de variables de entorno

## Pasos para Deployment

### 1. Configurar Variables de Entorno
```bash
# Copiar y editar el archivo de variables
cp .env.example .env
# Editar .env con tus valores reales
```

### 2. Construir y Ejecutar
```bash
# Construir las imágenes
docker-compose build

# Ejecutar en background
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### 3. Verificar Servicios
```bash
# Ver estado de contenedores
docker-compose ps

# Acceder al backend
curl http://localhost:8000/api/products/

# Acceder al admin
# http://localhost:8000/admin/
```

## URLs Disponibles

- **API Base**: http://localhost:8000/api/
- **Admin**: http://localhost:8000/admin/
- **Token Auth**: http://localhost:8000/api/token/
- **Refresh Token**: http://localhost:8000/api/token/refresh/

## Notas de Seguridad

1. **Cambiar SECRET_KEY** en .env para producción
2. **Configurar ALLOWED_HOSTS** con tu dominio real
3. **Usar HTTPS** en producción real
4. **Cambiar passwords** por defecto

## Solución de Problemas

### Si el contenedor no inicia:
```bash
# Ver logs detallados
docker-compose logs backend

# Reiniciar servicios
docker-compose restart
```

### Si hay problemas de base de datos:
```bash
# Ejecutar migraciones manualmente
docker-compose exec backend python manage.py migrate --settings=royalbike.settings_prod
```

### Para desarrollo local:
```bash
# Usar configuración de desarrollo
python manage.py runserver --settings=royalbike.settings
```
