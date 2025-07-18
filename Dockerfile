# Multi-stage build para optimizar la imagen final
FROM python:3.10-slim as builder

# Variables de entorno para el build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema necesarias para el build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo temporal
WORKDIR /build

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# Etapa final
FROM python:3.10-slim

# Metadatos de la imagen
LABEL maintainer="Royal Bike Team"
LABEL version="1.0"
LABEL description="Royal Bike Backend API - Django REST Framework"

# Variables de entorno para producción
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=production

# Instalar dependencias del sistema para runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN addgroup --system appgroup && adduser --system --group appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar wheels desde builder e instalar
COPY --from=builder /build/wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache --find-links /wheels -r requirements.txt \
    && rm -rf /wheels

# Copiar el código de la aplicación
COPY . .

# Crear directorios necesarios y asignar permisos
RUN mkdir -p /app/static /app/media /app/logs && \
    chown -R appuser:appgroup /app

# Cambiar a usuario no-root
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["./entrypoint.sh"]
