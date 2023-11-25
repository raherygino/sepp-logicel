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
from ...common.database.entity.student import Student

class DialogStudent(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, parent=None, **params):
        super().__init__(parent=parent)
        self.studentId = 0
        self.service = params.get("service")
        self.student = Student()
        self.student.gender = "Male"
        if len(params.keys()) != 0:
            self.studentId = params.get("id")
            self.student = self.service.findById(self.studentId)
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
        self.inputLastname.setText(self.student.lastname)

        self.inputFirstname = InputText("Prénom", self.row)
        self.inputFirstname.setText(self.student.firstname)

        self.selectGenre = Select("Genre", ["M", "F"], self.row)
        self.selectGenre.comboBox.setCurrentText(self.student.gender)

        self.row_1 = Frame('horizontal', 'row_1', parent=parent)
        self.inputLevel = InputText("Niveau", self.row_1)
        self.inputLevel.setText(self.student.level)

        self.inputMatricule = InputText("Matricule", self.row_1)
        self.inputMatricule.setText(self.student.matricule)

        self.inputCompany = InputText("Compagnie", self.row_1)
        self.inputCompany.setText(self.student.company)
        self.inputCompany.lineEdit.setReadOnly(True)

        self.inputSection = InputText("Section", self.row_1)
        self.inputSection.setText(self.student.section)
        self.inputSection.lineEdit.setReadOnly(True)

        self.inputNumber = InputText("Numéro", self.row_1)
        self.inputNumber.setText(self.student.matricule[2:])
        self.inputNumber.lineEdit.setReadOnly(True)
        

        #self.layoutTitle.setMargins(8,4,0,0)
        self.row.setMargins(0,0,0,0)
        self.row_1.setMargins(0,0,0,0)

        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_1)

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
    
    def getId(self):
        return self.studentId

    def studentData(self) -> Student:
        matricule = self.inputMatricule.text()
        return Student(
            self.inputLastname.text(),
            self.inputFirstname.text(),
            self.selectGenre.text(),
            self.inputLevel.text(),
            matricule[0],
            matricule[1],
            matricule[2:],
            matricule
        )
    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
