from pydantic import BaseModel, ConfigDict
from app.packages.models import TypeEnum


class PackagePydantic(BaseModel):
    name: str
    weight: float
    type_id: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class PackageResposePydantic(BaseModel):
    name: str
    weight: float
    type_name: str
    price: float
    delivery_price: str | float

    model_config = ConfigDict(from_attributes=True)


class PackageTypePydantic(BaseModel):
    id: int
    name: TypeEnum

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
