from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import TextWrap, FluentStyleSheet, PrimaryPushButton, SubtitleLabel
from ...components.dialog.mask import MaskDialogBase
from ...components.dialog.dialog import Ui_MessageBox
from ...components.layout.Frame import Frame
from ...components.input.InputText import InputText
from ...components.input.SpinBox import InputSpinBox
from ...components.input.DatePicker import InputDatePicker
from ...components.input.Select import Select

from ...backend.models.Student import Student

class DialogStudent(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initWidgets(parent=parent)
        self._setUpUi(self.content, self.widget)
        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.buttonGroup.setMinimumWidth(280)

    def initWidgets(self, parent):

        self.content = Frame('vertical', 'content_dial', parent=parent)
        self.layoutTitle = Frame('horizontal', 'row', parent=parent)
        self.title = SubtitleLabel('Ajouter un(e) élève')

        self.row = Frame('horizontal', 'row', parent=parent)
        self.inputLastname = InputText("Nom", self.row)
        self.inputFirstname = InputText("Prénom", self.row)

        self.row_1 = Frame('horizontal', 'row_1', parent=parent)
        self.selectGenre = Select("Genre", ["Masculin", "Féminin"], self.row_1)
        self.inputBirthday = InputDatePicker("Date de naissance", self.row_1)
        self.inputBirthplace = InputText("Lieu de naissance", self.row_1)

        self.row_3 = Frame('horizontal', 'row_3', parent=parent)
        self.inputAddress = InputText("Adresse", self.row_3)
        self.inputPhone = InputText("Téléphone", self.row_3)

        self.row_4 = Frame('horizontal', 'row_4', parent=parent)
        self.selectLevel = Select("Niveau", ["Elève Agent de Police", "Elève Inspecteur de Police"], self.row_4)
        self.selectCompany = Select("Compagnie", ["1ère", "2ème", "3ème"], self.row_4)
        self.selectSection = Select("Section", ["1ère", "2ème", "3ème", "4ème", "5ème", "6ème","7ème", "8ème",], self.row_4)
        self.inputNumber = InputSpinBox("Numéro",False, self.row_4)

        self.layoutTitle.setMargins(8,4,0,0)
        self.row.setMargins(0,0,0,0)
        self.row_1.setMargins(0,0,0,0)
        self.row_3.setMargins(0,0,0,0)
        self.row_4.setMargins(0,0,0,0)

        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_1)
        self.content.addWidget(self.row_3)
        self.content.addWidget(self.row_4)

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
    
    def studentData(self):
        return Student(
            self.inputLastname.text(),
            self.inputFirstname.text(),
            self.selectGenre.text(),
            self.inputHeight.text(),
            self.inputWeight.text(),
            self.inputBirthday.text(),
            self.inputBirthplace.text(),
            self.inputPhone.text(),
            self.inputAddress.text(),
            self.selectLevel.text(),
            self.selectCompany.text(),
            self.selectSection.text(),
            self.inputNumber.text()
        )
        
    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
