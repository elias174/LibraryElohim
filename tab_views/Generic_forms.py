from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from sqlalchemy.orm import mapper
from models import *

MAX_VALUE_INT = 100000000
MAX_VALUE_FLOAT = 1000000000.0


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

    def is_valid(self):
        return True


class AdvSpinBox(QtGui.QSpinBox):
    def __init__(self, parent=None):
        super(AdvSpinBox, self).__init__(parent)
        self.setRange(0, MAX_VALUE_INT)
        self.setValue(int(1))

    def extract_value(self):
        return self.value()

    def set_value_object(self, data):
        self.setValue(data)

    def is_valid(self):
        return self.value() != 0


class AdvCheckBox(QtGui.QCheckBox):
    def __init__(self, parent=None):
        super(AdvCheckBox, self).__init__(parent)
        self.setChecked(False)

    def extract_value(self):
        return self.isChecked()

    def set_value_object(self, data):
        self.setChecked(bool(data))

    def is_valid(self):
        return True


class AdvDoubleSpinBox(QtGui.QDoubleSpinBox):
    def __init__(self, parent=None):
        super(AdvDoubleSpinBox, self).__init__(parent)
        self.setRange(0, MAX_VALUE_FLOAT)

    def extract_value(self):
        return self.value()

    def set_value_object(self, data):
        self.setValue(data)

    def is_valid(self):
        return self.value() != 0.00


class AdvLineEdit(QtGui.QLineEdit):
    def __init__(self, parent=None):
        super(AdvLineEdit, self).__init__(parent)

    def extract_value(self):
        return str(self.text())

    def set_value_object(self, data):
        self.setText(data)

    def is_valid(self):
        return str(self.text()) != ''


class AdvDateEdit(QtGui.QDateEdit):
    def __init__(self, parent=None):
        super(AdvDateEdit, self).__init__(parent)
        self.setDate(QtCore.QDate.currentDate())
        self.setCalendarPopup(True)

    def extract_value(self):
        return self.date().toPyDate()

    def set_value_object(self, data):
        self.setDate(QtCore.QDate(data.year, data.month, data.day))

    def is_valid(self):
        return True


class AdvTextEdit(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(AdvTextEdit, self).__init__(parent)

    def extract_value(self):
        return str(self.toPlainText())

    def set_value_object(self, data):
        self.setPlainText(data)

    def is_valid(self):
        return str(self.toPlainText()) != ''

TYPES_MAP = {
    'Integer': AdvSpinBox,
    'Date': AdvDateEdit,
    'Numeric': AdvDoubleSpinBox,
    'String': AdvLineEdit,
    'Foreign_Key': AdvComboBox,
    'LargeString': AdvTextEdit,
    'Boolean': AdvCheckBox
}


class GenericFormDialog(QtGui.QDialog):
    def __init__(
            self, AlchemyModel, parent=None, object_edit=None, fields=None,
            custom_widgets=[]):

        def contains_fields(member):
            if not fields:
                return True
            return member in fields

        self.parent = parent
        super(GenericFormDialog, self).__init__(parent)
        self.setWindowTitle('Nuevo %s' % (AlchemyModel.__name__))
        self.my_layout = QtGui.QFormLayout(self)
        foreign_keys = {k.parent.key: k.column.table
                        for k in list(AlchemyModel.__table__.foreign_keys)
                        if contains_fields(k.parent.key)}
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
            if not contains_fields(member.key) or (
                            member.key in foreign_keys or member.key is 'id'):
                continue
            label = QtGui.QLabel(member.key)
            type_member = type(member.type).__name__
            # print dir(member.type)
            if type_member is 'String':
                if member.type.length > 70:
                    type_member = 'LargeString'
            widget = TYPES_MAP[type_member]()
            if object_edit:
                data = getattr(object_edit, member.key)
                widget.set_value_object(data)
            self.my_layout.addRow(label, widget)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        for widget in custom_widgets:
            self.my_layout.addRow(str(widget[0]), widget[1])

        self.buttons.accepted.connect(self.validate_form)
        self.buttons.rejected.connect(self.reject)
        self.my_layout.addRow(self.buttons)
        self.setLayout(self.my_layout)

    def validate_form(self):
        self.data = self.get_all_data()
        if self.data:
            self.accept()

    def get_all_data(self):
        widgets = [self.my_layout.itemAt(i).widget()
                   for i in range(self.my_layout.count())]
        data = {}
        for i in range(0, len(widgets)-1, 2):
            try:
                if widgets[i+1].is_valid():
                    data[str(widgets[i].text())] = widgets[i+1].extract_value()
                else:
                    errors = 'Campo %s Invalido' % str(widgets[i].text())
                    QtGui.QMessageBox.critical(self.parent, 'Error',
                                               errors,
                                               QtGui.QMessageBox.Ok)
                    return {}
            except AttributeError:
                continue
        return data

    @staticmethod
    def get_data(AlchemyModel, parent=None, obj_edit=None, fields=None,
                 customs_widgets=[]):
        data = {}
        dialog = GenericFormDialog(AlchemyModel, parent, obj_edit, fields,
                                   customs_widgets)
        if obj_edit:
            dialog.setWindowTitle('Editar %s' % (AlchemyModel.__name__))
        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            data = dialog.get_all_data()
            return data, True
        return {}, False
