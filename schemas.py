from pydantic import BaseModel
from typing import List

class User(BaseModel):
    username : str
    email : str
    phone : str
    password : str
    class Config(): 
        orm_mode = True


class ShowUser(BaseModel):
    username : str
    email : str
    phone: str
    class Config(): 
        orm_mode = True




class Login(BaseModel):
    username : str
    password : str
    class Config(): 
        orm_mode = True



class Token(BaseModel):
    access_token: str
    token_type: str
    user_id : int


class TokenData(BaseModel):
    email: str | None = None





class FavCompanies(BaseModel):
    user_id : int
    company : str
    class Config:
        orm_mode = True 


