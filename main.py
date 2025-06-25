from fastapi import FastAPI
from routes import router
import routes
import models
from database import Base,engine

app=FastAPI()

models.Base.metadata.create_all(bind=engine)
app.include_router(router)
