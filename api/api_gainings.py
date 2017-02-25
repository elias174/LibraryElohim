import os, sys
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
# from models import *
from models import *

class GainingsApi:

    def __init__(self):
        self.result_query = []

    def gainings_by_date(self, type, year, month = None, day = None):
        if not month and not day:
            day_query = '%'+str(year)+'%'

        elif not day:
            day_query = '%'+str(year)+'%'+'%-'+str(month).zfill(2)+'-%'

        else:
            day_query = '%'+str(year)+'%'+'%-'+str(month).zfill(2)+'-%'+'%'+str(day).zfill(2)+'%'

        if type == "Libreria":
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
            self.result_query = list_query
        elif type == "Servicios":
            final_query = (
                session.query(Factura, Factura.cliente ,Servicio.tipo, Detalle.precio_total).join(
                    Detalle, Factura.id == Detalle.factura).filter(Factura.fecha.like(day_query)).join(
                    Servicio, Detalle.servicio == Servicio.id)).all()
            list_query = []
            for query_ in range(len(final_query)):
                result = {'cliente':final_query[query_].cliente,'servicio':final_query[query_].tipo,
                        'utilidad':final_query[query_].precio_total}
                list_query.append(result)
            self.result_query = list_query
            
        assert len(self.result_query) > 0

    def export_xlsx(self, file_name):
        print len(self.result_query)
