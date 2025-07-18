#!/bin/bash

# Script para desarrollo y deployment del backend
# Uso: ./dev.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
IMAGE_NAME="bike-backend"
CONTAINER_NAME="bike_backend"
DOCKER_TAG="latest"

# Función para mostrar ayuda
show_help() {
    echo -e "${GREEN}🚴‍♂️ Royal Bike Backend - Script de Desarrollo${NC}"
    echo ""
    echo "Uso: ./dev.sh [comando]"
    echo ""
    echo "Comandos disponibles:"
    echo "  dev         - Iniciar servidor de desarrollo local"
    echo "  build       - Construir imagen Docker"
    echo "  run         - Ejecutar contenedor individual"
    echo "  test        - Ejecutar tests"
    echo "  migrate     - Ejecutar migraciones"
    echo "  shell       - Abrir shell de Django"
    echo "  collectstatic - Recopilar archivos estáticos"
    echo "  load-data   - Cargar datos de ejemplo"
    echo "  clean       - Limpiar cache y archivos temporales"
    echo "  push        - Subir imagen a Docker Hub"
    echo "  help        - Mostrar esta ayuda"
}

# Verificar si Python está instalado
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 no está instalado${NC}"
        exit 1
    fi
}

# Verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        exit 1
    fi
}

# Verificar variables de entorno
check_env() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  Archivo .env no encontrado${NC}"
        echo "Copiando .env.example a .env..."
        cp .env.example .env
        echo -e "${YELLOW}📝 Por favor edita .env con tus configuraciones${NC}"
    fi
}

# Función principal
main() {
    case "${1:-help}" in
        "dev"|"start")
            echo -e "${GREEN}🔥 Iniciando servidor de desarrollo...${NC}"
            check_python
            check_env
            source venv/bin/activate 2>/dev/null || {
                echo "Creando entorno virtual..."
                python3 -m venv venv
                source venv/bin/activate
                pip install -r requirements.txt
            }
            python manage.py migrate
            python manage.py runserver 0.0.0.0:8000
            ;;
        "build")
            echo -e "${GREEN}🏗️  Construyendo imagen Docker...${NC}"
            check_docker
            docker build -t $IMAGE_NAME:$DOCKER_TAG .
            echo -e "${GREEN}✅ Imagen construida: $IMAGE_NAME:$DOCKER_TAG${NC}"
            ;;
        "run")
            echo -e "${GREEN}🐳 Ejecutando contenedor...${NC}"
            check_docker
            docker run -d \
                --name $CONTAINER_NAME \
                --env-file .env \
                -p 8000:8000 \
                $IMAGE_NAME:$DOCKER_TAG
            echo -e "${GREEN}✅ Contenedor ejecutándose en http://localhost:8000${NC}"
            ;;
        "test")
            echo -e "${GREEN}🧪 Ejecutando tests...${NC}"
            check_python
            source venv/bin/activate 2>/dev/null || echo "Activando entorno virtual..."
            python manage.py test
            ;;
        "migrate")
            echo -e "${GREEN}📦 Ejecutando migraciones...${NC}"
            check_python
            source venv/bin/activate 2>/dev/null || echo "Activando entorno virtual..."
            python manage.py makemigrations
            python manage.py migrate
            ;;
        "shell")
            echo -e "${GREEN}🐚 Abriendo Django shell...${NC}"
            check_python
            source venv/bin/activate 2>/dev/null || echo "Activando entorno virtual..."
            python manage.py shell
            ;;
        "collectstatic")
            echo -e "${GREEN}📁 Recopilando archivos estáticos...${NC}"
            check_python
            source venv/bin/activate 2>/dev/null || echo "Activando entorno virtual..."
            python manage.py collectstatic --noinput
            ;;
        "load-data")
            echo -e "${GREEN}📋 Cargando datos de ejemplo...${NC}"
            check_python
            source venv/bin/activate 2>/dev/null || echo "Activando entorno virtual..."
            python manage.py load_sample_data
            ;;
        "clean")
            echo -e "${YELLOW}🧹 Limpiando cache y archivos temporales...${NC}"
            find . -name "*.pyc" -delete
            find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
            rm -rf .pytest_cache
            echo -e "${GREEN}✅ Limpieza completada${NC}"
            ;;
        "push")
            echo -e "${BLUE}📤 Subiendo imagen a Docker Hub...${NC}"
            check_docker
            read -p "Ingresa tu usuario de Docker Hub: " DOCKER_USERNAME
            docker tag $IMAGE_NAME:$DOCKER_TAG $DOCKER_USERNAME/$IMAGE_NAME:$DOCKER_TAG
            docker push $DOCKER_USERNAME/$IMAGE_NAME:$DOCKER_TAG
            echo -e "${GREEN}✅ Imagen subida: $DOCKER_USERNAME/$IMAGE_NAME:$DOCKER_TAG${NC}"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            echo -e "${RED}❌ Comando desconocido: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
