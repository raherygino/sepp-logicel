from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import TextWrap, FluentStyleSheet, SubtitleLabel,StrongBodyLabel,  TitleLabel, CaptionLabel, SubtitleLabel, ImageLabel
from ...components.dialog.mask import MaskDialogBase
from ...components.dialog.dialog import Ui_MessageBox
from ...components.layout.Frame import Frame
from ...components.input.InputText import InputText
from ...components.input.DatePicker import InputDatePicker
from ...components.table.TableView import Table

from ...backend.models.Student import Student
from ...backend.controllers.StudentController import StudentController
from ...backend.controllers.MovementController import MovementController

class DialogStudentShow(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self,idStudent: int, parent=None):
        super().__init__(parent=parent)
        self.id = idStudent
        self.controller = StudentController()
        self.controllerMove = MovementController()
        self.student = self.controller.get(idStudent)
        self.initWidgets(parent=parent)
        self._setUpUi(self.content, self.widget)
        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.buttonGroup.setMinimumWidth(340)

    def initWidgets(self, parent):

        self.content = Frame('vertical', 'content_dial', parent=parent)
        self.row = Frame('horizontal', 'row', parent=parent)
        self.ImageLabel = ImageLabel(self.row)
        self.ImageLabel.setImage("app/resource/images/user.bmp")
        self.ImageLabel.setFixedSize(QSize(130,130))
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.row.addWidget(self.ImageLabel)

        self.col = Frame('vertical', 'col', parent=parent)
        self.showData(self.col, "Nom", "lastname")
        self.showData(self.col, "Prénom", "firstname")
        self.showData(self.col, "Genre", "genre")
        self.row.layout.addWidget(self.col, 0, Qt.AlignTop)

        self.col_2 = Frame('vertical', 'col', parent=parent)
        self.col_2.addWidget(StrongBodyLabel('Date et lieu de naissance'))
        self.col_2.addWidget(CaptionLabel(self.student.get('birthday')+" à "+self.student.get('birthplace')))
        self.showData(self.col_2, "Adresse", "address")
        self.showData(self.col_2, "Phone", "phone")
        self.row.layout.addWidget(self.col_2, 0, Qt.AlignTop)

        self.col_3 = Frame('vertical', 'col', parent=parent)

        self.col_3.addWidget(StrongBodyLabel('Compagnie'))
        self.col_3.addWidget(CaptionLabel(self.student.get('company')))
        self.col_3.addWidget(StrongBodyLabel('Section'))
        self.col_3.addWidget(CaptionLabel(self.student.get('section')))
        self.col_3.addWidget(StrongBodyLabel('Numéros'))
        self.col_3.addWidget(CaptionLabel(self.student.get('number')))
        self.row.layout.addWidget(self.col_3, 0, Qt.AlignTop)
        self.row.setMargins(0,0,0,0)
        self.content.addWidget(self.row)
        
        
        sumOfDay = self.controllerMove.sumOfDay(self.id)
        if sumOfDay != 0:
            data = self.controllerMove.getByIdStudent(self.id)
            data.append(["Total", "", sumOfDay])
            self.table = Table(self.content, ["Date","Motif","Jour"], data).widget()
            self.content.layout.addWidget(self.table)

    def showData(self, parent, title:str, key:str):
        parent.addWidget(StrongBodyLabel(title))
        parent.addWidget(CaptionLabel(self.student.get(key)))

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
