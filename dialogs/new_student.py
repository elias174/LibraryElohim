from PyQt4 import QtCore, QtGui

#from specialized_models import *


class NewStudentDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(NewStudentDialog, self).__init__(parent)
        self.my_layout = QtGui.QFormLayout(self)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)

        self.buttons.accepted.connect(self.validate_form)
        self.buttons.rejected.connect(self.reject)

        self.my_layout.addRow(self.buttons)
        self.setLayout(self.my_layout)

    def get_all_data(self):
        data = {}
        return data

    def validate_form(self):
        self.data = self.get_all_data()
        if self.data:
            self.accept()

    @staticmethod
    def get_data(parent=None, obj_edit=None, fields=None,
                 customs_widgets=[], title=''):
        dialog = NewStudentDialog(parent=parent)
        dialog.setWindowTitle('Registrar nuevo alumno')

        result = dialog.exec_()
        if result == QtGui.QDialog.Accepted:
            data = {'success': True}
            return data, True
        return {}, False
