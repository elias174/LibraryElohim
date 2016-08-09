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
from AddExpense import Add_Expense
from DetailExpense import Detail_Expense


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
        self.control_singleton = False
        self.central_layout.addWidget(self.search_group, 0, 0)
        self.initialize_search_group()
        self.setLayout(self.central_layout)
        

#        to connect the text_search
    def initialize_search_group(self):
        self.layout_line_main = QtGui.QGridLayout()
        self.layout_line_radio = QtGui.QHBoxLayout()
        self.layout_line_search = QtGui.QHBoxLayout()
        self.layout_line_table = QtGui.QVBoxLayout()
        self.layout_line_gain = QtGui.QHBoxLayout()
        self.layout_line_expenses = QtGui.QHBoxLayout()

        self.search_bill_today = QRadioButton("Ver Facturas de Hoy")
        self.search_bill_name = QRadioButton("Buscar Factura por Nombre")
        self.search_bill_day = QRadioButton("Buscar Factura por Dia")
        self.edit_search = QtGui.QLineEdit(self)
        self.edit_date = QDateEdit(datetime.now())
        self.edit_date.setDisplayFormat(('yyyy-MM-dd'))
        self.edit_search_name = QtGui.QLineEdit(self)
        self.edit_search_name.hide()
        self.edit_date.hide()

        self.search_bill_today.setChecked(True)

        self.search_bill_today.toggled.connect(self.add_searcher)
        self.search_bill_day.toggled.connect(self.add_date_searcher)
        self.search_bill_name.toggled.connect(self.add_searcher_name)

        #Buttons and Texts lines
        #For search_bill_today
        self.day_gain = QtGui.QLabel("Ganancia del Dia ", self)
        self.day_expenses = QtGui.QLabel("Gastos del Dia ", self)
        self.edit_day_gain = QtGui.QLineEdit(self)
        self.edit_day_gain.setDisabled(1)
        self.edit_day_expenses = QtGui.QLineEdit(self)
        self.edit_day_expenses.setDisabled(1)

        

        self.buttonAddExpense = QtGui.QPushButton("Agregar Gasto", self)
        self.buttonAddExpense.clicked.connect(self.add_expense)

        self.buttonDetailExpense = QtGui.QPushButton("Detalles de Gastos", self)
        self.buttonDetailExpense.clicked.connect(self.detail_expense)

        self.buttonCloseBox = QtGui.QPushButton("Cerrar Caja de Hoy", self)
        self.buttonCloseBox.clicked.connect(self.close_box)

        self.buttonShowBox = QtGui.QPushButton("Ver Caja del Dia", self)
        self.buttonShowBox.clicked.connect(self.show_box)
        self.buttonShowBox.hide()
        
        header_names = ['ID', 'Factura', 'Fecha', 'Detalles']
        self.tablemodel = MyTableModel(Factura, header_names, self)
        self.tableview = TableView()
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.tablemodel)
        self.tableview.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        for row in xrange(self.tablemodel.rowCount()):
            self.tableview.openPersistentEditor(self.tablemodel.index(row, 3))

        self.layout_line_radio.addWidget(self.search_bill_today)
        self.layout_line_radio.addWidget(self.search_bill_day)
        self.layout_line_radio.addWidget(self.search_bill_name)
        self.layout_line_search.addWidget(self.edit_search)
        self.layout_line_search.addWidget(self.edit_date)
        self.layout_line_search.addWidget(self.edit_search_name)
        self.layout_line_gain.addWidget(self.day_gain)
        self.layout_line_gain.addWidget(self.edit_day_gain)
        self.layout_line_expenses.addWidget(self.day_expenses)
        self.layout_line_expenses.addWidget(self.edit_day_expenses)
        self.layout_line_expenses.addWidget(self.buttonAddExpense)
        self.layout_line_expenses.addWidget(self.buttonDetailExpense)
        self.layout_line_table.addWidget(self.tableview)
        self.layout_line_main.addLayout(self.layout_line_radio, 1, 1)
        self.layout_line_main.addLayout(self.layout_line_search, 2, 1)
        self.layout_line_main.addLayout(self.layout_line_table, 3, 1)
        self.layout_line_main.addLayout(self.layout_line_gain, 4, 1)
        self.layout_line_main.addLayout(self.layout_line_expenses, 5, 1)
        self.layout_line_main.addWidget(self.buttonCloseBox, 7, 1)
        self.layout_line_main.addWidget(self.buttonShowBox, 7, 1)

        self.search_group.setLayout(self.layout_line_main)
        self.edit_search.textChanged.connect(self.on_search_table_edit_changed)
        self.edit_search_name.textChanged.connect(self.on_search_table_by_name_changed)
        self.edit_date.dateChanged.connect(self.on_search_table_by_date_changed)

    def on_search_table_edit_changed(self, string):
        if self.search_bill_today.isChecked():
            self.tablemodel.searchBillToday(string)

    def on_search_table_by_name_changed(self, string):
        if self.search_bill_name.isChecked():
            self.tablemodel.setFilter('id', string)

    def on_search_table_by_date_changed(self, string):
        if self.search_bill_day.isChecked():
            string = string.toString("yyyy-MM-dd")
            self.tablemodel.searchBillDay(string)
        
    def add_searcher(self):
        self.edit_date.hide()
        self.edit_search_name.hide()
        self.edit_search.show()
        self.buttonCloseBox.show()
        self.buttonShowBox.hide()
        self.buttonAddExpense.show()
        self.buttonDetailExpense.show()
        self.edit_day_gain.show()
        self.edit_day_expenses.show()
        self.day_expenses.show()
        self.day_gain.show()

    def add_date_searcher(self):
        self.edit_search.hide()
        self.edit_search_name.hide()
        self.edit_date.show()
        self.buttonCloseBox.hide()
        self.buttonShowBox.show()
        self.buttonAddExpense.hide()
        self.buttonDetailExpense.show()
        self.edit_day_gain.show()
        self.edit_day_expenses.show()
        self.day_expenses.show()
        self.day_gain.show()

    def add_searcher_name(self):
        self.edit_date.hide()
        self.edit_search_name.show()
        self.edit_search.hide()
        self.buttonCloseBox.hide()
        self.buttonShowBox.hide()
        self.buttonAddExpense.hide()
        self.buttonDetailExpense.hide()
        self.edit_day_gain.hide()
        self.edit_day_expenses.hide()
        self.day_expenses.hide()
        self.day_gain.hide()

    def add_expense(self):
        #if (self.control_singleton):
        #    QMessageBox.warning(self, 'Error', ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
        #else:
        #    self.control_singleton = True
        Add_Expense().exec_()
        #    self.control_singleton = False

    def detail_expense(self):
        #if (self.control_singleton):
        #    QMessageBox.warning(self, 'Error', ERROR_A_PROCESS_OPENED, QMessageBox.Ok)
        #else:
        #    self.control_singleton = True
        Detail_Expense().exec_()
        #self.control_singleton = False

    def close_box(self):
        return "Cerrar Caja"

    def show_box(self):
        return 0