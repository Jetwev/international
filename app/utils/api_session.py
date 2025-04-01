import uuid
from fastapi import Request, Response
from itsdangerous import Serializer
from app.config import settings

serializer = Serializer(settings.COOKIE_SECRET_KEY)


def create_session(response: Response):
    signed_cookie_value = serializer.dumps({"session": str(uuid.uuid4())})
    response.set_cookie(key="session", value=signed_cookie_value, httponly=True, max_age=86400)


def check_session(request: Request, response: Response):
    try:
        serializer.loads(request.cookies["session"])
        ids_cookie = request.cookies.get("ids") or ""
    except Exception as e:
        signed_cookie_value = serializer.dumps({"session": str(uuid.uuid4())})
        response.set_cookie(key="session", value=signed_cookie_value, httponly=True, max_age=86400)
        ids_cookie = ""
    finally:
        return ids_cookie


def check_presence_session(request: Request):
    if not request.cookies.get("session"):
        False
    return True
