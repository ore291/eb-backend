from models import Client, Blurb
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

client_pydantic = pydantic_model_creator(Client, name="Client")

client_pydanticCreate = pydantic_model_creator(Client, name="ClientIn", exclude_readonly=True)

blurb_pydantic = pydantic_model_creator(Blurb, name="Blurb")
blurb_pydanticCreate = pydantic_model_creator(Blurb, name="BlurbIn", exclude_readonly=True)