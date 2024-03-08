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
        self.setWindowTitle('CSV Editor')
        self.setGeometry(100, 100, 1000, 800)


        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.createMenuBar()
        self.createTable()

    def createMenuBar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu('Fichier')

        load_action = QAction(QIcon('./logo/Import.png'), 'Importer un fichier CSV', self, checkable=False)
        load_action.triggered.connect(self.loadCSV)
        file_menu.addAction(load_action)

        export_action = QAction(QIcon('./logo/Export.png'), 'Exporter en CSV', self, checkable=False)
        export_action.triggered.connect(self.exportCSV)
        file_menu.addAction(export_action)

        self.smenu = menubar.addMenu("&Trier")
        self.smenu.setEnabled(False)

    def createTable(self):
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)

        self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        action = QAction(QIcon('./logo/Plus.png'), "Nouvelle Ligne", self, checkable=False)
        action.triggered.connect(self.NewLine)
        self.table.addAction(action)

        self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        action = QAction(QIcon('./logo/Plus.png'), "Nouvelle Colonne", self, checkable=False)
        action.triggered.connect(self.NewColumn)
        self.table.addAction(action)

    def loadCSV(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Charger un fichier CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)", options=options)

        if filePath:
            self.CSV = csvf()
            self.CSV.Import(filePath)

            self.update_smenu()
            self.smenu.setEnabled(True)

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
    
    def update_smenu(self):
        if self.smenu:
            self.smenu.clear()

        group = QActionGroup(self.smenu)
        action = QAction("Aucun", self, checkable=True)
        action.setChecked(True)
        action.triggered.connect(lambda: self.on_header_selected(self.smenu))
        self.smenu.addAction(action)
        group.addAction(action)

        for h in self.CSV.header:
            action = QAction(h, self, checkable=True)
            action.triggered.connect(lambda: self.on_header_selected(self.smenu))
            self.smenu.addAction(action)
            group.addAction(action)

        group.setExclusive(True)

    def on_header_selected(self, sort_menu):
        selected_text = sort_menu.sender().text()
        self.displayCSV([self.CSV.header] + self.CSV.SortByHeader(selected_text))
            
    def NewLine(self):
        self.CSV.content.append([None for _ in range(len(self.CSV.header))])
        data = [self.CSV.header] + self.CSV.content
        self.displayCSV(data)

    def NewColumn(self):
        data = [self.CSV.header] + self.CSV.content
        [line.append(None) for line in data]
        self.displayCSV(data)
        self.table.editItem(self.table.item(0, len(self.CSV.header)-1))
        self.update_smenu()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())
