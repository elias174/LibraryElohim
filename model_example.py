#(leaves out sqlalchemy & PyQt boilerplate, will not run)
#Define SQL Alchemy model
from qvariantalchemy import String, Integer, Boolean
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PyQt4 import QtCore, QtGui

Base = declarative_base()

class Entity(Base):
	__tablename__ = 'entities'

	ent_id = Column(Integer, primary_key=True)
	name = Column(String)
	enabled = Column(Boolean)
	
	def __init__(self,name,enabled):
		self.name = name
		self.enabled = enabled

#create QTable Model/View
engine = create_engine('sqlite:///D:\\data.db', echo=True)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from alchemical_model import AlchemicalTableModel
model = AlchemicalTableModel(
    session, #FIXME pass in sqlalchemy session object
    session.query(Entity), #sql alchemy mapped object
    [ # list of column 4-tuples(header, sqlalchemy column, column name, extra parameters as dict
      # if the sqlalchemy column object is Entity.name, then column name should probably be name,
      # Entity.name is what will be used when setting data, and sorting, 'name' will be used to retrieve the data.
        ('Entity Name', Entity.name, 'name', {'editable': True}),
        ('Enabled', Entity.enabled, 'enabled', {}),
    ])

ind = model.createIndex(0,0)
print len(model.results)