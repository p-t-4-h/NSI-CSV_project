# Credit : Noah Delrue | Alias pt4h
# 2024 for school

import re

class csvf:
    def __init__(self):
        self.header = []
        self.content = []
        self.psep = [',', ';', '|'] # Séparateurs acceptés 
        self.sep = str()

    def Import(self, fn):
        # Import un fichier csv avec une détection de separateur automatique
        with open(fn, 'r') as file:
            file = file.read()
            self.sep = self.psep[[file.count(x) for x in self.psep].index(max([file.count(x) for x in self.psep]))]
            file = file.split("\n")
            self.header = file[0].split(self.sep)
            self.content = [row.split(self.sep) for row in file[1:]]
            return self.header, self.content
    
    def Export(self, fn, data):
        # Export une liste en fichier CSV
        with open(fn, 'w') as file:
            file.write("\n".join([self.sep.join(row) for row in data]))
        
    def Add(self, content):
        # Ajoute du contenu a une liste
        self.content.append(content)

    def GetHeaderID(self, header):
        # Renvoit l'index d'un header 
        try:
            return self.header.index(header)
        except ValueError:
            print("Cet HEADER n'existe pas !")

    def GetByHeader(self, header):
        # Renvoit uniquement une colonne par son header
        id = self.GetHeaderID(header)
        return [e[id] for e in self.content]
    
    def GetByID(self, ID:int):
        # Récupère une ligne a un ID précis
        return self.content[ID]

    def GetByValue(self, value, header=None):
        # Renvoit toutes les valeurs qui matchent/ Une amélioration avec des regex est à venir
        if header:
            id = self.GetHeaderID(header)
            return [e for e in self.content if e[id]==value]
        else:
            return [e for e in self.content if value in e]

    def SortByHeader(self, header, reverse=False):
        # Tri par header
        if header == "Aucun":
            return self.content
        else:
            id = self.GetHeaderID(header)
            return sorted(self.content, key=lambda _: _[id], reverse=reverse)

    def GetID(self, header, value):
        # Récupère une valeur par header
        id = self.GetHeaderID(header)
        return [self.content.index(l) for l in self.content if l[id]==value]
    
    def MoveByID(self, old_ID:int, new_ID:int):
        # Déplace une ligne par ID
        self.content = self.content.insert(new_ID, self.content.pop(old_ID))

    def Edit(self, ID:int, modifications: dict):
        # Modifie les données de la liste
        modifications = {self.GetHeaderID(header):value for header, value in modifications.items()}
        for key, value in modifications.items():
            self.content[ID][key] = value
        return self.content
    
    def Delete(self, ID:int):
        # Suprimme une ligne
        return self.content.pop(ID)
