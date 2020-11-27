import os
from openpyxl import load_workbook

filePath = r"E:\TodoList\GBW\test"
for dirpath, dirnames, filenames in os.walk(filePath):
    path = [os.path.join(dirpath, names) for names in filenames]
for filename in path:
    workbook = load_workbook(filename=filename)
    sheet = workbook['Sheet1']
    for i in range(42):
        sheet.row_dimensions[i].height = 18
    workbook.save(filename)