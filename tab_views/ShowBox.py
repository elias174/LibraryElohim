import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from models import *
from models_qt import MyTableModel


class Show_Box(QDialog):
    def __init__(self, string, parent=None):
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
        self.tableview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableview.resizeColumnsToContents()

        for row in xrange(self.tablemodel.rowCount()):
            self.tableview.openPersistentEditor(self.tablemodel.index(row, 3))

        string = string.toString("yyyy-MM-dd")
        self.tablemodel.searchCashDay(string)
        self.tableview.resizeColumnsToContents()

        self.layout_line_table.addWidget(self.tableview)
        self.layout_line_date.addWidget(self.date)
        self.layout_line_date.addWidget(self.edit_date)

        self.grid = QGridLayout()
        self.grid.addLayout(self.layout_line_date, 1, 0)
        self.grid.addLayout(self.layout_line_table, 3, 0)
        self.grid.addWidget(self.acceptButton, 8, 0)
        self.setLayout(self.grid)

        desktopSize = QDesktopWidget().screenGeometry()
        self.setFixedSize(desktopSize.width() / 2, desktopSize.height() / 2)
        size = self.size()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Ver Caja')
        self.show()
        self.acceptButton.clicked.connect(self.close)