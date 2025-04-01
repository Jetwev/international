import uuid
from fastapi import APIRouter, Depends, Request, Response
from app.packages.schemas import PackagePydantic, PackageTypePydantic, PackageResposePydantic
from app.packages.methods import add_package, select_one_or_none, select_types, select_by_ids
from app.exceptions import CookieNotSetException
from app.utils.api_session import create_session, check_session, check_presence_session
from app.scheduler.scheduler import update_and_process


api_router = APIRouter(prefix='/package')


@api_router.post('/add')
async def package_addition(request: Request, response: Response, package: PackagePydantic) -> str:
    if not request.cookies.get('session'):
        create_session(response)
    
    ids_cookie = check_session(request, response)
    id = await add_package(data=package)
    updated_ids = f"{ids_cookie},{id}" if ids_cookie else str(id)
    response.set_cookie(key="ids", value=updated_ids, max_age=86400)
    return id


@api_router.get('/info')
async def package_info(id: str, check_cookie: bool = Depends(check_presence_session)) -> PackageResposePydantic:
    if not check_cookie:
        raise CookieNotSetException

    try:
        uuid.UUID(id, version=4)
    except ValueError:
        return {
            'error': 'Not right id format'
        }
    info = await select_one_or_none(id=id)
    if not info:
        return {
            'error': 'ID does not exist'
        }
    return info


@api_router.get('/types')
async def package_types(check_cookie: bool = Depends(check_presence_session)) -> list[PackageTypePydantic]:
    if not check_cookie:
        raise CookieNotSetException
    types = await select_types()
    return types


@api_router.get('/my/ids')
async def get_cookie_ids(request: Request, check_cookie: bool = Depends(check_presence_session)) -> dict[str, list[PackageResposePydantic | None]]:
    if not check_cookie:
        raise CookieNotSetException
    
    ids_cookie = request.cookies.get("ids").split(',')
    if ids_cookie:
        packages = await select_by_ids(ids=ids_cookie)
        return {"ids": packages}
    else:
        return {"ids": []}


@api_router.get('/dev/update')
async def update_rate_and_records():
    status = await update_and_process()
    if status == -1:
        return {'error': 'not updated'}
    return {'status': 'ok'}
