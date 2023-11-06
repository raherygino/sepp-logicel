
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import TextWrap, FluentStyleSheet, PrimaryPushButton, SubtitleLabel, ImageLabel

from ...components.dialog.mask import MaskDialogBase
from ...components.dialog.dialog import Ui_MessageBox
from ...components.layout.Frame import Frame
from ...components.input.InputText import InputText
from ...components.input.SpinBox import InputSpinBox
from ...components.input.DatePicker import InputDatePicker
from ...components.input.Select import Select
from ...common.database.entity.student import Student

class DialogStudentShow(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, service, id, parent=None):
        super().__init__(parent=parent)
        self.studentId = id
        self.service = service
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
        self.layoutTitle = Frame('horizontal', 'row', parent=parent)
        self.title = SubtitleLabel(self.student.lastname)

        self.row = Frame('horizontal', 'row', parent=parent)
        self.row.setMargins(12,12,0,0)
        
        self.ImageLabel = ImageLabel(self.row)
        self.ImageLabel.setImage("app/resource/images/user.bmp")
        self.ImageLabel.setFixedSize(QSize(130,130))
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.row.layout.addWidget(self.ImageLabel, 1, Qt.AlignTop)

        self.col =  Frame('vertical', 'col', parent=parent)
        self.col.setMargins(0,0,0,0)
        self.col.setSpacing(0)

        self.col_2 =  Frame('horizontal', 'col_2', parent=parent)
        self.col_2.setMargins(0,0,0,0)
        self.col_2.setSpacing(0)

        self.inputLastname = InputText("Lastname", self.col_2)
        self.inputLastname.lineEdit.setReadOnly(True)
        self.inputLastname.setText(self.student.lastname)
        self.inputLastname.setMargins(8,0,3,0)

        self.inputFirstname = InputText("Firstname", self.col_2)
        self.inputFirstname.lineEdit.setReadOnly(True)
        self.inputFirstname.setText(self.student.firstname)
        self.inputFirstname.setMargins(3,0,8,0)

        self.col.addWidget(self.col_2)

        
        self.col_3 =  Frame('horizontal', 'col_3', parent=parent)
        self.col_3.setMargins(0,0,0,0)
        self.col_3.setSpacing(0)

        self.selectGenre = InputText("Gender", self.col_3)
        self.selectGenre.lineEdit.setReadOnly(True)
        self.selectGenre.setText(self.student.gender)

        self.inputBirthday = InputText("Birthday", self.col_3)
        self.inputBirthday.lineEdit.setReadOnly(True)
        self.inputBirthday.lineEdit.setText(self.student.birthday)

        self.inputBirthplace = InputText("Birthplace", self.col_3)
        self.inputBirthplace.lineEdit.setReadOnly(True)
        self.inputBirthplace.setText(self.student.birthplace)
        
        self.col.addWidget(self.col_3)
        self.row.addWidget(self.col)
        
        self.row_2 = Frame('horizontal', 'row_2', parent=parent)
        self.row_2.setMargins(12,0,8,0)


        self.inputAddress = InputText("Address", self.row_2)
        self.inputAddress.setMargins(0,0,0,0)
        self.inputAddress.setText(self.student.address)
        self.inputAddress.lineEdit.setReadOnly(True)
        self.inputPhone = InputText("Phone", self.row_2)
        self.inputPhone.setMargins(0,0,0,0)
        self.inputPhone.lineEdit.setReadOnly(True)
        self.inputPhone.setText(self.student.phone)

        self.layoutTitle.setMargins(8,4,0,0)
        #self.row.setMargins(0,0,0,0)

        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_2)

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
        
    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
