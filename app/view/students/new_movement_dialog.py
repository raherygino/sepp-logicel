from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, BodyLabel
from ...components import EditWithLabel

class NewMouvementDialog(MessageBoxBase):
    typesMove = ["Permission", 
                     "Repos médical ou convalescence",
                     "Sanction disciplinaire",
                     "Absent non motivé", 
                     "Remarque positive"]
    subType = [
        ["-", "Exant d'effort physique"],
        ["CODIS", "Hors Tour", "Bemolenge", "Perte effet policier", "Autre"],
        ["Lettre de felicitation", "Autre"]
    ]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout()
        self.title = SubtitleLabel("Mouvement", self)
        self.subTitle = BodyLabel("Elève Agent de Police")
        
        self.row = QHBoxLayout()
        self.typeEdit = EditWithLabel("Type", self, combox=self.typesMove)
        self.typeEdit.combox.currentTextChanged.connect(self.typeChanged)
        self.subTypeEdit = EditWithLabel("Sous type", self, combox=[])
        self.subTypeEdit.combox.setEnabled(False)
        self.subTypeEdit.combox.currentTextChanged.connect(self.subTypeChanged)
        self.row.addLayout(self.typeEdit)
        self.row.addLayout(self.subTypeEdit)
        
        self.row_2 = QHBoxLayout()
        self.dateEdit = EditWithLabel("Date", self, date="Date")
        self.dayEdit = EditWithLabel("Nombre de jour", self, spin="Nombre de jour")
        self.dayMove = self.dayEdit.spin
        
        self.row_2.addLayout(self.dateEdit)
        self.row_2.addLayout(self.dayEdit)
        
        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addWidget(self.subTitle)
        self.vBoxLayout.addLayout(self.row)
        self.vBoxLayout.addLayout(self.row_2)
        self.viewLayout.addLayout(self.vBoxLayout)

    def typeChanged(self, current):
        comb = self.subTypeEdit.combox
        comb.items.clear()
        comb.removeItem(0)
        comb.setDisabled(False)
        self.dayMove.setEnabled(False)
        self.dayMove.clear()

        if (current == self.typesMove[1]):
            comb.insertItems(0, self.subType[0])
            comb.setCurrentIndex(0)
            self.dayMove.setEnabled(True)
            
        elif (current == self.typesMove[2]):
            sanction = self.subType[1]
            comb.insertItems(0, sanction)
            comb.setCurrentIndex(0)
            self.dayMove.setEnabled(False)

        elif (current == self.typesMove[4]):
            remPositive = self.subType[2]
            comb.insertItems(0, remPositive)
            comb.setCurrentIndex(0)
            self.dayMove.setEnabled(False)
        else:
            comb.clear()
            comb.setDisabled(True)
            self.dayMove.setEnabled(True)

    def subTypeChanged(self,current):
        if current == "Hors Tour" or current == "-" or current == "Exant d'effort physique":
            self.dayMove.setEnabled(True)
        else:
            self.dayMove.setEnabled(False)