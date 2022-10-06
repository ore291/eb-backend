from datetime import datetime, timedelta
from typing import Optional, Union, List
from utils.fields import *
from py_models.location import state_pydantic, state_pydantic_list

from fastapi import Depends, APIRouter, HTTPException, status, Form, File, UploadFile, BackgroundTasks






router = APIRouter()



@router.get("/fields/states", response_model=List[state_pydantic])
async def get_states():
    return await get_db_states()





