# Credit : Noah Delrue | Alias pt4h
# 2024 for school


import sys
from AppFuncs import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QWidget, QFileDialog, QMenuBar, QDialog, QLabel, QLineEdit, QVBoxLayout,  QAbstractScrollArea

# Modèles de fichiers csv ajoutés a l'application
models = {"Série": [["Titre", "Genre", "Année", "Nombre d'épisodes", "Informations", "Plateforme"]], "Film": [["Titre", "Genre", "Année", "Durée", "Informations"]],}

# Classe pour générer une fenêtre 
class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.smenu_checked = "Aucun" # Valeur de tri
        self.empty = True

    def initUI(self):

        # Création de la forme de la fenêtre et des logos

        self.setWindowTitle('CSV Editor')
        self.setGeometry(0, 0, 1100, 700)
        self.setWindowIcon(QIcon('./logo/Logo.png'))

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.createMenuBar()
        self.createTable()

    def createMenuBar(self):

        # Création de la barre de menu pour effectuer des actions

        menubar = self.menuBar()

        file_menu = menubar.addMenu('Fichier')

        new_action = QAction(QIcon('./logo/Plus.png'), 'Nouveau fichier CSV', file_menu, checkable=False)
        new_action.triggered.connect(self.NewCSV)
        file_menu.addAction(new_action)

        model_action = file_menu.addMenu(QIcon('./logo/Plus.png'), "Créer depuis un modèle")
        for key in models:
            sub_model_action = QAction(key, model_action, checkable=False)
            sub_model_action.triggered.connect(lambda: self.NewCSV(model_action))
            model_action.addAction(sub_model_action)

        load_action = QAction(QIcon('./logo/Import.png'), 'Importer un fichier CSV', file_menu, checkable=False)
        load_action.triggered.connect(self.ImportCSV)
        file_menu.addAction(load_action)

        self.export_action = QAction(QIcon('./logo/Export.png'), 'Exporter en CSV', file_menu, checkable=False)
        self.export_action.triggered.connect(self.ExportCSV)
        file_menu.addAction(self.export_action)
        self.export_action.setEnabled(False)

        self.smenu = menubar.addMenu("&Trier")
        self.smenu.setEnabled(False)
        self.smenu_group = QActionGroup(self.smenu)
        self.smenu_group.setExclusive(True)

    
    def contextMenuEvent(self, event):
        
        # Ouverture d'un menu popup pour ajouter/supprimer des lignes/colonnes

        if self.empty == True:
            self.NewCSV()

        menu = QMenu(self.table)

        action_n_row = QAction(QIcon('./logo/Plus.png'), "Nouvelle Ligne", self, checkable=False)
        action_n_row.triggered.connect(self.NewRow)
        menu.addAction(action_n_row)

        action_n_col = QAction(QIcon('./logo/Plus.png'), "Nouvelle Colonne", self, checkable=False)
        action_n_col.triggered.connect(self.NewColumn)
        menu.addAction(action_n_col)

        action_delete = QAction(QIcon('./logo/Delete.png'), "Supprimer", self.table)
        action_delete.triggered.connect(self.Delete)

        if self.table.selectedItems():
            menu.addAction(action_delete)

        menu.exec(event.globalPos())
    
    def createTable(self):

        # Crée un widget Table pour afficher les valeurs du fichier

        self.table = QTableWidget(self.central_widget)
        self.layout.addWidget(self.table)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setEnabled(False)
        self.table.itemChanged.connect(self.handleItemChange)
        self.table.itemActivated.connect(self.handleItemChange)

    def handleItemChange(self, item):
        
        # Evènement exécuté quand il y a un changement dans la Table
        
        self.updateTable()
       
        # Met a jour l'élément dans la table originale
        if item.text() != list([self.CSV.header]+self.CSV.content)[item.row()] and self.onchange == False:
            self.odata[self.row_current_pos[item.row()]][item.column()] = item.text()
            self.table.resizeColumnToContents(item.column())
            self.table.resizeRowToContents(item.row())

        self.update_smenu()
        

    def ImportCSV(self):

        # Fonction pour ouvir un explorateur pour importer un fichier CSV

        filePath, _ = QFileDialog.getOpenFileName(self, "Charger un fichier CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)")

        if filePath:
            self.CSV = csvf()
            self.CSV.Import(filePath)
            self.smenu.setEnabled(True)
            self.export_action.setEnabled(True)
            self.table.setEnabled(True)
            self.empty = False

            self.odata = [self.CSV.header] + self.CSV.content
            self.row_current_pos = list(range(len(self.odata)))
            self.displayCSV(self.odata)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

    def ExportCSV(self):

        # Fonction pour exporter un fichier csv avec un exploreur de fichier

        filePath, _ = QFileDialog.getSaveFileName(self, "Exporter en CSV", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)")

        if filePath:
            self.saveCSV(filePath)

    def displayCSV(self, data):

        # Affiche les valeurs dans la table

        self.onchange = True
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data[0]))
        
        for row in range(len(data)):
            for column in range(len(data[0])):
                item = QTableWidgetItem(data[row][column])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, column, item)
        
        self.onchange = False

    def saveCSV(self, filePath):

        # Action exécutée quand le boutton sauvegarder est cliqué

        self.updateTable()
        self.CSV.Export(filePath, self.odata)
    
    def updateTable(self):

        # Met a jour la table avec les élément actuellement présent

        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                row_data.append(item.text() if item is not None else '')
            data += [row_data]
        self.CSV.header = data[0]
        self.CSV.content = data[1:]
        

    def update_smenu(self):
        
        # Met a jour le menu de tri en fonction des header du fichier

        if self.smenu:
            self.smenu.clear()
        
        for h in ["Aucun"]+self.CSV.header:
            action = QAction(h, self.smenu, checkable=True)
            action.triggered.connect(lambda: self.on_header_selected(self.smenu))
            action.setObjectName(h)
            self.smenu.addAction(action)
            self.smenu_group.addAction(action)

        self.smenu.findChild(QAction, self.smenu_checked).setChecked(True)
        
    def on_header_selected(self, sort_menu):

        # Action exécutée quand un filtre est choisi

        self.updateTable()

        self.smenu_checked = sort_menu.sender().text()

        if self.smenu_checked!="Aucun":
            data = [self.CSV.header] + self.CSV.SortByHeader(self.smenu_checked)
        else:
            data = self.odata

        self.row_current_pos = [self.odata.index(x) for x in data]
        self.odata = [data[self.row_current_pos.index(data.index(n))] for n in data]
        self.displayCSV(data)

    def NewCSV(self, model=None):
            
            # Crée un nouveau fichier CSV vide ou a partir d'un modele

            self.CSV = csvf()
            self.smenu_checked = "Aucun"
            self.update_smenu()
            self.smenu.setEnabled(True)
            self.export_action.setEnabled(True)
            self.table.setEnabled(True)
            self.empty = False
            if model:
                model = models[model.sender().text()]
                self.odata = model
                self.row_current_pos = list(range(len(self.odata)))
                self.displayCSV(model)
                self.table.resizeColumnsToContents()
                self.table.resizeRowsToContents()
            else:
                self.odata = [[]]
                self.row_current_pos = [0]
                self.NewColumn()

    def NewRow(self):

        # Action pour créer une nouvelle ligne

        self.CSV.content.append(['' for _ in range(len(self.CSV.header))])
        self.odata.append(['' for _ in range(len(self.CSV.header))])
        data = [self.CSV.header] + self.CSV.content
        self.row_current_pos = [self.odata.index(x) for x in data]
        self.displayCSV(data)

    def NewColumn(self):

        # Action pour créer une nouvelle colonne

        self.CSV.header.append('')
        [row.append('') for row in self.CSV.content]
        [row.append('') for row in self.odata]
        self.displayCSV([self.CSV.header] + self.CSV.content)
        self.table.editItem(self.table.item(0, len(self.CSV.header)-1))

    def Delete(self):

        # Action pour supprimer une ligne, une colonne ou plusieurs éléments

        data = [self.CSV.header] + self.CSV.content
        indexes = [(x.row(), x.column()) for x in self.table.selectedIndexes()]
        if all(tup[0] == indexes[0][0] for tup in indexes) and [tup[1] for tup in indexes] == list(range(len(self.CSV.header))):
            data.pop(indexes[0][0])
            self.odata.pop(self.row_current_pos[indexes[0][0]])
        elif all(tup[1] == indexes[0][1] for tup in indexes) and [tup[0] for tup in indexes] == list(range(len(data))):
            [x.pop(indexes[0][1]) for x in data]
            [x.pop(indexes[0][1]) for x in self.odata]
        else:
            for row, col in indexes:
                data[row][col] = ''
                self.odata[self.row_current_pos[row]][col] = ''

        if data == []:
            self.NewCSV()
        else:
            self.displayCSV(data)


if __name__ == '__main__':
    # Ouverture de l'app GUI quand le programme est exécuté depuis ce fichier main.py
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec())
