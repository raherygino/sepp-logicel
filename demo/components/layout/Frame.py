from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

class Frame(QFrame):

    def __init__(self, layoutType: str, name: str, parent=None):
        super().__init__(parent=parent)
        
        if (layoutType == "vertical"):
            self.layout = QVBoxLayout(self)
        else:
            self.layout = QHBoxLayout(self)
        
        
        self.setObjectName(name.replace(' ', '-'))

    def addWidget(self, widget):
        self.layout.addWidget(widget)
    
    def setMargins(self, left:int , top:int, right:int, bottom:int):
        self.layout.setContentsMargins(left,top,right,bottom)
        
    def setSpacing(self, space: int):
        self.layout.setSpacing(space)
