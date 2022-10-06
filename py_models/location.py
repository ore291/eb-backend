
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from models import Lga, State

lgaIn = pydantic_model_creator(Lga, name="lgaIn", exclude_readonly=True)

state_pydantic = pydantic_model_creator(State, name="StateIn", exclude=("state"))
state_pydantic_list = pydantic_queryset_creator(State, name="StateList")