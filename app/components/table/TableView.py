from qfluentwidgets import TableWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class Table():
    
    def __init__(self, parent, header: list, data: list):
        self.latestData = data
        self.table = TableWidget(parent)
        self.table.setWordWrap(False)
        self.setData(self.table, header, data)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(header)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def setData(self, tableUpdated:TableWidget, header:list, data:list):
        columnCount = len(header)
        tableUpdated.setColumnCount(columnCount)
        self.table.setRowCount(len(data))
        for i, value in enumerate(data):
            for j in range(columnCount):
                tableUpdated.setItem(i, j, QTableWidgetItem(str(value[j])))


    def widget(self) -> TableWidget:
        return self.table
    
    def refresh(self,tableUpdated, header: list, data: list):
        self.setData(tableUpdated, header, data)
