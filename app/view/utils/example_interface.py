from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import TitleLabel

class ExampleInterface(QWidget):

    def __init__(self, text:str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout()
        self.setLayout(self.vBoxLayout)
        self.label = TitleLabel(text, self)
        self.vBoxLayout.addWidget(self.label)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.setObjectName(text.replace(" ", "-"))
