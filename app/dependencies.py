import sqlite3

import redis

from app import settings

redis_client = redis.Redis(
	host=settings.redis_host,
	port=settings.redis_port,
	password=settings.redis_password
)

DB_CONN = sqlite3.connect(settings.db_path)

def get_db_conn() -> sqlite3.Connection:
	global DB_CONN
	if DB_CONN is None:
		DB_CONN = sqlite3.connect(settings.db_path)

	return DB_CONN


def close_db_conn():
	global DB_CONN
	DB_CONN.close()