import database
from database import engine,sessionLocal,Base
from sqlalchemy import Column,Integer,String,ForeignKey,Float
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True)
    hashed_password=Column(String)

    expenses=relationship("Expense",back_populates="owner")

class Expense(Base):
    __tablename__='expenses'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    amount=Column(Float)
    user_id=Column(Integer,ForeignKey("users.id"))

    owner=relationship("User",back_populates='expenses')