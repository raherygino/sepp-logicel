from typing import Iterable
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from ..common.config import cfg
import darkdetect

class TableView(QTableWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWordWrap(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.header = self.horizontalHeader()
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setContentsMargins(0,0,0,0)
        self.setQss(cfg.get(cfg.theme))
    
    def setQss(self, newTheme: str):
        theme = newTheme.lower()
        themeColor = f'rgba{str(cfg.get(cfg.themeColor).getRgb())}'
        if theme == "auto":
            theme = "light" if darkdetect.isLight() else "dark"
        with open(f'app/resource/{theme}.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read().replace("#327bcc", themeColor))
    
    def setHorizontalHeaderLabels(self, labels: Iterable[str | None]) -> None:
        self.setColumnCount(len(labels))
        self.header.setSectionResizeMode(len(labels) - 1, QHeaderView.Stretch)
        return super().setHorizontalHeaderLabels(labels)
        
    def setData(self, items):
        self.setRowCount(0)
        for row, item in enumerate(items):
            self.insertRow(row)
            for col, value in enumerate(item):
                self.setItem(row, col, QTableWidgetItem(str(value)))
                
        self.resizeColumnsToContents()