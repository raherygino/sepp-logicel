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

class StudentInterface(GalleryInterface):
    """ Student interface """

    def __init__(self, parent=None):
        self.t = Translator()
        super().__init__(
            title=self.t.name_promotion,
            subtitle='',
            parent=parent
        )

        self.widgetsInCard(parent=parent)
        self.setObjectName('StudentInterface')

    def widgetsInCard(self, parent):
        self.container = Frame('horizontal', 'row_1', parent=parent)
        self.container.addWidget(self.tableStudents())
        self.addCard(self.t.students, self.container)

    def func_test(self, item: QModelIndex):
        #print(item.)
        
        menu = RoundMenu(parent=self)
        # menu = CheckableMenu(parent=self, indicatorType=MenuIndicatorType.RADIO)

        # NOTE: hide the shortcut key
        # menu.view.setItemDelegate(MenuItemDelegate())

        # add actions
        menu.addAction(Action(FIF.COPY, 'Copy'))
        menu.addAction(Action(FIF.CUT, 'Cut'))
        menu.menuActions()[0].setCheckable(True)
        menu.menuActions()[0].setChecked(True)

        # add sub menu
        submenu = RoundMenu("Add to", self)
        submenu.setIcon(FIF.ADD)
        submenu.addActions([
            Action(FIF.VIDEO, 'Video'),
            Action(FIF.MUSIC, 'Music'),
        ])
        menu.addMenu(submenu)

        # add actions
        menu.addActions([
            Action(FIF.PASTE, 'Paste'),
            Action(FIF.CANCEL, 'Undo')
        ])

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(f'Select all', shortcut='Ctrl+A'))

        # insert actions
        menu.insertAction(
            menu.menuActions()[-1], Action(FIF.SETTING, 'Settings', shortcut='Ctrl+S'))
        menu.insertActions(
            menu.menuActions()[-1],
            [Action(FIF.HELP, 'Help', shortcut='Ctrl+H'),
             Action(FIF.FEEDBACK, 'Feedback', shortcut='Ctrl+F')]
        )
        menu.menuActions()[-2].setCheckable(True)
        menu.menuActions()[-2].setChecked(True)

        # show menu
        menu.exec(QtCore.QPoint(679, 380), aniType=MenuAnimationType.DROP_DOWN)
        

    def tableStudents(self) -> TableWidget:
        
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

        return self.tableView

