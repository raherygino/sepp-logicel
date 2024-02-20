# coding:utf-8
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar,
                            SegmentedToggleToolWidget, FluentIcon)
from ...common.style_sheet import StyleSheet
from .list_student_tab import ListStudent
from ...presenter import StudentPresenter
from ...models import StudentModel

class StudentInterface(QWidget):
    """ Student interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainWindow = parent
        self.tabCount = 1
        self.tabItems = []
        self.tabBar = TabBar(self)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
    
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)

        # add items to pivot
        self.setObjectName("tabInterface")
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.connectSignalToSlot()

    def connectSignalToSlot(self):

        self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.addButton.setVisible(False)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


    def addSubInterface(self, widget, text, icon):
        objectName = text.replace(" ", "-")
        widget.setObjectName(objectName)
        #widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )


    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        self.tabBar.setCurrentTab(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def addTab(self, entity):
        text = entity.rank
        objName = text.replace(" ", "-")
        if objName not in self.tabItems:
            self.tabItems.append(objName)
            widget = ListStudent(self)
            studentModel = StudentModel()
            StudentPresenter(widget, studentModel, entity)
            self.addSubInterface(widget, text, FluentIcon.PEOPLE)
            self.tabCount += 1
            self.stackedWidget.setCurrentWidget(widget)

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(ListStudent, item.routeKey())
        self.tabItems.remove(item.routeKey())
        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()