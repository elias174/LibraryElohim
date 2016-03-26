from PyQt4 import QtGui
from PyQt4 import QtCore
from collections import namedtuple
from datetime import datetime, timedelta, date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *


Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("Sistema Pagos")

        central_layout = QtGui.QVBoxLayout()
        tabs = QtGui.QTabWidget(self)
        tab_sells = Sale_Tab()

        tab_rapid_sell = QtGui.QWidget()
        tabs.addTab(tab_sells, 'Ventas')
        tabs.addTab(tab_rapid_sell, 'Venta Rapida')

        pushButton1 = QtGui.QPushButton("QPushButton 1")
        vBoxlayout = QtGui.QVBoxLayout()
        vBoxlayout.addWidget(pushButton1)
        tab_rapid_sell.setLayout(vBoxlayout)

        central_layout.addWidget(tabs)
        self.setLayout(central_layout)

    def closeEvent(self, event):
        event.ignore()
        ok = QtGui.QMessageBox.question(self, u'Salir',
                                        "Seguro?",
                                        QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
        if ok:
            event.accept()


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
    def __init__(self):
        super(Sale_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout
        self.last_query = (session.query(Producto).limit(12).all())

        self.central_layout = QtGui.QGridLayout()

        self.sale_group = QtGui.QGroupBox(str("Venta"), self)
        self.results_group = QtGui.QGroupBox(str("Resultados Busqueda"), self)

        self.central_layout.addWidget(self.sale_group, 0, 0)
        self.central_layout.addWidget(self.results_group, 0, 1)

        self.initialize_sale_group()
        self.initialize_results_group()

        QtCore.QObject.connect(self.button_group, QtCore.SIGNAL("buttonClicked(int)"),
                               self, QtCore.SLOT("ResultButtonClick(int)"))

        self.setLayout(self.central_layout)

    def initialize_sale_group(self):
        self.layout_line = QtGui.QFormLayout()
        # First Line
        self.label_search = QtGui.QLabel("Buscar Producto:", self)
        self.edit_search = QtGui.QLineEdit(self)
        self.edit_search.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, 
                                                         QtGui.QSizePolicy.Fixed))
        # Second Line
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setColumnCount(5)
        self.table_items.setRowCount(0)

        self.table_items.setHorizontalHeaderLabels(["Cantidad", "Producto",
                                                    "P.Unidad", "P.Total",
                                                    "Eliminar"])

        self.layout_line.addRow(self.label_search, self.edit_search)
        self.layout_line.addRow(self.table_items)

        self.sale_group.setMaximumWidth(self.screenGeometry.width() / 2)
        self.sale_group.setLayout(self.layout_line)

#        to connect the text_search
        self.edit_search.textChanged.connect(self.on_search_edit_changed)

    def initialize_results_group(self):
        self.layout_results = QtGui.QGridLayout()
        self.button_group = ResultsButtonGroup(self, self.last_query,
                                               self.layout_results)
        self.results_group.setLayout(self.layout_results)

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
                print 'said yes'
                self.add_product_table(product)
            else:
                print 'said no'
                return
        else:
            self.add_product_table(product)

    def on_search_edit_changed(self, string):
        text_query = '%'+unicode(string.toUtf8(), encoding="UTF-8")+'%'
        self.last_query = (session.query(Producto)
                           .filter(Producto.nombre.like(text_query)).all())
        for i in reversed(range(self.layout_results.count())):
            self.layout_results.itemAt(i).widget().setParent(None)
        self.button_group.refresh(self.last_query)

    def delete_row(self):
        button = QtGui.qApp.focusWidget()
        index = self.table_items.indexAt(button.pos())
        self.table_items.removeRow(index.row())

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

#        print self.table_items.cellWidget(0,0).value()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    mw = MainWindow()
    screenGeometry = QtGui.QApplication.desktop().availableGeometry()
    mw.resize(screenGeometry.width(), screenGeometry.height())
    mw.showMaximized()
    app.exec_()
