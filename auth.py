from jose import JWTError,jwt
from typing import Annotated
from passlib.context import CryptContext
from database import sessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends ,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,HTTPAuthorizationCredentials,HTTPBearer
from datetime import datetime,timezone,timedelta
from schemes import Tokencheck
import models
from models import User,Expense

SECRET_KEY='aaaaaaaaakksdhdhudsvhxxjjkjhbvgtuytrsawasjsdgshsv'
ALGORITHM='HS256'
TOKEN_EXPIRY_TIME=30
HTTPDATA=HTTPBearer()

pass_check=CryptContext(schemes=['bcrypt'],deprecated='auto')
form_data=Annotated[OAuth2PasswordRequestForm,Depends()]
Tokendatacheck=Annotated[HTTPAuthorizationCredentials,Depends(HTTPDATA)]

#important functions:

def getDB():
    try:
        db=sessionLocal()
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(getDB)]

def getToken(username:str,id:int):
    payload={'sub':username,'id':id,'exp':datetime.now(timezone.utc)+ timedelta(minutes=TOKEN_EXPIRY_TIME)}
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    return token

def decodeToken(token:Tokendatacheck,db:db_dependency):
    try:
        payload=jwt.decode(token.credentials,SECRET_KEY,algorithms=ALGORITHM)
        username=payload.get("sub")
        if not username:
            raise HTTPException (status_code=401,detail='invalid user')
        userdetail=db.query(User).filter(User.username==username).first()
        if not userdetail:
            raise HTTPException(status_code=401,detail='invalid user')
        return userdetail
    except JWTError:
        raise HTTPException(status_code=401,detail='invalid user')
