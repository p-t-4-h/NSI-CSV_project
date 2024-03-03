from CSVF import * 

c = csv(";", "file.csv")
c.Import()
c.Edit(1, {"Location": "Lisbon"})
c.Export("file2.csv", ";")
