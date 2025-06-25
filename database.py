from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL="postgresql://postgres:saket1234@database-1.cxckkueqetdr.eu-west-1.rds.amazonaws.com:5432/ExpenseTrackerDatabase"


engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(bind=engine)

Base=declarative_base()
