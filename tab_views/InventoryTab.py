import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from AddNewProduct import Add_New_Product
from ModifyProduct import Modify_Product
from Generic_forms import GenericFormDialog

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class Inventory_Tab(QtGui.QWidget):
    change_table = QtCore.pyqtSignal()

    def __init__(self):
        super(Inventory_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout

        # Signal to check total
        self.central_layout = QtGui.QGridLayout()

        self.control_singleton = False

        self.product_group = QtGui.QGroupBox(str("Productos"), self)
        self.search_group = QtGui.QGroupBox(str("Busqueda"), self)

        self.central_layout.addWidget(self.search_group, 0, 0)
        self.central_layout.addWidget(self.product_group, 1, 0)

        self.initialize_product_group()
        self.initialize_results_group()

        self.setLayout(self.central_layout)

    def add_new_product(self):
        data, window = GenericFormDialog.get_data(Producto, self)
        if window:
            session.add(Producto(data['categoria'], data['nombre'], 
                                    data['precio_compra'],data['precio_venta'],
                                    data['stock'],data['detalle']))
            session.commit()

    def modify_product(self):
        button = qApp.focusWidget()
        index = self.table_items.indexAt(button.pos())
        if index.isValid():
            product = self.query[index.row()]
            data, window = GenericFormDialog.get_data(Producto, self, product)
            if window:
                product.categoria = data['categoria']
                product.precio_compra = data['precio_compra']
                product.precio_venta = data['precio_venta']
                product.nombre = data['nombre']
                product.detalle = data['detalle']
                product.stock = data['stock']
                session.commit()
                self.refresh_table()

    def initialize_product_group(self):
        self.layout_line = QtGui.QVBoxLayout()

        #Creating table
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table_items.setRowCount(0)

        self.table_items.setColumnCount(8)
        self.table_items.setHorizontalHeaderLabels(['ID', 'Categoria', 
                                                    'Nombre', 'Precio Compra',
                                                    'Precio Venta', 'Stock', 
                                                    'Detalle', 'Modificar'])
        header = self.table_items.horizontalHeader()
        header.setResizeMode(QHeaderView.Stretch)
        self.stringRow = ''

        self.table_items.setVerticalHeaderLabels(QString(self.stringRow).split(','))

        self.NewProductoButton = QtGui.QPushButton("Agregar Nuevo Producto", self)
        self.NewProductoButton.clicked.connect(self.add_new_product)

        self.layout_line.addWidget(self.table_items)
        self.layout_line.addWidget(self.NewProductoButton)
        self.product_group.setLayout(self.layout_line)
        self.refresh_table()

    def clear_table(self):
        self.table_items.clear();
        self.table_items.setRowCount(0);
        self.table_items.setColumnCount(8)
        self.table_items.setHorizontalHeaderLabels(['ID', 'Categoria', 
                                                    'Nombre', 'Precio Compra',
                                                    'Precio Venta', 'Stock', 
                                                    'Detalle', 'Modificar'])

    def refresh_table(self, string=None):
        self.clear_table()
        if string:
            text_query = '%'+unicode(string.toUtf8(), encoding="UTF-8")+'%'
            if self.search_name.isChecked():
                self.query = (session.query(Producto).filter(
                    Producto.nombre.like(text_query)).all())
            elif self.search_category.isChecked():
                self.query = (session.query(Producto).join(Categoria).filter(
                    Categoria.nombre.like(text_query)).all())
            elif self.search_min_stock.isChecked():
                text_query = unicode(string.toUtf8(), encoding="UTF-8")
                self.query = (session.query(Producto).filter(
                    Producto.stock <= text_query).all())
            elif self.search_max_stock.isChecked():
                text_query = unicode(string.toUtf8(), encoding="UTF-8")
                self.query = (session.query(Producto).filter(
                    Producto.stock >= text_query).all())
        else:
            self.query = (session.query(Producto).limit(20).all())

        self.table_items.setRowCount(len(self.query))
        self.stringRow = ''
        for product in range(len(self.query)):
            self.table_items.setItem(product, 0,
                                     QtGui.QTableWidgetItem(str(self.query[product].id)))

            category_name = (session.query(Categoria).get(
                self.query[product].categoria)).nombre

            self.table_items.setItem(product, 1,
                                     QtGui.QTableWidgetItem(str(category_name)))
            self.table_items.setItem(product, 2,
                                     QtGui.QTableWidgetItem(str(self.query[product].nombre)))
            self.table_items.setItem(product, 3,
                                     QtGui.QTableWidgetItem(str(self.query[product].precio_compra)))
            self.table_items.setItem(product, 4,
                                     QtGui.QTableWidgetItem(str(self.query[product].precio_venta)))
            self.table_items.setItem(product, 5,
                                     QtGui.QTableWidgetItem(str(self.query[product].stock)))
            self.table_items.setItem(product, 6,
                                     QtGui.QTableWidgetItem(str(self.query[product].detalle)))
            buttonModify = QtGui.QPushButton()
            buttonModify.clicked.connect(self.modify_product)
            buttonModify.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            buttonModify.setIcon(QtGui.QIcon('icons/Icon_edit.png'))
            self.table_items.setCellWidget(product, 7, buttonModify)
            self.stringRow = self.stringRow + str(product+1) + ','

        self.table_items.setVerticalHeaderLabels(QString(self.stringRow).split(','))

    def initialize_results_group(self):
        self.layout_line_results = QtGui.QFormLayout()

        self.label_search = QtGui.QLabel("Buscar Producto:", self)
        self.edit_search = QtGui.QLineEdit(self)

        self.search_name = QRadioButton("Buscar por nombre")
        self.search_name.setChecked(True)
        self.search_category = QRadioButton("Buscar por Categoria")
        self.search_min_stock = QRadioButton("Buscar los de Menor Stock")
        self.search_max_stock = QRadioButton("Buscar los de Mayor Stock")

        self.layout_line_results.addRow(self.label_search, self.edit_search)
        self.layout_line_results.addRow(self.search_name, self.search_category)
        self.layout_line_results.addRow(self.search_min_stock, self.search_max_stock)
        self.search_group.setLayout(self.layout_line_results)
        self.edit_search.textChanged.connect(self.on_search_table_edit_changed)

    def on_search_table_edit_changed(self, string):
        self.refresh_table(string)