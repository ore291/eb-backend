from fastapi import Depends, APIRouter, HTTPException
from fastapi_crudrouter.core.tortoise import TortoiseCRUDRouter
from py_models.clients import product_pydantic,product_pydantic_create
from models import Product

router = TortoiseCRUDRouter(schema=product_pydantic, db_model=Product, create_schema=product_pydantic_create)