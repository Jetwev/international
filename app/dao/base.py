from typing import TypeVar, Generic, Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.database import Base


T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: Type[T] = None

    def __init__(self, session: AsyncSession):
        if self.model is None:
            raise ValueError("Model should be defined...")
