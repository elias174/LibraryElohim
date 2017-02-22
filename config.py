from escpos.printer import Serial
from escpos.printer import Usb
from datetime import datetime, timedelta

from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


# You need use the correct interface
# PRINTER = Usb(0x04b8, 0x0e15)
PRINTER = None
NO_PRINT = True
# PRINTER = Serial('COM1')
TWO_COPIES = False
TIME_OUT_PRINTER = 7
# you need change the parameters for the db

user_db = 'root'
password_db = 'sergio092005'
host = 'localhost'
database_name = 'libreria_elohim'

ALCHEMY_BASE = declarative_base()

# you can change the database engine (for ex if you use sqlite)
# its recommended use mysql for major performance
db = create_engine('mysql://%s:%s@%s/%s' % (user_db, password_db, host, database_name), echo=False)
ALCHEMY_METADATA = MetaData(db)
Session = sessionmaker(bind=db, autoflush=True, autocommit=False, expire_on_commit=True)
ALCHEMY_SESSION = scoped_session(Session)
