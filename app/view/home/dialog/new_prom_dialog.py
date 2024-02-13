
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, PushButton, setTheme, Theme
from ....common.functions import Function

class NewPromotionDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.func = Function()
        self.titleLabel = SubtitleLabel('Promotion', self)
        
        self.rankLineEdit = LineEdit(self)
        self.rankLineEdit.setPlaceholderText('Rang | Exemple: XXIXème Promotion')
        self.rankLineEdit.setClearButtonEnabled(True)
        self.rankLineEdit.textChanged.connect(self.__onChangeName)
        
        self.nameLineEdit = LineEdit(self)
        self.nameLineEdit.setPlaceholderText('Nom de la promotion')
        self.nameLineEdit.setClearButtonEnabled(True)
        
        
        self.logoLineEdit = LineEdit(self)
        self.logoLineEdit.setPlaceholderText('Logo')
        self.logoLineEdit.setReadOnly(True)
        self.logoLineEdit.setClearButtonEnabled(True)
        self.logoLineEdit.mouseDoubleClickEvent = lambda event: self.fetchLogo(event)
        
        self.yearLineEdit = LineEdit(self)
        self.yearLineEdit.setPlaceholderText('Année')
        self.yearLineEdit.setClearButtonEnabled(True)
        
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.rankLineEdit)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.logoLineEdit)
        self.viewLayout.addWidget(self.yearLineEdit)

        # change the text of button
        self.yesButton.setText('Ajouter')
        self.cancelButton.setText('Annuler')
        self.yesButton.setEnabled(False)
        self.widget.setMinimumWidth(450)

        # self.hideYesButton()
    def __onChangeName(self, text):
        if text != "":
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)
            
    def fetchLogo(self, event):
        fileName = self.func.importFile(self, "Import image", "PNG File (*.png);;JPG File (*.jpg);;GIF File (*.gif)")
        if fileName:
            self.logoLineEdit.setText(fileName)
        else:
            self.logoLineEdit.setText("")
