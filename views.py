from PyQt4 import QtGui
from PyQt4 import QtCore


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(1000, 800)
        self.setWindowTitle("Sistema Pagos")
        
        central_layout = QtGui.QVBoxLayout()
        tabs = QtGui.QTabWidget(self)
        tab_sells = Sale_Tab()

        tab_rapid_sell = QtGui.QWidget()
        tabs.addTab(tab_sells, 'Ventas')
        tabs.addTab(tab_rapid_sell, 'Venta Rapida')

        pushButton1 = QtGui.QPushButton("QPushButton 1")
        vBoxlayout = QtGui.QVBoxLayout()
        vBoxlayout.addWidget(pushButton1)
        tab_rapid_sell.setLayout(vBoxlayout)

        central_layout.addWidget(tabs)
        self.setLayout(central_layout)

    def closeEvent(self, event):
        event.ignore()
        ok = QtGui.QMessageBox.question(self, u'Salir',
                                        "Seguro?",
                                        QtGui.QMessageBox.Yes,
                                        QtGui.QMessageBox.No)
        if ok:
            event.accept()


class Sale_Tab(QtGui.QWidget):
    def __init__(self):
        super(Sale_Tab, self).__init__()

        self.screenGeometry = QtGui.QApplication.desktop().availableGeometry()
        # Initialize Layout

        self.central_layout = QtGui.QGridLayout()

        self.sale_group = QtGui.QGroupBox(str("Venta"), self)
        self.results_group = QtGui.QGroupBox(str("Resultados Busqueda"), self)

        self.central_layout.addWidget(self.sale_group, 0, 0)
        self.central_layout.addWidget(self.results_group, 0, 1)

        self.initialize_sale_group()

        self.setLayout(self.central_layout)

    def initialize_sale_group(self):
        self.layout_line = QtGui.QFormLayout()
        # First Line
        self.label_search = QtGui.QLabel("Buscar Producto:", self)
        self.edit_search = QtGui.QLineEdit(self)
        self.edit_search.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        # Second Line
        self.table_items = QtGui.QTableWidget(self)

        self.layout_line.addRow(self.label_search, self.edit_search)
        self.layout_line.addRow(self.table_items)

        self.sale_group.setMaximumWidth(self.screenGeometry.width() / 2)
        self.sale_group.setLayout(self.layout_line)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    mw = MainWindow()
    screenGeometry = QtGui.QApplication.desktop().availableGeometry()
    mw.resize(screenGeometry.width(), screenGeometry.height())
    mw.showMaximized()
    app.exec_()
