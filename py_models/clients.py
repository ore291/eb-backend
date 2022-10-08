from models import Client, Blurb, Product
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

client_pydantic = pydantic_model_creator(Client, name="Client")
product_pydantic = pydantic_model_creator(Product, name="Product", exclude=("plan","transactions",))
product_pydantic_create = pydantic_model_creator(Product, name="ProductCreate", exclude_readonly=True)

client_pydanticCreate = pydantic_model_creator(Client, name="ClientIn", exclude_readonly=True)

blurb_pydantic = pydantic_model_creator(Blurb, name="Blurb")
blurb_pydanticCreate = pydantic_model_creator(Blurb, name="BlurbIn", exclude_readonly=True)