from specialized_models import *

import datetime
import collections

class GainingsApi:

    def __init__(self):
        self.result_query = []

    def gainings_by_date(self, type, year, month = None, day = None):
        year_query = int(year)
        filtered_detalles = None

        if type == "Libreria":
            filtered_detalles = session.query(Detalle).join(Factura).filter(
                extract('year', Factura.fecha) == year_query).filter(
                Detalle.producto != None)

        elif type == "Servicios":
            filtered_detalles = session.query(Detalle).join(Factura).filter(
                extract('year', Factura.fecha) == year_query).filter(
                Detalle.servicio != None)

        # filtered_detalles = session.query(Detalle).join(Factura).filter(
        #     extract('year', Factura.fecha) == year_query)

        if month is not None:
            month_query = int(month)
            filtered_detalles = filtered_detalles.filter(
                extract('month', Factura.fecha) == month_query)

        if day is not None:
            day_query = int(day)
            filtered_detalles = filtered_detalles.filter(
                extract('day', Factura.fecha) == day_query)

        if type == "Libreria":
            results = {
            }
            for detalle in filtered_detalles:
                try:
                    results[str(detalle.producto)]['cantidad'] += detalle.cantidad
                    results[str(detalle.producto)]['p_total_venta'] += detalle.precio_total

                except KeyError:
                    results.update(
                        {
                            str(detalle.producto):{
                                'cantidad': detalle.cantidad,
                                'producto': detalle.producto,
                                'p_total_compra': (
                                    0
                                ),
                                'p_total_venta': detalle.precio_total,
                                'utilidad': 0

                            }
                        }
                    )

            self.result_query = results.values()

        elif type == "Servicios":
            results_service = {
            }
            for detalle in filtered_detalles:
                servicio = session.query(Servicio).get(detalle.servicio)
                try:
                    results_service[str(servicio.tipo)]['cantidad'] += detalle.cantidad
                    results_service[str(servicio.tipo)]['utilidad'] += detalle.precio_total

                except KeyError:
                    results_service.update(
                        {
                            str(servicio.tipo):{
                                'servicio': servicio.tipo,
                                'cantidad': detalle.cantidad,
                                'utilidad': detalle.precio_total
                            }
                        }
                    )
            self.result_query = results_service.values()
            
        assert len(self.result_query) > 0

    def export_xlsx(self, file_name):
        print len(self.result_query)
