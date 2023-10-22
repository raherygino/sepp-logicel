from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import TextWrap, FluentStyleSheet, PrimaryPushButton, LineEdit, SubtitleLabel
from ...components.dialog.mask import MaskDialogBase
from ...components.dialog.dialog import Ui_MessageBox
from ...components.layout.Frame import Frame
from ...components.input.InputText import InputText
from ...components.input.Select import Select

class DialogProduct(MaskDialogBase, Ui_MessageBox):

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.initWidgets(parent=parent)
        self._setUpUi(self.content, self.widget)
        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.buttonGroup.setMinimumWidth(280)
        #self.yesButton.clicked.connect(self.yesBtnEvent)

    def initWidgets(self, parent):
        self.content = Frame('vertical', 'content_dial', parent=parent)
        self.layoutTitle = Frame('horizontal', 'row', parent=parent)
        self.title = SubtitleLabel('Nouveau produit')

        self.row = Frame('horizontal', 'row', parent=parent)
        self.inputCode = InputText("Code", self.row)
        self.inputDesignation = InputText("Designation", self.row)

        self.row_2 = Frame('horizontal', 'row_2', parent=parent)
        self.selectCategory = Select("Catégorie", ["Options 1", "Options 2"], self.row_2)
        self.selectSubCategory = Select("Sous catégorie", ["Options 1", "Options 2"], self.row_2)

        self.layoutTitle.setMargins(8,4,0,0)
        self.row.setMargins(0,0,0,0)
        self.row_2.setMargins(0,0,0,0)

        self.layoutTitle.addWidget(self.title)
        self.content.addWidget(self.layoutTitle)
        self.content.addWidget(self.row)
        self.content.addWidget(self.row_2)

    def yesBtnEvent(self):
        print(self.inputCode.text())
        self.accept()

    def getYesBtn(self):
        return self.yesButton

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
