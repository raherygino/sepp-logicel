from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import ComboBox, CommandBar, FluentIcon, Action, \
    ToggleToolButton, setFont, RoundMenu, SearchLineEdit
from ...components import TableView
from ...common.config import OptionsConfigItem

class ListStudent(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(5, 0, 12, 0)
        self.parent = parent
        self.__initCommandBar()
        self.__initTableView(parent)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.tableView)
        
    def __initCommandBar(self):
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.setButtonTight(True)
        setFont(self.commandBar, 14)
        
        self.addAction = Action(FluentIcon.ADD, "Ajouter", self)
        self.importAction = Action(FluentIcon.FOLDER_ADD, "Importer", self)
        self.exportAction = Action(FluentIcon.SHARE, "Exporter", self)
        
        self.commandBar.addAction(self.addAction)
        self.commandBar.addAction(self.importAction)
        self.commandBar.addAction(self.exportAction)
        
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText("Recherche")
        self.searchLineEdit.setFixedWidth(200)
        
        self.comboBoxCompany = ComboBox(self)
        self.comboBoxCompany.setFixedWidth(150)
        
        self.comboBoxSection = ComboBox(self)
        self.comboBoxSection.setFixedWidth(150)

        # toggle tool button
        self.toggleSelection = ToggleToolButton(FluentIcon.FILTER, self)
        #self.toggleSelection.toggled.connect(self.setSelection)
        
        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        self.hBoxLayout.addWidget(self.comboBoxCompany)
        self.hBoxLayout.addWidget(self.comboBoxSection)
        self.hBoxLayout.addWidget(self.toggleSelection)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        
    def __initTableView(self, parent):
        self.tableView = TableView(self)
        parent.mainWindow.settingInterface.themeCard.optionChanged.connect(self.setTableTheme)
        
    def setTableTheme(self, config: OptionsConfigItem):
        self.tableView.setQss(config.value.value)