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


class SaleApi(object):
    def __init__(self, price_total, client_id=None):
        self.price_total = price_total
        self.client_id = None
        self.details = []

    def generate_factura():
        self.factura = Factura(self.client_id, datetime.utcnow())
        session.add(self.factura)
        return self.factura

    def add_detail(id_product, quantity):
        product = session.query(Producto).get(id_product)
        assert quantity >= product.stock
        detail = Detalle(self.factura.id, quantity,
                         float(quantity * product.precio_venta))
        self.details.append(detail)
        session.add(detail)