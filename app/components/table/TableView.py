from qfluentwidgets import TableWidget
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout

class TableView():
    
    def __init__(self):
                
        self.table = TableWidget(self)
        #self.tableView.clicked.connect(self.func_test)
        self.table.setWordWrap(False)
        self.table.setRowCount(5)
        self.table.setColumnCount(5)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        songInfos = [
            ['data 1.1', 'data 1.2', 'data 1.3', 'data 1.4', 'data 1.5'],
            ['data 2.1', 'data 2.2', 'data 2.3', 'data 2.4', 'data 2.5'],
            ['data 3.1', 'data 3.2', 'data 3.3', 'data 3.4', 'data 3.5'],
            ['data 4.1', 'data 4.2', 'data 4.3', 'data 4.4', 'data 4.5'],
            ['data 5.1', 'data 5.2', 'data 5.3', 'data 5.4', 'data 5.5'],
        ]
        
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.table.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(['Header 01', 'Header 02', 'Header 03', 'Header 04', 'Header 05'])
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def table(self):
        return self.table