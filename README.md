# 🚴‍♂️ Royal Bike Backend API

API backend completa para la gestión de tienda de bicicletas con autenticación JWT, carrito de compras, gestión de productos y sistema de checkout.

## 🛠️ Tecnologías Utilizadas

- **Framework:** Django 5.2.4 + Django REST Framework
- **Base de datos:** PostgreSQL 15
- **Cache/Sesiones:** Redis 7
- **Autenticación:** JWT (JSON Web Tokens)
- **Contenedores:** Docker + Docker Compose
- **Seguridad:** CORS configurado, usuario no-root
- **Monitoreo:** Health checks incluidos

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Backend API   │───▶│   PostgreSQL    │
│   (port 3000)   │    │   (port 8000)   │    │   (port 5434)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │     Redis       │
                       │   (port 6380)   │
                       └─────────────────┘
```

## 📋 Características Principales

### **API Endpoints:**
- 🛍️ **Productos:** Listado, búsqueda, categorías
- 🛒 **Carrito:** Agregar, actualizar, eliminar items
- 💳 **Checkout:** Proceso de compra completo
- 👤 **Perfil:** Gestión de usuarios y créditos
- 📊 **Analytics:** Top productos, descuentos
- 🏥 **Health Check:** Monitoreo del servicio

### **Funcionalidades:**
- ✅ Autenticación JWT integrada
- ✅ Sistema de carrito con Redis
- ✅ Gestión de stock en tiempo real
- ✅ Sistema de descuentos
- ✅ Carga de datos de ejemplo
- ✅ API documentada con DRF

## 🚀 Inicio Rápido

### **Con Docker (Recomendado):**

1. **Clonar el repositorio:**
```bash
git clone https://github.com/danielcolimba/bike-authjwt.git
cd bike-authjwt/bike-backend
```

2. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env según tus necesidades
```

3. **Levantar servicios con Docker Compose:**
```bash
docker-compose up -d
```

4. **Cargar datos de ejemplo:**
```bash
./dev.sh load-data
```

5. **Acceder a la API:**
   - API: http://localhost:8000/api/
   - Health: http://localhost:8000/api/health/
   - Admin: http://localhost:8000/admin/

### **Desarrollo Local (Sin Docker):**

1. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos:**
```bash
# Asegúrate de tener PostgreSQL ejecutándose
python manage.py migrate
```

4. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

5. **Cargar datos de ejemplo:**
```bash
python manage.py load_sample_data
```

6. **Iniciar servidor:**
```bash
python manage.py runserver 0.0.0.0:8000
```

## 🔧 Scripts de Automatización

Usa el script `dev.sh` para tareas comunes:

```bash
./dev.sh dev         # Servidor de desarrollo
./dev.sh build       # Construir imagen Docker
./dev.sh test        # Ejecutar tests
./dev.sh migrate     # Aplicar migraciones
./dev.sh load-data   # Cargar datos de ejemplo
./dev.sh clean       # Limpiar cache
./dev.sh push        # Subir a Docker Hub
./dev.sh help        # Ver todos los comandos
```

## 📡 Endpoints de la API

### **Productos:**
```http
GET    /api/products/              # Listar todos los productos
GET    /api/top-bicycles/          # Top bicicletas más vendidas
GET    /api/gear-discounts/        # Accesorios con descuento
```

### **Carrito:**
```http
GET    /api/cart/view/             # Ver carrito
POST   /api/cart/add/              # Agregar producto
PUT    /api/cart/update/           # Actualizar cantidad
DELETE /api/cart/remove/           # Eliminar producto
DELETE /api/cart/clear/            # Vaciar carrito
```

### **Compras:**
```http
POST   /api/buy/checkout/          # Procesar compra
GET    /api/user/credit/           # Ver crédito usuario
```

### **Sistema:**
```http
GET    /api/health/                # Estado del servicio
```

## 🌐 Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DEBUG` | Modo debug | `False` |
| `SECRET_KEY` | Clave secreta Django | `tu-clave-secreta` |
| `DB_HOST` | Host base de datos | `localhost` o `db` |
| `DB_NAME` | Nombre base de datos | `bikedb` |
| `DB_USER` | Usuario base de datos | `danny` |
| `DB_PASSWORD` | Contraseña BD | `royal` |
| `REDIS_HOST` | Host Redis | `localhost` o `redis` |
| `JWT_SECRET_KEY` | Clave JWT | `tu-jwt-secret` |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |

## 🐳 Docker

### **Construir imagen:**
```bash
docker build -t bike-backend:latest .
```

### **Ejecutar contenedor:**
```bash
docker run -d \
  --name bike-backend \
  --env-file .env \
  -p 8000:8000 \
  bike-backend:latest
```

### **Docker Compose completo:**
```bash
# Levantar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Parar servicios
docker-compose down
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Con coverage
coverage run --source='.' manage.py test
coverage report
```

## 📊 Monitoreo

### **Health Check:**
```bash
curl http://localhost:8000/api/health/
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "bike-backend",
  "version": "1.0.0"
}
```

### **Métricas Docker:**
```bash
# Ver estado de contenedores
docker ps

# Ver uso de recursos
docker stats bike_backend
```

## 🔒 Seguridad

- ✅ Usuario no-root en contenedor
- ✅ Variables de entorno para credenciales
- ✅ CORS configurado correctamente
- ✅ Validación de JWT tokens
- ✅ Sanitización de inputs
- ✅ Headers de seguridad

## 🚀 Deployment

### **Para Producción:**

1. **Configurar variables de entorno:**
```bash
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
SECRET_KEY=clave-super-segura
```

2. **Usar imagen Docker:**
```bash
docker pull danielcolimba/bike-backend:latest
```

3. **Configurar proxy reverso (nginx):**
```nginx
location /api/ {
    proxy_pass http://backend:8000/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## 🐛 Troubleshooting

### **Problemas comunes:**

1. **Error de conexión a BD:**
   - Verificar que PostgreSQL esté ejecutándose
   - Comprobar variables de entorno
   - Verificar permisos de usuario

2. **Error de Redis:**
   - Verificar que Redis esté activo
   - Comprobar host y puerto
   - Verificar conectividad de red

3. **Error de migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Limpiar cache:**
   ```bash
   ./dev.sh clean
   ```

## 📁 Estructura del Proyecto

```
bike-backend/
├── api/                    # App principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas API
│   ├── serializers.py     # Serializadores DRF
│   ├── urls.py            # URLs de la API
│   ├── management/        # Comandos personalizados
│   └── utils/             # Utilidades
├── royalbike/             # Configuración Django
│   ├── settings.py        # Configuración principal
│   └── urls.py            # URLs principales
├── requirements.txt       # Dependencias Python
├── Dockerfile            # Imagen Docker
├── docker-compose.yml    # Orquestación
├── dev.sh               # Script de desarrollo
├── .env.example         # Template variables
└── README.md            # Este archivo
```

## 🤝 Contribuir

1. Fork del proyecto
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Daniel Colimba** - [GitHub](https://github.com/danielcolimba)

---

⭐ ¡Dale una estrella si este proyecto te ayudó!