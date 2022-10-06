from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status
from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List, Dict, Any
from dotenv import dotenv_values
from models import User
import jwt
from jinja2 import Environment, select_autoescape, PackageLoader
from pathlib import Path


class EmailSchema(BaseModel):
    email: List[EmailStr]


config_credentials = dotenv_values(".env")

conf = ConnectionConfig(
    MAIL_USERNAME=config_credentials['EMAIL_USERNAME'],
    MAIL_PASSWORD=config_credentials['EMAIL_PASSWORD'],
    MAIL_FROM=config_credentials['EMAIL_FROM'],
    MAIL_PORT=config_credentials['EMAIL_PORT'],
    MAIL_SERVER=config_credentials['EMAIL_HOST'],
    MAIL_FROM_NAME="Blurb Test",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_verification_email(
    background_tasks: BackgroundTasks,
    email: List[EmailStr],
    instance: User

) -> JSONResponse:

    token_data = {
        "id": instance.id,
        "email": instance.email
    }

    token = jwt.encode(
        token_data, config_credentials['SECRET_KEY'], algorithm='HS256')
    base_url = config_credentials['BASE_URL']
    siteName = config_credentials['SITE_NAME']

    message = MessageSchema(
        subject=f'{siteName} Account Verification Email',
        recipients=email,
        template_body={"url": f'{base_url}/verify?token={token}'}


    )

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message,
                              template_name='email_confirm.html')

    return JSONResponse(status_code=200, content={"message": "email has been sent"})
