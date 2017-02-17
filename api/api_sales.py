#!/usr/bin/env python
import os
from datetime import datetime, timedelta, date

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from api_printer import printer_render
from models import *
from config import TWO_COPIES, NO_PRINT
from decimal import Decimal

ID_CLIENT_ANONYMOUS = 1

PATH = os.path.dirname(os.path.abspath(__file__))


class SaleApi(object):
    def __init__(self, price_total, client_id=ID_CLIENT_ANONYMOUS):
        self.price_total = price_total
        self.details = []
        self.client_id = client_id
        self.factura = None

    def generate_factura(self):
        self.factura = Factura(self.client_id, datetime.now())
        session.add(self.factura)
        session.flush()
        session.refresh(self.factura)

    # def get_client_anonymous():
    #     client = session.query(Cliente).get(ID_CLIENT_ANONYMOUS)
    #     return client

    def add_detail(self, id_product, quantity):
        product = session.query(Producto).get(id_product)
        assert quantity <= product.stock
        detail = Detalle(id_factura=self.factura.id, producto=product.id,
                         cantidad=quantity,
                         precio_total=float(quantity * product.precio_venta))
        self.details.append(
            (detail, [product.nombre, str(product.precio_venta)])
        )
        product.stock -= quantity
        session.add(detail)

    def add_detail_service(self, id_service=None,
                           type_service=None, quantity=1, canceled=False):
        if not id_service:
            service = Servicio(type_service, canceled, self.price_total)
            session.add(service)
            session.flush()
            session.refresh(service)
            type_service_obj = session.query(TipoServicio).get(type_service)
        else:
            service = session.query(Servicio).get(id_service)
            service.cancelado = canceled
            service.monto += Decimal(self.price_total)
            type_service_obj = session.query(TipoServicio).get(service.tipo)

        detail = Detalle(id_factura=self.factura.id, servicio=service.id,
                         cantidad=quantity, precio_total=self.price_total)

        self.details.append(
            (detail, [type_service_obj.nombre, str(self.price_total)])
        )
        session.add(detail)

    def save_sale(self):
        session.commit()

    def print_factura(self, parent=None):
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
        if not TWO_COPIES or NO_PRINT:
            printer_render(context, fontfullpath='fonts/DejaVuSans.ttf', fontsize=21)
            return

        img = printer_render(
            context, fontfullpath='fonts/DejaVuSans.ttf', fontsize=21)
        QtGui.QMessageBox.information(
            parent, 'Finalizado', 'Ticket Imprimido, entregue este ticket')
        printer_render(context, fontfullpath='fonts/DejaVuSans.ttf', fontsize=21,
                       img_default=img)
        QtGui.QMessageBox.information(
            parent, 'Finalizado', 'Ticket Imprimido, Guarde ticket')

    @staticmethod
    def get_quantity_product(id_product):
        product = session.query(Producto).get(id_product)
        return product.stock


def test_api():
    sale_api = SaleApi(float(3.0), 2)
    sale_api.generate_factura()
    sale_api.add_detail_service(type_service=None)
    sale_api.save_sale()