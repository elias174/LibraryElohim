import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from AddNewProduct import Add_New_Product

class ResultsButtonGroup(QtGui.QButtonGroup):
    def __init__(self, parent, results, layout):
        super(QtGui.QButtonGroup, self).__init__()
        self.parent = parent
        self.layout = layout
        self.refresh(results)

#   Maybe this should be change for personalize
    def refresh(self, results):
        n = 0
        rows = None
        cols = 4
        if len(results) % 4 == 0:
            rows = len(results)/4
        else:
            rows = (len(results)/4)+1
        j = 0
        for i in range(rows):
            for result in results[n:n+4]:
                button = QtGui.QPushButton(result.nombre, self.parent)
                self.addButton(button, result.id)
                self.layout.addWidget(button, i, j)
                j += 1
            j = 0
            n += 4


class Inventory_Tab(QtGui.QWidget):
    change_table = QtCore.pyqtSignal()

    def __init__(self):
        super(Inventory_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout

        # Signal to check total
        self.central_layout = QtGui.QGridLayout()

        self.product_group = QtGui.QGroupBox(str("Productos"), self)
        self.search_group = QtGui.QGroupBox(str("Busqueda"), self)

        self.central_layout.addWidget(self.search_group, 0, 0)
        self.central_layout.addWidget(self.product_group, 1, 0)

        self.initialize_product_group()
        self.initialize_results_group()

        #QtCore.QObject.connect(self.button_group, QtCore.SIGNAL("buttonClicked(int)"),
        #                       self, QtCore.SLOT("ResultButtonClick(int)"))

        self.change_table.connect(self.update_total)
        self.setLayout(self.central_layout)

    def add_new_product(self):
        window = Add_New_Product().exec_()

    def modify_product(self):
        return 

    def initialize_product_group(self):
        self.layout_line = QtGui.QFormLayout()
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setColumnCount(8)
        self.table_items.setRowCount(1)
        #Query
        self.NewProductoButton = QtGui.QPushButton("Agregar Nuevo Producto",self)
        self.NewProductoButton.clicked.connect(self.add_new_product)

        self.table_items.setHorizontalHeaderLabels(['ID', 'Categoria', 
                                                    'Nombre', 'Precio Compra',
                                                    'Precio Venta', 'Stock', 
                                                    'Detalle', 'Modificar'])
        #addin table with the query
        button = QtGui.QPushButton()
        button.clicked.connect(self.modify_product)
        button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        button.setIcon(QtGui.QIcon('icons/Icon_edit.png'))

        self.table_items.setItem(0, 1,
                                 QtGui.QTableWidgetItem("Categoria"))
        self.table_items.setItem(0, 2,
                                 QtGui.QTableWidgetItem("Nombre"))
        self.table_items.setItem(0, 3,
                                 QtGui.QTableWidgetItem("Precio Compra"))
        self.table_items.setItem(0, 4,
                                 QtGui.QTableWidgetItem("Precio Venta"))
        self.table_items.setItem(0, 5,
                                 QtGui.QTableWidgetItem("Precio Stock"))
        self.table_items.setItem(0, 6,
                                 QtGui.QTableWidgetItem("Precio Detalle"))
        self.table_items.setCellWidget(0, 7, button)
        
        #self.layout_line.addRow(self.label_search, self.edit_search)
        self.layout_line.addRow(self.table_items)
        self.layout_line.addRow(self.NewProductoButton)
        
        self.product_group.setLayout(self.layout_line)

#        to connect the text_search
    def initialize_results_group(self):
        self.layout_line_results = QtGui.QFormLayout()

        self.label_search = QtGui.QLabel("Buscar Producto:", self)
        self.edit_search = QtGui.QLineEdit(self)

        self.layout_line_results.addRow(self.label_search, self.edit_search)

        self.search_group.setLayout(self.layout_line_results)

        #self.button_group = ResultsButtonGroup(self, self.last_query,
        #                                       self.layout_results)
        #self.layout_line_results.addRow(self.layout_results)
        #self.results_group.setLayout(self.layout_line_results)

        #self.edit_search.textChanged.connect(self.on_search_edit_changed)
        #self.edit_search_added.textChanged.connect(self.on_search_edit_added_changed)

    @QtCore.pyqtSlot(int)
    def ResultButtonClick(self, id):
        product = session.query(Producto).get(id)
        product_name = str(product.nombre)
        items = self.table_items.findItems(product_name, QtCore.Qt.MatchExactly)
        if items:
            ok = QtGui.QMessageBox.question(self, u'Doble Producto',
                                            "Desea Agregarlo de nuevo?",
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
            if ok == QtGui.QMessageBox.Yes:
                self.add_product_table(product)
                self.product_total+=1
            else:
                return
        else:
            self.add_product_table(product)
            self.product_total+=1

    def on_search_edit_changed(self, string):
        text_query = '%'+unicode(string.toUtf8(), encoding="UTF-8")+'%'
        self.last_query = (session.query(Producto)
                           .filter(Producto.nombre.like(text_query)).all())
        for i in reversed(range(self.layout_results.count())):
            self.layout_results.itemAt(i).widget().setParent(None)
        self.button_group.refresh(self.last_query)

    def on_search_edit_added_changed(self, string):
        for row in xrange(self.table_items.rowCount()):
                self.table_items.showRow(row)
        if string != '':
            to_hide = []
            items = [item.row()
                     for item in self.table_items.findItems(string, QtCore.Qt.MatchContains)
                     if item.column() == 1]
            for row in xrange(self.table_items.rowCount()):
                if not (row in items):
                    self.table_items.hideRow(row)

    def update_total(self):
        index_price = 3
        price = 0
        for row in xrange(self.table_items.rowCount()):
            item = self.table_items.item(row, index_price)
            price += float(item.text())
        self.total_line.setText(QtCore.QString(str(price)))