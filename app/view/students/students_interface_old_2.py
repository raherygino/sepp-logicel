# coding:utf-8
from ..utils.gallery_interface import GalleryInterface
from ...common.translator import Translator
from ...components import *
from qfluentwidgets import BodyLabel
from PyQt5 import QtWidgets, QtCore
from ...components import *
from qfluentwidgets import (isDarkTheme, FluentIcon, Action, 
    CommandBar, TransparentDropDownPushButton, setFont, RoundMenu, TableWidget, LineEdit)
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout

from PyQt5.QtWidgets import QApplication, QWidget, QAction, QHBoxLayout, QLabel
from qfluentwidgets import RoundMenu, setTheme, Theme, Action, MenuAnimationType, MenuItemDelegate, CheckableMenu, MenuIndicatorType
from qfluentwidgets import FluentIcon as FIF
from ...components.table.TableView import *
from ...backend.models.Student import Student

class StudentInterface(GalleryInterface):
    """ Student interface """

    def __init__(self, parent=None):
        self.t = Translator()
        
        super().__init__(
            title=self.t.name_promotion,
            subtitle='',
            parent=parent
        )
        
        '''
        MODELS 
        student = Student("lastname", "firstname", "genre", "height", "weight", 
                          "birthday", "birthplace", "phone", "address", "level",
                          "company", "section","number")
        '''
        '''student = Student("Armelin", "Georginot", "M", "68", "175", "20/04/1997", "Ranotsara Nord", "034 65 007 00",
                          "Bevokatra Antsirabe", "EAP", 2,7,23)
        student.create() '''
        student = Student("Armelin", "Georginot", "M", "68", "175", "20/04/1997", "Ranotsara Nord", "034 65 007 00",
                          "Bevokatra Antsirabe", "EAP", 2,7,23)
        student.create()

        rows = student.fetch(['firstname', 'lastname', 'genre', 'company', 'section', 'number'])
        head = ['Nom', 'Prénoms', 'Genre', 'Compagnie', 'Section', 'Numéros']

        #self.widgetsInCard(parent, head, rows)
        table = Table(self, head, rows)
        self.container = Frame('horizontal', 'row_1', parent=parent)
        self.container.layout.addWidget(table.widget())

        #self.add addWidget(self.container)
        # self.layout.addWidget(self.container)
        self.widgetsInCard(parent, ["hello", "gfg"], [["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"],["dsfd","sdfd"]])
        self.setObjectName('StudentInterface')

    def widgetsInCard(self, parent, header, data):
        self.container = Frame('horizontal', 'row_1', parent=parent)
       # header = ["Nom", "prénom", "Date de naissance", "Lieu de naissance", "Adresse", "N° Téléphone", "Compagnie", "Section"]
       # data = [["Georginot", "Armelin", "12/12/96", "Ranotsara Nord", "Antsirabe", "0346500700", "IIème", "7ème"]]
        table = Table(self, header, data)
        #table.table.clicked.connect(self.func_test)
        self.container.layout.addWidget(table.widget())
        self.addCard(self.t.students, self.container)

    def get_var_name(self, variable):
        for name in globals():
            if id(globals()[name]) == id(variable):
                return name
        for name in locals():
            if id(locals()[name]) == id(variable):
                return name
        return None 

    ''' def func_test(self, item: QModelIndex):
        print("hello world") '''
        