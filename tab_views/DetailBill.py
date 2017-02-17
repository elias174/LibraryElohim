import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from models import *


class Detail_Bill(QDialog):

    MAPPER_BOOLEAN_TYPES = {
        'False': 'No',
        'True': 'Si'
    }

    def __init__(self, object_id, parent = None):
        # QDialog.__init__(self, parent)
        super(Detail_Bill, self).__init__(parent)
        self.product_id = object_id

        self.query = (session.query(Detalle)
                      .filter(Detalle.factura == self.product_id).all())

        self.query_bill = (session.query(Factura, Cliente)
                           .join(Cliente)
                           .filter(Factura.id == self.product_id)
                           .filter(Factura.cliente == Cliente.id).first())

        self.control_singleton = False
        self.acceptButton = QPushButton("Aceptar", self)

        client = QLabel('Cliente')
        bill = QLabel('Factura')
        date = QLabel('Fecha')

        self.edit_client = QLineEdit()
        self.edit_client.setText(str(self.query_bill[1].nombre))
        self.edit_client.setDisabled(True)
        self.edit_bill = QLineEdit()
        self.edit_bill.setText(str(self.product_id))
        self.edit_bill.setDisabled(True)
        self.edit_date = QDateEdit(self.query_bill[0].fecha)
        self.edit_date.setDisplayFormat(('yyyy-MM-dd'))
        self.edit_date.setDisabled(True)

        self.products_group = QtGui.QGroupBox(str("Productos"), self)
        self.initializate_products_group()

        grid = QGridLayout()
        self.layout_line_bill = QtGui.QHBoxLayout()
        self.layout_line_date = QtGui.QHBoxLayout()
        self.layout_line_bill.addWidget(client)
        self.layout_line_bill.addWidget(self.edit_client)
        self.layout_line_bill.addWidget(bill)
        self.layout_line_bill.addWidget(self.edit_bill)
        self.layout_line_date.addWidget(date)
        self.layout_line_date.addWidget(self.edit_date)
        grid.addLayout(self.layout_line_bill, 1, 0)
        grid.addLayout(self.layout_line_date, 2, 0)
        grid.addWidget(self.products_group, 3, 0)
        grid.addWidget(self.acceptButton, 5, 0)

        self.setLayout(grid)

        desktopSize = QDesktopWidget().screenGeometry()
        self.setFixedSize(desktopSize.width() / 2, desktopSize.height() / 2)
        size = self.size()
        top = (desktopSize.height() / 2) - (size.height() / 2)
        left = (desktopSize.width() / 2) - (size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Ver Detalle de Factura')
        self.show()
        self.acceptButton.clicked.connect(self.close)

    def initializate_products_group(self):
        self.layout_line = QtGui.QFormLayout()
        # Creating table
        self.table_items = QtGui.QTableWidget(self)

        self.table_items.setRowCount(len(self.query))

        self.table_items.setColumnCount(3)
        self.table_items.resizeColumnsToContents()

        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table_items.horizontalHeader()
        self.stringRow = ''
        for detail in range(len(self.query)):
            try:
                self.table_items.setHorizontalHeaderLabels(['Producto', 'Cantidad',
                                                            'Precio Total'])
                product = session.query(Producto).get(self.query[detail].producto)
                self.table_items.setItem(detail, 0,
                                         QtGui.QTableWidgetItem(str(product.nombre)))
                self.table_items.setItem(detail, 1,
                                         QtGui.QTableWidgetItem(str(self.query[detail].cantidad)))
                self.table_items.setItem(detail, 2,
                                         QtGui.QTableWidgetItem(str(self.query[detail].precio_total)))
            except TypeError:
                service = session.query(Servicio).get(self.query[detail].servicio)
                self.table_items.setHorizontalHeaderLabels(['Servicio', 'Cancelado',
                                                            'Precio Total'])
                tipo = session.query(TipoServicio).get(service.tipo)
                self.table_items.setItem(detail, 0,
                                         QtGui.QTableWidgetItem(str(tipo.nombre)))
                self.table_items.setItem(detail, 1,
                                         QtGui.QTableWidgetItem(
                                             self.MAPPER_BOOLEAN_TYPES[str(service.cancelado)]))
                self.table_items.setItem(detail, 2,
                                         QtGui.QTableWidgetItem(str(self.query[detail].precio_total)))

            self.stringRow = self.stringRow + str(detail+1) + ','

        self.table_items.setVerticalHeaderLabels(
            QString(self.stringRow).split(','))
        self.table_items.resizeColumnsToContents()
        self.layout_line.addRow(self.table_items)
        self.products_group.setLayout(self.layout_line)