from PyQt5.QtWidgets import QFrame, QVBoxLayout, QTableWidgetItem
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from qfluentwidgets import SubtitleLabel, setFont, SearchLineEdit, PushButton, PrimaryPushButton
from qfluentwidgets import FluentIcon as FIF
from components import *
from components.dialog.dialog import MessageBox
from components.input import InputText
from common.keys import *
from backend.models.Student import Student
from backend.controllers.StudentController import StudentController

class StudentInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.hBoxLayout = QVBoxLayout(self)
        self.myParent = parent
        self.titleContainte(parent=parent)
        self.container(parent=parent)
        self.setObjectName(STUDENT+INTERFACE)
        self.student = Student(None, None, None, None, None, None, None, None, None, None, None, None, None)
        self.studentController = StudentController(self.student)

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
        
        col = Frame(HORIZONTAL, COL+str(1),parent=parent)
        self.btnAdd =  PushButton('Ajouter', self, FIF.ADD)
        self.btnAdd.setObjectName(u"PrimaryToolButton")
        self.btnAdd.clicked.connect(self.createStudent)

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
        self.table_student = self.tbStudent[0]
        self.container.addWidget(self.table)

        self.hBoxLayout.addWidget(self.container)

    def createStudent(self):
        '''
        student = Student("Georginot", "Armelin",
                          "M", 56, 175, "20/04/1997", "Ranotsara Nord",
                          "034 65 007 00","Bevokatra Antsirabe", "EAP", 2, 7, 23)
        self.studentController = StudentController(student)
        self.studentController.create()
        data = student.fetch(['id_student', 'firstname', 'lastname', 'company', 'section', 'number'])
        header = ['ID', 'Nom', 'prénom', 'Compagnie', 'Section', 'Numéro']
        self.table_student.refresh(self.table, header, data)
        '''
        st = self.newStudent(self.myParent)
        st.show()
        
    class newStudent():
        def __init__(self, parent):
            dialogContainer = Frame(VERTICAL, "containerDialog", parent)
            row = Frame(HORIZONTAL, "dialogRow1", dialogContainer)
            col = Frame(VERTICAL, "dialoCol1", row)
            lastnameInput = InputText("Lastname", col)

            row.addWidget(col)
            dialogContainer.addWidget(row)
            self.dialog = MessageBox(dialogContainer, parent)

        def show(self):
            self.dialog.show()
        

    
    def tableStudent(self, parent):
        student = Student("Georginost", "Armelin",
                          "M", 56, 175, "20/04/1997", "Ranotsara Nord",
                          "034 65 007 00","Bevokatra Antsirabe", "EAP", 2, 7, 23)
        data = student.fetch(['id_student', 'firstname', 'lastname', 'company', 'section', 'number'])
        header = ['ID', 'Nom', 'prénom', 'Compagnie', 'Section', 'Numéro']
        table = Table(parent, header, data)
        return [table,table.widget()]
    
    def refreshTable(self, parent):
        self.tableStudent()

