from sqlalchemy import select
from dependeses import SessAsync
from db import MODEL
from pydantic import BaseModel
import uuid


async def add_db(ORMmodel: MODEL,data: dict,session: SessAsync):
    save_adv = ORMmodel(**data.dict())
    session.add(save_adv)
    await session.commit()

async def in_db_id(ORMmodel: MODEL,data: int,session: SessAsync):
    adv = select(ORMmodel).where(ORMmodel.id == data)
    result = await session.execute(adv)
    user = result.scalars().first()
    return user

async def for_login(ORMmodel: MODEL,data: str,session: SessAsync):
    adv = select(ORMmodel).where(ORMmodel.login == data)
    result = await session.execute(adv)
    user = result.scalars().first()
    return user

async def for_token(ORMmodel: MODEL,data: uuid.UUID,session: SessAsync):
    tokenORM = select(ORMmodel).where(ORMmodel.token == data)
    result = await session.execute(tokenORM)
    token = result.scalars().first()
    return token
    
