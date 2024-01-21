
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QDate
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import BodyLabel, StrongBodyLabel, CalendarPicker, SubtitleLabel, ImageLabel

from ...components.dialog.mask import MaskDialogBase
from ...components.dialog.dialog import Ui_MessageBox
from ...components.layout.Frame import Frame
from ...components.input.InputText import InputText
from ...components.label.LabelData import LabelData
from ...components.input.SpinBox import InputSpinBox
from ...components.input.DatePicker import InputDatePicker
from ...components.input.Select import Select
from ...common.database.entity.student import Student
from .student_show import DialogStudentShow
from ...common.database.entity.mouvement import Mouvement
from ...common.database.utils.constants import *

class DialogStudentMove(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, service, serviceMove, id, parent=None):
        super().__init__(parent=parent)
        self.studentId = id
        self.service = service
        self.row = DialogStudentShow(service, serviceMove, id, parent).row
        self.student = self.service.findById(self.studentId)
        self.initWidgets(parent=parent)
        self._setUpUi(self.content, self.widget)
        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.buttonGroup.setMinimumWidth(280)
        self.yesButton.setText("Ok")

    def initWidgets(self, parent):
        self.content = Frame('vertical', 'content_dial', parent=parent)
        self.content.setSpacing(0)

        self.layoutTitle = Frame('vertical', 'row', parent=parent)
        self.layoutTitle.setMargins(10,0,0,0)
        self.layoutTitle.setSpacing(0)

        self.title = SubtitleLabel(f"Nouvelle mouvement")
        self.subtitle = BodyLabel(f"{self.student.level} {self.student.firstname}")

        self.layoutTitle.addWidget(self.title)
        self.layoutTitle.addWidget(self.subtitle)

        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)

        self.row_2 = Frame("vertical", "row_2", self.content)
        self.row_2.setMargins(0,0,0,0)
        self.row_2.setSpacing(0)

        self.col = Frame("horizontal", "col", self.content)
        self.col.setMargins(0,0,0,0)
        self.col.setSpacing(0)
        self.typesMove = ["Permission", 
                     "Repos médical ou convalescence",
                     "Sanction disciplinaire",
                     "Absent non motivé", 
                     "Remarque positive"]
        
        self.typeMove = Select("Type", self.typesMove, self.col)
        self.typeMove.comboBox.currentTextChanged.connect(self.typeChanged)

        self.subTypeMove = Select("Sous type", [], self.col)
        self.subTypeMove.comboBox.currentTextChanged.connect(self.subTypeChanged)
        self.subTypeMove.comboBox.setDisabled(True)

        self.row_3 = Frame("horizontal", "row_3", self.content)
        self.row_3.setMargins(0,0,0,0)
        
        self.dateMove = InputDatePicker("Date", self.row_3)
        self.dateMove.lineEdit.setDate(QDate(2023,1,1))
        self.dayMove = InputSpinBox("Nombre de jour",False, self.row_3)

        self.row_2.addWidget(self.col)
        self.row_2.addWidget(self.row_3)
        
        self.content.addWidget(self.row_2)

    def typeChanged(self, current):
        comb = self.subTypeMove.comboBox
        comb.items.clear()
        comb.removeItem(0)
        comb.setDisabled(False)
        self.dayMove.setEnabledLineEdit(False)
        self.dayMove.lineEdit.clear()

        if (current == self.typesMove[1]):
            comb.insertItems(0, ["-", "Exant d'effort physique"])
            comb.setCurrentIndex(0)
            self.dayMove.setEnabledLineEdit(True)
            
        elif (current == self.typesMove[2]):
            sanction = ["CODIS", "Hors Tour", "Bemolenge", "Perte effet policier", "Autre"]
            comb.insertItems(0, sanction)
            comb.setCurrentIndex(0)
            self.dayMove.setEnabledLineEdit(False)

        elif (current == self.typesMove[4]):
            remPositive = ["Lettre de felicitation", "Autre"]
            comb.insertItems(0, remPositive)
            comb.setCurrentIndex(0)
            self.dayMove.setEnabledLineEdit(False)
        else:
            comb.clear()
            comb.setDisabled(True)
            self.dayMove.setEnabledLineEdit(True)

        #print(comb.text())

    def subTypeChanged(self,current):
        if current == SUB_TYPE_MOVE["HORS_TOUR"] or current == "-" or current == SUB_TYPE_MOVE['EX_PHYS']:
            self.dayMove.setEnabledLineEdit(True)
        else:
            self.dayMove.setEnabledLineEdit(False)


    def dataMouvement(self):
        typeMove = self.typeMove.text()
        subTypeMove =  self.subTypeMove.text()
        if typeMove == TYPE_MOVE["REM_POS"] and subTypeMove == SUB_TYPE_MOVE['OTHER']:
            subTypeMove = f'{subTypeMove} {typeMove}'
        if typeMove == TYPE_MOVE["SACT_DISC"] and subTypeMove == SUB_TYPE_MOVE["OTHER"]:
            subTypeMove = f'{subTypeMove} {typeMove}'

        return Mouvement(
            self.studentId,
            typeMove,
            subTypeMove,
            self.dateMove.text(),
            self.dayMove.text()
        )

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
        
    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
