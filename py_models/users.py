from models import User
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator


user_pydantic = pydantic_model_creator(User, name="User", exclude=("is_verified", "is_active",'password_hash' ))
user_pydanticCreate =  pydantic_model_creator(User, name="UserIn", exclude=("is_verified", "is_active","id" ))
user_pydanticOut = pydantic_model_creator(User, name="UserOut",exclude=("password_hash"))