from qfluentwidgets import TableWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

class Table():
    
    def __init__(self, parent, header: list, data: list):
        
        columnCount = len(header)
        rowCount = len(data)
        self.table = TableWidget(parent)
        self.table.setWordWrap(False)
        self.table.setRowCount(rowCount)
        self.table.setColumnCount(columnCount)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        for i, value in enumerate(data):
            for j in range(columnCount):
                self.table.setItem(i, j, QTableWidgetItem(str(value[j])))
        
        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(header)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def widget(self) -> TableWidget:
        return self.table