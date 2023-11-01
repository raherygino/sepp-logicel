from PyQt5.QtWidgets import QFrame
from qfluentwidgets import SpinBox, DoubleSpinBox
from ..layout.inputLabel import InputLabel

class InputSpinBox(QFrame):

    def __init__(self, label: str, isDouble:bool, parent):
        self.inputLabel = InputLabel(label, parent)
        if isDouble :
            self.lineEdit = DoubleSpinBox(self.inputLabel)
        else :
            self.lineEdit = SpinBox(self.inputLabel)
        self.inputLabel.addWidget(self.lineEdit)
        parent.addWidget(self.inputLabel)
    
    def text(self)-> str :
        return self.lineEdit.text()

    def setText(self, text:str):
        self.lineEdit.setText(text)

    def setMargins(self, left:int, top:int, right:int, bottom:int):
        self.inputLabel.setMargins(left, top, right, bottom)