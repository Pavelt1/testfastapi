from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Header
from schema import postUser
from dependeses import SessAsync
from db import Role, User, Token
from auth import hash_password, check_password,ROL
from sqlalchemy import select
from crud import in_db_id, add_db,for_login


router = APIRouter(
    prefix="/user",
    tags = ["user"]
)



@router.post("/")
async def post_user(jsonForm: postUser, session: SessAsync, header_role: Optional[ROL] = Header(None)):
    hashed_password = hash_password(jsonForm.password)
    jsonForm = {"password" : hashed_password}
    new_user = add_db(User,jsonForm,session)
    role_user = "user"
    if header_role:
        role_user = "admin"
    save = Role(role=role_user,user=new_user)
    session.add(save)
    await session.commit()
    return {"login":jsonForm.login,"role":role_user}

@router.post("/login")
async def create_token(jsonForm: postUser, session: SessAsync):
    user = await for_login(User,jsonForm.login,session)
    if user:
        if check_password(user.password,(hash_password(jsonForm.password))):
            save = Token(user=user)
            session.add(save)
            await session.commit()
            return {"token" : save.token}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password.")
    else:
        raise HTTPException(status_code=404, detail=f"User {jsonForm.password} not found in the database.")

@router.get("/{user_id}/")
async def get_user(user_id: int, session: SessAsync):
    result = await in_db_id(User,user_id,session)
    if result:
        return {"user":True,
                "id": user_id,
                "role": result.role,
                "advertisement": result.advertisement}
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found in the database.")

@router.patch("/{user_id}/")
async def patch_user(user_id: int,jsonForm: postUser, session: SessAsync):
    user = await in_db_id(User,user_id,session)
    if user:
        if check_password(user.password,(hash_password(jsonForm.password))):
            new_data={"login":jsonForm.new_login,"password":hash_password(jsonForm.new_password)}
            for key,value in new_data.dict().items():
                setattr(user, key, value)
            await session.commit()
            return {"data" : True}

        else:
            raise HTTPException(status_code=401, detail="Incorrect password.")
    else:
        raise HTTPException(status_code=404, detail=f"User {jsonForm.password} not found in the database.")


@router.delete("/{user_id}/")
async def del_user(user_id: int,jsonForm: postUser, session: SessAsync):
    user = await in_db_id(User,user_id,session)
    if user:
        if check_password(user.password,(hash_password(jsonForm.password))):
            user.delete()
            await session.commit()   
            return {f"advertisement {user_id}" : "Delete"}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password.")
    else:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found in the database.")