#!/usr/bin/env python
import os
from datetime import datetime, timedelta, date

from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo=False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

ID_CLIENT_ANONYMOUS = 1

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)


class SaleApi(object):
    def __init__(self, price_total, client_id=ID_CLIENT_ANONYMOUS):
        self.price_total = price_total
        self.details = []
        self.client_id = client_id
        self.factura = None

    def generate_factura(self):
        self.factura = Factura(self.client_id, datetime.utcnow())
        session.add(self.factura)
        session.flush()
        session.refresh(self.factura)

    # def get_client_anonymous():
    #     client = session.query(Cliente).get(ID_CLIENT_ANONYMOUS)
    #     return client

    def add_detail(self, id_product, quantity):
        product = session.query(Producto).get(id_product)
        assert quantity <= product.stock
        detail = Detalle(self.factura.id, product.id, quantity,
                         float(quantity * product.precio_venta))
        self.details.append((detail, product))
        product.stock -= quantity
        session.add(detail)

    def save_sale(self):
        session.commit()

    def print_factura(self):
        client = session.query(Cliente).get(self.client_id)
        assert len(self.details) > 0

        def render_template(template_filename, context):
            return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

        file_output = "ouput_factura.txt"
        context = {
            'factura': self.factura,
            'details': self.details,
            'client': client,
            'price_total': self.price_total
        }
        with open(file_output, 'w') as f:
            html = render_template('factura.txt', context)
            f.write(html)

    @staticmethod
    def get_quantity_product(id_product):
        product = session.query(Producto).get(id_product)
        return product.stock


def test_api():
    sale_api = SaleApi(float(14.5))
    sale_api.generate_factura()
    sale_api.add_detail(3, 2)
    sale_api.add_detail(4, 1)
    sale_api.save_sale()
