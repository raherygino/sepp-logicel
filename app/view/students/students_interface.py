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
from ...backend.models.Student import Student
from ...backend.controllers.StudentController import StudentController
import random

from .students_new_dialog import DialogStudent
from .students_show_dialog import DialogStudentShow

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
        self.myParent = parent
        self.hBoxLayout = QVBoxLayout(self)
        self.student = Student(None, None, None, None, None, None, None, None, None, None, None, None, None)
        self.student.initTable()
        self.studentController = StudentController(self.student)
        #self.student.create()
        self.container(parent=parent)
        self.setObjectName('studentInterface')
        #self.student.seeds(6)
        
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
        #print(self.btnAdd.event.po)
        self.btnAdd.clicked.connect(self.showDialog)

        self.btnFlux =  PrimaryPushButton('Mouvement', self, FIF.CHAT)
        self.btnFlux.setObjectName(u"PrimaryToolButton")

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

        self.dialog = DialogStudent(self.myParent)

    def searchStudent(self, text:str):
        if '\'' not in text:
            header = ['ID', 'Nom', 'prénom', 'Compagnie', 'Section', 'Numéro', 'Niveau']
            data = self.student.search(['id_student', 'lastname', 'firstname', 'company', 'section', 'number', 'level'], text)
            self.table_student.refresh(self.table, header, data)

    def selectItem(self, item: QModelIndex):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.FOLDER, 'Ouvrir', triggered=lambda:self.showItem(item)))
        menu.addAction(Action(FIF.EDIT, 'Modifier'))
        menu.addAction(Action(FIF.SCROLL, 'Mouvement'))
        menu.addSeparator()
        menu.addAction(Action(FIF.DELETE, 'Supprimer', triggered=lambda:self.confirmDeleteItem(item)))
        menu.menuActions()[-2].setCheckable(True)
        menu.menuActions()[-2].setChecked(True)

        x = self.table.width()
        pos = self.table.mapToGlobal(QPoint(50, (item.row()+1)*34))
        menu.exec(pos, aniType=MenuAnimationType.DROP_DOWN)

    def showItem(self, item: QModelIndex):
        id = self.table.item(item.row(), 0).text()
        DialogStudentShow(id, self.myParent).show()

    def confirmDeleteItem(self, item: QModelIndex):
        confirm = MessageBox("Confirmation", "Voulez vous supprimer vraiment", self.myParent)
        confirm.accepted.connect(lambda:self.deleteItem(item))
        confirm.show()

    def deleteItem(self, item:QModelIndex):
        id = self.table.item(item.row(), 0).text()
        self.student.delete(id)
        self.refreshTable(self.student)


    def showDialog(self):
        self.dialog.yesButton.clicked.connect(self.createStudent)
        self.dialog.show()
        
    def createStudent(self):
        student = self.dialog.studentData()
        student.create()
        self.refreshTable(student)
        self.dialog.accept()
        
    def tableStudent(self, parent):
        student = Student("Georginost", "Armelin",
                          "M", 56, 175, "20/04/1997", "Ranotsara Nord",
                          "034 65 007 00","Bevokatra Antsirabe", "EAP", 2, 7, 23)
        data = student.fetch(['id_student', 'lastname', 'firstname', 'company', 'section', 'number', 'level'])
        header = ['ID', 'Nom', 'prénom', 'Compagnie', 'Section', 'Numéro', 'Niveau']
        table = Table(parent, header, data)
        return [table,table.widget()]
    
    def refreshTable(self, student):
        data = student.fetch(['id_student', 'lastname', 'firstname', 'company', 'section', 'number', 'level'])
        header = ['ID', 'Nom', 'prénom', 'Compagnie', 'Section', 'Numéro', 'Niveau']
        self.table_student.refresh(self.table, header, data)
