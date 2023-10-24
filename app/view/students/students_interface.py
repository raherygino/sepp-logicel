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
from ...components.table.TableView import Table

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
        header = ["Nom", "prénom", "Date de naissance", "Lieu de naissance", "Adresse", "N° Téléphone", "Compagnie", "Section"]
        data = [["Georginot", "Armelin", "12/12/96", "Ranotsara Nord", "Antsirabe", "0346500700", "IIème", "7ème"]]
        table = Table(self, header, data)
        table.table.clicked.connect(self.func_test)
        self.container.layout.addWidget(table.widget())
        self.addCard(self.t.students, self.container)

    def func_test(self, item: QModelIndex):
        print("hello world")
        