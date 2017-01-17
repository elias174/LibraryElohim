import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class Detail_Bill_Service(QDialog):
    def __init__(self, object_id,parent = None):
        super(Detail_Bill_Service, self).__init__(parent)
        self.product_id = object_id
        #SELECT cancelado, monto, nombre FROM Detalle JOIN Servicio ON(Detalle.servicio = Servicio.id) JOIN TipoServicio ON Servicio.tipo = TipoServicio.id
        self.query = (session.query(Detalle, Servicio, TipoServicio)
                        .join(Servicio)
                        .join(TipoServicio)
                        .filter(Detalle.factura == self.product_id)
                        .filter(Detalle.servicio == Servicio.id)
                        .filter(Servicio.tipo == TipoServicio.id).all())

        self.query_bill = (session.query(Factura, Cliente)
                        .join(Cliente)
                        .filter(Factura.id == self.product_id)
                        .filter(Factura.cliente == Cliente.id).first())

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

        self.products_group = QtGui.QGroupBox(str(""), self)
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
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Detalle de Factura')
        self.show()
        self.acceptButton.clicked.connect(self.close)
        
    def initializate_products_group(self):
        self.layout_line = QtGui.QFormLayout()
        #Creating table
        self.table_items = QtGui.QTableWidget(self)
    
        self.table_items.setRowCount(len(self.query))

        self.table_items.setColumnCount(4)
        self.table_items.resizeColumnsToContents()
        self.table_items.setHorizontalHeaderLabels(['Servicio','Monto de Factura', 
                                                    'Monto Total', 'Estado'])
        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table_items.horizontalHeader()
        self.stringRow = ''

        for detail in range(len(self.query)):
            self.table_items.setItem(detail, 0,
                                     QtGui.QTableWidgetItem(str(self.query[detail][2].nombre)))
            self.table_items.setItem(detail, 1,
                                     QtGui.QTableWidgetItem(str(self.query[detail][0].precio_total)))
            self.table_items.setItem(detail, 2,
                                     QtGui.QTableWidgetItem(str(self.query[detail][1].monto)))
            self.table_items.setItem(detail, 3,
                                     QtGui.QTableWidgetItem(str("No Cancelado" 
                                        if self.query[detail][1].cancelado == False 
                                        else "Cancelado")))
            self.stringRow = self.stringRow + str(detail+1) + ','

        self.table_items.setVerticalHeaderLabels(QString(self.stringRow).split(','))
        #addin table with the query
        self.table_items.resizeColumnsToContents()
        self.layout_line.addRow(self.table_items)
        self.products_group.setLayout(self.layout_line)
