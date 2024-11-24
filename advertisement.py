import uuid
from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import select
from schema import postAdvertisement, patchAdvertisement
from db import Advertisement, User
from dependeses import SessAsync
from pydantic import BaseModel
from crud import in_db_id, add_db,for_login
from auth import check_right, hash_password, check_password,ROL,format_json

router = APIRouter(
    prefix="/advertisement",
    tags = ["advertisement"]
)
 
@router.post("/") 
async def post_advertisement(new_adv: postAdvertisement, 
                             session: SessAsync, 
                             token: Optional[str] = Header()):
    data = new_adv.dict()
    response = await check_right(session, token)
    if isinstance(response, dict):
        new = await add_db(Advertisement, format_json(data,response["user"]), session)
        return new
    else:
        raise HTTPException(status_code=403, detail={"token": response})
    

@router.patch("/{advertisement_id}/")
async def patch_advertisement(advertisement_id: int ,
                              new_adv: patchAdvertisement, 
                              session: SessAsync,
                              token: Optional[str] = Header()):
    data = new_adv.dict()
    response = await check_right(session,token)
    if isinstance(response,dict):
        result = await in_db_id(Advertisement,advertisement_id,session)
        if result:
            for key,value in (format_json(data,response["user"])).items():
                setattr(result, key, value)
            await session.commit()
            return {"data": True}
        else:
            raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")
    else:
        raise HTTPException(status_code=403, detail={"token" : response})
    
    
@router.delete("/{advertisement_id}/")
async def del_one(advertisement_id: int, session: SessAsync,token: Optional[str] = Header(None)):
    response = await check_right(session,token)
    if isinstance(response,dict):
        result = await in_db_id(Advertisement,advertisement_id,session)
        if result:
            await session.delete(result)
            await session.commit()  
            return {f"advertisement {advertisement_id}" : "Delete"}
        
        else:
            raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")
    else:
        raise HTTPException(status_code=403, detail={"token" : response})

@router.get("/{advertisement_id}/")
async def get_advertisement(advertisement_id: int , session: SessAsync):
    result = await in_db_id(Advertisement,advertisement_id,session)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")
    return result.dict()