#!/usr/bin/env python
import os
from datetime import datetime, timedelta, date

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from api_printer import printer_render
from models import *
from decimal import Decimal

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo=False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

ID_CLIENT_ANONYMOUS = 1

PATH = os.path.dirname(os.path.abspath(__file__))
# TEMPLATE_ENVIRONMENT = Environment(
#     autoescape=False,
#     loader=FileSystemLoader(os.path.join(PATH, 'templates')),
#     trim_blocks=False)


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

    def add_detail_service(self, id_service=None,
                           type_service=None, quantity=1, canceled=False):
        if not id_service:
            service = Servicio(type_service, canceled, self.price_total)
            session.add(service)
            session.flush()
            session.refresh(service)
        else:
            service = session.query(Servicio).get(id_service)
            service.cancelado = canceled
            service.monto += Decimal(self.price_total)

        detail = Detalle(id_factura=self.factura.id, servicio=service.id,
                         cantidad=quantity, precio_total=self.price_total)
        self.details.append((detail, service))
        session.add(detail)

    def save_sale(self):
        session.commit()

    def print_factura(self):
        client = session.query(Cliente).get(self.client_id)
        assert len(self.details) > 0

        # def render_template(template_filename, context):
        #     return TEMPLATE_ENVIRONMENT.get_template(
        # template_filename).render(context)
        # file_output = "output_factura.txt"

        context = {
            'factura': self.factura,
            'details': self.details,
            'client': client,
            'price_total': self.price_total
        }
        # with open(file_output, 'w') as f:
        #     html = render_template('factura.txt', context)
        #     f.write(html)
        printer_render(context, fontfullpath='DejaVuSans.ttf', fontsize=21)

    @staticmethod
    def get_quantity_product(id_product):
        product = session.query(Producto).get(id_product)
        return product.stock


def test_api():
    sale_api = SaleApi(float(3.0), 2)
    sale_api.generate_factura()
    sale_api.add_detail_service(type_service=None)
    sale_api.save_sale()