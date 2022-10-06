from pydantic import BaseModel, EmailStr
from typing import List

from datetime import datetime


class Lga(BaseModel):
    id : int
    name : str


class State(BaseModel):
    id : int
    name : str
    lgas : List[Lga]