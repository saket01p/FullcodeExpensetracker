from fastapi import APIRouter,HTTPException,status,Depends
from models import User,Expense
from schemes import Userdatacheck,UserOut,ExpenseOut
from auth import db_dependency,form_data
from auth import pass_check
import auth
import schemes
import models
from typing import Annotated

router=APIRouter()

@router.post("/Register",response_model=UserOut)
def registerUser(user:Userdatacheck,db:db_dependency):
    check=db.query(User).filter(User.username==user.username).first()
    if check:
        raise HTTPException(status_code =401,detail='User already exists')

    user_model=User(username=user.username,hashed_password=pass_check.hash(user.password))
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model

@router.post("/login" ,response_model=schemes.Tokencheck)
def UserLogin(user:form_data,db:db_dependency):
    userdata=db.query(User).filter(User.username==user.username).first()
    if not userdata:
        raise HTTPException(status_code=401,detail='invalid user')
    if not pass_check.verify(user.password,userdata.hashed_password):
        raise HTTPException(status_code=401,detail='invalid user')
    Token=auth.getToken(user.username,userdata.id)
    return {"access_token":Token,"token_type":"bearer"}

@router.post("/expenseData",response_model=schemes.ExpenseOut)
def GetExpenseadata(expensedata:schemes.Expense,db:db_dependency,user:Annotated[models.User,Depends(auth.decodeToken)]):
    userdata=db.query(User).filter(User.username==user.username).first()
    if userdata is None:
        raise HTTPException(status_code=401,detail="User not found")
    model_expense=Expense(amount=expensedata.amount,title=expensedata.title,user_id=user.id)
    db.add(model_expense)
    db.commit()
    db.refresh(model_expense)
    db.close()
    return model_expense
    



