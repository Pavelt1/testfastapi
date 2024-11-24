from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Header,Response
from schema import postUser,pachUser
from dependeses import SessAsync
from db import Role, User, Token
from auth import hash_password, check_password,ROL
from sqlalchemy import select
from crud import in_db_id, add_db,for_login
from pydantic import BaseModel


router = APIRouter(
    prefix="/user",
    tags = ["user"]
)



@router.post("/")
async def post_user(jsonForm: postUser, session: SessAsync, header: Optional[ROL] = Header()):
    data = jsonForm.dict()
    user = await for_login(User,data["login"],session)
    if user:
        raise HTTPException(status_code=409, detail=f"User {data['login']} already exists in the database.")
    data["password"] = hash_password(data["password"])
    new_user = await add_db(User,data,session)
    role_user = "user"
    if header:
        role_user = header
    save = Role(role=role_user,user_id = new_user.id,user=new_user)
    session.add(save)
    await session.commit()
    return {"login":data["login"],"role":role_user}

@router.post("/login/")
async def create_token(jsonForm: postUser, session: SessAsync):
    data = jsonForm.dict()
    user = await for_login(User,data["login"],session)
    if user:
        if check_password(data["password"],user.password):
            save = Token(user_id = user.id,user=user)
            session.add(save)
            await session.commit()
            return {"token" : save.token}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password.")
    else:
        raise HTTPException(status_code=404, detail=f"User not found in the database.")

@router.get("/{user_id}/")
async def get_user(user_id: int, session: SessAsync):
    result = await in_db_id(User,user_id,session)
    if result:
        return {"user":True,
                "id": user_id,
                "role": result.role.role if result.role else None,
                "advertisement": result.advertisement}
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found in the database.")

@router.patch("/{user_id}/")
async def patch_user(user_id: int, jsonForm: pachUser, session: SessAsync):
    data = jsonForm.dict()
    user = await for_login(User,data["login"],session)
    if user:
        if check_password(data["password"], user.password):
            new_data = {"login": jsonForm.new_login, "password": hash_password(jsonForm.new_password)}
            for key, value in new_data.items():
                setattr(user, key, value)
            await session.commit()
            return {"data": True}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password.")
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found in the database.")


@router.delete("/{user_id}/")
async def del_user(user_id: int,jsonForm: postUser, session: SessAsync):
    data = jsonForm.dict()
    user = await for_login(User,data["login"],session)
    if user:
        if check_password(data["password"], user.password):
            await session.delete(user)
            await session.commit()   
            return {f"advertisement {user_id}" : "Delete"}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password.")
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found in the database.")