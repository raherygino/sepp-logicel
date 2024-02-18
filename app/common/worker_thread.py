import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sqlite3

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, data, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.data = data
        self.new_data = []
    def run(self):
        
        total_rows = len(self.data)

        # Update progress bar and emit signals
        for i, row in enumerate(self.data):
            # Simulate processing delay
            self.msleep(100)
            progress = int((i + 1) / total_rows * 100)
            self.update_progress.emit(progress)
            self.new_data.append(row)
        self.finished.emit()

'''class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite TableWidget with Progress")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.worker_thread = WorkerThread()
        self.worker_thread.update_progress.connect(self.update_progress_bar)
        self.worker_thread.finished.connect(self.fetch_data_finished)
        self.worker_thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def fetch_data_finished(self):
        # Once data fetching is finished, update TableWidget
        # For demonstration purposes, add data to TableWidget
        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(500)
        for i in range(500):
            item1 = QTableWidgetItem(f"Row {i+1}, Col 1")
            item2 = QTableWidgetItem(f"Row {i+1}, Col 2")
            self.table_widget.setItem(i, 0, item1)
            self.table_widget.setItem(i, 1, item2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())'''