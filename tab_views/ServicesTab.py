import sys
import os
import types

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from models import *
from models_qt import MyTableModel
from Generic_forms import GenericFormDialog, AdvComboBox, AdvCheckBox
from api.api_sales import SaleApi
# from config import ALCHEMY_SESSION as session


class ServicesTab(QtGui.QWidget):

    service_payment_realeased = QtCore.pyqtSignal(float)

    def __init__(self):
        super(ServicesTab, self).__init__()
        self.client_id = None
        self.last_query_services = None
        self.array_data = []
        self.exist_client = False

        self.layout = QtGui.QFormLayout(self)
        self.layout_line_client = QtGui.QHBoxLayout()
        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()

        self.label = QtGui.QLabel('Nombre')
        self.last_name = QtGui.QLabel('Apellido')

        self.line_edit_search = QtGui.QLineEdit()
        self.line_edit_last_name = QtGui.QLineEdit()

        header_names = ['ID', 'Nombre', 'Apellido', 'DNI']
        self.tablemodel = MyTableModel(Cliente, header_names, self)
        self.tableview = QtGui.QTableView()
        self.tableview.setAlternatingRowColors(True)
        self.tableview.setModel(self.tablemodel)
        self.tableview.setMaximumHeight(self.screenGeometry.height() / 6)
        self.tableview.setColumnWidth(1, self.screenGeometry.width() * 0.3)
        self.tableview.setColumnWidth(2, self.screenGeometry.width() * 0.3)
        self.tableview.setColumnWidth(3, self.screenGeometry.width() * 0.15)

        self.button_new_type_service = QtGui.QPushButton('Nuevo Servicio')
        self.button_new_type_service.setMaximumWidth(
            self.screenGeometry.width() / 6)
        self.button_new_type_service.setMinimumWidth(
            self.screenGeometry.width() / 6)

        self.button_search_client = QtGui.QPushButton('Buscar Cliente')
        self.button_search_client.setMaximumWidth(
            self.screenGeometry.width() / 4)
        self.button_new_client = QtGui.QPushButton('Nuevo Cliente')
        self.button_new_client.setMaximumWidth(
            self.screenGeometry.width() / 4)

        self.button_clean = QtGui.QPushButton('Limpiar')

        self.third_contain_layout = QtGui.QHBoxLayout()
        self.third_contain_layout.addWidget(self.button_search_client)
        self.third_contain_layout.addWidget(self.button_new_client)
        self.third_contain_layout.setSpacing(self.screenGeometry.width() / 2)

        self.first_contain_layout = QtGui.QHBoxLayout()
        self.first_contain_layout.addWidget(
            self.button_new_type_service, 0, QtCore.Qt.AlignRight)

        self.line_edit_search.textChanged.connect(
            self.auto_complete_client_search)
        self.line_edit_last_name.textChanged.connect(
            self.auto_complete_last_name_search)
        self.button_search_client.clicked.connect(
            self.search_client_clicked)
        self.button_new_type_service.clicked.connect(
            self.new_service)
        self.button_clean.clicked.connect(
            self.clean_results)
        self.button_new_client.clicked.connect(
            self.new_client)

        self.group_results = QtGui.QGroupBox(str("Resultados Busqueda"))
        self.layout_results = QtGui.QHBoxLayout()
        self.layout_buttons_results = QtGui.QVBoxLayout()
        self.tableview_results = QtGui.QTableView()
        self.button_add_payment = QtGui.QPushButton("Agregar Pago")
        self.button_cancel_payment = QtGui.QPushButton("Cancelar Pago")
        self.button_new_service_payment = QtGui.QPushButton(
            "Nuevo Pago Servicio")

        self.button_add_payment.setMinimumWidth(
            self.screenGeometry.width() / 6)
        self.button_cancel_payment.setMinimumWidth(
            self.screenGeometry.width() / 6)

        self.button_new_service_payment.setMinimumWidth(
            self.screenGeometry.width() / 6)

        self.layout_results.addWidget(self.tableview_results)
        self.layout_results.addLayout(self.layout_buttons_results)
        self.layout_buttons_results.addWidget(self.button_add_payment)
        self.layout_buttons_results.addWidget(self.button_cancel_payment)
        self.layout_buttons_results.addWidget(self.button_new_service_payment)
        self.group_results.setLayout(self.layout_results)

        self.button_add_payment.clicked.connect(self.add_payment_to_service)
        self.button_cancel_payment.clicked.connect(self.cancel_payment)
        self.button_new_service_payment.clicked.connect(
            self.new_service_payment)

        verticalSpacer = QtGui.QSpacerItem(20, 70, QtGui.QSizePolicy.Minimum,
                                           QSizePolicy.Expanding)
        verticalSpacer_2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum,
                                             QSizePolicy.Expanding)

        self.layout_line_client.addWidget(self.label)
        self.layout_line_client.addWidget(self.line_edit_search)
        self.layout_line_client.addWidget(self.last_name)
        self.layout_line_client.addWidget(self.line_edit_last_name)
        self.layout.addRow(self.first_contain_layout)
        self.layout.addRow(self.layout_line_client)
        self.layout.addRow(self.tableview)
        self.layout.addRow(self.third_contain_layout)
        self.layout.addItem(verticalSpacer)
        self.layout.addRow(self.group_results)
        self.layout.addItem(verticalSpacer)
        self.layout.addRow(self.button_clean)

        self.setLayout(self.layout)

    def search_client_clicked(self):
        indexes = self.tableview.selectedIndexes()
        if len(indexes) < 1:
            QtGui.QMessageBox.critical(
                self, 'Error', 'No se selecciono ningun cliente',
                QtGui.QMessageBox.Ok)
            self.client_id = None
            return
        else:
            client_id = self.tablemodel.get_id_object_alchemy(indexes[0].row())
        self.client_id = client_id
        self.last_query_services = (
            session.query(Detalle.servicio).distinct().join(Factura).
            filter(Detalle.servicio.isnot(None), Factura.cliente == self.client_id).all())
        self.array_data = [session.query(Servicio).get(service)
                           for service in self.last_query_services]

        header_names = ['ID', 'Tipo', 'Cancelado', 'Monto Total']
        self.table_model_result = MyTableModel(
            Servicio, header_names, self, self.array_data)
        self.tableview_results.setModel(self.table_model_result)
        self.tableview_results.resizeColumnsToContents()
        self.exist_client = True

    def auto_complete_client_search(self, string):
        self.tablemodel.searchClient(string, self.line_edit_last_name.text())

    def auto_complete_last_name_search(self, string):
        self.tablemodel.searchClient(self.line_edit_search.text(), string)

    def new_service(self):
        data, result = GenericFormDialog.get_data(TipoServicio, self)
        if result:
            new_type_service = TipoServicio(
                data['nombre'],
                data['descripcion'],
            )
            session.add(new_type_service)
            session.commit()

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
            self.tableview.model().refresh_data()

    def clean_results(self):
        if self.exist_client:
            self.client_id = None
            self.last_query_services = None
            self.array_data = []
            self.exist_client = False
            self.tableview_results.model().clear()
        return

    def cancel_payment(self):
        if not self.exist_client:
            QtGui.QMessageBox.critical(
                self, 'Error', 'Primero Busque un Cliente',
                QtGui.QMessageBox.Ok)
            return

        indexes = self.tableview_results.selectedIndexes()
        if len(indexes) < 1:
            QtGui.QMessageBox.critical(
                self, 'Error', 'No se selecciono ningun servicio',
                QtGui.QMessageBox.Ok)
            return
        row = indexes[0].row()
        service_id = self.table_model_result.get_id_object_alchemy(row)
        service = session.query(Servicio).get(service_id)
        index_type_service = self.table_model_result.index(row, 1)
        type_service = self.table_model_result.data(
            index_type_service, Qt.DisplayRole)
        if service.cancelado:
            QtGui.QMessageBox.information(self, 'Servicio cancelado',
                                          'Este servicio ya esta cancelado')
            return
        cancel_question = (
            QtGui.QMessageBox.question(self, u'Cancelar %s'
                                       % str(type_service),
                                       "Desea Cancelar el pago?",
                                       QtGui.QMessageBox.Yes,
                                       QtGui.QMessageBox.No))
        if cancel_question == QtGui.QMessageBox.Yes:
            service.cancelado = True
            session.add(service)
            session.commit()
            self.tableview_results.model().refresh_data(self.array_data)

    def add_payment_to_service(self):
        if not self.exist_client:
            QtGui.QMessageBox.critical(
                self, 'Error', 'Primero Busque un Cliente',
                QtGui.QMessageBox.Ok)
            return

        indexes = self.tableview_results.selectedIndexes()
        if len(indexes) < 1:
            QtGui.QMessageBox.critical(
                self, 'Error', 'No se selecciono ningun servicio',
                QtGui.QMessageBox.Ok)
            return
        row = indexes[0].row()
        index_type_service = self.table_model_result.index(row, 1)
        service_id = self.table_model_result.get_id_object_alchemy(row)
        service = session.query(Servicio).get(service_id)
        type_service = self.table_model_result.data(
            index_type_service, Qt.DisplayRole)
        label_service = QtGui.QLabel(str(type_service))
        widget_canceled = AdvCheckBox()
        widget_canceled.setChecked(service.cancelado)

        customs_widgets = [('Servicio:', label_service),
                           ('Cancelado', widget_canceled)]
        fields = ['precio_total']
        data_pay, result_pay = GenericFormDialog.get_data(
            Detalle, self, fields=fields, customs_widgets=customs_widgets)
        if result_pay:
            sale = SaleApi(float(data_pay['precio_total']), self.client_id)
            sale.generate_factura()
            sale.add_detail_service(id_service=service_id,
                                    canceled=data_pay['Cancelado'])
            sale.save_sale()
            QtGui.QMessageBox.information(self, 'Finalizado', 'Pago Guardado')
            sale.print_factura(self)
            QtGui.QMessageBox.information(self, 'Finalizado',
                                          'Ticket Imprimido')
            # very dangerous, we need use the same object session
            session.commit()

            self.tableview_results.model().refresh_data(self.array_data)
            self.tableview_results.resizeColumnsToContents()
            self.service_payment_realeased.emit(float(data_pay['precio_total']))

    def new_service_payment(self):
        if not self.exist_client:
            QtGui.QMessageBox.critical(
                self, 'Error', 'Primero Busque un Cliente',
                QtGui.QMessageBox.Ok)
            return
        data_type_service = ['%s %s' % (str(e.id), str(e.nombre))
                             for e in session.query(TipoServicio).all()]

        widget_type_service = AdvComboBox()
        widget_type_service.addItems(data_type_service)

        widget_canceled = AdvCheckBox()
        custom_widgets = [('TipoServicio', widget_type_service),
                          ('Cancelado', widget_canceled)]
        fields = ['precio_total']
        data_payment, result_payment = GenericFormDialog.get_data(
            Detalle, self, fields=fields, customs_widgets=custom_widgets)
        if result_payment:
            sale = SaleApi(float(data_payment['precio_total']), self.client_id)
            sale.generate_factura()
            sale.add_detail_service(type_service=data_payment['TipoServicio'],
                                    canceled=data_payment['Cancelado'])
            sale.save_sale()
            QtGui.QMessageBox.information(self, 'Finalizado', 'Pago Guardado')
            sale.print_factura(self)
            QtGui.QMessageBox.information(self, 'Finalizado',
                                          'Ticket Imprimido')

            self.last_query_services = (
                session.query(Detalle.servicio).distinct().join(Factura).
                filter_by(cliente=self.client_id).all())

            self.array_data = [session.query(Servicio).get(service)
                               for service in self.last_query_services]
            self.tableview_results.model().refresh_data(self.array_data)
            self.tableview_results.resizeColumnsToContents()
            self.service_payment_realeased.emit(float(data_payment['precio_total']))



