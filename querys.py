#!/usr/bin/env python
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


client = Cliente('user1', 'apellido', 'av alto', date(1995,4,12), 986141682)
print(client.id_cliente, client.nombre)
session.add(client)
session.commit()

qr = session.query(Cliente).filter(Cliente.id_cliente == 1)

'''
result = Cliente.insert().returning(Cliente.id_cliente, Cliente.nombre).values(nombre='user1', apellido='apellido', direccion='av alto',fecha_nacimiento=date(1995,4,12), telefono=986141682)
print result.fetchall()'''


