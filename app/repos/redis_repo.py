import logging
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
		try:
			cls._redis_client.set(name=key, value=value, ex=seconds_to_expire)
		except Exception as err:
			logging.error(f"Failed to set key-valye with error: {str(err)}")

	@classmethod
	def _get_value_by_key(cls, key: str) -> Optional[str]:
		try:
			value = cls._redis_client.get(key)
		except Exception as err:
			logging.error(f"Failed to get value by key: {key} with error: {str(err)}")
			value = None
		
		return value
	