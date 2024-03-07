import sys
from AppFuncs import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog, QAction, QMenuBar, QDialog, QLabel, QLineEdit, QVBoxLayout, QActionGroup

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Configuration')
        self.setGeometry(200, 200, 300, 100)

        self.layout = QVBoxLayout(self)

        self.label = QLabel('Paramètre:', self)
        self.layout.addWidget(self.label)

        self.input_field = QLineEdit(self)
        self.layout.addWidget(self.input_field)

        self.ok_button = QPushButton('OK', self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.CSV = None

    def initUI(self):
        self.setWindowTitle('CSV Viewer')
        self.setGeometry(100, 100, 800, 600)


        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.createMenuBar()
        self.createTable()

    def createMenuBar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Fichier')

        load_action = QAction('Charger un fichier CSV', self)
        load_action.triggered.connect(self.loadCSV)
        file_menu.addAction(load_action)

        export_action = QAction('Exporter en CSV', self)
        export_action.triggered.connect(self.exportCSV)
        file_menu.addAction(export_action)

    def createTable(self):
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

    def loadCSV(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Charger un fichier CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)", options=options)

        if filePath:
            self.CSV = csvf()
            header, content, = self.CSV.Import(filePath)

            sort_menu = self.menuBar().addMenu("&Trier")
            group = QActionGroup(sort_menu)
            action = QAction("Aucun", self, checkable=True)
            action.setChecked(True)
            action.triggered.connect(lambda: self.on_header_selected(sort_menu))
            sort_menu.addAction(action)
            group.addAction(action)

            for h in header:
                action = QAction(h, self, checkable=True)
                action.triggered.connect(lambda: self.on_header_selected(sort_menu))
                sort_menu.addAction(action)
                group.addAction(action)

            group.setExclusive(True)

            data = [self.CSV.header] + self.CSV.content
            self.displayCSV(data)

    def exportCSV(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(self, "Exporter en CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)", options=options)

        if filePath:
            self.saveCSV(filePath)

    def displayCSV(self, data):

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))

        for row in range(len(data)):
            for column in range(len(data[0])):
                item = QTableWidgetItem(data[row][column])
                self.table.setItem(row, column, item)

    def saveCSV(self, filePath):
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                row_data.append(item.text() if item is not None else '')
            data += [row_data]
        self.CSV.header = data[0]
        self.CSV.content = data[1:]
        self.CSV.Export(filePath)
            

    def on_header_selected(self, sort_menu):
        selected_text = sort_menu.sender().text()
        self.displayCSV([self.CSV.header] + self.CSV.SortByHeader(selected_text))
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())
