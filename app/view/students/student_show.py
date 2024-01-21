
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize, QModelIndex,QPoint
from PyQt5.QtGui import QColor,QCursor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import (BodyLabel, StrongBodyLabel,MenuAnimationType, PrimaryPushButton, 
                            Action, SubtitleLabel, ImageLabel, RoundMenu, MessageBox)
from qfluentwidgets import FluentIcon as FIF

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

    def __init__(self,interface, service, serviceMove, id, parent):
        super().__init__(parent=parent)
        self.interface = interface
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
        
        self.table = Table(self.row_2, ["Date", "Mouvement", "Nombre de jour"], self.setData(self.d))
        self.refreshData(self.d)

        self.table.setSectionResizeMode()
        self.tableMove = self.table.widget()
        self.tableMove.clicked.connect(self.selectItem)
        self.row_2.addWidget(self.table.widget())
        self.noMove = BodyLabel('Aucun mouvement')
        self.row_2.addWidget(self.noMove)
        self.noMove.setVisible(False)
        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_2)
        if len(self.setData(self.d)) == 1:
            self.tableMove.setVisible(False)
            self.noMove.setVisible(True)

    def setData(self, data):
        list = [[]]
        list.clear()
        day = "0"
        for mv in data:
            list.append([mv.date, f"{mv.type}\n{mv.subType}", mv.day])
            if(len(mv.day) != 0):
                day +=  "+"+mv.day
        list.append(["Total", "",str(eval(day))])
        return list


    def refreshData(self, data):
        list = self.setData(data)
        self.table.setData(self.table.widget(), ["Date", "Mouvement", "Nombre de jour"],list)

    def yesBtnEvent(self):
        self.accept()

    def getYesBtn(self):
        return self.yesButton
    
    
    def selectItem(self, item: QModelIndex):
        text = self.tableMove.item(item.row(), 0).text()
        if text != "Total":
            menu = RoundMenu(parent=self)
            menu.addAction(Action(FIF.DELETE, 'Supprimer', triggered=lambda:self.confirmDelete(item)))
            self.posCur = QCursor().pos()
            cur_x = self.posCur.x()
            cur_y = self.posCur.y()
            menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.DROP_DOWN)


    def confirmDelete(self, item: QModelIndex):
        
        exitDialog = MessageBox(
            'Supprimer', 'Voulez vous supprimer vraiment?',
            self
        )
        exitDialog.yesButton.setText('Oui')
        exitDialog.cancelButton.setText('Non')

        if exitDialog.exec():
            self.deleteItem(item)
            data = self.serviceMove.listByStudentId(self.studentId)
            self.refreshData(data)
            if len(self.setData(data)) == 1:
                self.tableMove.setVisible(False)
                self.noMove.setVisible(True)
     
    def deleteItem(self, item: QModelIndex):
        daty = self.tableMove.item(item.row(), 0).text()
        sact = self.tableMove.item(item.row(), 1).text()
        typs = sact.split("\n")
        typ = typs[0]
        subTyp = typs[1]
        if len(subTyp) == 0:
            self.serviceMove.deleteByDateType(daty, typ)
        else:
            self.serviceMove.deleteByDateTypeSubType(daty, typ, subTyp)
        self.interface.refreshTable()

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
