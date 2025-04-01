from loguru import logger
from app.scheduler.parser import get_rate
from app.scheduler.redis import redis_client, usd_to_rub_rate_key, update_ids_key
from app.packages.methods import update_record


def update_usd_to_rub_rate():
    try:
        rate = get_rate()
        redis_client.set(usd_to_rub_rate_key, rate)
        logger.info(f'Rate was updated: {rate}')
    except Exception as e:
        logger.info(f'Error while updating rate: {e}')


async def process_update_ids():
    while True:
        id = redis_client.lpop(update_ids_key)
        usd_to_rub_rate = float(redis_client.get(usd_to_rub_rate_key).decode('utf-8'))

        if id is None:
            logger.info("Queue is empty, waiting for ids...")
            break

        logger.info(f"Updating ID: {id.decode('utf-8')}")
        await update_record(id=id, rate=usd_to_rub_rate)


async def update_and_process():
    update_usd_to_rub_rate()
    await process_update_ids()
