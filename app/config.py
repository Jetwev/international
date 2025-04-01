import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int
    CURRENCY_URL: str

    COOKIE_SECRET_KEY: str
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()

if os.environ.get('MYREDIS_HOST'):
    settings.REDIS_HOST = os.environ.get('MYREDIS_HOST')


def get_db_url():
    if os.environ.get('MYSQL_HOST'):
        return (f"mysql+aiomysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
                f"{os.environ.get('MYSQL_HOST')}:{settings.DB_PORT}/{settings.DB_NAME}")
    return  (f"mysql+aiomysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@"
             f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

database_url = get_db_url()
