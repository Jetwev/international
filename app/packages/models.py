from enum import Enum
from sqlalchemy import ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.dao.database import Base


class Package(Base):
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(String(36), unique=True)
    name: Mapped[str] = mapped_column(String(256))
    weight: Mapped[float]
    type_id: Mapped[int] = mapped_column(ForeignKey('packagetypes.id'))
    price: Mapped[float]
    delivery_price: Mapped[float] = mapped_column(Float, server_default='-1')


class TypeEnum(str, Enum):
    CLOTHES = 'CLOTHES'
    ELECTRONICS = 'ELECTRONICS'
    OTHER = 'OTHER'


class PackageType(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[TypeEnum]

