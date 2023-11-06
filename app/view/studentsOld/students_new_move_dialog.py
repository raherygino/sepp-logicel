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
from ...backend.controllers.StudentController import StudentController

class DialogStudentMove(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self,idStudent, parent=None):
        super().__init__(parent=parent)
        self.controller = StudentController()
        self.student = self.controller.get(idStudent)
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
        self.title = SubtitleLabel('Mouvement')

        self.row = Frame('horizontal', 'row', parent=parent)
        self.inputLastname = InputText("Nom", self.row)
        self.inputLastname.lineEdit.setText(self.student.get('lastname'))
        self.inputLastname.lineEdit.setReadOnly(True)

        self.inputFirstname = InputText("Prénom", self.row)
        self.inputFirstname.lineEdit.setText(self.student.get('firstname'))
        self.inputFirstname.lineEdit.setReadOnly(True)

        self.row_1 = Frame('horizontal', 'row_2', parent=parent)
        self.selectLevel = InputText("Niveau", self.row_1)
        self.selectLevel.setText(self.student.get('level'))
        self.selectLevel.lineEdit.setReadOnly(True)

        self.selectCompany = InputText("Compagnie", self.row_1)
        self.selectCompany.setText(self.student.get('company'))
        self.selectCompany.lineEdit.setReadOnly(True)

        self.selectSection = InputText("Section", self.row_1)
        self.selectSection.setText(self.student.get('section'))
        self.selectSection.lineEdit.setReadOnly(True)

        self.inputNumber = InputText("Numéro", self.row_1)
        self.inputNumber.setText(self.student.get('number'))
        self.inputNumber.lineEdit.setReadOnly(True)
        
        self.row_2 = Frame('horizontal', 'row_2', parent=parent)
        self.inputMotif = Select("Motif",["Repos médical", "Permission"], self.row_2)
        self.inputDateStart = InputDatePicker("Date de debut", self.row_2)
        self.inputDayNb= InputSpinBox("Nombre de jour",False, self.row_2)

        self.layoutTitle.setMargins(8,4,0,0)
        self.row.setMargins(0,0,0,0)
        self.row_1.setMargins(0,0,0,0)
        self.row_2.setMargins(0,0,0,0)

        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_1)
        self.content.addWidget(self.row_2)

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
    
    def Data(self):
        return {
            "motif": self.inputMotif.text(),
            "dateStart": self.inputDateStart.text(),
            "day": self.inputDayNb.text()
        }
        
    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
