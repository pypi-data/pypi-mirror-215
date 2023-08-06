from psalpsdtools import Edrw

# SET REGION TO PROCESS
regName = "Caraga"
# SET QUARTER, ALSO USED IN READING THE S-D FILE
qtr = "Q1"
# SET FOLDER OF SOURCES/FINAL FILES INCLUDING S-D FILE
baseFolder = "D:/EDRW/Q1"
# SET S-D FILE NAME
sdFile = 'SD Q1 2023.xlsm'

myedrw = Edrw()
myedrw.update_sources(regName,qtr,baseFolder,sdFile)