import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from models_qt import MyTableModel
from models_qt import TableView


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


class Administrator_Tab(QtGui.QWidget):
    change_table = QtCore.pyqtSignal()

    def __init__(self):
        super(Administrator_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout

        # Signal to check total
        self.last_query = (session.query(Producto).limit(12).all())

        self.central_layout = QtGui.QGridLayout()

        self.search_group = QtGui.QGroupBox(str("Busqueda"), self)

        self.central_layout.addWidget(self.search_group, 0, 0)

        self.initialize_search_group()

        self.setLayout(self.central_layout)


#        to connect the text_search
    def initialize_search_group(self):
        self.layout_line_search = QtGui.QFormLayout()

        self.search_bill_today = QRadioButton("Ver Facturas de Hoy")
        self.search_bill_name = QRadioButton("Buscar Factura por Nombre")
        self.search_bill_day = QRadioButton("Buscar Factura por Dia")
        self.edit_search = QtGui.QLineEdit(self)
        self.edit_date = QDateEdit(datetime.now())

        self.search_bill_today.setChecked(True)

        self.search_bill_today.toggled.connect(self.add_searcher)
        self.search_bill_day.toggled.connect(self.add_date_searcher)
        self.search_bill_name.toggled.connect(self.add_searcher)

        #Buttons and Texts lines
        #For search_bill_today
        self.day_gain = QtGui.QLabel("Ganancia del Dia ", self)
        self.day_expenses = QtGui.QLabel("Gastos del Dia ", self)
        self.edit_day_gain = QtGui.QLineEdit(self)
        self.edit_day_expenses = QtGui.QLineEdit(self)

        self.buttonAddExpense = QtGui.QPushButton("Agregar Gasto", self)
        self.buttonAddExpense.clicked.connect(self.add_expense)

        self.buttonDetailExpense = QtGui.QPushButton("Detalles de Gastos", self)
        self.buttonDetailExpense.clicked.connect(self.detail_expense)

        self.buttonCloseBox = QtGui.QPushButton("Cerrar Caja de Hoy", self)
        self.buttonCloseBox.clicked.connect(self.close_box)
        
        header_names = ['ID', 'Factura', 'Fecha', 'Detalles']
        self.tablemodel = MyTableModel(Producto, header_names, self)
        self.tableview = TableView()
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.tablemodel)
        #self.tableview.resizeColumnsToContents()
        self.tableview.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        for row in xrange(self.tablemodel.rowCount()):
            self.tableview.openPersistentEditor(self.tablemodel.index(row, 3))
            
        self.layout_line_search.addRow(self.search_bill_today, self.search_bill_day)
        self.layout_line_search.addRow(self.search_bill_name)
        self.layout_line_search.addRow(self.edit_search)
        self.layout_line_search.addRow(self.edit_date)
        self.layout_line_search.addRow(self.tableview)
        self.edit_date.hide()

        #Add buttons to layout
        self.layout_line_search.addRow(self.day_gain, self.edit_day_gain)
        self.layout_line_search.addRow(self.day_expenses, self.edit_day_expenses)
        self.layout_line_search.addRow(self.buttonAddExpense, self.buttonDetailExpense)
        self.layout_line_search.addRow(self.buttonCloseBox)


        self.search_group.setLayout(self.layout_line_search)
        #self.edit_search_added.textChanged.connect(self.on_search_edit_added_changed)

    def add_searcher(self):
        self.edit_date.hide()
        self.edit_search.show()

    def add_date_searcher(self):
        self.edit_search.hide()
        self.edit_date.show()

    def add_expense(self):
        return "Agregar gasto"

    def detail_expense(self):
        return "Detalle de gasto"

    def close_box(self):
        return "Cerrar Caja"

    def add_selected_rows(self):
        indexes = self.tableview.selectedIndexes()
        for index in indexes:
            product_id = self.tablemodel.get_id_object_alchemy(index.row())
            self.ResultButtonClick(product_id)


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