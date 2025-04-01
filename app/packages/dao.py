import uuid
from datetime import datetime
from app.dao.base import BaseDAO
from app.packages.models import Package, PackageType
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.scheduler.redis import redis_client, update_ids_key
from app.scheduler.parser import calculate_delivery_cost


class PackageDAO(BaseDAO):
    model = Package

    @classmethod
    def _add_update_id_to_redis(cls, id):
        try:
            redis_client.rpush(update_ids_key, id)
        except Exception as e:
            logger.info(f'[{datetime.now()}]: Error while pushing id {id}: {e}')

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, id: str):
        try:
            query = select(cls.model, PackageType.name.label("type_name")).filter_by(id=id).join(PackageType, cls.model.type_id == PackageType.id)
            result = await session.execute(query)
            record = result.first()
            model_instance = None
            if record:
                model_instance = record[0].to_dict()
                model_instance['type_name'] = record[1].value
            log_message = f"Package with ID {id} {'was found...' if record else 'was not found...'}."
            logger.info(log_message)
            return model_instance
        except SQLAlchemyError as e:
            logger.error(f"Error while finding data with ID {id}: {e}")
            raise
    
    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: list[str]):
        try:
            query = select(cls.model, PackageType.name.label("type_name")).where(cls.model.id.in_(ids)).join(PackageType, cls.model.type_id == PackageType.id)
            result = await session.execute(query)
            records = result.all()
            res = []
            for record in records:
                inst = record[0].to_dict()
                inst['type_name'] = record[1].value
                res.append(inst)
            logger.info(f"Found {len(records)} Packages by IDs: {ids}")
            return res
        except SQLAlchemyError as e:
            logger.error(f"Error while finding data with IDs {ids}: {e}")
            raise
    
    @classmethod
    async def add(cls, session: AsyncSession, data: BaseModel):
        data_dict = data.model_dump(exclude_unset=True)
        data_dict['id'] = str(uuid.uuid4())
        new_instance = cls.model(**data_dict)
        try:
            session.add(new_instance)
            await session.flush()
            cls._add_update_id_to_redis(data_dict['id'])
        except SQLAlchemyError as e:
            logger.error(f"Error with adding data: {e}")
            await session.rollback()
            raise e
        return data_dict['id']

    @classmethod
    async def update_rate(cls, session: AsyncSession, id: str, rate: float):
        try:
            result = await session.execute(select(cls.model).where(cls.model.id == id))
            model_to_upd = result.scalar_one_or_none()
            if not model_to_upd:
                return -1
            model_to_upd.delivery_price = calculate_delivery_cost(model_to_upd.weight, model_to_upd.price, rate) 
            await session.flush()
            logger.info(f'Row with id {id} was updated')
            return 1
        except SQLAlchemyError as e:
            logger.error(f"Error with adding data: {e}")
            await session.rollback()
            raise e


class PackageTypeDAO(BaseDAO):
    model = PackageType

    @classmethod
    async def find_all_types(cls, session: AsyncSession):
        try:
            query = select(cls.model)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            logger.error(f"Error while returning all types: {e}")
            raise