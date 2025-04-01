import uuid
from app.packages.dao import PackageDAO, PackageTypeDAO
from app.utils.session_maker import connection
from sqlalchemy.ext.asyncio import AsyncSession
from app.packages.schemas import PackagePydantic, PackageTypePydantic, PackageResposePydantic
from app.packages.models import TypeEnum
from app.exceptions import TypeIsNotExistException, WrongIDsFormatException


@connection(commit=False)
async def select_one_or_none(session:AsyncSession, id: str):
    package = await PackageDAO.find_one_or_none_by_id(session=session, id=id)
    if package:
        if package['delivery_price'] < 0:
            package['delivery_price'] = 'Not calculated'
        return PackageResposePydantic(**package)
    return None


@connection(commit=False)
async def select_by_ids(session:AsyncSession, ids: list[str]) -> list[PackageResposePydantic]:
    try:
        [uuid.UUID(idd, version=4) for idd in ids]
    except Exception as e:
        raise WrongIDsFormatException

    packages = await PackageDAO.find_by_ids(session=session, ids=ids)
    valid_packages = [PackageResposePydantic(**package) for package in packages]
    for package in valid_packages:
            if package.delivery_price < 0:
                package.delivery_price = 'Not calculated'
    return valid_packages


@connection(commit=False)
async def select_types(session: AsyncSession):
    types = await PackageTypeDAO.find_all_types(session=session)
    valid_types = [PackageTypePydantic.model_validate(t) for t in types]
    return valid_types


@connection(commit=True)
async def add_package(session: AsyncSession, data: PackagePydantic):
    if data.type_id > len(TypeEnum) or data.type_id < 1:
        raise TypeIsNotExistException
    id = await PackageDAO.add(session=session, data=data)
    return id


@connection(commit=True)
async def update_record(session: AsyncSession, id: str, rate: float):
    status = await PackageDAO.update_rate(session=session, id=id, rate=rate)
    return status
