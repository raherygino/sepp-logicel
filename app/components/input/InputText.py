from PyQt5.QtWidgets import QFrame
from qfluentwidgets import LineEdit
from ..layout.inputLabel import InputLabel

class InputText(QFrame):

    def __init__(self, label: str, parent):
        self.inputLabel = InputLabel(label, parent)
        self.lineEdit = LineEdit(self.inputLabel)
        self.inputLabel.addWidget(self.lineEdit)
        parent.addWidget(self.inputLabel)
    
    def text(self)-> str :
        return self.lineEdit.text()

    def setText(self, text:str):
        self.lineEdit.setText(text)

    def setMargins(self, left:int, top:int, right:int, bottom:int):
        self.inputLabel.setMargins(left, top, right, bottom)