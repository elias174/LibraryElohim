import sys
from datetime import datetime

from PyQt4 import QtGui
from PyQt4 import QtCore

from tab_views.SaleTab import Sale_Tab
from tab_views.ServicesTab import ServicesTab
from tab_views.InventoryTab import Inventory_Tab
from tab_views.AdministratorTab import Administrator_Tab

from models import *

reload(sys)
sys.setdefaultencoding('utf8')


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Sistema Pagos")
        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()

        central_layout = QtGui.QHBoxLayout()
        self.left_list = QtGui.QListWidget()
        qss_file = open('styles/styles_qstack.qss').read()
        self.left_list.setStyleSheet(qss_file)
        self.left_list.setMovement(QtGui.QListView.Static)
        central_layout.setContentsMargins(0, 0, 0, 0)

        self.left_list.setMaximumWidth((self.screenGeometry.width() / 13) - 4)
        self.left_list.setViewMode(QtGui.QListWidget.IconMode)
        self.left_list.setResizeMode(QtGui.QListWidget.Adjust)
        self.left_list.setIconSize(QtCore.QSize(70, 70))
        self.left_list.setUniformItemSizes(True)

        self.sale_widget_item = QtGui.QListWidgetItem(
            QtGui.QIcon('icons/stationer.png'), 'Ventas')
        self.sale_widget_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.sale_widget_item.setToolTip('Ventas: Realizar Ventas de Libreria')

        self.service_widget_item = QtGui.QListWidgetItem(
            QtGui.QIcon('icons/service.png'), 'Servicios')
        self.service_widget_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.service_widget_item.setToolTip(
            'Inventario: Realizar Pagos Matricula, Alimentacion, etc')

        self.inventory_widget_item = QtGui.QListWidgetItem(
            QtGui.QIcon('icons/inventory.png'), 'Inventario')
        self.inventory_widget_item.setTextAlignment(QtCore.Qt.AlignCenter)

        self.administrator_widget_item = QtGui.QListWidgetItem(
            QtGui.QIcon('icons/bill.png'), 'Facturas')
        self.administrator_widget_item.setTextAlignment(QtCore.Qt.AlignCenter)

        self.left_list.insertItem(0, self.sale_widget_item)
        self.left_list.insertItem(1, self.service_widget_item)
        self.left_list.insertItem(2, self.inventory_widget_item)
        self.left_list.insertItem(3, self.administrator_widget_item)

        self.tab_sells = Sale_Tab()
        self.tab_services = ServicesTab()
        self.tab_inventary = Inventory_Tab()
        self.tab_administrator = Administrator_Tab()

        self.stack_widget = QtGui.QStackedWidget()
        self.stack_widget.addWidget(self.tab_sells)
        self.stack_widget.addWidget(self.tab_services)
        self.stack_widget.addWidget(self.tab_inventary)
        self.stack_widget.addWidget(self.tab_administrator)

        central_layout.addWidget(self.left_list)
        central_layout.addWidget(self.stack_widget)
        self.setLayout(central_layout)
        self.setWindowIcon(QtGui.QIcon('icons/principal.png'))

        self.left_list.currentRowChanged.connect(self.change_display)
        self.tab_sells.sale_realeased.connect(self.update_administrator_tab)
        self.tab_services.service_payment_realeased.connect(self.update_administrator_tab)
        # tabs = QtGui.QTabWidget(self)
        # # tabs.setStyleSheet(
        # #     "QTabWidget::tab-bar {height: 30 px ;alignment : top;}")
        # tab_sells = Sale_Tab()
        # tab_services = ServicesTab()
        # tab_invontary = Inventory_Tab()
        # tab_administrator = Administrator_Tab()
        #
        # tabs.addTab(tab_sells, 'Ventas')
        # tabs.addTab(tab_services, 'Servicios (Matriculas, Otros)')
        # tabs.addTab(tab_invontary, 'Inventario')
        # tabs.addTab(tab_administrator, 'Administrador de Ventas')
        #
        # central_layout.addWidget(tabs)

    def update_administrator_tab(self, balance):
        self.tab_administrator.update_all_search()
        self.tab_administrator.close_box(1, balance, datetime.now())

    def change_display(self, i):
        self.stack_widget.setCurrentIndex(i)

    def closeEvent(self, event):
        event.ignore()
        ok = QtGui.QMessageBox.question(self, u'Salir',
                                        u'Seguro?',
                                        QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
        if ok == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            return

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    screenGeometry = QtGui.QApplication.desktop().availableGeometry()
    mw.resize(screenGeometry.width(), screenGeometry.height())
    mw.showMaximized()
    sys.exit(app.exec_())