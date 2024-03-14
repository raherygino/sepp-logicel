
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox, PushButton, setTheme, Theme
from ....common.functions import Function

class NewComportementDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.func = Function()
        self.titleLabel = SubtitleLabel('Comportement', self)
        
        self.nameLineEdit = LineEdit(self)
        self.nameLineEdit.setPlaceholderText('Titre')
        self.nameLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.textChanged.connect(self.__onChangeName)
        
        self.abrLineEdit = LineEdit(self)
        self.abrLineEdit.setPlaceholderText('Abréviation')
        self.abrLineEdit.setClearButtonEnabled(True)
        
        self.typeCombox = ComboBox(self)
        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(self.abrLineEdit)
        self.viewLayout.addWidget(self.typeCombox)

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
            