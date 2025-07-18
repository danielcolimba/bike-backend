"""
WSGI config for royalbike project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# En producción usamos settings_prod.py
env = os.environ.get('DJANGO_ENV', 'development')
if env == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royalbike.settings_prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'royalbike.settings')

application = get_wsgi_application()
