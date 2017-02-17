from  datetime import date
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship, mapper
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *


# class MyWindow(QWidget):
#     def __init__(self, *args):
#         QWidget.__init__(self, *args)
# 
#         header_names = ['ID', 'Categoria', 'Nombre', 'Precio Compra',
#                         'Precio Venta', 'Stock', 'Detalle']
#         self.tablemodel = MyTableModel(Producto, my_array, header_names, self)
#         self.tableview = QTableView()
#         self.tableview.setModel(self.tablemodel)
# 
#         self.proxy = QtGui.QSortFilterProxyModel(self)
#         self.proxy.setSourceModel(self.tablemodel)
#         line_edit = QtGui.QLineEdit()
#         line_edit.textChanged.connect(self.on_text_changed)
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.tableview)
#         layout.addWidget(line_edit)
#         self.setLayout(layout)
# 
#     def on_text_changed(self, text):
#         self.tablemodel.setFilter('nombre', text)


class MyTableModel(QAbstractTableModel):

    MAPPER_TYPES = {
        'False': 'No',
        'True': 'Si'
    }

    def __init__(self, model_alchemy, header_names, parent = None,
                 custom_query = None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.model_alchemy = model_alchemy
        self.exist_custom_query = (True
                                   if custom_query >= 0
                                   else False)
        self.custom_query = custom_query
        self.last_query = (
            custom_query if self.exist_custom_query
            else(session.query(model_alchemy).limit(20).all()))

        self.foreign_keys = {k.parent.key: k.column.table for k in
                             list(self.model_alchemy.__table__.foreign_keys)}

        self.arraydata = self.last_query
        self.header_names = header_names
        self.columns_name = model_alchemy.__table__.columns.keys()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_names[col])
        return QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.arraydata)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self.header_names)

    def data(self, index, role):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        row = self.arraydata[index.row()]

        if self.columns_name[index.column()] in self.foreign_keys:
            id_obj = getattr(row, self.columns_name[index.column()])
            value = self.foreign_keys[self.columns_name[index.column()]]

            # maybe this is evil
            class AbstractClassForeign(object):
                pass

            mapper(AbstractClassForeign, value)
            obj_foreign = session.query(AbstractClassForeign).get(id_obj)
            try:
                ret = obj_foreign.nombre
            except AttributeError:
                ret = value
            return ret

        ret = (str(getattr(row, self.columns_name[index.column()])))
        return self.MAPPER_TYPES.get(ret, ret)

    def get_id_object_alchemy(self, row):
        id_product = getattr(self.arraydata[row], self.columns_name[0])
        return id_product

    def get_specific_data_alchemy(self, row, col):
        data = getattr(self.arraydata[row], self.columns_name[col])
        return data

    def setFilter(self, name_column, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        obj_column = getattr(self.model_alchemy, name_column)

        self.arraydata = (
            self.custom_query.filter(obj_column.like(text_query)).all()
            if self.exist_custom_query
            else
            session.query(self.model_alchemy).filter(obj_column.like(text_query)).all()
        )
        self.layoutChanged.emit()

    def clear(self):
        self.arraydata = []
        self.layoutChanged.emit()

    def refresh_data(self, array_data=None):
        if self.exist_custom_query:
            self.arraydata = array_data
        else:
            self.arraydata = (session.query(self.model_alchemy).limit(20).all())

        self.layoutChanged.emit()

    def searchBillToday(self, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        today = '%'+str(date.today())+'%'
        self.arraydata = (session.query(Factura)
                        .filter(Factura.id.like(text_query))
                        .filter(Factura.fecha.like(today)).all())
        self.layoutChanged.emit()

    def searchBillDay(self, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        self.arraydata = (session.query(Factura)
                        .filter(Factura.fecha.like(text_query)).all())
        self.layoutChanged.emit()

    def searchCashDay(self, search_text=None):
        text_query = '%'+unicode(search_text.toUtf8(), encoding="UTF-8")+'%'
        self.arraydata = (session.query(Caja)
                        .filter(Caja.fecha.like(text_query)).all())
        self.layoutChanged.emit()