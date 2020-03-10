import os
import sys
from sqlalchemy import Column,ForeignKey,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,backref
from sqlalchemy import create_engine
from flask_login import UserMixin

Base=declarative_base()

engine = create_engine('sqlite:///practice.db')


class Register(Base,UserMixin):
	__tablename__='signup_data'
	id=Column(Integer,primary_key=True)
	Fname=Column(String(20))
	Lname=Column(String(20))
	image=Column(String(150),nullable=False)
	username=Column(String(100))
	Email=Column(String(100),unique=True)
	Adharno=Column(String(50),unique=True)
	Password=Column(String(50),nullable=False)
class ComplaintBox(Base):
	__tablename__='complaintbox'
	id = Column(Integer,primary_key=True)
	Sector=Column(String(500))
	Sector_area=Column(String(250),nullable=False)
	complaint=Column(String(450),nullable=False)
	image1=Column(String(3050))
class Areas(Base):
	__tablename__='areas'
	id = Column(Integer,primary_key=True)
	Sector=Column(String(500))
	area=Column(String(250),nullable=False)
	contact=Column(Integer)
	email1=Column(String(100),nullable=False)
	email2=Column(String(100),nullable=False)
	


Base.metadata.create_all(engine)	
	


	