from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class postAdvertisement(BaseModel):
    title : str 
    description : str 
    price : float
    author : str
    date_of_creation: Optional[datetime] = None 

    

class patchAdvertisement(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    author: Optional[str] = None


class postUser(BaseModel):
    login  : str 
    password : str

class pachUser(postUser):
    new_login  : Optional[str] = None
    wew_password : Optional[str] = None

    