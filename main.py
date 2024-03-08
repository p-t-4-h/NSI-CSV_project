import sys
from AppFuncs import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog, QAction, QMenuBar, QDialog, QLabel, QLineEdit, QVBoxLayout, QActionGroup

class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        #self.CSV = None

    def initUI(self):
        self.setWindowTitle('CSV Editor')
        self.setGeometry(0, 0, 1200, 900)


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

    def createPopupMenu(self):

        """self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        action = QAction(QIcon('./logo/Plus.png'), "Nouvelle Ligne", self, checkable=False)
        action.triggered.connect(self.NewRow)
        self.table.addAction(action)

        self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
        action = QAction(QIcon('./logo/Plus.png'), "Nouvelle Colonne", self, checkable=False)
        action.triggered.connect(self.NewColumn)
        self.table.addAction(action)
        self.table.contextMenuEvent()"""
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showContextMenu)
        pass
    
    def showContextMenu(self, pos):

        indexes = [(x.column(), x.row()) for x in self.table.selectedIndexes()]
        are_equal = all(tup[0] == indexes[0][0] for tup in indexes)

        menu = QMenu(self.table)

        action = QAction(QIcon('./logo/Plus.png'), "Nouvelle Ligne", self, checkable=False)
        action.triggered.connect(self.NewRow)
        menu.addAction(action)

        action = QAction(QIcon('./logo/Plus.png'), "Nouvelle Colonne", self, checkable=False)
        action.triggered.connect(self.NewColumn)
        menu.addAction(action)

        action_delete = QAction("Supprimer", self.table)
        action.triggered.connect(lambda: self.Delete(indexes))

        if are_equal:
            menu.addAction(action_delete)

        menu.exec_(self.table.mapToGlobal(pos))
    
    def createTable(self):
        self.table = QTableWidget(self)
        self.layout.addWidget(self.table)
        self.createPopupMenu()
        self.table.setEnabled(False)

    def loadCSV(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getOpenFileName(self, "Charger un fichier CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)", options=options)

        if filePath:
            self.CSV = csvf()
            self.CSV.Import(filePath)

            self.update_smenu()
            self.smenu.setEnabled(True)
            self.table.setEnabled(True)

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
            
    def NewRow(self):
        self.CSV.content.append([None for _ in range(len(self.CSV.header))])
        data = [self.CSV.header] + self.CSV.content
        self.displayCSV(data)

    def NewColumn(self):
        data = [self.CSV.header] + self.CSV.content
        [row.append(None) for row in data]
        self.displayCSV(data)
        self.table.editItem(self.table.item(0, len(self.CSV.header)-1))
        self.update_smenu()

    def Delete(self, indexes):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())
