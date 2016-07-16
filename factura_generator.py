from PyQt4 import QtGui
from PyQt4 import QtCore
from collections import namedtuple
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class GeneratorFactura():
    def __init__(self, table_items):
                        
        pass
