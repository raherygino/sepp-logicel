import sys
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget
import sqlite3

# Worker class to perform database operation
class DatabaseWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    result = pyqtSignal(list)

    def __init__(self, dataFetch):
        super().__init__()
        self.dataFetch = dataFetch
        
    def setData(self, dataFetch):
        self.dataFetch = dataFetch

    def run(self):
        # Simulate database operation
        data = []
        total_rows = len(self.dataFetch)
        for i, row in enumerate(self.dataFetch):
            data.append(row)
            self.progress.emit(int((i + 1) * 100 / total_rows))  # Emit progress signal
            time.sleep(0.001)  # Simulate work
        self.result.emit(data)  # Emit result signal
        self.finished.emit()  # Emit finished signal