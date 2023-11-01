# coding:utf-8
from ..utils.gallery_interface import GalleryInterface
from ...common.translator import Translator
from ...common.Translate import Translate
from ...common.config import Lang
from ...common.keys import *
from ...components import *
from qfluentwidgets import (SubtitleLabel, SearchLineEdit, PushButton,MenuAnimationType, 
                            PrimaryPushButton, RoundMenu, Action, MessageBox)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTableWidgetItem, QAction
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QModelIndex, QPoint
from PyQt5.QtGui import QCursor
from ...backend.models.Student import Student
from ...backend.models.Example import Example
from ...backend.controllers.StudentController import StudentController
from ...backend.controllers.ExampleController import ExampleController
from ...backend.models.keys import * 

from .students_new_dialog import DialogStudent
from .students_show_dialog import DialogStudentShow
from ...common.config import *

class StudentInterface(GalleryInterface):
    """ Student interface """

    def __init__(self, parent=None):
        t = Translator()
        self.trans = Translate(Lang().current).text
        super().__init__(
            title='',
            subtitle='',
            parent=parent
        )
        self.studentCtrl = StudentController()
        self.myParent = parent
        self.hBoxLayout = QVBoxLayout(self)
        self.container(parent=parent)
        self.setObjectName('studentInterface')
        
    def titleContainte(self, parent):
        row = Frame(VERTICAL, ROW+str(1), parent=parent)
        label = SubtitleLabel("Liste", parent)
        row.setMargins(9,0,9,0)
        row.addWidget(label)
        self.hBoxLayout.addWidget(row)
        
    def container(self, parent):
        self.container = Frame(VERTICAL, STUDENT+CONTAINER, parent=parent)
        self.row_2 = Frame(HORIZONTAL, ROW+str(2), parent=parent)
        self.searchLineStudent = SearchLineEdit(self)
        self.searchLineStudent.setPlaceholderText(QCoreApplication.translate(FORM, u"Recherche", None))
        self.searchLineStudent.setMaximumSize(QSize(240, 50))
        self.searchLineStudent.textChanged.connect(self.searchStudent)
        
        col = Frame(HORIZONTAL, COL+str(1),parent=parent)
        self.btnAdd =  PushButton('Ajouter', self, FIF.ADD)
        self.btnAdd.setObjectName(u"PrimaryToolButton")
        self.btnAdd.clicked.connect(self.showDialog)

        self.btnFlux =  PrimaryPushButton('Mouvement', self, FIF.CHAT)
        self.btnFlux.setObjectName(u"PrimaryToolButton")
        self.btnFlux.clicked.connect(self.seed)

        col.layout.addWidget(self.btnAdd)
        col.layout.addWidget(self.btnFlux)
        col.setMargins(0,0,0,0)
        
        self.row_2.setMargins(0,0,0,0)
        self.row_2.addWidget(self.searchLineStudent)
        self.row_2.layout.addWidget(col, 0, Qt.AlignRight)
        
        self.container.addWidget(self.row_2)
        self.tbStudent = self.tableStudent(parent)
        self.table = self.tbStudent[1]
        self.table.clicked.connect(self.selectItem)
        self.table_student = self.tbStudent[0]
        self.container.addWidget(self.table)
        self.hBoxLayout.addWidget(self.container)
        self.dialog = None

    def seed(self):
        self.studentCtrl.seed(12)
        self.refreshTable()

    def searchStudent(self, text:str):
        if '\'' not in text:
            self.table_student.refresh(self.table,
                                       self.studentCtrl.label,
                                       self.studentCtrl.search(text))

    def selectItem(self, item: QModelIndex):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.FOLDER, 'Ouvrir', triggered=lambda:self.showItem(item)))
        menu.addAction(Action(FIF.EDIT, 'Modifier'))
        menu.addAction(Action(FIF.SCROLL, 'Mouvement'))
        menu.addSeparator()
        menu.addAction(Action(FIF.DELETE, 'Supprimer', triggered=lambda:self.confirmDeleteItem(item)))
        menu.menuActions()[-2].setCheckable(True)
        menu.menuActions()[-2].setChecked(True)

        self.posCur = QCursor().pos()
        cur_x = self.posCur.x()
        cur_y = self.posCur.y()

        menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.DROP_DOWN)

    def showItem(self, item: QModelIndex):
        id = self.table.item(item.row(), 0).text()
        DialogStudentShow(id, self.myParent).show()

    def confirmDeleteItem(self, item: QModelIndex):
        confirm = MessageBox("Confirmation", "Voulez vous supprimer vraiment", self.myParent)
        confirm.accepted.connect(lambda:self.deleteItem(item))
        confirm.show()

    def deleteItem(self, item:QModelIndex):
        id = self.table.item(item.row(), 0).text()
        self.studentCtrl.delete(id)
        self.refreshTable()

    def showDialog(self):
        self.dialog = DialogStudent(self.myParent)
        self.dialog.yesButton.clicked.connect(self.createStudent)
        self.dialog.show()
        
    def createStudent(self):
        self.studentCtrl.store(self.dialog.studentData())
        self.refreshTable()
        self.dialog.accept()
        self.dialog = None
        
    def tableStudent(self, parent):
        data = self.studentCtrl.fetch()
        header = self.studentCtrl.label
        table = Table(parent, header, data)
        return [table,table.widget()]
    
    def refreshTable(self):
        self.table_student.refresh(
            self.table, 
            self.studentCtrl.label,
            self.studentCtrl.fetch())
