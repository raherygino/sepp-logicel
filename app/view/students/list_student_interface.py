from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from qfluentwidgets import ComboBox, CommandBar, FluentIcon, Action, \
    ToolButton, setFont, RoundMenu, SearchLineEdit, IndeterminateProgressBar, \
    TransparentDropDownPushButton, ProgressBar
from ...components import TableView
from ...common.config import OptionsConfigItem

class ListStudentInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setContentsMargins(5, 10, 12, 0)
        self.parent = parent
        self.__initCommandBar()
        self.__initTableView(parent)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.progressBar)
        self.vBoxLayout.addWidget(self.tableView)
        self.setObjectName("listStudentInterface")
        
    def createDropDownButton(self, parent):
        button = TransparentDropDownPushButton('Ajouter', self, FluentIcon.ADD)
        button.setFixedHeight(34)
        setFont(button, 12)

        self.addAction = Action(FluentIcon.PEOPLE, "Elève", self)
        self.addComp = Action(FluentIcon.DICTIONARY, "Comportement", self)
        menu = RoundMenu(parent=parent)
        menu.addActions([
            self.addAction,
            self.addComp
        ])
        button.setMenu(menu)
        return button
        
    def __initCommandBar(self):
        self.commandBar = CommandBar(self)
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.commandBar.setButtonTight(True)
        setFont(self.commandBar, 14)
        self.dropDownButton = self.createDropDownButton(self)
        
        self.importAction = Action(FluentIcon.FOLDER_ADD, "Importer", self)
        self.exportAction = Action(FluentIcon.SHARE, "Exporter", self)
        self.deleteAction = Action(FluentIcon.DELETE, "Supprimer tous", self)
        
        self.commandBar.addWidget(self.dropDownButton)

        self.commandBar.addAction(self.importAction)
        self.commandBar.addAction(self.exportAction)
        self.commandBar.addSeparator()
        self.commandBar.addAction(self.deleteAction)
        
        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText("Recherche")
        self.searchLineEdit.setFixedWidth(200)
        
        self.comboBoxCompany = ComboBox(self)
        self.comboBoxCompany.setFixedWidth(150)
        
        self.comboBoxSection = ComboBox(self)
        self.comboBoxSection.setFixedWidth(150)

        # toggle tool button
        self.toggleSelection = ToolButton(FluentIcon.CANCEL, self)
        #self.toggleSelection.toggled.connect(self.setSelection)
        
        self.hBoxLayout.addWidget(self.commandBar)
        self.hBoxLayout.addWidget(self.searchLineEdit)
        self.hBoxLayout.addWidget(self.comboBoxCompany)
        self.hBoxLayout.addWidget(self.comboBoxSection)
        self.hBoxLayout.addWidget(self.toggleSelection)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        
    def __initTableView(self, parent):
        
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)
        self.tableView = TableView(self)
        #parent.mainWindow.settingInterface.themeCard.optionChanged.connect(self.setTableTheme)
        
    def setTableTheme(self, config: OptionsConfigItem):
        self.tableView.setQss(config.value.value)