from typing import Iterable
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5 import QtWidgets
from qfluentwidgets import TableWidget

class TableView(TableWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWordWrap(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #self.header = self.horizontalHeader()
        self.verticalHeader().hide()
        self.resizeColumnsToContents()
    
    def setHorizontalHeaderLabels(self, labels: Iterable[str | None]) -> None:
        self.setColumnCount(len(labels))
        #self.header.setSectionResizeMode(len(labels) - 1, QHeaderView.Stretch)
        
        #self.header.setSectionResizeMode(len(labels) - 1, QHeaderView.Stretch)
        return super().setHorizontalHeaderLabels(labels)
        
    def setData(self, items):
        self.setRowCount(0)
        for row, item in enumerate(items):
            self.insertRow(row)
            for col, value in enumerate(item):
                self.setItem(row, col, QTableWidgetItem(str(value)))
        
        
            