import ast
import sys
import os

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *


from models import *
from models_qt import MyTableModel
from Generic_forms import GenericFormDialog, AdvComboBox
from Client import ClientDialog
from api.api_sales import SaleApi


LIMIT_RESULTS = 20
MIN_PRODUCTS = 1


class ResultsButtonGroup(QtGui.QButtonGroup):
    def __init__(self, parent, results, layout):
        super(QtGui.QButtonGroup, self).__init__()
        self.parent = parent
        self.layout = layout
        self.refresh(results)

#   Maybe this should be change for personalize
    def refresh(self, results):
        n = 0
        rows = None
        cols = 4
        if len(results) % 4 == 0:
            rows = len(results)/4
        else:
            rows = (len(results)/4)+1
        j = 0
        for i in range(rows):
            for result in results[n:n+4]:
                button = QtGui.QPushButton(self.parent)
                playout = QtGui.QVBoxLayout()

                font_label_product = QtGui.QFont()
                font_label_product.setBold(True)

                font_label_price = QtGui.QFont()
                font_label_price.setUnderline(True)

                label = QtGui.QLabel(result.nombre)
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setWordWrap(True)
                label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                label.setMouseTracking(False)
                label.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
                label.setFont(font_label_product)

                label_detail = QtGui.QLabel(result.detalle)
                label_detail.setAlignment(QtCore.Qt.AlignCenter)
                label_detail.setWordWrap(True)
                label_detail.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                label_detail.setMouseTracking(False)
                label_detail.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

                label_price = QtGui.QLabel(str(result.precio_venta))
                label_price.setAlignment(QtCore.Qt.AlignCenter)
                label_price.setWordWrap(True)
                label_price.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
                label_price.setMouseTracking(False)
                label_price.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
                label_price.setFont(font_label_price)

                playout.addWidget(label)
                playout.addWidget(label_price)
                playout.addWidget(label_detail)
                playout.setSpacing(0)
                playout.setMargin(0)
                playout.setContentsMargins(5, 5, 5, 5)

                button.setText('')
                button.setMinimumHeight(110)
                button.setLayout(playout)

                tool_tip = '%s \n Stock: %s \n Precio: %s' % (
                    result.nombre,
                    result.stock,
                    str(result.precio_venta))
                button.setToolTip(QtCore.QString(tool_tip))
                self.addButton(button, result.id)
                self.layout.addWidget(button, i, j)
                j += 1
            j = 0
            n += 4


class Sale_Tab(QtGui.QWidget):
    change_table = QtCore.pyqtSignal()
    sale_realeased = QtCore.pyqtSignal(float)

    def __init__(self):
        super(Sale_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout

        # Signal to check total
        self.last_query = (session.query(Producto).limit(LIMIT_RESULTS).all())

        self.central_layout = QtGui.QGridLayout()

        self.sale_group = QtGui.QGroupBox(str("Venta"), self)
        self.search_group = QtGui.QGroupBox(str("Busqueda"), self)

        self.central_layout.addWidget(self.sale_group, 0, 0)
        self.central_layout.addWidget(self.search_group, 0, 1)

        self.initialize_sale_group()
        self.initialize_search_group()

        #QtCore.QObject.connect(self.button_group, QtCore.SIGNAL("buttonClicked(int)"),
        #                      self, QtCore.SLOT("ResultButtonClick(int)"))
        self.change_table.connect(self.update_total)
        self.setLayout(self.central_layout)

    def update_last_query(self):
        self.last_query = (session.query(Producto).limit(LIMIT_RESULTS).all())

    def initialize_sale_group(self):
        self.layout_line = QtGui.QFormLayout()
        # First Line
        # self.label_search = QtGui.QLabel("Buscar Producto:", self)
        # self.edit_search = QtGui.QLineEdit(self)
        # self.edit_search.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, 
        #                                                  QtGui.QSizePolicy.Fixed))
        # Second Line
        self.table_items = QtGui.QTableWidget(self)
        self.table_items.setColumnCount(6)
        self.table_items.setRowCount(0)
        self.table_items.setMinimumHeight(self.screenGeometry.height() / 2)
        self.layout_line.addRow(self.table_items)
        self.table_items.setHorizontalHeaderLabels(["ID", "Cantidad", "Producto",
                                                    "P.Unidad", "P.Total",
                                                    "Eliminar"])

        self.sale_group.setMaximumWidth(self.screenGeometry.width() / 2)
        self.sale_group.setLayout(self.layout_line)

        # third line, 4th line
        self.edit_search_added = QtGui.QLineEdit(self)
        self.label_search_added = QtGui.QLabel("Buscar en Aniadidos:", self)
        self.total_line = QtGui.QLabel("0.00", self)
        self.pay_line = QtGui.QLabel("0.00", self)
        self.layout_line.addRow(self.label_search_added, self.edit_search_added)
        self.layout_line.addRow("Total: ", self.total_line)
        self.layout_line.addRow("A pagar: ", self.pay_line)

        # Line Client
        self.client_label = QtGui.QLabel('1 Cliente Anonimo')
        self.button_client = QtGui.QPushButton('Aniadir Cliente')
        self.button_client.setMaximumWidth(self.screenGeometry.width() / 8)
        self.layout_line.addRow(self.client_label, self.button_client)

        self.button_client.clicked.connect(self.open_dialog_client)

        self.button_generate_sale = QtGui.QPushButton('Realizar Venta')
        self.button_clean_table = QtGui.QPushButton('Limpiar')

        self.label_list = QtGui.QLabel('Administrar Listas:')
        self.button_save_list = QtGui.QPushButton('Guardar como Lista')
        self.button_load_list = QtGui.QPushButton('Cargar Lista')
        self.button_erase_list = QtGui.QPushButton('Eliminar una Lista')

        self.button_load_list.clicked.connect(self.load_list)
        self.button_save_list.clicked.connect(self.save_list)
        self.button_generate_sale.clicked.connect(self.realease_sale)
        self.button_clean_table.clicked.connect(self.clear_table)
        self.button_erase_list.clicked.connect(self.erase_list)

        self.layout_line.addRow(self.table_items)
        self.layout_line.addRow(self.button_generate_sale)
        self.layout_line.addRow(self.button_clean_table)

        self.group_list = QtGui.QGroupBox('Administrar Listas')

        self.layout_lists = QtGui.QHBoxLayout()
        self.layout_lists.addWidget(self.button_save_list)
        self.layout_lists.addWidget(self.button_load_list)
        self.layout_lists.addWidget(self.button_erase_list)
        self.group_list.setLayout(self.layout_lists)

        self.layout_line.addRow(self.group_list)

    def initialize_search_group(self):
        self.layout_line_search = QtGui.QFormLayout()

        self.label_search = QtGui.QLabel("Buscar Producto:", self)
        self.label_type_view = QtGui.QLabel("Tipo de Vista:", self)
        self.results_group = QtGui.QGroupBox(str("Resultados:"), self)

        self.edit_search = QtGui.QLineEdit(self)
        self.combo_type_search = QtGui.QComboBox()
        self.combo_type_search.addItem("Botones")
        self.combo_type_search.addItem("Tabla")
        self.combo_type_search.setMaximumWidth(100)

        self.layout_line_search.addRow(self.label_search, self.edit_search)
        self.layout_line_search.addRow(self.label_type_view, self.combo_type_search)

        header_names = ['ID', 'Categoria', 'Nombre', 'Precio Compra',
                        'Precio Venta', 'Stock', 'Detalle']
        self.tablemodel = MyTableModel(Producto, header_names, self)
        self.layout_results = QtGui.QGridLayout()
        self.results_group.setLayout(self.layout_results)
        self.results_group.setMinimumHeight(self.screenGeometry.height() -
                                            (self.screenGeometry.height() / 3.5))

        def view_buttons():
            QtGui.QWidget().setLayout(self.layout_results)
            self.layout_results = QtGui.QGridLayout()
            self.results_group.setLayout(self.layout_results)
            self.button_group = ResultsButtonGroup(self, self.last_query,
                                                   self.layout_results)
            QtCore.QObject.connect(self.button_group,
                                   QtCore.SIGNAL("buttonClicked(int)"), self,
                                   QtCore.SLOT("ResultButtonClick(int)"))
            self.edit_search.textChanged.connect(self.on_search_edit_changed)

        def view_table():
            self.tableview = QTableView()
            self.button_add_table = QtGui.QPushButton('Aniadir')
            self.tableview.setAlternatingRowColors(True)
            self.tableview.setModel(self.tablemodel)
            self.tableview.resizeColumnsToContents()
            QtGui.QWidget().setLayout(self.layout_results)
            self.layout_results = QtGui.QVBoxLayout()
            self.layout_results.addWidget(self.tableview)
            self.layout_results.addWidget(self.button_add_table)
            self.results_group.setLayout(self.layout_results)
            self.results_group.setMinimumHeight(self.screenGeometry.height() -
                                                (self.screenGeometry.height() / 3.5))
            self.edit_search.textChanged.connect(self.on_search_table_edit_changed)
            self.button_add_table.clicked.connect(self.add_selected_rows)

        def change_results_view(index):
            try:
                self.edit_search.textChanged.disconnect()
            except TypeError:
                pass
            if index is 0:
                view_buttons()
            elif index is 1:
                view_table()

        self.layout_line_search.addRow(self.results_group)

        self.search_group.setLayout(self.layout_line_search)
        self.edit_search_added.textChanged.connect(self.on_search_edit_added_changed)
        self.combo_type_search.activated.connect(change_results_view)
        view_buttons()

    def add_selected_rows(self):
        indexes = self.tableview.selectedIndexes()
        for index in indexes:
            product_id = self.tablemodel.get_id_object_alchemy(index.row())
            self.ResultButtonClick(product_id)

    def open_dialog_client(self):
        if self.client_label.text() != '1 Cliente Anonimo':
            self.button_client.setText('Aniadir Cliente')
            self.client_label.setText('1 Cliente Anonimo')
        else:
            id_client, result = ClientDialog.get_client(self)
            if result and id_client:
                client = session.query(Cliente).get(id_client)
                self.client_label.setText('%s %s %s' % (str(client.id),
                                                        client.nombre,
                                                        client.apellido))
                self.button_client.setText('Eliminar Cliente')

    @QtCore.pyqtSlot(int)
    def ResultButtonClick(self, id):
        product = session.query(Producto).get(id)
        if product.stock < 1:
            QtGui.QMessageBox.critical(self, 'Error',
                                       'No hay stock de este producto',
                                       QtGui.QMessageBox.Ok)
            return
        product_id = str(product.id)
        items = self.table_items.findItems(product_id, QtCore.Qt.MatchExactly)
        if items:
            ok = QtGui.QMessageBox.question(self, u'Doble Producto %s'
                                            % str(product.nombre),
                                            "Desea Agregarlo de nuevo?",
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
            if ok == QtGui.QMessageBox.Yes:
                row_item = items[0].row()
                widget_spin = self.table_items.cellWidget(row_item, 1)
                val = (widget_spin.value() + 1)
                if SaleApi.get_quantity_product(product.id) >= val:
                    # to avoid that other function tries to change the value
                    widget_spin.blockSignals(True)
                    widget_spin.setValue(val)
                    qty = float(val)
                    new_value = str(float(self.table_items.item(row_item, 3).text()) * qty)
                    self.table_items.item(row_item, 4).setText(new_value)
                    self.change_table.emit()
                    widget_spin.blockSignals(False)
                    return
                else:
                    QtGui.QMessageBox.critical(self,
                                               'Error',
                                               'No hay mas stock de este producto',
                                               QtGui.QMessageBox.Ok)
            else:
                return
        else:
            self.add_product_table(product)

    def on_search_table_edit_changed(self, string):
        self.tablemodel.setFilter('nombre', string)

    def on_search_edit_changed(self, string):
        text_query = '%'+unicode(string.toUtf8(), encoding="UTF-8")+'%'
        self.last_query = (
            session.query(Producto).filter(
                Producto.nombre.like(text_query),
                Producto.stock > MIN_PRODUCTS).limit(LIMIT_RESULTS).all()
        )

        for i in reversed(range(self.layout_results.count())):
            self.layout_results.itemAt(i).widget().setParent(None)
        self.button_group.refresh(self.last_query)

    def on_search_edit_added_changed(self, string):
        for row in xrange(self.table_items.rowCount()):
                self.table_items.showRow(row)
        if string != '':
            to_hide = []
            items = [item.row()
                     for item in self.table_items.findItems(string, QtCore.Qt.MatchContains)
                     if item.column() == 2]
            for row in xrange(self.table_items.rowCount()):
                if not (row in items):
                    self.table_items.hideRow(row)

    def delete_row(self):
        button = QtGui.qApp.focusWidget()
        index = self.table_items.indexAt(button.pos())
        self.table_items.removeRow(index.row())
        self.change_table.emit()

    def add_product_table(self, product, quantity=1):
        stock_product = SaleApi.get_quantity_product(product.id)
        if stock_product < quantity:
            QMessageBox.critical(
                self,
                'Error',
                'No tenemos Stock para %s no es posible agregarlo' % product.nombre,
                QtGui.QMessageBox.Ok)
            return
        self.i = self.table_items.rowCount()
        self.table_items.insertRow(self.i)

        button = QtGui.QPushButton()
        button.clicked.connect(self.delete_row)
        button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        button.setIcon(QtGui.QIcon('icons/delete-128.png'))

        def quantity_changed(val):
            old_value = spinbox.value()
            spin = QtGui.qApp.focusWidget()
            try:
                row = self.table_items.indexAt(spin.pos()).row()
            except AttributeError:
                return
            qty = float(val)
            new_value = str(float(self.table_items.item(row, 3).text()) * qty)
            self.table_items.setItem(row, 4, QtGui.QTableWidgetItem(new_value))
            self.change_table.emit()

        spinbox = QtGui.QSpinBox()
        spinbox.setValue(quantity)
        spinbox.setMinimum(1)
        spinbox.setMaximum(stock_product)

        spinbox.valueChanged.connect(quantity_changed)

        product_item = QtGui.QTableWidgetItem(str(product.id))
        product_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.table_items.setItem(self.i, 0, product_item)

        self.table_items.setCellWidget(self.i, 1, spinbox)

        product_name = QtGui.QTableWidgetItem(str(product.nombre))
        product_name.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.table_items.setItem(self.i, 2, product_name)

        product_price_sale = QtGui.QTableWidgetItem(str(product.precio_venta))
        product_price_sale.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        self.table_items.setItem(self.i, 3, product_price_sale)

        product_price_sale_total = QtGui.QTableWidgetItem(str(product.precio_venta * quantity))
        product_price_sale_total.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

        self.table_items.setItem(self.i, 4, product_price_sale_total)

        self.table_items.setCellWidget(self.i, 5, button)

        self.table_items.resizeColumnsToContents()
        self.change_table.emit()

    def update_total(self):
        index_price = 4
        price = 0
        for row in xrange(self.table_items.rowCount()):
            item = self.table_items.item(row, index_price)
            price += float(item.text())
        self.total_line.setText(QtCore.QString(str(price)))

    def clear_table(self):
        while self.table_items.rowCount() > 0:
            self.table_items.removeRow(0)
        self.table_items.setRowCount(0)
        self.change_table.emit()

    def save_list(self):

        if self.table_items.rowCount() < 1:
            QtGui.QMessageBox.critical(self, 'Error',
                                       'Debe agregar por lo menos un producto',
                                       QtGui.QMessageBox.Ok)
            return

        message = QtGui.QMessageBox(self)
        message.setText('Como desea guardar la lista?')
        message.setIcon(QtGui.QMessageBox.Question)
        button_update = QtGui.QPushButton('Actualizar')
        message.addButton(button_update, QtGui.QMessageBox.ActionRole)
        button_new = QtGui.QPushButton('Crear Nuevo')
        message.addButton(button_new, QtGui.QMessageBox.ActionRole)
        message.addButton(QtGui.QMessageBox.Cancel)

        message.exec_()

        if message.clickedButton() == button_update:
            lists = ['%s %s' % (str(e.id), str(e.nombre))
                    for e in session.query(Lista).all()]
            if len(lists) < 1:
                QtGui.QMessageBox.critical(self, 'Error',
                                           'No existen listas guardadas',
                                           QtGui.QMessageBox.Ok)
                return
            combo = AdvComboBox(self)
            combo.addItems(lists)
            data, result = GenericFormDialog.get_data(
                Lista, parent=self, fields=[''],
                customs_widgets=[('Lista', combo)], title='Actualizar Lista'
            )
            if result:
                question = QtGui.QMessageBox.question(
                    self, 'Confirmar',
                    'Desea sobreescribir esta lista?',
                    QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if question == QtGui.QMessageBox.No:
                    return
                id_list = data['Lista']
                elements = str(self.extract_id_quantity_table())
                current_list = session.query(Lista).get(id_list)
                current_list.elementos = elements
                session.commit()
                QtGui.QMessageBox.information(self, 'Finalizado',
                                              'Lista guardada')

        elif message.clickedButton() == button_new:
            data, result = GenericFormDialog.get_data(
                Lista, parent=self, fields=['nombre'])
            if result:
                name_list = data['nombre']
                elements = str(self.extract_id_quantity_table())
                new_list = Lista(name_list, elements)
                session.add(new_list)
                session.commit()
                QtGui.QMessageBox.information(self, 'Finalizado',
                                              'Lista guardada')

    def load_list(self):
        lists = ['%s %s' % (str(e.id), str(e.nombre))
                 for e in session.query(Lista).all()]
        if len(lists) < 1:
            QtGui.QMessageBox.critical(self, 'Error',
                                       'No existen listas guardadas',
                                       QtGui.QMessageBox.Ok)
            return
        combo = AdvComboBox(self)
        combo.addItems(lists)
        data, result = GenericFormDialog.get_data(
            Lista, parent=self, fields=[''],
            customs_widgets=[('Lista', combo)], title='Cargar Lista'
        )
        if result:
            question = QtGui.QMessageBox.question(
                self, 'Confirmar', 'Cargar esta lista eliminara los productos '
                                   'agregados, desea continuar?',
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if question == QtGui.QMessageBox.No:
                return
            self.clear_table()
            id_list = data['Lista']
            current_list = session.query(Lista).get(id_list)
            elements = ast.literal_eval(current_list.elementos)
            not_availables = []
            for e in elements:
                self.add_product_table(session.query(Producto).get(e[0]), e[1])

    def erase_list(self):
        lists = ['%s %s' % (str(e.id), str(e.nombre))
                 for e in session.query(Lista).all()]
        if len(lists) < 1:
            QtGui.QMessageBox.critical(self, 'Error',
                                       'No existen listas guardadas',
                                       QtGui.QMessageBox.Ok)
            return
        combo = AdvComboBox(self)
        combo.addItems(lists)
        data, result = GenericFormDialog.get_data(
            Lista, parent=self, fields=[''],
            customs_widgets=[('Lista', combo)], title='Borrar una Lista'
        )
        if result:
            id_list = data['Lista']
            current_list = session.query(Lista).get(id_list)
            question = QtGui.QMessageBox.question(
                self, 'Confirmar', 'Eliminar Lista: %s?' % current_list.nombre,
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if question == QtGui.QMessageBox.No:
                return
            session.delete(current_list)
            session.commit()
            QtGui.QMessageBox.information(self, 'Finalizado',
                                          'Lista Eliminada')

    def extract_id_quantity_table(self):
        data = []
        index_id = 0
        index_quantity = 1
        for row in xrange(self.table_items.rowCount()):
            item_id = int(self.table_items.item(row, index_id).text())
            quantity = self.table_items.cellWidget(row, index_quantity).value()
            data.append((item_id, quantity))
        return data

    def realease_sale(self):
        result = QtGui.QMessageBox.question(self, 'Confirmar',
                                            'Realizar Venta?',
                                            QtGui.QMessageBox.Yes,
                                            QtGui.QMessageBox.No)
        if result == QMessageBox.Yes:
            index_id = 0
            index_quantity = 1
            client_id = int(str(self.client_label.text()).split(' ')[0])
            price_total = float(str(self.total_line.text()))
            if price_total > float(0):
                sale = SaleApi(price_total, client_id)
                sale.generate_factura()
                for row in xrange(self.table_items.rowCount()):
                    item_id = int(self.table_items.item(row, index_id).text())
                    quantity = self.table_items.cellWidget(row, index_quantity).value()
                    try:
                        sale.add_detail(item_id, quantity)
                    except AssertionError:
                        QtGui.QMessageBox.critical(self, 'Error',
                                                   'Algo salio mal, venta anulada',
                                                   QtGui.QMessageBox.Ok)
                        return
                sale.save_sale()
                QtGui.QMessageBox.information(self, 'Finalizado', 'Venta Guardada')
                sale.print_factura(self)
                QtGui.QMessageBox.information(self, 'Finalizado', 'Ticket Imprimido')
                self.clear_table()
                QtGui.QMessageBox.information(self, 'Finalizado', 'Venta Finalizada')
                self.sale_realeased.emit(price_total)
                self.update_last_query()
                self.button_group.refresh(self.last_query)

            else:
                QtGui.QMessageBox.critical(self, 'Error',
                                           'Venta vacia, no es posible realizar',
                                           QtGui.QMessageBox.Ok)
                return
        else:
            return