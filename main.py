from core.db.db_config import Base, engine
from core.routes.router import rest_router

from fastapi import FastAPI


app = FastAPI()

Base.metadata.create_all(engine)

app.include_router(rest_router)
