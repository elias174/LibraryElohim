import sys
import os
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from models import *
from models_qt import MyTableModel
from Generic_forms import GenericFormDialog

sys.path.append(os.path.abspath(os.path.join('..', 'api')))

#Client Dialog
class ClientDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(ClientDialog, self).__init__(parent)
        self.layout = QtGui.QFormLayout(self)
        self.label = QtGui.QLabel('Nombre')
        self.last_name = QtGui.QLabel('Apellido')
        self.layout_line_client = QtGui.QHBoxLayout()
        self.line_edit_search = QtGui.QLineEdit()
        self.line_edit_last_name = QtGui.QLineEdit()
        screen_size = QtGui.QApplication.desktop().availableGeometry()

        header_names = ['ID', 'Nombre', 'Apellido', 'DNI']
        self.tablemodel = MyTableModel(Cliente, header_names, self)
        self.tableview = QtGui.QTableView()
        self.tableview.setModel(self.tablemodel)
        self.layout_line_client.addWidget(self.label)
        self.layout_line_client.addWidget(self.line_edit_search)
        self.layout_line_client.addWidget(self.last_name)
        self.layout_line_client.addWidget(self.line_edit_last_name)
        self.layout.addRow(self.layout_line_client)

        self.button_new_client = QtGui.QPushButton('Nuevo Cliente')
        self.button_new_client.setMaximumWidth(screen_size.height()/6)
        self.layout.addRow(self.button_new_client)
        self.layout.addRow(self.tableview)
        self.tableview.setMinimumSize(screen_size.width() / 2,
                                      screen_size.height() / 4)
        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.button_new_client.clicked.connect(self.new_client)
        self.line_edit_search.textChanged.connect(self.search_client)
        self.line_edit_last_name.textChanged.connect(
            self.last_name_search)

        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)
        self.setWindowTitle('Clientes Administrador')

    def search_client(self, string):
        self.tablemodel.searchClient(string, self.line_edit_last_name.text())

    def last_name_search(self, string):
        self.tablemodel.searchClient(self.line_edit_search.text(), string)

    def new_client(self):
        data, result = GenericFormDialog.get_data(Cliente, self)
        if result:
            new_client = Cliente(
                data['nombre'],
                data['apellido'],
                data['dni'],
            )
            session.add(new_client)
            session.commit()
            #QtCore.QAbstractTableModel.dataChanged()
            self.tableview.model().refresh_data()

    def get_id_selected_client(self):
        indexes = self.tableview.selectedIndexes()
        if len(indexes) < 1:
            client_id = None
        else:
            client_id = self.tablemodel.get_id_object_alchemy(indexes[0].row())
        return client_id

    @staticmethod
    def get_client(parent=None):
        dialog = ClientDialog(parent)
        result = dialog.exec_()
        id_client = dialog.get_id_selected_client()
        return (id_client, result == QtGui.QDialog.Accepted)
