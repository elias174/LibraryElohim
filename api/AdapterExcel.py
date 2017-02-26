import sys
import openpyxl

from models import *

# Base = declarative_base()
#
# db = create_engine('sqlite:///dataBase.db', echo=False, encoding='utf8')
# metadata = MetaData(db)
#
# Session = sessionmaker(bind=db)
#
# session = Session()

reload(sys)
sys.setdefaultencoding('utf8')


class NotFilledError(Exception):
    pass


class Adapter_XLSX:
    def __init__(self, file_name):
        self.default_categoria = self.get_or_create_category('Utiles Libreria')
        self.productos = []
        self.dict_data = {}
        self.generate_sheet(file_name)

    def get_or_create_category(self, name):
        instance = session.query(Categoria).filter_by(nombre=name).first()
        if instance:
            return instance
        else:
            category = Categoria(
                name, 'Venta libreria')
            session.add(category)
            session.flush()
            session.refresh(category)
            return category

    def generate_sheet(self, name_file):
        wb = openpyxl.load_workbook(name_file)
        self.sheet = wb.get_sheet_by_name(wb.get_sheet_names()[0])

    def extract_data(self):
        # assert(self.categoria)
        for row in range(2, self.sheet.max_row + 1):
            articulo = self.sheet['A' + str(row)].value
            marca = self.sheet['B' + str(row)].value
            cantidad = self.sheet['C' + str(row)].value
            p_compra = self.sheet['D' + str(row)].value
            p_venta = self.sheet['E' + str(row)].value
            categoria = self.sheet['F' + str(row)].value

            if not articulo:
                raise NotFilledError(
                    'Revisar fila %s columna Articulo' % str(row))
            if cantidad < 0:
                raise NotFilledError(
                    'Revisar fila %s columna Cantidad' % str(row))
            if p_compra < float(0):
                raise NotFilledError(
                    'Revisar fila %s columna P.Compra' % str(row))
            if p_venta < float(0):
                raise NotFilledError(
                    'Revisar fila %s columna P.Venta' % str(row))

            articulo = articulo.capitalize()
            if marca:
                articulo = '%s %s' % (articulo, marca.capitalize())
            categoria_id = self.default_categoria.id
            if categoria:
                categoria_id = self.get_or_create_category(categoria).id
            producto = Producto(
                categoria_id,
                articulo,
                float(p_compra),
                float(p_venta),
                int(cantidad),
                'Producto Nuevo'
            )
            self.productos.append(producto)

    def save_products(self):
        self.extract_data()
        if len(self.productos) <= 0:
            raise NotFilledError('No existe ningun Producto en su XLSX')
        for producto in self.productos:
            session.add(producto)
        session.commit()
