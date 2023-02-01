import redis
import os
from dotenv import load_dotenv

load_dotenv()


def get_cache():
    cache = redis.StrictRedis(
        host=os.getenv('CACHE_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        decode_responses=True,
        encoding='utf-8',
    )
    yield cache
