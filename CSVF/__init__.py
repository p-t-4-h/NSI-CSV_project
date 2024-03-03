class csv:
    def __init__(self, sep: chr, fn: str):
        self.sep = sep
        self.fn = fn
        self.header = None
        self.content = None

    def Import(self):
        with open(self.fn, 'r') as file:
            file = file.read().split("\n")
            self.header = file[0].split(self.sep)
            self.content = [line.split(self.sep) for line in file[1:]]
            return self.header, self.content
    
    def Export(self, fn, sep):
        with open(fn, 'w') as file:
            file.write(sep.join([header for header in self.header])+"\n" + "\n".join([sep.join(line) for line in self.content]))
        
    def Add(self, content):
        self.content.append(content)

    def GetHeaderID(self, header):
        try:
            return self.header.index(header)
        except ValueError:
            print("Cet HEADER n'existe pas !")

    def GetByHeader(self, header):
        id = self.GetHeaderID(header)
        return [e[id] for e in self.content]
    
    def GetByID(self, ID:int):
        return self.content[ID]

    def GetByValue(self, value, header=None):
        if header:
            id = self.GetHeaderID(header)
            return [e for e in self.content if e[id]==value]
        else:
            return [e for e in self.content if value in e]

    def SortByHeader(self, header, reverse=False):
        id = self.GetHeaderID(header)
        return sorted(self.data, key=lambda _: _[id], reverse=reverse)

    def GetID(self, header, value):
        id = self.GetHeaderID(header)
        return [self.content.index(l) for l in self.content if l[id]==value]
    
    def MoveByID(self, old_ID:int, new_ID:int):
        self.content = self.content.insert(new_ID, self.content.pop(old_ID))

    def Edit(self, ID:int, modifications: dict):
        modifications = {self.GetHeaderID(header):value for header, value in modifications.items()}
        for key, value in modifications.items():
            self.content[ID][key] = value
        return self.content
    
    def Delete(self, ID:int):
        return self.content.pop(ID)