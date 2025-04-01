from sqlalchemy import text
from app.dao.database import async_session_maker, engine, Base
from loguru import logger


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            return await func(session, *args, **kwargs)
    return wrapper


async def insert_package_types():
    async with engine.connect() as conn:
        await conn.execute(text("""INSERT INTO packagetypes (name) VALUES ('CLOTHES'), ('ELECTRONICS'), ('OTHER');"""))
        await conn.commit()


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await insert_package_types()


async def drop_db():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("DELETE FROM packages"))
        except Exception as e:
            logger.info('Table packages does not exist...')
        try:    
            await conn.execute(text("DELETE FROM packagetypes"))
        except Exception as e:
            logger.info('Table packagetypes does not exist...')
        await conn.execute(text("DROP TABLE IF EXISTS packages"))
        await conn.execute(text("DROP TABLE IF EXISTS packagetypes"))
