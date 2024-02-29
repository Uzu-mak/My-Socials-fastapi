from pydantic import BaseModel, EmailStr,Field
from typing import Optional,Union
from datetime import datetime


class PostBase(BaseModel):
        title:str
        content:str
        published:bool = True
        id: Optional[int] = None
        #owner_id: int
                     
class PostCreate(PostBase):
        pass

class UserResponse(BaseModel):
        id:int
        email:EmailStr
        created_at:datetime
        
class PostResponse(PostBase):
        id:int
        created_at:datetime
        owner_id: int
        owner:UserResponse
        
        class config:
                orm_mode = True
                
class PostOut(BaseModel):
        post:PostResponse
        votes:int
        
        class config:
                orm_mode = True
                
class UserCreate(BaseModel):
        email:EmailStr
        password:str
                

        
        class config:
                orm_mode = True
                
                
class UserLogin(BaseModel):
        email:str
        password:str
                
class Token(BaseModel):
        access_token:str
        token_type:str
        
        
        
class TokenData(BaseModel):
        id:Union[str,int]=None
        
        
        


class voteAccept(BaseModel):
    post_id: int
    dir:int = Field(..., description="A binary flag (0 or 1)", ge=0, le=1)
