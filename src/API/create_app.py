from . import router_main
from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager
from bot.bot import bot_main
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(bot_main())
    yield


app = FastAPI(docs_url='/api/docs', lifespan=lifespan)


def create_app():
    logger.add(
    "sys.stdout",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {file}:{line} - {message}",
    colorize=True,
    level="INFO"
    )
    
    app.include_router(router_main.router)

    return app
