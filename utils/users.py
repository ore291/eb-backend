from datetime import datetime, timedelta
from typing import List, Optional, Type
import shortuuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models import User, user_pydantic, user_pydanticCreate, user_pydanticOut, Client, Blurb, blurb_pydanticCreate, client_pydanticCreate, UserType
from schemas.users import UserBlurbIn, UserClientIn
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from tortoise import BaseDBAsyncClient
from tortoise.signals import post_save
import aiofiles
from emails import send_verification_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "dd40cfe414d78fbded2207166e034e5c76f75eaf5f4e27e679eaaef5ced745a9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


# @post_save(User)
# async def create_user_type_data(
#     sender: "Type[User]",
#     instance: User,
#     created: bool,
#     using_db: "Optional[BaseDBAsyncClient]",
#     update_fields: List[str],
# ) -> None:
#     if created:
        
       


async def register_blurb(background_tasks: BackgroundTasks, user: UserBlurbIn):
    # registered email check
    if await User.get_or_none(email=user.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    # existing phone number check
    if await User.get_or_none(phone=user.phone) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone Number already registered"
        )

    # creating a new user
    userIn = user.dict(exclude_unset=True)
    userIn["password_hash"] = get_password_hash(userIn["password"])
    userIn['username'] = userIn["phone"]
    db_user = await User.create(**userIn)
    created_user = await user_pydantic.from_tortoise_orm(db_user)

    # creating a blurb profile for the new user
    if user.user_type == 2:
        blurb_data = await Blurb.create(
            **userIn, user=db_user
        )
        await blurb_pydanticCreate.from_tortoise_orm(blurb_data)

    await send_verification_email(background_tasks, [created_user.email], db_user)

    return created_user


async def register_client(background_tasks: BackgroundTasks, email: EmailStr, phone: str,  user_type: UserType, password: str, company_name: str, city: str, rep_name: str, rep_contact: str, rep_email: str, blurb_angel_id: str, file: UploadFile = File(...)):
    if await User.get_or_none(email=email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    if await User.get_or_none(phone=phone) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone Number already registered"
        )

   # creating a new user
    userIn = dict(email=email, phone=phone, user_type=user_type, company_name=company_name, city=city,
                  rep_name=rep_name, rep_contact=rep_contact, rep_email=rep_email, blurb_angel_id=blurb_angel_id)
    userIn["password_hash"] = get_password_hash(password)
    userIn['username'] = userIn["phone"]

    db_user = await User.create(**userIn)
    created_user = await user_pydantic.from_tortoise_orm(db_user)

    image_id = shortuuid.uuid()

    try:
        async with aiofiles.open(f'static/companies/{image_id}{file.filename}', 'wb') as f:
            contents = await file.read()
            await f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        await file.close()

    userIn['company_logo'] = image_id + file.filename

    # creating a client profile for the new user
    if user_type == 3:
        client_data = await Client.create(
            **userIn, user=db_user
        )
        await client_pydanticCreate.from_tortoise_orm(client_data)


    await send_verification_email(background_tasks, [created_user.email], db_user)

    return created_user


async def get_user(email: str):
    user = await User.get_or_none(email=email)
    return user


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: user_pydantic = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
