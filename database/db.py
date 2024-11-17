import os

import datetime
from typing import List
import uuid

from sqlalchemy import ForeignKey, MetaData, Integer, String, Float, Text, DateTime, UUID, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv('POSTGRES_USER',"postgres")
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD',"0596")
POSTGRES_DB = os.getenv('POSTGRES_DB',"postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","5432")

DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_HOST}/{POSTGRES_DB}"
engine = create_async_engine(DSN,echo=True) 
#Указание echo=True при инициализации движка позволит нам увидеть сгенерированные SQL-запросы в консоли.

Base = declarative_base(metadata=MetaData())

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
# Создаем фабрику сессий для взаимодействия с базой данных

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    login: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    passwird: Mapped[str] = mapped_column(String,nullable=False)

    token: Mapped[List["Token"]] = relationship("Token", lazy="joined",back_populates="user")
    #lazy = "joined"  при запросе юзера будет автоматически приклеивать токен
    advertisement: Mapped[list["Advertisement"]] = relationship("Advertisement", lazy="joined",back_populates="user")
    role: Mapped[List["Role"]] = relationship("Role", lazy="joined",back_populates="user",uselist=False)
    # uselist=False Показывает что это все один к одному

    def dict(self):
        return {
            "id":self.id,
            "login":self.login,
            "role":[ad.role for ad in self.role],
            "token":self.token,
            "advertisement":[ad.title for ad in self.advertisement],
            }


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    role: Mapped[str] = mapped_column(String,nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    
    user: Mapped[User] = relationship("User", lazy="joined",back_populates="role") 

class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(UUID,server_default=func.gen_random_uuid())
    create_datetime: Mapped[datetime.datetime] =  mapped_column(DateTime,server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"),nullable=False)

    user: Mapped[User] = relationship("User", lazy="joined",back_populates="token")

    def dict(self):
        return {
            "id":self.id,
            "token":self.token,
            "create_datetime":self.create_datetime,
            "user":self.user
            }


class Advertisement(Base):
    __tablename__ = "advertisement"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String,nullable=False)
    description: Mapped[str] = mapped_column(Text,nullable=False)
    price: Mapped[float] = mapped_column(Float,nullable=False)
    author: Mapped[str] = mapped_column(String,nullable=False)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(DateTime,server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped[User] = relationship("User", lazy="joined",back_populates="advertisement")


    def dict(self):
        return {
            "id":self.id,
            "title":self.title,
            "description":self.description,
            "price":self.price,
            "author":self.author,
            "date_of_creation":self.date_of_creation
            }
    

async def async_session():
    async with async_session_maker() as session:
        yield session
 

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


MODEL = User | Token | Advertisement