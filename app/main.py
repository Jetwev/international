from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter, Request, Response
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.dao.operations_db import drop_db, create_db
from app.api.router import api_router
from app.scheduler.scheduler import update_and_process
from app.scheduler.redis import clear_redis
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
    try:
        logger.info("Initialization...")
        await drop_db()
        await create_db()
        clear_redis()
        logger.info('Redis initialization...')
        scheduler.add_job(update_and_process, trigger=IntervalTrigger(minutes=5), id='update', replace_existing=True)
        scheduler.start()
        logger.info("Scheduler is up")
        yield
    except Exception as e:
        logger.error(f"Some error with initialization: {e}")
    finally:
        scheduler.shutdown()
        logger.info("Scheduler is down")
        logger.info("Shutting down...")


def register_routers(app: FastAPI) -> None:
    root_router = APIRouter()

    @root_router.get("/")
    async def healthcheck(request: Request, response: Response):
        if request.cookies.get('session'):
            response.delete_cookie('session')
        if request.cookies.get('ids'):
            response.delete_cookie('ids')
        return {
            "status": "ok"
        }
    
    app.include_router(root_router)
    app.include_router(api_router)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Application",
        version="1.0.0",
        lifespan=lifespan,
    )

    register_routers(app)

    return app

scheduler = AsyncIOScheduler()
app = create_app()
