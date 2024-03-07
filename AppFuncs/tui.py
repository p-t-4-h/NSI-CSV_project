from tabulate import tabulate
from AppFuncs.csvf import *       

class ui:

    def __init__(self):
        self.errors = []

    @staticmethod
    def Clear():
        print("\x1B[2J")
        ui.MoveTo(0, 0)

    @staticmethod
    def MoveTo(x, y):
        print(f"\x1B[{y};{x}H")
    
    @staticmethod
    def CreateTable(csv):
        if csv.header != None and csv.content != None:
            table = [csv.header]+csv.content
            return tabulate(table, headers="firstrow", showindex="always", tablefmt='fancy_grid')
        else:
            return str()

    @staticmethod
    def StartMessage():
        print("""
                  /$$$$$$   /$$$$$$  /$$    /$$       /$$$$$$$$       /$$ /$$   /$$                        
                 /$$__  $$ /$$__  $$| $$   | $$      | $$_____/      | $$|__/  | $$                        
                | $$  \__/| $$  \__/| $$   | $$      | $$        /$$$$$$$ /$$ /$$$$$$    /$$$$$$   /$$$$$$ 
                | $$      |  $$$$$$ |  $$ / $$/      | $$$$$    /$$__  $$| $$|_  $$_/   /$$__  $$ /$$__  $$
                | $$       \____  $$ \  $$ $$/       | $$__/   | $$  | $$| $$  | $$    | $$  \ $$| $$  \__/
                | $$    $$ /$$  \ $$  \  $$$/        | $$      | $$  | $$| $$  | $$ /$$| $$  | $$| $$      
                |  $$$$$$/|  $$$$$$/   \  $/         | $$$$$$$$|  $$$$$$$| $$  |  $$$$/|  $$$$$$/| $$      
                 \______/  \______/     \_/          |________/ \_______/|__/   \___/   \______/ |__/      
                                                                                           
                                                                                           
                                                                                           """)
        print("Import CSV file with : csv.Import('<filename>.csv', '<separator>')")

    def StartUi(self):
        csv = csvf()
        ui.StartMessage()
        while True:
            print(self.CreateTable(csv), "\n")
            command = input("~$> ")
            try:    
                exec(command)
                input()
            except Exception as e:
                self.errors.append(e)
                print(e)
            self.Clear()
