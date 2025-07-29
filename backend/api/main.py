#TODO: add tasks routes later

from fastapi import FastAPI
from auth.routes import router as auth_router
from tasks.routes import router as tasks_router
from middleware.api_key import api_key_middleware
from database import create_db_and_tables

app = FastAPI()

app.middleware("http")(api_key_middleware)

app.include_router(auth_router)
app.include_router(tasks_router)

@app.on_event("startup")
async def startup():
    await create_db_and_tables()
