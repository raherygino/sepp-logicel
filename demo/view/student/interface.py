from PyQt5.QtWidgets import QFrame, QVBoxLayout
from PyQt5.QtCore import Qt, QSize, QCoreApplication
from qfluentwidgets import SubtitleLabel, setFont, SearchLineEdit, PushButton
from qfluentwidgets import FluentIcon as FIF
from components import *
from common.keys import *
from backend.models.Student import Student

class StudentInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QVBoxLayout(self)
        self.titleContainte(parent=parent)
        self.container(parent=parent)
        self.setObjectName(STUDENT+INTERFACE)

    def titleContainte(self, parent):
        row = Frame(VERTICAL, ROW+str(1), parent=parent)
        label = SubtitleLabel("Liste des élèves promotion SANDRATRA", parent)
        row.setMargins(9,0,9,0)
        row.addWidget(label)
        self.hBoxLayout.addWidget(row)

    def container(self, parent):
        container = Frame(VERTICAL, STUDENT+CONTAINER, parent=parent)
        row_2 = Frame(HORIZONTAL, ROW+str(2), parent=parent)
        self.searchLineStudent = SearchLineEdit(self)
        self.searchLineStudent.setPlaceholderText(QCoreApplication.translate(FORM, u"Recherche", None))
        self.searchLineStudent.setMaximumSize(QSize(240, 50))
        
        col = Frame(HORIZONTAL, COL+str(1),parent=parent)

        self.btnAdd =  PushButton('Ajouter', self, FIF.ADD)
        self.btnAdd.setObjectName(u"PrimaryToolButton")

        #self.btnFlux =  PushButton('Mouvement', self, FIF.CHAT)
        #self.btnFlux.setObjectName(u"PrimaryToolButton")


        col.layout.addWidget(self.btnAdd, 3, Qt.AlignRight)
        #col.layout.addWidget(self.btnFlux, 1, Qt.AlignRight)
        col.setMargins(0,0,0,0)
        
        row_2.setMargins(0,0,0,0)
        row_2.addWidget(self.searchLineStudent)
        row_2.addWidget(col)
        student = Student("Georginot", "Armelin",
                          "M", 56, 175, "20/04/1997", "Ranotsara Nord", "034 65 007 00", 
                          "Bevokatra Antsirabe", "EAP", 2, 7, 23)
        
        student.create()
        data = student.fetch(['firstname', 'lastname', 'company', 'section', 'number'])
        header = ['Nom', 'prénom', 'Compagnie', 'Section', 'Numéro']
        table = Table(parent, header, data)
        container.addWidget(row_2)
        container.addWidget(table.widget())

        self.hBoxLayout.addWidget(container)

