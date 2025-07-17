# en cualquier archivo reutilizable como utils/redis_client.py

import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True  # para que los datos estén en string
)
