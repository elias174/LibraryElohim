import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from models_qt import MyTableModel

# Base = declarative_base()
# 
# db = create_engine('sqlite:///dataBase.db', echo = False)
# metadata = MetaData(db)
# 
# Session = sessionmaker(bind=db)
# session = Session()


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


class Sale_Tab(QtGui.QWidget):
    change_table = QtCore.pyqtSignal()

    def __init__(self):
        super(Sale_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout

        # Signal to check total
        self.last_query = (session.query(Producto).limit(12).all())

        self.central_layout = QtGui.QGridLayout()

        self.sale_group = QtGui.QGroupBox(str("Venta"), self)
        self.search_group = QtGui.QGroupBox(str("Busqueda"), self)

        self.central_layout.addWidget(self.sale_group, 0, 0)
        self.central_layout.addWidget(self.search_group, 0, 1)

        self.initialize_sale_group()
        self.initialize_search_group()

        #QtCore.QObject.connect(self.button_group, QtCore.SIGNAL("buttonClicked(int)"),
        #                      self, QtCore.SLOT("ResultButtonClick(int)"))
        self.change_table.connect(self.update_total)
        self.setLayout(self.central_layout)

    def initialize_sale_group(self):
        self.layout_line = QtGui.QFormLayout()
        # First Line
        # self.label_search = QtGui.QLabel("Buscar Producto:", self)
        # self.edit_search = QtGui.QLineEdit(self)
        # self.edit_search.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, 
        #                                                  QtGui.QSizePolicy.Fixed))
        # Second Line
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setColumnCount(5)
        self.table_items.setRowCount(0)

        self.table_items.setHorizontalHeaderLabels(["Cantidad", "Producto",
                                                    "P.Unidad", "P.Total",
                                                    "Eliminar"])

        self.layout_line.addRow(self.table_items)

        self.sale_group.setMaximumWidth(self.screenGeometry.width() / 2)
        self.sale_group.setLayout(self.layout_line)

        #third line, 4th line
        self.edit_search_added = QtGui.QLineEdit(self)
        self.label_search_added = QtGui.QLabel("Buscar en Aniadidos:", self)
        self.total_line = QtGui.QLabel("0.00", self)
        self.pay_line = QtGui.QLabel("0.00", self)
        self.layout_line.addRow(self.label_search_added, self.edit_search_added)
        self.layout_line.addRow("Total: ", self.total_line)
        self.layout_line.addRow("A pagar: ", self.pay_line)

#        to connect the text_search
    def initialize_search_group(self):
        self.layout_line_search = QtGui.QFormLayout()

        self.label_search = QtGui.QLabel("Buscar Producto:", self)
        self.label_type_view = QtGui.QLabel("Tipo de Vista:", self)
        self.results_group = QtGui.QGroupBox(str("Resultados:"), self)

        self.edit_search = QtGui.QLineEdit(self)
        self.combo_type_search = QtGui.QComboBox()
        self.combo_type_search.addItem("Botones")
        self.combo_type_search.addItem("Tabla")
        self.combo_type_search.setMaximumWidth(100)

        self.layout_line_search.addRow(self.label_search, self.edit_search)
        self.layout_line_search.addRow(self.label_type_view, self.combo_type_search)

        header_names = ['ID', 'Categoria', 'Nombre', 'Precio Compra',
                        'Precio Venta', 'Stock', 'Detalle']
        self.tablemodel = MyTableModel(Producto, header_names, self)
        self.layout_results = QtGui.QGridLayout()
        self.results_group.setLayout(self.layout_results)
        self.results_group.setMinimumHeight(self.screenGeometry.height() -
                                            (self.screenGeometry.height() / 3.5))

        self.button_add_table = QtGui.QPushButton('Aniadir')

        def view_buttons():
            QtGui.QWidget().setLayout(self.layout_results)
            self.layout_results = QtGui.QGridLayout()
            self.results_group.setLayout(self.layout_results)
            self.button_group = ResultsButtonGroup(self, self.last_query,
                                                   self.layout_results)
            QtCore.QObject.connect(self.button_group,
                                   QtCore.SIGNAL("buttonClicked(int)"), self,
                                   QtCore.SLOT("ResultButtonClick(int)"))
            self.edit_search.textChanged.connect(self.on_search_edit_changed)

        def view_table():
            self.tableview = QTableView()
            self.tableview.setModel(self.tablemodel)
            QtGui.QWidget().setLayout(self.layout_results)
            self.layout_results = QtGui.QVBoxLayout()
            self.layout_results.addWidget(self.tableview)
            self.layout_results.addWidget(self.button_add_table)
            self.results_group.setLayout(self.layout_results)
            self.results_group.setMinimumHeight(self.screenGeometry.height() -
                                                (self.screenGeometry.height() / 3.5))
            self.edit_search.textChanged.connect(self.on_search_table_edit_changed)
            self.button_add_table.clicked.connect(self.add_selected_rows)

        def change_results_view(index):
            self.edit_search.textChanged.disconnect()
            if index is 0:
                view_buttons()
            elif index is 1:
                view_table()

        self.layout_line_search.addRow(self.results_group)

        self.search_group.setLayout(self.layout_line_search)
        self.edit_search_added.textChanged.connect(self.on_search_edit_added_changed)
        self.combo_type_search.activated.connect(change_results_view)
        view_buttons()

    def add_selected_rows(self):
        indexes = self.tableview.selectedIndexes()
        for index in indexes:
            product_id = self.tablemodel.get_id_object_alchemy(index.row())
            self.ResultButtonClick(product_id)

    @QtCore.pyqtSlot(int)
    def ResultButtonClick(self, id):
        product = session.query(Producto).get(id)
        product_name = str(product.nombre)
        items = self.table_items.findItems(product_name, QtCore.Qt.MatchExactly)
        if items:
            ok = QtGui.QMessageBox.question(self, u'Doble Producto %s'
                                            % str(product_name),
                                            "Desea Agregarlo de nuevo?",
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
            if ok == QtGui.QMessageBox.Yes:
                self.add_product_table(product)
            else:
                return
        else:
            self.add_product_table(product)

    def on_search_table_edit_changed(self, string):
        self.tablemodel.setFilter('nombre', string)

    def on_search_edit_changed(self, string):
        text_query = '%'+unicode(string.toUtf8(), encoding="UTF-8")+'%'
        self.last_query = (session.query(Producto)
                           .filter(Producto.nombre.like(text_query)).all())
        for i in reversed(range(self.layout_results.count())):
            self.layout_results.itemAt(i).widget().setParent(None)
        self.button_group.refresh (self.last_query)

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

    def delete_row(self):
        button = QtGui.qApp.focusWidget()
        index = self.table_items.indexAt(button.pos())
        self.table_items.removeRow(index.row())
        self.change_table.emit()

    def add_product_table(self, product):
        self.i = self.table_items.rowCount()

        self.table_items.insertRow(self.i)

        button = QtGui.QPushButton()
        button.clicked.connect(self.delete_row)
        button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        button.setIcon(QtGui.QIcon('icons/delete-128.png'))

        def quantity_changed(val):
            spin = QtGui.qApp.focusWidget()
            row = self.table_items.indexAt(spin.pos()).row()
            qty = float(val)
            new_value = str(float(self.table_items.item(row, 2).text()) * qty)
            self.table_items.setItem(row, 3, QtGui.QTableWidgetItem(new_value))
            self.change_table.emit()

        spinbox = QtGui.QSpinBox()
        spinbox.setValue(1)
        spinbox.setMinimum(1)

        spinbox.valueChanged.connect(quantity_changed)

        self.table_items.setCellWidget(self.i, 0, spinbox)
        self.table_items.setItem(self.i, 1,
                                 QtGui.QTableWidgetItem(str(product.nombre)))
        self.table_items.setItem(self.i, 2,
                                 QtGui.QTableWidgetItem(str(product.precio_venta)))
        self.table_items.setItem(self.i, 3,
                                 QtGui.QTableWidgetItem(str(product.precio_venta)))
        self.table_items.setCellWidget(self.i, 4, button)
        self.change_table.emit()

    def update_total(self):
        index_price = 3
        price = 0
        for row in xrange(self.table_items.rowCount()):
            item = self.table_items.item(row, index_price)
            price += float(item.text())
        self.total_line.setText(QtCore.QString(str(price)))