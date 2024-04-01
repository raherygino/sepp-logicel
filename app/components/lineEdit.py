from PyQt5.QtWidgets import QVBoxLayout
from qfluentwidgets import LineEdit, BodyLabel, ComboBox, CompactSpinBox


class LineEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.lineEdit = LineEdit(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.lineEdit)
        
class ComboxEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, data=[], parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.combox = ComboBox(parent)
        self.combox.addItems(data)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.combox)
        
class SpinBoxEditWithLabel(QVBoxLayout):
    def __init__(self, label:str, parent=None):
        super().__init__(parent)
        self.setSpacing(2)
        self.spinbox = CompactSpinBox(parent)
        self.label = BodyLabel(label)
        self.addWidget(self.label)
        self.addWidget(self.spinbox)
        