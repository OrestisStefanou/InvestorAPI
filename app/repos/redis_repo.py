from typing import Optional

from app import dependencies

class RedisRepo(object):
	_redis_client = dependencies.redis_client

	@classmethod
	def _set_key_value(cls, key: str, value: str, seconds_to_expire: int = 3600) -> None:
		"""
		Sets <key>-<value> in Redis that will expire after <seconds_to_expire> time.
		Default expiration time is 1 hour
		"""
		cls._redis_client.set(name=key, value=value, ex=seconds_to_expire)

	@classmethod
	def _get_value_by_key(cls, key: str) -> Optional[str]:
		return cls._redis_client.get(key)
