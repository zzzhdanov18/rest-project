from core.service.templates import AbstractCache
from redis.client import Redis


class RedisCache(AbstractCache):
    cache: Redis

    def __init__(self, cache):
        self.cache = cache

    def set(self, key: str, value):
        self.cache.set(key, value)

    def delete(self, key: str):
        self.cache.delete(key)

    def get(self, key: str):
        return self.cache.get(key)
