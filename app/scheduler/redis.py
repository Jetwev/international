import redis
from app.config import settings


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
update_ids_key = 'update_ids'
usd_to_rub_rate_key = 'usd_to_rub_rate'


def clear_redis():
    deleted_count = redis_client.delete(update_ids_key, usd_to_rub_rate_key)
    return deleted_count
