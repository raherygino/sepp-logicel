# coding:utf-8
#from ..gallery_interface import GalleryInterface
from ..utils.gallery_interface import GalleryInterface
from ...common.translator import Translator
from ...common.Translate import Translate
from ...common.config import Lang
from ...components import *
from qfluentwidgets import (isDarkTheme, FluentIcon, Action, 
    CommandBar, TransparentDropDownPushButton, setFont, RoundMenu, TableWidget, LineEdit)

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QFrame, QHBoxLayout
from .students_dialog import DialogProduct

from ...backend.controllers.UserController import UserController
from ...backend.models.User import User

class StudentInterface(GalleryInterface):
    """ Student interface """

    def __init__(self, parent=None):
        t = Translator()
        self.trans = Translate(Lang().current).text
        super().__init__(
            title=t.name_promotion,
            subtitle='',
            parent=parent
        )

        user = User("Gino", "arme", "zorz197", "georgino197@gmail.com", "0346500700")
        userController = UserController(user)
        userController.create()
        
        self.content = Frame('vertical', 'content', parent=parent)
        self.commandBar = CommandBar(self)
        self.dropDownButton = self.createDropDownButton()
        self.content.addWidget(self.commandBar)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addButton(FluentIcon.ADD, 'add', "Ajouter")
        self.commandBar.addSeparator()
        self.commandBar.addAction(Action(FluentIcon.EDIT, 'Edit', triggered=self.onEdit, checkable=True))
        self.addButton(FluentIcon.COPY, 'copy', 'Copy')
        self.addButton(FluentIcon.SHARE, 'share', 'Share')

        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)
        # add hidden actions
        self.commandBar.addHiddenAction(Action(FluentIcon.SCROLL, 'Sort', triggered=lambda: print('排序')))
        self.commandBar.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))

        self.tableView = TableWidget(self)
        self.tableView.clicked.connect(self.func_test)
        self.tableView.setWordWrap(False)
        self.tableView.setRowCount(5)
        self.tableView.setColumnCount(5)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        songInfos = [
            ['data 1.1', 'data 1.2', 'data 1.3', 'data 1.4', 'data 1.5'],
            ['data 2.1', 'data 2.2', 'data 2.3', 'data 2.4', 'data 2.5'],
            ['data 3.1', 'data 3.2', 'data 3.3', 'data 3.4', 'data 3.5'],
            ['data 4.1', 'data 4.2', 'data 4.3', 'data 4.4', 'data 4.5'],
            ['data 5.1', 'data 5.2', 'data 5.3', 'data 5.4', 'data 5.5'],
        ]
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.tableView.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.tableView.verticalHeader().hide()
        self.tableView.setHorizontalHeaderLabels(['Header 01', 'Header 02', 'Header 03', 'Header 04', 'Header 05'])
        self.tableView.resizeColumnsToContents()
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.content.addWidget(self.tableView)

        self.addCard('Liste des élèves', self.content)

        self.setObjectName('studenteInterface')

    def func_test(self, item: QModelIndex):
        #print(item.row())
        print(self.tableView.itemFromIndex(item).text())
        #self.tableView.itemAt().text()
        #print("You clicked on {0}x{1}".format(item.column(), item.row()))
    
    def addButton(self, icon, key, text):
        action = Action(icon, text, self)
        if key == "add" :
            action.triggered.connect(lambda: self.show_dialog())
        #action.triggered.connect(lambda: print(key))
        self.commandBar.addAction(action)
        #self.commandBar.childAt(0)

    def onEdit(self, isChecked):
        print('Enter edit mode' if isChecked else 'Exit edit mode')

    def createDropDownButton(self):
        button = TransparentDropDownPushButton('Menu', self, FluentIcon.MENU)
        button.setFixedHeight(34)
        setFont(button, 12)

        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(FluentIcon.COPY, 'Copy'),
            Action(FluentIcon.CUT, 'Cut'),
            Action(FluentIcon.PASTE, 'Paste'),
            Action(FluentIcon.CANCEL, 'Cancel'),
            Action('Select all'),
        ])
        button.setMenu(menu)
        return button

    def show_dialog(self):
        self.dialog = DialogProduct(parent=self)
        btn = self.dialog.getYesBtn()
        btn.clicked.connect(self.hello_world)
        self.dialog.show()
    
    def hello_world(self):
        code = self.dialog.inputCode.text()
        designation = self.dialog.inputDesignation.text()
        category = self.dialog.selectCategory.text()
        '''
        self.db.query("INSERT INTO products(code, designation) VALUES('"+code+"', '"+designation+"')")
        print(self.db.fetch()) '''
        self.dialog.accept()