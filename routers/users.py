from datetime import datetime, timedelta
from typing import Optional, Union
from models import user_pydanticCreate, lgaIn, user_pydantic
from utils.users import *
from schemas.users import UserBlurbIn, UserClientIn
from pydantic import EmailStr

from fastapi import Depends, APIRouter, HTTPException, status, Form, File, UploadFile, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from pydantic import BaseModel


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "dd40cfe414d78fbded2207166e034e5c76f75eaf5f4e27e679eaaef5ced745a9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

# @router.get('/get_user')
# async def get_user_name(email : str, password : str):
#     return await authenticate_user(email, password)

@router.post('/register/blurb')
async def blurb_registeration(background_tasks: BackgroundTasks, user: UserBlurbIn):
    result = await register_blurb(background_tasks, user)
    return result


@router.post('/register/client')
async def client_registeration( background_tasks: BackgroundTasks, email: EmailStr = Form(), phone: str = Form(), user_type: int = Form(3), password: str = Form(), company_name: str = Form(), city: str = Form(), rep_name: str = Form(), rep_contact: str = Form(), rep_email: str = Form(), blurb_angel_id: int = Form(), file: Union[UploadFile, None] = None, ):
    result = await register_client( background_tasks = background_tasks,email=email, phone = phone,file=file, user_type=user_type, password=password, company_name=company_name, city=city, rep_name=rep_name, rep_contact=rep_contact, rep_email=rep_email, blurb_angel_id=blurb_angel_id)
    return result


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(email = form_data.username,password = form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=user_pydantic)
async def read_users_me(current_user: user_pydantic = Depends(get_current_active_user)):
    return current_user


# @router.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]



