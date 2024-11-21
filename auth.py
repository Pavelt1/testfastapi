import datetime
import uuid
import bcrypt
from typing import Literal, Optional
from dependeses import SessAsync
from crud import for_token
from db import Token
from fastapi import Header

ROL = Literal["admin", "user"]

ADV_format = ["title","description","price","author"]

def format_json(data: dict, user: dict) -> dict:
    format_data = {i : data.get(i) for i in ADV_format if data.get(i) is not None}
    format_data["user"] =user
    return format_data

def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.hashpw(password,bcrypt.gensalt())
    return password.decode()

def check_password(user_password: str,hashed_password: str) -> bool:
    user_password = user_password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(user_password,hashed_password)

async def check_right(session: SessAsync, token : str | None) :
    if token == None:
        return "Token is None"
    token = uuid.UUID(token)
    token_db =  await for_token(Token,token,session)
    if token_db:
        data_x = datetime.datetime.now()
        if (data_x - token_db.create_datetime).total_seconds() <= 48 * 3600:
            return token_db.user
        else:
            return "Token has expired."
    else:
        raise "Token not found."
