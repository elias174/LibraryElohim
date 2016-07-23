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

class Add_Category(QDialog):
	def __init__(self, parent=None):
		#QDialog.__init__(self, parent)
		super(Add_Category, self).__init__(parent)

		self.acceptButton = QPushButton("Guardar Categoria", self)
		self.cancelButton = QPushButton("Cancelar")
		name = QLabel('Nombre de la Categoria')
		description = QLabel('Descripcion')

		self.edit_name = QLineEdit()
		self.edit_description = QTextEdit()

		grid = QGridLayout()
		grid.addWidget(name,1,0)
		grid.addWidget(self.edit_name,1,1)

		grid.addWidget(description,2,0)
		grid.addWidget(self.edit_description,2,1)

		grid.addWidget(self.acceptButton,3,1)
		grid.addWidget(self.cancelButton,3,2)

		self.setLayout(grid)

		size=self.size()
		desktopSize=QDesktopWidget().screenGeometry()
		top=(desktopSize.height()/2)-(size.height()/2)
		left=(desktopSize.width()/2)-(size.width()/2)

		self.move(left, top)
		self.setWindowTitle('Agregar Categoria')
		self.show()
		self.cancelButton.clicked.connect(self.close)
		self.connect(self.acceptButton, SIGNAL("clicked()"), self.create_Category)

	def create_Category(self):
		name = str(self.edit_name.text())
		description = unicode(self.edit_description.toPlainText())
		#Query insert
		self.close()
