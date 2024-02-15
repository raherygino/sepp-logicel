from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from qfluentwidgets import TitleLabel, CommandBar, FluentIcon, Action, \
    TransparentDropDownPushButton, setFont, RoundMenu, TableWidget
from ...components import TableView

class ListStudent(QWidget):

    def __init__(self, promotion , parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.commandBar = CommandBar(self)
        self.dropDownButton = self.createDropDownButton()

        self.vBoxLayout.addWidget(self.commandBar, 0)

        # change button style
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        # self.commandBar.setMenuDropDown(False)
        # self.commandBar.setButtonTight(True)
        # setFont(self.commandBar, 14)

        self.addButton(FluentIcon.ADD, 'Add')
        self.commandBar.addSeparator()

        self.commandBar.addAction(Action(FluentIcon.EDIT, 'Edit', triggered=self.onEdit, checkable=True))
        self.addButton(FluentIcon.COPY, 'Copy')
        self.addButton(FluentIcon.SHARE, 'Share')

        # add custom widget
        self.commandBar.addWidget(self.dropDownButton)

        # add hidden actions
        self.commandBar.addHiddenAction(Action(FluentIcon.SCROLL, 'Sort', triggered=lambda: print('排序')))
        self.commandBar.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))
        
        
        self.tableView = TableView(self)
        #self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableView.setSortingEnabled(True)

        self.setStyleSheet("Demo{background: rgb(249, 249, 249)} ")
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.tableView)
    

    def addButton(self, icon, text):
        action = Action(icon, text, self)
        action.triggered.connect(lambda: print(text))
        self.commandBar.addAction(action)

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