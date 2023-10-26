# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from qframelesswindow import FramelessDialog
from qfluentwidgets import TextWrap, FluentStyleSheet, PrimaryPushButton, LineEdit
from .mask import MaskDialogBase

class Ui_MessageBox:
    """ Ui of message box """

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def _setUpUi(self, content: QFrame, parent):
        #self.content = content
        #self.titleLabel = QLabel(title, parent)
        self.contentLabel = content
        self.contentLabel.setMinimumSize(QSize(520, 0))
        self.buttonGroup = QFrame(parent)
        self.yesButton = PrimaryPushButton(self.tr('Confirm'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(parent)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        # fixes https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/19
        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)

        self.yesButton.setFocus()
        self.buttonGroup.setFixedHeight(81)

        self._adjustText()

        #self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def _adjustText(self):
        if self.isWindow():
            if self.parent():
                #w = max(self.titleLabel.width(), self.parent().width())
                chars = 140
            else:
                chars = 100
        else:
            #w = max(self.titleLabel.width(), self.window().width())
            chars = 130

        # self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.textLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.textLayout.setSpacing(0)
        self.textLayout.setContentsMargins(0, 0, 0, 0)
        #self.textLayout.addWidget(self.titleLabel, 0, Qt.AlignTop)
        self.textLayout.addWidget(self.contentLabel, 0, Qt.AlignTop)
        #self.textLayout.addWidget(self.content, 0, Qt.AlignTop)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def __onCancelButtonClicked(self):
        self.reject()
        self.cancelSignal.emit()

    def __onYesButtonClicked(self):
        self.accept()
        self.yesSignal.emit()

    def __setQss(self):
        #self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')

        FluentStyleSheet.DIALOG.apply(self)

        self.yesButton.adjustSize()
        self.cancelButton.adjustSize()

class MessageBox(MaskDialogBase, Ui_MessageBox):
    """ Message box """

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, content: QFrame, parent=None):
        super().__init__(parent=parent)
        self._setUpUi(content, self.widget)
        # self.layo

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)
        self.buttonGroup.setMinimumWidth(280)
        '''
        width = max(self.contentLabel.width(), self.titleLabel.width()) + 48
        height = self.contentLabel.y() + self.contentLabel.height() + 105
        self.widget.setFixedSize(width, height)
        '''


    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self._adjustText()

        return super().eventFilter(obj, e)
