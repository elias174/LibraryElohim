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


class Detail_Product(QDialog):
    def __init__(self, parent = None):
        #QDialog.__init__(self, parent)
        super(Detail_Product, self).__init__(parent)

        self.control_singleton = False
        self.acceptButton = QPushButton("Aceptar", self)

        bill = QLabel('Factura')
        date = QLabel('Fecha')

        self.edit_bill = QLineEdit()
        self.edit_date = QDateEdit(datetime.now())

        self.products_group = QtGui.QGroupBox(str("Productos"), self)
        self.initializate_products_group()

        grid = QGridLayout()
        grid.addWidget(bill, 1, 0)
        grid.addWidget(self.edit_bill, 1, 1)

        grid.addWidget(date, 2, 0)
        grid.addWidget(self.edit_date, 2, 1)

        grid.addWidget(self.products_group, 3, 0, 3, 2)

        grid.addWidget(self.acceptButton, 4, 1)

        self.setLayout(grid)

        size = self.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Ver Detalle de Factura')
        self.show()
        self.acceptButton.clicked.connect(self.close)
        
    def initializate_products_group(self):
        self.layout_line = QtGui.QFormLayout()
        #Creating table
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
    
        self.table_items.setRowCount(0)

        self.table_items.setColumnCount(3)
        self.table_items.setHorizontalHeaderLabels(['Producto', 'Cantidad', 
                                                    'Precio Total'])
        header = self.table_items.horizontalHeader()
        header.setResizeMode(QHeaderView.Stretch)
        self.stringRow = ''
        #query
        """
        self.query = (session.query(Producto).limit(20).all())
        self.table_items.setRowCount(len(self.query))
        self.stringRow = ''
        for detail in range(len(self.query)):
            self.table_items.setItem(detail, 0,
                                     QtGui.QTableWidgetItem(str(self.query[detail].id)))
            self.table_items.setItem(detail, 1,
                                     QtGui.QTableWidgetItem(str(self.query[detail].categoria)))
            self.stringRow = self.stringRow + str(product+1) + ','

        self.table_items.setVerticalHeaderLabels(QString(self.stringRow).split(','))
        """
        #addin table with the query

        self.layout_line.addRow(self.table_items)
        self.products_group.setLayout(self.layout_line)
