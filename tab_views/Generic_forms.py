import sys
import os
import importlib
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy.orm import sessionmaker, relationship, mapper
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from models import *

Base = declarative_base()

db = create_engine('sqlite:///dataBase.db', echo=False)
metadata = MetaData(db)

Session = sessionmaker(bind=db)
session = Session()

MAX_VALUE_INT = 10000000000
MAX_VALUE_FLOAT = 10000000000.0


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
        self.setRange(0, MAX_VALUE_INT)

    def extract_value(self):
        return self.value()

    def set_value_object(self, data):
        self.setValue(data)


class AdvDoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(AdvDoubleSpinBox, self).__init__(parent)
        self.setRange(0, MAX_VALUE_FLOAT)

    def extract_value(self):
        return self.value()

    def set_value_object(self, data):
        self.setValue(data)


class AdvLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(AdvLineEdit, self).__init__(parent)

    def extract_value(self):
        return str(self.text())

    def set_value_object(self, data):
        self.setText(data)


class AdvDateEdit(QtGui.QDateEdit):
    def __init__(self, parent=None):
        super(AdvDateEdit, self).__init__(parent)
        self.setCalendarPopup(True)

    def extract_value(self):
        return self.date().toPyDate()

    def set_value_object(self, data):
        self.setDate(QtCore.QDate(data.year, data.month, data.day))


TYPES_MAP = {
    'Integer': AdvSpinBox,
    'Date': AdvDateEdit,
    'Numeric': AdvDoubleSpinBox,
    'String': AdvLineEdit,
    'Foreign_Key': AdvComboBox,
}


class GenericFormDialog(QtGui.QDialog):
    def __init__(self, AlchemyModel, parent=None, object_edit=None):
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
                data = ['%s %s' % (str(e.id), str(value.name))
                        for e in session.query(value).all()]
            widget = TYPES_MAP['Foreign_Key']()
            widget.addItems(data)
            # to fill the widget foreign key
            if object_edit:
                id_obj = getattr(object_edit, key)

                # maybe this is evil
                class AbstractClassForeign(object):
                    pass

                mapper(AbstractClassForeign, value)
                obj_foreign = session.query(AbstractClassForeign).get(id_obj)
                try:
                    text = '%s %s' % (str(id_obj), str(obj_foreign.nombre))
                except AttributeError:
                    text = '%s %s' % (str(id_obj), str(value.name))
                index = widget.findText(text, QtCore.Qt.MatchFixedString)
                if index >= 0:
                    widget.setCurrentIndex(index)
            self.my_layout.addRow(label, widget)

        members = AlchemyModel.__table__.columns
        for member in members:
            if member.key in foreign_keys or member.key is 'id':
                continue
            label = QtGui.QLabel(member.key)
            type_member = type(member.type).__name__
            widget = TYPES_MAP[type_member]()
            if object_edit:
                data = getattr(object_edit, member.key)
                widget.set_value_object(data)
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
    def get_data(AlchemyModel, parent=None, obj_edit=None):
        dialog = GenericFormDialog(AlchemyModel, parent, obj_edit)
        if obj_edit:
            dialog.setWindowTitle('Editar %s' % (AlchemyModel.__name__))
        result = dialog.exec_()
        data = dialog.get_all_data()
        return (data, result == QtGui.QDialog.Accepted)