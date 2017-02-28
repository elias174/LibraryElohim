import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from models import *



class Generate_Table_Report(QDialog):

    MONTHS = {
        1 : 'Enero',
        2 : 'Febrero',
        3 : 'Marzo',
        4 : 'Abril',
        5 : 'Mayo',
        6 : 'Junio',
        7 : 'Julio',
        8 : 'Agosto',
        9 : 'Septiembre',
        10 : 'Octubre',
        11 : 'Noviembre',
        12 : 'Diciembre'
    }

    def __init__(self, query, validated_data, parent = None):
        # QDialog.__init__(self, parent)
        super(Generate_Table_Report, self).__init__(parent)
        self.query = query
        self.control_singleton = False
        self.acceptButton = QPushButton("Aceptar", self)

        day = QLabel('Dia')
        month = QLabel('Mes')
        year = QLabel('Anio')
        total_purchase = QLabel('Precio Compra Total')
        total_sale = QLabel('Precio Venta Total')
        total_avail = QLabel('Utilidad Total')

        self.edit_day = QLineEdit()
        self.edit_day.setText(
            str(validated_data['day'] if validated_data['day'] else ''))
        self.edit_day.setDisabled(True)
        self.edit_month = QLineEdit()
        self.edit_month.setText(self.MONTHS.get(validated_data['month'], ''))
        self.edit_month.setDisabled(True)
        self.edit_year = QLineEdit()
        self.edit_year.setText(str(validated_data['year']))
        self.edit_year.setDisabled(True)
        self.edit_total_purchase = QLineEdit()
        self.edit_total_purchase.setDisabled(True)
        self.edit_total_sale = QLineEdit()
        self.edit_total_sale.setDisabled(True)
        self.edit_total_avail = QLineEdit()
        self.edit_total_avail.setDisabled(True)

        self.type = str(validated_data['type'])
        self.service_group = QtGui.QGroupBox(self.type, self)

        if self.type == "Libreria":
            self.initializate_library_group()
        else:
            self.initializate_service_group()
            self.edit_total_sale.hide()
            self.edit_total_purchase.hide()
            total_sale.hide()
            total_purchase.hide()

        grid = QGridLayout()
        self.layout_line_date = QtGui.QHBoxLayout()
        self.layout_line_total = QtGui.QHBoxLayout()
        self.layout_line_date.addWidget(day)
        self.layout_line_date.addWidget(self.edit_day)
        self.layout_line_date.addWidget(month)
        self.layout_line_date.addWidget(self.edit_month)
        self.layout_line_date.addWidget(year)
        self.layout_line_date.addWidget(self.edit_year)
        self.layout_line_total.addWidget(total_purchase)
        self.layout_line_total.addWidget(self.edit_total_purchase)
        self.layout_line_total.addWidget(total_sale)
        self.layout_line_total.addWidget(self.edit_total_sale)
        self.layout_line_total.addWidget(total_avail)
        self.layout_line_total.addWidget(self.edit_total_avail)
        grid.addLayout(self.layout_line_date, 1, 0)
        grid.addWidget(self.service_group, 2, 0)
        grid.addLayout(self.layout_line_total, 3, 0)
        grid.addWidget(self.acceptButton, 4, 0)

        self.setLayout(grid)

        desktopSize = QDesktopWidget().screenGeometry()
        self.setFixedSize(desktopSize.width() / 2, desktopSize.height() / 2)
        size = self.size()
        top = (desktopSize.height() / 2) - (size.height() / 2)
        left = (desktopSize.width() / 2) - (size.width() / 2)

        self.move(left, top)
        self.setWindowTitle('Mostrar Reporte')
        self.acceptButton.clicked.connect(self.close)

    def initializate_library_group(self):
        self.layout_line = QtGui.QFormLayout()
        # Creating table
        self.table_items = QtGui.QTableWidget(self)

        self.table_items.setRowCount(len(self.query))

        self.table_items.setColumnCount(5)
        self.table_items.resizeColumnsToContents()

        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table_items.horizontalHeader()
        self.table_items.setHorizontalHeaderLabels(['Producto', 'Cantidad',
                                            'Precio Compra', 'Precio Venta',
                                            'Utilidad'])
        self.stringRow = ''
        purchase = 0
        sale = 0
        avail = 0
        for detail in range(len(self.query)):
            product = session.query(Producto).get(self.query[detail]['producto'])
            self.table_items.setItem(detail, 0,
                                     QtGui.QTableWidgetItem(str(product.nombre)))
            self.table_items.setItem(detail, 1,
                                     QtGui.QTableWidgetItem(str(self.query[detail]['cantidad'])))
            self.table_items.setItem(detail, 2,
                                     QtGui.QTableWidgetItem(str(self.query[detail]['p_total_compra'])))
            self.table_items.setItem(detail, 3,
                                     QtGui.QTableWidgetItem(str(self.query[detail]['p_total_venta'])))
            self.table_items.setItem(detail, 4,
                                     QtGui.QTableWidgetItem(str(self.query[detail]['utilidad'])))

            purchase += self.query[detail]['p_total_compra']
            sale += self.query[detail]['p_total_venta']
            avail += self.query[detail]['utilidad']
            
            self.stringRow = self.stringRow + str(detail+1) + ','

        self.edit_total_purchase.setText(str(purchase))
        self.edit_total_sale.setText(str(sale))
        self.edit_total_avail.setText(str(avail))
        self.table_items.setVerticalHeaderLabels(
            QString(self.stringRow).split(','))
        self.table_items.resizeColumnsToContents()
        self.layout_line.addRow(self.table_items)
        self.service_group.setLayout(self.layout_line)

    def initializate_service_group(self):
        self.layout_line = QtGui.QFormLayout()
        # Creating table
        self.table_items = QtGui.QTableWidget(self)

        self.table_items.setRowCount(len(self.query))

        self.table_items.setColumnCount(4)
        self.table_items.resizeColumnsToContents()

        self.table_items.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table_items.horizontalHeader()

        self.table_items.setHorizontalHeaderLabels(['Nombre', 'Apellido',
                                                    'Servicio', 'Utilidad'])
        self.stringRow = ''
        avail = 0
        for detail in range(len(self.query)):
            client = session.query(Cliente).get(self.query[detail]['cliente'])
            service = session.query(TipoServicio).get(self.query[detail]['servicio'])
            self.table_items.setItem(detail, 0,
                                     QtGui.QTableWidgetItem(str(client.nombre)))
            self.table_items.setItem(detail, 1,
                                     QtGui.QTableWidgetItem(str(client.apellido)))
            self.table_items.setItem(detail, 2,
                                     QtGui.QTableWidgetItem(str(service.nombre)))
            self.table_items.setItem(detail, 3,
                                     QtGui.QTableWidgetItem(str(self.query[detail]['utilidad'])))

            avail += self.query[detail]['utilidad']
            
            self.stringRow = self.stringRow + str(detail+1) + ','

        self.edit_total_avail.setText(str(avail))
        self.table_items.setVerticalHeaderLabels(
            QString(self.stringRow).split(','))
        self.table_items.resizeColumnsToContents()
        self.layout_line.addRow(self.table_items)
        self.service_group.setLayout(self.layout_line)