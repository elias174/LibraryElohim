import os, sys
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo=False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


def gainings_by_month(year, month = None, day = None):
	if(month == None and day == None):
		day_query = '%'+str(year)+'%'
	elif (day == None):
		day_query = '%'+str(year)+'%'+'%-'+str(month)+'-%'
	else:
		day_query = '%'+str(year)+'%'+'%-'+str(month)+'-%'+'%'+str(day)+'%'
	print day_query
	final_query = (session.query(Factura, Detalle.cantidad, Producto.id, Producto.precio_compra, Producto.precio_venta).join(Detalle, Factura.id==Detalle.factura).\
					filter(Factura.fecha.like(day_query)).\
					join(Producto, Detalle.producto==Producto.id)).all()
	list_query = []
	for que in range(len(final_query)):
		print final_query[que].cantidad, final_query[que].id, final_query[que].precio_compra, final_query[que].precio_venta
		result = {'cantidad':final_query[que].cantidad, 'producto':final_query[que].id, 
				'p_total_compra':final_query[que].precio_compra, 'p_total_venta':final_query[que].precio_venta,
				'utilidad':final_query[que].precio_venta-final_query[que].precio_compra}
		list_query.append(result)
	return list_query
