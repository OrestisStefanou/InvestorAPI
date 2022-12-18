import sqlite3

import redis

from app import settings

redis_client = redis.Redis(
	host=settings.redis_host,
	port=settings.redis_port,
	password=settings.redis_password
)

db_conn = sqlite3.connect(settings.db_path)
