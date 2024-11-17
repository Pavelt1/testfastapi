from typing import Annotated
from database.db import async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessAsync = Annotated[AsyncSession, Depends(async_session)]