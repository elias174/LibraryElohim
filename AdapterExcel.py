import openpyxl

from models import *

from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo=False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)

session = Session()


CATEGORIA_ID = 1


class Adapter_XLSX:
    def __init__(self, file_name, sheet, id_categoria=CATEGORIA_ID):
        self.categoria = id_categoria
        self.productos = []
        self.dict_data = {}
        self.generate_sheet(file_name, sheet)

    def generate_sheet(self, name_file, sheet):
        wb = openpyxl.load_workbook(name_file)
        self.sheet = wb.get_sheet_by_name(sheet)

    def extract_data(self):
        for row in range(2, self.sheet.max_row + 1):
            articulo = self.sheet['A' + str(row)].value
            marca = self.sheet['B' + str(row)].value
            cantidad = self.sheet['C' + str(row)].value
            p_compra = self.sheet['D' + str(row)].value
            p_venta = self.sheet['E' + str(row)].value
            assert articulo
            assert cantidad
            assert p_compra
            assert p_venta
            articulo = articulo.capitalize()
            if marca:
                articulo = '%s %s' % (articulo, marca.capitalize())
            producto = Producto(
                self.categoria,
                articulo,
                float(p_compra),
                float(p_venta),
                int(cantidad),
                'Producto Nuevo'
            )
            self.productos.append(producto)

    def save_products(self):
        assert len(self.productos) > 0
        for producto in self.productos:
            session.add(producto)
        session.commit()


ad = Adapter_XLSX('inventario_aug.xlsx', 'libreria')
ad.extract_data()
ad.save_products()