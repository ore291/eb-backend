from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import *
from py_models.location import state_pydantic, state_pydantic_list
from py_models.clients import product_pydantic
from tortoise import Tortoise
from routers import users, fields, clients
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter


import os
from dotenv import load_dotenv


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()


db_url = os.getenv("DATABASE_URL")




async def init():
    register_tortoise(
        app,
        db_url=db_url,
        modules={"models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )


@app.on_event("startup")
async def startup_event(): 
    await init()


@app.on_event("shutdown")
async def close_orm():
    await Tortoise.close_connections()




@app.get("/")
def index():
    return {"message": "Hello World"}


app.include_router(users.router, prefix="/api")
app.include_router(fields.router, prefix="/api")
app.include_router(clients.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")


   

