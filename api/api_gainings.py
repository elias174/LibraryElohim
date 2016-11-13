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
    if not month and not day:
        day_query = '%'+str(year)+'%'

    elif not day:
        day_query = '%'+str(year)+'%'+'%-'+str(month)+'-%'

    else:
        day_query = '%'+str(year)+'%'+'%-'+str(month)+'-%'+'%'+str(day)+'%'
    final_query = (
        session.query(Factura, Detalle.cantidad, Producto.id, Producto.precio_compra, Producto.precio_venta).join(
            Detalle, Factura.id == Detalle.factura).filter(Factura.fecha.like(day_query)).join(
            Producto, Detalle.producto==Producto.id)).all()
    list_query = []
    for query_ in range(len(final_query)):
        result = {'cantidad':final_query[query_].cantidad, 'producto':final_query[query_].id,
                'p_total_compra':final_query[query_].precio_compra, 'p_total_venta':final_query[query_].precio_venta,
                'utilidad':final_query[query_].precio_venta-final_query[query_].precio_compra}
        list_query.append(result)
    return list_query
