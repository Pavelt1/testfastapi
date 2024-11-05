from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MyAdvertisement(BaseModel):
    id: int
    title : str 
    description : str 
    price : float
    author : str
    date_of_creation: datetime = Field(default=None)
    

class UpdateAdvertisement(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None