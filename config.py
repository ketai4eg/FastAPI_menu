import os
import redis
from dotenv import load_dotenv

load_dotenv()

PG_USER = os.getenv('PG_USER', 'admin1')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'admin111')
PG_HOST = os.getenv('PG_HOST', '127.0.0.1')
PG_PORT = os.getenv('PG_PORT', 5433)
PG_DB = os.getenv('PG_DB', 'app_db')

PG_DSN = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
REDIS_DB = os.getenv('REDIS_DB', 0)
REDIS_ENCODING = os.getenv('REDIS_ENCODING', 'utf-8')
REDIS_CACHE_EXPIRE_TIME = os.getenv('REDIS_CACHE_EXPIRE_TIME', 300)

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
r = redis.Redis(
    connection_pool=pool, encoding=REDIS_ENCODING,
    max_connections=10,
)
