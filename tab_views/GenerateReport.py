import sys
import os
import calendar
from collections import OrderedDict
from datetime import date

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from api.api_gainings import GainingsApi
from GenerateTableReport import Generate_Table_Report


# Dialog to export report xlsx format
class ReportExportDialog(QtGui.QDialog):

    YEARS = [
        '2017',
        '2018',
        '2019',
        '2020',
        '2021',
    ]

    MONTHS = {
        'Enero': 1,
        'Febrero': 2,
        'Marzo': 3,
        'Abril': 4,
        'Mayo': 5,
        'Junio': 6,
        'Julio': 7,
        'Agosto': 8,
        'Septiembre': 9,
        'Octubre': 10,
        'Noviembre': 11,
        'Diciembre': 12
    }

    def __init__(self, screen_size, type_report, parent=None):

        self.TYPE_REPORTS = {
            'xlsx': self.export_xlsx,
            'table': self.report_table
        }

        super(ReportExportDialog, self).__init__(parent)
        self.layout = QtGui.QFormLayout(self)
        self.type = type
        # self.setMinimumSize(400, 320)

        self.combobox_year = QtGui.QComboBox(self)
        self.combobox_year.setMaximumWidth(screen_size.width() / 8)
        self.combobox_year.addItems(self.YEARS)

        self.combobox_month = QtGui.QComboBox(self)
        self.combobox_month.setMaximumWidth(screen_size.width() / 8)
        self.combobox_month.addItem('-')
        self.combobox_month.addItems(sorted(self.MONTHS, key=self.MONTHS.get))

        self.combobox_day = QtGui.QComboBox(self)
        self.combobox_day.setMaximumWidth(screen_size.width() / 8)
        self.update_days()

        self.combobox_type = QtGui.QComboBox(self)
        self.combobox_type.setMaximumWidth(screen_size.width() / 8)
        self.combobox_type.addItems(['Libreria', 'Servicios'])

        self.combobox_year.currentIndexChanged.connect(self.update_days)
        self.combobox_month.currentIndexChanged.connect(self.update_days)

        verticalSpacer = QtGui.QSpacerItem(20, 25, QtGui.QSizePolicy.Minimum,
                                           QSizePolicy.Expanding)

        self.buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.TYPE_REPORTS[type_report])
        self.buttons.rejected.connect(self.reject)

        self.layout.addRow('Anio', self.combobox_year)
        self.layout.addRow('Mes', self.combobox_month)
        self.layout.addRow('Dia', self.combobox_day)
        self.layout.addRow('Tipo', self.combobox_type)
        self.layout.addItem(verticalSpacer)

        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)
        self.setWindowTitle('Elegir Fecha')
        self.setFixedSize(self.sizeHint())

    def update_days(self):
        self.combobox_day.clear()
        if str(self.combobox_month.currentText()) is '-':
            self.combobox_day.addItem('-')
            self.combobox_day.setEditable(False)
            return
        month = self.MONTHS[str(self.combobox_month.currentText())]
        year = int(self.combobox_year.currentText())
        days = xrange(1, calendar.monthrange(year, month)[1] + 1)
        days = map(str, days)
        self.combobox_day.addItem('-')
        self.combobox_day.addItems(days)

    def get_valid_data(self):
        validated_data = dict()
        validated_data['year'] = int(self.combobox_year.currentText())
        validated_data['month'] = (
            self.MONTHS[str(self.combobox_month.currentText())]
            if str(self.combobox_month.currentText()) != '-' else None
        )
        validated_data['day'] = (int(self.combobox_day.currentText())
                                 if self.combobox_day.currentText() != '-'
                                 else None)
        validated_data['type'] = str(self.combobox_type.currentText())
        return validated_data

    def export_xlsx(self):
        validated_data = self.get_valid_data()
        gainings_api = GainingsApi()
        try:
            gainings_api.gainings_by_date(**validated_data)
        except AssertionError:
            QtGui.QMessageBox.warning(self, 'Atencion',
                                      'No existen Registros', QtGui.QMessageBox.Ok)
            return
        file_name = QtGui.QFileDialog.getSaveFileName(self, 'Guardar XLSX', QtCore.QDir.homePath(),
                                                      "Excel (*.xlsx )")
        gainings_api.export_xlsx(file_name)

    def report_table(self):
        validated_data = self.get_valid_data()
        gainings_api = GainingsApi()
        try:
            gainings_api.gainings_by_date(**validated_data)
        except AssertionError:
            QtGui.QMessageBox.warning(self, 'Atencion',
                                      'No existen Registros', QtGui.QMessageBox.Ok)
            return
        dialog = Generate_Table_Report(gainings_api.result_query,
                                       validated_data, self)
        dialog.exec_()

    @staticmethod
    def get_report(screensize, type_report, parent=None):
        dialog_date = ReportExportDialog(
            screen_size=screensize, parent=parent, type_report=type_report)
        dialog_date.exec_()
