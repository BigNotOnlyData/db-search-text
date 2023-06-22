import time
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Отвечает за выполнение функий до запуска приложения и после завершения
    """
    # # перед запуском
    # app.sync.on_startup()
    while not app.sync.es.client.ping():
        time.sleep(15)
    app.sync.on_startup()
    yield
    # после завершения
    app.sync.on_shutdown()
