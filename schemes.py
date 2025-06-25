from models import User,Expense
from pydantic import BaseModel

class Userdatacheck(BaseModel):
    
    username:str
    password:str

class Expense(BaseModel):
    
    amount:float
    title:str
    

class UserOut(BaseModel):
    username:str
    id:int

class ExpenseOut(BaseModel):
    title:str
    amount:float

class Tokencheck(BaseModel):
    access_token:str
    token_type: str
