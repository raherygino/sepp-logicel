
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import BodyLabel, StrongBodyLabel, PrimaryPushButton, SubtitleLabel, ImageLabel

from ...components.dialog.mask import MaskDialogBase
from ...components.dialog.dialog import Ui_MessageBox
from ...components.layout.Frame import Frame
from ...components.input.InputText import InputText
from ...components.label.LabelData import LabelData
from ...components.input.SpinBox import InputSpinBox
from ...components.input.DatePicker import InputDatePicker
from ...components.input.Select import Select
from ...components.table.TableView import Table
from ...common.database.entity.student import Student
from ...common.database.service.mouvement_service import MouvementService

class DialogStudentShow(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, service, serviceMove, id, parent=None):
        super().__init__(parent=parent)
        self.studentId = id
        self.service = service
        self.student = self.service.findById(self.studentId)
        self.serviceMove = serviceMove
        self.initWidgets(parent=parent)
        self._setUpUi(self.content, self.widget)
        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        #self.buttonGroup.setMinimumWidth(480)
        self.yesButton.setText("Exporter")

    def initWidgets(self, parent):

        self.content = Frame('vertical', 'content_dial', parent=parent)
        self.content.setSpacing(0)
        self.layoutTitle = Frame('horizontal', 'row', parent=parent)
        self.title = SubtitleLabel(self.student.lastname)
        

        self.row = Frame('horizontal', 'row', parent=parent)
        self.row.setMargins(12,12,0,0)
        
        self.ImageLabel = ImageLabel(self.row)
        self.ImageLabel.setImage("app/resource/images/user.bmp")
        self.ImageLabel.setFixedSize(QSize(100,100))
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.row.layout.addWidget(self.ImageLabel, 1, Qt.AlignTop)

        self.col =  Frame('vertical', 'col', parent=parent)
        self.col.setMargins(0,0,0,0)
        self.col.setSpacing(0)

        self.col_2 =  Frame('horizontal', 'col_2', parent=parent)
        self.col_2.setMargins(0,0,0,0)
        self.col_2.setSpacing(0)
        
        self.lastname = LabelData(self.col_2, "Nom", self.student.lastname)
        self.firstname = LabelData(self.col_2, "Prénom", self.student.firstname)
        self.gender = LabelData(self.col_2, "Genre", self.student.gender)
        self.col.addWidget(self.col_2)

        self.col_3 =  Frame('horizontal', 'col_3', parent=parent)
        self.col_3.setMargins(0,0,0,0)
        self.col_3.setSpacing(0)

        self.level = LabelData(self.col_3, "Niveau", self.student.level)
        ''' self.matricule = LabelData(self.col_3, "Matricule", self.student.matricule)
        self.company = LabelData(self.col_3, "Compagnie", self.student.company)
        self.section = LabelData(self.col_3, "Section", self.student.section) '''
        self.col.addWidget(self.col_3)
        self.row.addWidget(self.col)
        
        self.row_2 = Frame('vertical', 'row_2', parent=parent)
        self.row_2.addWidget(SubtitleLabel('Mouvement'))
        self.d = self.serviceMove.listByStudentId(self.studentId)
        
        list = [[]]
        list.clear()
        day = "0"
        print()
        for mv in self.d:
            list.append([mv.date, f"{mv.type} {mv.subType}", mv.day])
            if(len(mv.day) != 0):
                day +=  "+"+mv.day
        list.append(["Total", "",str(eval(day))])
        table = Table(self.row_2, ["Date", "Mouvement", "Nombre de jour"], list)
        self.row_2.addWidget(table.widget())
        noMove = BodyLabel('Aucun mouvement')
        self.row_2.addWidget(noMove)
        noMove.setVisible(False)
        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_2)
        if len(list) == 1:
            table.widget().setVisible(False)
            noMove.setVisible(True)

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
        
    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
