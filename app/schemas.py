from pydantic import BaseModel

class CompanieBase(BaseModel):
    symbol: str
    name: str
    type: str
    region: str
    currency: str
    matchScore: float

class Companie(CompanieBase):
    id: int
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str
    password: str
    type_id: int

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class UserSelect(BaseModel):
    name: str
    email: str
    type_id: int
