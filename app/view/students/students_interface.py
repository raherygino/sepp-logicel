# coding:utf-8
from ..utils.gallery_interface import GalleryInterface
from ...common.translator import Translator
from ...common.Translate import Translate
from ...common.config import Lang
from ...common.keys import *
from ...components import *
from qfluentwidgets import (SubtitleLabel, SearchLineEdit, PushButton,MenuAnimationType, 
                            PrimaryPushButton, RoundMenu, Action, MessageBox, InfoBar, InfoBarPosition)
from qfluentwidgets import FluentIcon as FIF
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTableWidgetItem, QAction
from PyQt5.QtCore import Qt, QSize, QCoreApplication, QModelIndex, QPoint
from PyQt5.QtGui import QCursor
from ...common.config import *
from .students_new_dialog import DialogStudent
from .student_show import DialogStudentShow
from ...common.database.service.student_service import StudentService
from PyQt5.QtSql import QSqlDatabase
from ...common.database.db_initializer import DBInitializer as DB
from ...common.database.dao.student_dao import Student

class StudentInterface(GalleryInterface):
    """ Student interface """

    def __init__(self, parent=None):
        self.db = parent.db
        self.trans = Translate(Lang().current).text

        super().__init__(
            title='',
            subtitle='',
            parent=parent
        )
        
        self.db = QSqlDatabase.database(self.db.CONNECTION_NAME, True)
        self.studentService = StudentService(self.db)
        self.parent = parent
        self.hBoxLayout = QVBoxLayout(self)
        self.titleContainte(parent)
        self.container(parent)
        self.setObjectName('studentInterface')

    def titleContainte(self, parent):
        row = Frame(VERTICAL, ROW+str(1), parent=parent)
        label = SubtitleLabel("List students", parent)
        row.setMargins(9,0,9,0)
        row.addWidget(label)
        self.hBoxLayout.addWidget(row)

    def container(self, parent):
        self.container = Frame(VERTICAL, STUDENT+CONTAINER, parent=parent)
        self.row_2 = Frame(HORIZONTAL, ROW+str(2), parent=parent)
        self.searchLineStudent = SearchLineEdit(self)
        self.searchLineStudent.setPlaceholderText(QCoreApplication.translate(FORM, u"Search", None))
        self.searchLineStudent.setMaximumSize(QSize(240, 50))
        self.searchLineStudent.textChanged.connect(self.searchStudent)
        
        col = Frame(HORIZONTAL, COL+str(1),parent=parent)
        self.btnAdd =  PrimaryPushButton('Add new student', self, FIF.ADD)
        self.btnAdd.setObjectName(u"ButtonAdd")
        self.btnAdd.clicked.connect(self.showDialog)

        #self.btnFlux =  PrimaryPushButton('Seed', self, FIF.DEVELOPER_TOOLS)
        #self.btnFlux.setObjectName(u"PrimaryToolButton")
        #self.btnFlux.clicked.connect(self.seed)

        col.layout.addWidget(self.btnAdd)
        #col.layout.addWidget(self.btnFlux)
        col.setMargins(0,0,0,0)
        
        self.row_2.setMargins(0,0,0,0)
        self.row_2.addWidget(self.searchLineStudent)
        self.row_2.layout.addWidget(col, 0, Qt.AlignRight)
        self.container.addWidget(self.row_2)

        students = self.listStudent(self.studentService.listAll())
        self.tbStudent = Table(parent, students.get("header"), students.get("data"))
        self.table = self.tbStudent.widget()
        self.table.clicked.connect(self.selectItem)
        self.container.addWidget(self.tbStudent.widget())
        self.hBoxLayout.addWidget(self.container)
        self.dialog = None

    def listStudent(self, data):
        header = ["ID", "Lastname", "Firstname", "Gender", "Birthday", "Birthplace", "Address", "phone"]
        listStudent = [[
                student.get("id_tbl_student"),
                student.get("lastname"),
                student.get("firstname"),
                student.get("gender"),
                student.get("birthday"),
                student.get("birthplace"),
                student.get("address"),
                student.get("phone")]
                    for student in data]
        return {
            "header": header,
            "data": listStudent
        }
    
    def refreshTable(self, **kwargs):
        data = self.studentService.listAll()
        if (len(kwargs.keys()) != 0):
            data = self.studentService.search(kwargs.get('query'))

        listStudent = self.listStudent(data)
        self.tbStudent.refresh(self.table, listStudent.get("header"), listStudent.get("data"))

    def showDialog(self):
        self.dialog = DialogStudent(self.parent)
        self.dialog.title.setText("Add new student")
        btnOk = self.dialog.yesButton
        btnOk.setText("Create")
        btnOk.clicked.connect(lambda: self.createStudent(self.dialog.studentData()))
        self.dialog.show()

    def showDialogItem(self, id):
        self.dialog = DialogStudentShow(self.studentService, id, self.parent)
        self.dialog.yesButton.clicked.connect(lambda: self.dialog.accept())
        self.dialog.show()
    
    def showDialogView(self, item:QModelIndex):
        id = self.table.item(item.row(), 0).text()
        self.dialog = DialogStudent(self.parent, service=self.studentService,id=id)
        self.dialog.title.setText(f"Update {self.dialog.student.lastname}")
        btnOk = self.dialog.yesButton
        btnOk.setText("Update")
        btnOk.clicked.connect(lambda: self.updateStudent(id, self.dialog.studentData()))
        self.dialog.show()

    def createStudent(self, student: Student):
        if (self.studentService.create(student)):
            self.infoMessage(self.parent, "Created", "Student created succesfully!")
            self.dialog.accept()
            self.dialog = None
            self.refreshTable()
        else:
            print("error")
    def updateStudent(self, id:int, student: Student):
            if(self.studentService.update(id, student)):
                self.infoMessage(self.parent, "Update", f"{student.firstname} updated succesfully!")
                self.dialog.accept()
                self.dialog = None
                self.refreshTable()
            else:
                print("Error")
    
    def searchStudent(self, text:str):
        if '\'' not in text:
            self.refreshTable(query=text)
        
    
    def selectItem(self, item: QModelIndex):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.FOLDER, 'Show', triggered=lambda:self.showItem(item)))
        menu.addAction(Action(FIF.EDIT, 'Edit', triggered=lambda:self.showDialogView(item)))
        #menu.addAction(Action(FIF.SCROLL, 'Mouvement', triggered=lambda:self.showDialogMove(item)))
        menu.addSeparator()
        menu.addAction(Action(FIF.DELETE, 'Delete', triggered=lambda:self.confirmDeleteItem(item)))
        menu.menuActions()[-2].setCheckable(True)
        menu.menuActions()[-2].setChecked(True)

        self.posCur = QCursor().pos()
        cur_x = self.posCur.x()
        cur_y = self.posCur.y()

        menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.DROP_DOWN)

    def confirmDeleteItem(self, item: QModelIndex):
        confirm = MessageBox("Confirmation", "You want to delete it?", self.parent)
        confirm.accepted.connect(lambda:self.deleteItem(item))
        confirm.show()
    
    def showItem(self, item: QModelIndex):
        id = self.table.item(item.row(), 0).text()
        #DialogStudentShow(id, self.myParent).show()
        self.showDialogItem(id)
        

    def deleteItem(self, item: QModelIndex):
        id = self.table.item(item.row(), 0).text()
        self.studentService.deleteById(id)
        self.infoMessage(self.parent, "Success", "Student deleted successfully")
        self.refreshTable()

    def infoMessage(self, parent, title:str, message:str):
        InfoBar.success(
            title=title,
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=parent
        )