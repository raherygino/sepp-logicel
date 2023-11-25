from ..layout.Frame import Frame
from qfluentwidgets import BodyLabel, StrongBodyLabel

class LabelData():
    def __init__(self, parent, label:str, value:str):
        self.col = Frame("vertical", value.replace(" ","_"), parent=parent)
        self.col.setMargins(8,0,8,8)
        self.col.addWidget(StrongBodyLabel(label))
        self.col.addWidget(BodyLabel(value))
        self.col.setSpacing(0)
        parent.addWidget(self.col)