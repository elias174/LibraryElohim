import sys
import os
import importlib
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo=False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()


class AdvComboBox(QtGui.QComboBox):
    def __init__(self, parent=None):
        super(AdvComboBox, self).__init__(parent)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setEditable(True)

        self.pFilterModel = QtGui.QSortFilterProxyModel(self)
        self.pFilterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.pFilterModel.setSourceModel(self.model())

        self.completer = QtGui.QCompleter(self.pFilterModel, self)
        self.completer.setCompletionMode(QtGui.QCompleter.UnfilteredPopupCompletion)

        self.setCompleter(self.completer)

        def filter(text):
            self.pFilterModel.setFilterFixedString(str(text))

        self.lineEdit().textEdited[unicode].connect(filter)
        self.completer.activated.connect(self.on_completer_activated)

    def on_completer_activated(self, text):
        if text:
            index = self.findText(str(text))
            self.setCurrentIndex(index)

    def extract_value(self):
        string = str(self.currentText())
        return int(string.split(' ')[0])


class AdvSpinBox(QtGui.QSpinBox):
    def __init__(self, parent=None):
        super(AdvSpinBox, self).__init__(parent)

    def extract_value(self):
        return self.value()


class AdvDoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(AdvDoubleSpinBox, self).__init__(parent)

    def extract_value(self):
        return self.value()


class AdvDoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(AdvDoubleSpinBox, self).__init__(parent)

    def extract_value(self):
        return self.value()


class AdvLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(AdvLineEdit, self).__init__(parent)

    def extract_value(self):
        return str(self.text())


class AdvDateEdit(QtGui.QDateEdit):
    def __init__(self, parent=None):
        super(AdvDateEdit, self).__init__(parent)
        self.setCalendarPopup(True)

    def extract_value(self):
        return self.date().toPyDate()


TYPES_MAP = {
    'Integer': AdvSpinBox,
    'Date': AdvDateEdit,
    'Numeric': AdvDoubleSpinBox,
    'String': AdvLineEdit,
    'Foreign_Key': AdvComboBox,
}


class GenericFormDialog(QtGui.QDialog):
    def __init__(self, AlchemyModel, parent=None):
        super(GenericFormDialog, self).__init__(parent)
        self.setWindowTitle('Nuevo %s' % (AlchemyModel.__name__))
        self.my_layout = QtGui.QFormLayout(self)
        foreign_keys = {k.parent.key: k.column.table
                        for k in list(AlchemyModel.__table__.foreign_keys)}
        for key, value in foreign_keys.iteritems():
            label = QtGui.QLabel(key)
            try:
                data = ['%s %s' % (str(e.id), str(e.nombre))
                        for e in session.query(value).all()]
            except AttributeError:
                continue
            widget = TYPES_MAP['Foreign_Key']()
            widget.addItems(data)
            self.my_layout.addRow(label, widget)

        members = AlchemyModel.__table__.columns
        for member in members:
            if member.key in foreign_keys:
                continue
            label = QtGui.QLabel(member.key)
            type_member = type(member.type).__name__
            widget = TYPES_MAP[type_member]()
            self.my_layout.addRow(label, widget)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.my_layout.addRow(self.buttons)
        self.setLayout(self.my_layout)

    def get_all_data(self):
        widgets = [self.my_layout.itemAt(i).widget()
                   for i in range(self.my_layout.count())]
        data = {}
        for i in range(0, len(widgets)-1, 2):
            data[str(widgets[i].text())] = widgets[i+1].extract_value()
        return data

    @staticmethod
    def get_data(AlchemyModel, parent=None):
        dialog = GenericFormDialog(AlchemyModel, parent)
        result = dialog.exec_()
        data = dialog.get_all_data()
        return (data, result == QtGui.QDialog.Accepted)