from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import *
from routers import users
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


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

app.include_router(users.router, prefix="/api")

app.mount("/static", StaticFiles(directory="static"), name="static")

load_dotenv()


db_url = os.getenv("DATABASE_URL")




@app.get("/")
def index():
    return {"message": "Hello World"}

register_tortoise(
    app,
    db_url = db_url,
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)




