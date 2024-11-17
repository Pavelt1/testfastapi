from typing import Optional
from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import select
from ..schema import postAdvertisement, patchAdvertisement
from ..database.db import Advertisement, User
from ..dependeses import SessAsync
from pydantic import BaseModel
from ..database.crud import in_db_id, add_db,for_login
from ..auth import check_right, hash_password, check_password,ROL,format_json

router = APIRouter(
    prefix="/advertisement",
    tags = ["advertisement"]
)
 
@router.post("/") 
async def post_advertisement(new_adv: postAdvertisement, session: SessAsync,token: Optional[str] = Header(None)):
    response = await check_right(session,token)
    if isinstance(response,dict):
        new_adv = add_db(Advertisement,format_json(new_adv,response),session)
    else:
        raise HTTPException(status_code=403, detail={"token" : response})
    

@router.patch("/{advertisement_id}/")
async def patch_advertisement(advertisement_id: int ,
                              new_adv: patchAdvertisement, 
                              session: SessAsync,
                              token: Optional[str] = Header(None)):
    response = await check_right(session,token)
    if isinstance(response,dict):
        result = in_db_id(Advertisement,advertisement_id,session)
        if result:
            for key,value in (format_json(new_adv,response)).items():
                setattr(result, key, value)
            await session.commit()
            return result
        else:
            raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")
    else:
        raise HTTPException(status_code=403, detail={"token" : response})
    
    
@router.delete("/{advertisement_id}/")
async def del_one(advertisement_id: int, session: SessAsync,token: Optional[str] = Header(None)):
    response = await check_right(session,token)
    if isinstance(response,dict):
        result = in_db_id(Advertisement,advertisement_id,session)
        if result:
            result.delete()
            await session.commit()   
            return {f"advertisement {advertisement_id}" : "Delete"}
        
        else:
            raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")
    else:
        raise HTTPException(status_code=403, detail={"token" : response})

@router.get("/{advertisement_id}/")
async def get_advertisement(advertisement_id: int , session: SessAsync):
    result = in_db_id(Advertisement,advertisement_id,session)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"Advertisement {advertisement_id} not found in the database.")

@router.get("/")
async def get_query_string(session: SessAsync,
                           id: Optional[int] = None,
                           title: Optional[str] = None,
                           description: Optional[str] = None,
                           price: Optional[float] = None,
                           author: Optional[str] = None):
    query = select(Advertisement)

    if id is not None:
        query = query.where(Advertisement.id == id)
    if title is not None:
        query = query.where(Advertisement.title.ilike(f"%{title}%"))
    if description is not None:
        query = query.where(Advertisement.description.ilike(f"%{description}%"))
    if price is not None:
        query = query.where(Advertisement.price == price)
    if author is not None:
        query = query.where(Advertisement.author.ilike(f"%{author}%"))

    result = await session.execute(query)
    advertisements = result.scalars().all()
    return advertisements
