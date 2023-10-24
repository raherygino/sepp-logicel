# coding: utf-8
from PyQt5.QtCore import QObject
from .Translate import Translate
from .config import Lang


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        trans = Translate(Lang().current).text

        self.students = trans['students']

        self.text = self.tr('Text')
        self.view = self.tr('View')
        self.menus = self.tr('Menus & toolbars')
        self.icons = self.tr('Icons')
        self.layout = self.tr('Layout')
        self.dialogs = self.tr('Dialogs & flyouts')
        self.scroll = self.tr('Scrolling')
        self.material = self.tr('Material')
        self.dateTime = self.tr('Date & time')
        self.navigation = self.tr('Navigation')
        self.basicInput = self.tr('Basic input')
        self.statusInfo = self.tr('Status & info')
        self.blank = self.tr('Blank')
        self.products = trans['products']
        self.name_promotion = trans['promotion']
        self.widgets = trans['widgets']
        self.table_view = trans['table_view']