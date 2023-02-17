from sqlalchemy import String,Column,Integer
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=True,default="",unique=True)
    first_name = Column(String,nullable=True,default="")
    last_name = Column(String, nullable=True,default="")
    email = Column(String,unique=True,index=True,default="")
    password = Column(String)
