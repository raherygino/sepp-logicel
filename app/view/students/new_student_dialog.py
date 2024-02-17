from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, setTheme, Theme, BodyLabel

class editWithLabel(QVBoxLayout):
    def __init__(self, label:str,parent=None, **kwargs):
        super().__init__(None)
        self.parent = parent
        self.setContentsMargins(0,0,0,0)
        self.setSpacing(5)
        self.label = BodyLabel(parent)
        self.label.setText(label)
        self.addWidget(self.label)
        self.args = kwargs
        self.lineEdits = []
        self.LineEdit()

    def LineEdit(self):
        self.hBoxLayout = QHBoxLayout()
        self.lineEdits.clear()
        if "placeholders" in self.args.keys():
            placeholders = self.args.get("placeholders")
            for placeholder in placeholders:
                lineEdit = LineEdit(self.parent)
                lineEdit.setClearButtonEnabled(True)
                lineEdit.setPlaceholderText(placeholder)
                self.hBoxLayout.addWidget(lineEdit)
                self.lineEdits.append(lineEdit)
                
        if "combox" in self.args.keys():
            self.combox = ComboBox(self.parent)
            self.combox.setMinimumWidth(200)
            self.combox.addItems(self.args.get("combox"))
            self.hBoxLayout.addWidget(self.combox)
        
        self.addLayout(self.hBoxLayout)
            
    def value(self):
        return self.combox.text()
    
    def text(self, pos:int):
        return self.lineEdits[pos].text()
    
    def lineEdit(self, pos:int) -> LineEdit:
        return self.lineEdits[pos]
        


class NewStudentDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Ajouter un élève', self)

        self.row = QHBoxLayout()
        self.lastnameEdit = editWithLabel("Nom", self, placeholders=["Nom"])
        self.lastnameEdit.lineEdit(0).textChanged.connect(self.__isValid)
        self.firstnameEdit = editWithLabel("Prénom(s)", self, placeholders=["Prénom(s)"])
        self.row.addLayout(self.lastnameEdit)
        self.row.addLayout(self.firstnameEdit)
        
        self.row_2 = QHBoxLayout()
        self.genderEdit = editWithLabel("Genre", self, combox=["M", "F"])
        self.matriculeEdit = editWithLabel("Matricule", self, placeholders=["Matricule"])
        self.matriculeEdit.lineEdit(0).textChanged.connect(self.__isValid)
        self.gradeEdit = editWithLabel("Grade", self, combox=["EIP", "EAP"])
        self.row_2.addLayout(self.genderEdit)
        self.row_2.addLayout(self.matriculeEdit)
        self.row_2.addLayout(self.gradeEdit)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)

        self.viewLayout.addLayout(self.row)
        self.viewLayout.addLayout(self.row_2)

        self.yesButton.setEnabled(False)
        # change the text of button
        self.yesButton.setText('Ajouter')
        self.cancelButton.setText('Annuler')

        self.widget.setMinimumWidth(650)

        # self.hideYesButton()
    
    def __isValid(self, text):
        name = self.lastnameEdit.text(0)
        matricule = self.matriculeEdit.text(0)
        if len(name) > 2 and len(matricule) == 4:
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)
