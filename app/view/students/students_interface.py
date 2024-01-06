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
from .student_move import DialogStudentMove
from ...common.database.service.student_service import StudentService
from PyQt5.QtSql import QSqlDatabase
from ...common.database.db_initializer import DBInitializer as DB
from ...common.database.dao.student_dao import Student
from ...common.database.entity import Mouvement
from ...common.database.service.mouvement_service import MouvementService
from ...common.database.utils.constants import *
from docx import Document
import os

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
        self.moveService = MouvementService(self.db)
        self.parent = parent
        self.hBoxLayout = QVBoxLayout(self)
        self.titleContainte(parent)
        self.container(parent)
        self.setObjectName('studentInterface')

    def titleContainte(self, parent):
        row = Frame(VERTICAL, ROW+str(1), parent=parent)
        label = SubtitleLabel("Liste des élèves de la promotion Sandratra", parent)
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
        #self.btnAdd =  PrimaryPushButton('Add new student', self, FIF.ADD)
        #self.btnAdd.setObjectName(u"ButtonAdd")
        #self.btnAdd.clicked.connect(self.showDialog)

        #self.btnFlux =  PrimaryPushButton('Seed', self, FIF.DEVELOPER_TOOLS)
        #self.btnFlux.setObjectName(u"PrimaryToolButton")
        #self.btnFlux.clicked.connect(self.seed)

        #col.layout.addWidget(self.btnAdd)
        #col.layout.addWidget(self.btnFlux)
        col.setMargins(0,0,0,0)
        
        self.row_2.setMargins(0,0,0,0)
        self.row_2.addWidget(self.searchLineStudent)
        self.row_2.layout.addWidget(col, 0, Qt.AlignRight)
        self.container.addWidget(self.row_2)

        students = self.listStudent(self.studentService.listAll())
        self.tbStudent = Table(parent, students.get("header"), students.get("data"))
        self.tbStudent.setRisizeMode(len(students.get("header")) - 1)
        self.table = self.tbStudent.widget()
        self.table.clicked.connect(self.selectItem)
        self.container.addWidget(self.tbStudent.widget())
        self.hBoxLayout.addWidget(self.container)
        self.dialog = None

    def listStudent(self, data):
        stude = self.studentService

        RM = TYPE_MOVE["RM_CONV"]
        EX = SUB_TYPE_MOVE["EX_PHYS"]
        PERM = TYPE_MOVE["PERMISSION"]
        CODIS = SUB_TYPE_MOVE["CODIS"]
        HORS_TOUR = SUB_TYPE_MOVE["HORS_TOUR"]
        BEM = SUB_TYPE_MOVE["BEM"]
        PEP = SUB_TYPE_MOVE["PEP"]
        ANM = TYPE_MOVE["ANM"]
        LETTRE_FEL = SUB_TYPE_MOVE["LETTRE_FEL"]
        OTHER_SAC = f'{SUB_TYPE_MOVE["OTHER"]} {TYPE_MOVE["SACT_DISC"]}'
        OTHER_REM_POS = f'{SUB_TYPE_MOVE["OTHER"]} {TYPE_MOVE["REM_POS"]}'

        header = [
            "ID","Matricule", "Niveau", "Nom",
            "Prénom", "Genre",RM,
            EX, PERM, CODIS, HORS_TOUR,
            BEM, PEP, 
            OTHER_SAC, ANM, 
            LETTRE_FEL, OTHER_REM_POS]
        listStudent = [[]]
        listStudent.clear()

        for student in data:
            idStudent = student.get("id_tbl_student")
            listStudent.append([
                idStudent,
                student.get("matricule"),
                student.get("level"),
                student.get("lastname"),
                student.get("firstname"),
                student.get("gender"),
                stude.sumOfDayTypeMove(idStudent, RM), 
                stude.sumOfDaySubTypeMove(idStudent, EX),
                stude.sumOfDayTypeMove(idStudent, PERM),
                stude.countSubTypeMove(idStudent, CODIS),
                stude.sumOfDayTypeMove(idStudent, HORS_TOUR),
                stude.countSubTypeMove(idStudent, BEM),
                stude.countSubTypeMove(idStudent, PEP),
                stude.countSubTypeMove(idStudent, OTHER_SAC),
                stude.countTypeMove(idStudent, ANM),
                stude.countSubTypeMove(idStudent, LETTRE_FEL),
                stude.countSubTypeMove(idStudent, OTHER_REM_POS)
                ])

        '''listStudent = [
                    for student in data]'''
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
        self.dialog = DialogStudentShow(self.studentService, self.moveService, id, self.parent)
        self.dialog.yesButton.clicked.connect(lambda: self.exportData(self.dialog.student, self.dialog.d))
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
        
    def exportData(self, student: Student, mouvement):
        document = Document()
        document.add_heading(f'Informations', level=1)
        pData = f'Nom: {student.lastname}\n'
        pData += f'Prénoms: {student.firstname}\n'
        pData += f'Genre: {student.gender}\n'
        pData += f'Niveau: {student.level}\n'
        document.add_paragraph(pData)
        document.add_heading(f'Mouvements', level=1)
        
        # get table data -------------
        items = [[]]
        items.clear()
        day = "0"
        for mouv in mouvement:
            items.append([mouv.date, f"{mouv.type} {mouv.subType}", mouv.day])
            if(len(mouv.day) != 0):
                day +=  "+"+mouv.day
        valDay = eval(day)
        items.append(["Total", "",str(valDay)])

        if valDay == 0:
            document.add_paragraph("Aucun mouvement")
        else:
            # add table ------------------
            table = document.add_table(1, 3)
            table.style = "Table Grid"

            # populate header row --------
            heading_cells = table.rows[0].cells
            heading_cells[0].text = 'Date'
            heading_cells[1].text = 'Mouvement'
            heading_cells[2].text = 'Nombre de jour'

            # add a data row for each item
            for item in items:
                cells = table.add_row().cells
                cells[0].text = str(item[0])
                cells[1].text = item[1]
                cells[2].text = item[2]
                
        # Save the document
        filename = f"{os.path.expanduser('~')}\Documents\{student.level}-{student.matricule}.docx";
        document.save(filename)
        self.dialog.yesButton.setVisible(False)
        os.startfile(filename)  
        

    
    def selectItem(self, item: QModelIndex):
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.FOLDER, 'Voir', triggered=lambda:self.showItem(item)))
        menu.addAction(Action(FIF.EDIT, 'Modifier', triggered=lambda:self.showDialogView(item)))
        menu.addAction(Action(FIF.SCROLL, 'Mouvement', triggered=lambda:self.showDialogMove(item)))
        menu.addSeparator()
       # menu.addAction(Action(FIF.DELETE, 'Delete', triggered=lambda:self.confirmDeleteItem(item)))
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

    def showDialogMove(self, item: QModelIndex):
        id = self.table.item(item.row(), 0).text()
        self.dialog = DialogStudentMove(self.studentService, self.moveService, id, self.parent)
        btn = self.dialog.yesButton
        btn.clicked.connect(lambda: self.newMouvement(self.dialog.dataMouvement()))
        self.dialog.show()
    
    def newMouvement(self, mouvement:Mouvement):
        service = MouvementService(self.db)
        service.create(mouvement)
        self.dialog.accept()
    
    def showItem(self, item: QModelIndex):
        id = self.table.item(item.row(), 0).text()
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