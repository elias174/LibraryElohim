import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *
from models_qt import MyTableModel

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo = False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class Show_Box(QDialog):
    def __init__(self, string, parent=None):
        #QDialog.__init__(self, parent)
        super(Show_Box, self).__init__(parent)

        self.layout_line_table = QtGui.QVBoxLayout()
        self.layout_line_date = QtGui.QHBoxLayout()

        self.date = QLabel('Fecha')
        self.current_date = string
        self.edit_date = QDateEdit(string)
        self.edit_date.setDisplayFormat(('yyyy-MM-dd'))
        self.edit_date.setDisabled(True)
        self.acceptButton = QPushButton("Aceptar")

        header_names = ['ID', 'Salgo Anterior', 'Ingreso', 'Egresos', 
                        'Saldo Actual', 'Fecha de Caja']

        self.tablemodel = MyTableModel(Caja, header_names, self)
        self.tableview = QtGui.QTableView()
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.tablemodel)
        self.tableview.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

        for row in xrange(self.tablemodel.rowCount()):
            self.tableview.openPersistentEditor(self.tablemodel.index(row, 3))

        string = string.toString("yyyy-MM-dd")
        self.tablemodel.searchCashDay(string)

        self.layout_line_table.addWidget(self.tableview)
        self.layout_line_date.addWidget(self.date)
        self.layout_line_date.addWidget(self.edit_date)

        self.grid = QGridLayout()
        self.grid.addLayout(self.layout_line_date, 1, 0)
        self.grid.addLayout(self.layout_line_table, 3, 0)
        self.grid.addWidget(self.acceptButton, 8, 0)
        self.setLayout(self.grid)

        size = self.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Ver Caja')
        self.show()
        self.acceptButton.clicked.connect(self.close)