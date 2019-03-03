from PyQt4 import QtGui
from PyQt4 import QtCore

from models_qt import MyTableModel
from specialized_models import *
from Generic_forms import (GenericFormDialog, AdvComboBox, AdvCheckBox,
    AdvLineEdit, AdvDoubleSpinBox, AdvSpinBox, AdvTextEdit)
from constants import (LIST_YEARS, INDEX_CURRENT_YEAR, CURRENT_YEAR,
    MATRICULA_MOUNT_DEFAULT, MONTHS)

class MatriculasTab(QtGui.QWidget):
    def __init__(self, parent):
        super(MatriculasTab, self).__init__(parent)
        self.alumno_id = None
        self.query_array = []
        self.build_widgets()

    def set_alumno_id(self, alumno_id):
        self.alumno_id = alumno_id
        self.build_widgets()

    def update_query_array(self):
        self.last_query_services = (
            session.query(
                Matricula).
                filter(Matricula.alumno_id == self.alumno_id).all()
        )
        self.query_array = self.last_query_services

    def build_widgets(self):
        if self.alumno_id is None:
            return

        header_names = ['ID', 'Anio', 'Monto', 'Cancelado']
        fields = ['id', 'matricula_anio', 'monto', 'cancelado']
        self.update_query_array()
        self.table_model_result = MyTableModel(
            Matricula, header_names, self, self.query_array,
            fields_columns=fields
        )

        self.layout_results = QtGui.QHBoxLayout()
        self.tableview_results = QtGui.QTableView()
        self.tableview_results.setModel(self.table_model_result)
        self.tableview_results.resizeColumnsToContents()

        self.layout_results.addWidget(self.tableview_results)
        self.setLayout(self.layout_results)

    def clear(self):
        self.tableview_results.model().clear()
        self.alumno_id = None


class MensualidadTab(QtGui.QWidget):
    def __init__(self, parent):
        super(MensualidadTab, self).__init__(parent)
        self.alumno_id = None
        self.query_array = []
        self.layout_results = QtGui.QHBoxLayout()
        self.setLayout(self.layout_results)

    def set_alumno_id(self, alumno_id):
        self.alumno_id = alumno_id
        self.build_widgets()

    def update_query_array(self):
        self.last_query_services = (
            session.query(
                Mensualidad).
                filter(Mensualidad.alumno_id == self.alumno_id).all()
        )
        print self.last_query_services
        self.query_array = self.last_query_services

    def build_widgets(self):
        if self.alumno_id is None:
            return

        header_names = ['ID', 'Anio', 'Mes', 'Monto', 'Cancelado']
        fields = [
            'id', 'mensualidad_anio', 'mensualidad_mes','monto', 'cancelado'
        ]
        self.update_query_array()
        self.table_model_result = MyTableModel(
            Mensualidad, header_names, self, self.query_array,
            fields_columns=fields
        )

        self.tableview_results = QtGui.QTableView()
        self.tableview_results.setModel(self.table_model_result)
        self.tableview_results.resizeColumnsToContents()
        self.layout_results.addWidget(self.tableview_results)

    def clear(self):
        self.tableview_results.model().clear()
        self.alumno_id = None


class DetailedServicesTabs(QtGui.QTabWidget):
    def __init__(self, parent):
        super(DetailedServicesTabs, self).__init__(parent)
        self.alumno_id = None

        self.tab_matriculas = MatriculasTab(parent=parent)
        self.tab_mensualidad = MensualidadTab(parent=parent)
        self.tab_otros = QtGui.QWidget(parent=parent)

        self.addTab(self.tab_matriculas, "Matricula")
        self.addTab(self.tab_mensualidad, "Mensualidad")
        self.addTab(self.tab_otros, "Otros (Certificados, constancias, etc)")

    def set_alumno_id(self, alumno_id):
        self.alumno_id = alumno_id
        self.tab_matriculas.set_alumno_id(alumno_id)
        self.tab_mensualidad.set_alumno_id(alumno_id)

    def get_type_service(self):
        self.types = {
            0: 'matricula',
            1: 'mensualidad',
            2: 'otros',
        }
        return self.types[self.currentIndex()]

    def clear(self):
        self.tab_matriculas.clear()
        self.tab_mensualidad.clear()

    def generate_dialog_data(self):
        widget_year = AdvSpinBox()
        widget_year.set_value_object(CURRENT_YEAR)
        widget_canceled = AdvCheckBox()
        widget_amount = AdvDoubleSpinBox()
        widget_amount.set_value_object(MATRICULA_MOUNT_DEFAULT)

        widget_months = AdvComboBox(custom=True)
        widget_months.set_values(sorted(MONTHS, key=MONTHS.get))
        widget_extra_info = AdvTextEdit()

        custom_widgets_matricula = [
            ('Anio Correspondiente', widget_year),
            ('Monto', widget_amount),
            ('Cancelado', widget_canceled),
        ]

        custom_widgets_mensualidad = [
            ('Anio Correspondiente', widget_year),
            ('Mes Correspondiente', widget_months),
            ('Monto', widget_amount),
            ('Cancelado', widget_canceled),
        ]

        self.customs_widgets = {
            'matricula': custom_widgets_matricula,
            'mensualidad': custom_widgets_mensualidad,
            'otros': custom_widgets_mensualidad,
        }

        data_payment, result_payment = GenericFormDialog.get_data(
            Servicio, self, fields=[],
            customs_widgets=self.customs_widgets[self.get_type_service()])

        return self.generate_object_service(data_payment), result_payment

    def generate_object_service(self, data_service):
        if self.get_type_service() == 'matricula':
            service = Matricula(
                alumno_id=self.alumno_id,
                cancelado=data_service['Cancelado'],
                monto=data_service['Monto'],
                matricula_anio=data_service['Anio Correspondiente']
            )
            return service

        elif self.get_type_service() == 'mensualidad':
            service = Mensualidad(
                alumno_id=self.alumno_id,
                cancelado=data_service['Cancelado'],
                monto=data_service['Monto'],
                mensualidad_anio=data_service['Anio Correspondiente'],
                mensualidad_mes = data_service['Mes Correspondiente']
            )
            return service