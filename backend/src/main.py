import uvicorn
from fastapi import FastAPI

from root.api.routers import router
from root.api.utils import lifespan
from root.databases import Postgres, Synchronizer, Elastic
from root import config as cfg

app = FastAPI(lifespan=lifespan, title='My amazing API')
app.include_router(router=router)


app.sync = Synchronizer(db=Postgres(cfg.PG_PARAMS),
                        es=Elastic(cfg.ES_PARAMS))


# if __name__ == "__main__":
#     uvicorn.run("main:app", host=cfg.API_HOST, port=cfg.API_PORT, reload=True)
