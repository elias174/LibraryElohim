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


class Show_Box(QDialog):
    def __init__(self, string, parent=None):
        #QDialog.__init__(self, parent)
        super(Show_Box, self).__init__(parent)

        self.current_date = string
        self.acceptButton = QPushButton("Aceptar")

        self.query = session.query(Categoria).all()

        previous_balance = QLabel('Saldo Anterior')
        income = QLabel('Ingresos')
        expenses = QLabel('Egresos')
        sell_price = QLabel('Precio Venta')
        current_balance = QLabel('Saldo Actual')
        date = QLabel('Fecha de Caja')

        self.edit_previous_balance = QDoubleSpinBox(self)
        self.edit_previous_balance.setSingleStep(00.01)
        self.edit_previous_balance.setMaximum(10000.00)
        self.edit_previous_balance.setMinimum(00.00)
        self.edit_previous_balance.setDisabled(True)
        self.edit_current_balance = QDoubleSpinBox(self)
        self.edit_current_balance.setSingleStep(00.01)
        self.edit_current_balance.setMaximum(10000.00)
        self.edit_current_balance.setMinimum(00.00)
        self.edit_current_balance.setDisabled(True)
        self.edit_income = QDoubleSpinBox(self)
        self.edit_income.setSingleStep(00.01)
        self.edit_income.setMaximum(10000.00)
        self.edit_income.setMinimum(00.00)
        self.edit_income.setDisabled(True)
        self.edit_expenses = QDoubleSpinBox(self)
        self.edit_expenses.setSingleStep(00.01)
        self.edit_expenses.setMaximum(10000.00)
        self.edit_expenses.setMinimum(00.00)
        self.edit_expenses.setDisabled(True)
        self.edit_date = QDateEdit(datetime.now())
        self.edit_date.setDisplayFormat(('yyyy-MM-dd'))
        self.edit_date.setDisabled(True)

        try:
            day = '%'+unicode(string.toString("yyyy-MM-dd").toUtf8(), encoding="UTF-8")+'%'
            self.box = (session.query(Caja).\
                           filter(Caja.fecha.like(day)).first())

            self.edit_previous_balance.setValue(float(self.box.saldo_anterior))
            self.edit_current_balance.setValue(float(self.box.saldo_actual))
            self.edit_income.setValue(float(self.box.ingresos))
            self.edit_expenses.setValue(float(self.box.egresos))
            self.edit_date.setDate(self.current_date) 

        except:
            msgBox = QtGui.QMessageBox()
            msgBox.setText('No existe Caja en la Fecha '+self.current_date.toString("yyyy-MM-dd"))
            msgBox.addButton(QtGui.QPushButton('Aceptar'), QtGui.QMessageBox.YesRole)
            msgBox.setWindowTitle("No existe Registro de Caja")
            msgBox.exec_()

        grid = QGridLayout()
        grid.addWidget(date, 1, 0)
        grid.addWidget(self.edit_date, 1, 1)

        grid.addWidget(previous_balance, 2, 0)
        grid.addWidget(self.edit_previous_balance, 2, 1)

        grid.addWidget(current_balance, 3, 0)
        grid.addWidget(self.edit_current_balance, 3, 1)

        grid.addWidget(income, 4, 0)
        grid.addWidget(self.edit_income, 4, 1)

        grid.addWidget(expenses, 5, 0)
        grid.addWidget(self.edit_expenses, 5, 1)

        grid.addWidget(self.acceptButton, 8, 1)

        self.setLayout(grid)

        size = self.size()
        desktopSize = QDesktopWidget().screenGeometry()
        top = (desktopSize.height() / 2)-(size.height() / 2)
        left = (desktopSize.width() / 2)-(size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Ver Caja')
        self.show()
        self.acceptButton.clicked.connect(self.close)
