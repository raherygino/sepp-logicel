# coding:utf-8
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import FluentStyleSheet, TextWrap
from .mask_dialog_base import MaskDialogBase


class MessageDialog(MaskDialogBase):
    """ Win10 style message dialog box with a mask """

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, title: str, content: str, parent):
        super().__init__(parent=parent)
        self.content = content
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.qWidget = QWidget(self.widget)
        self.qWidget.setStyleSheet("QWidget {background: rgba(255,255,255,0); border: none}")
        self.vBoxLayout = QVBoxLayout(self.qWidget)
        self.contentLayout = QVBoxLayout()
        self.hBoxLayout = QHBoxLayout()
        self.widget.setLayout(self.vBoxLayout)
        self.yesButton = QPushButton(self.tr('Confirm'), self.widget)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.widget)
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.windowMask.resize(self.size())
        self.widget.setMaximumWidth(540)
        self.contentLabel.setText(TextWrap.wrap(self.content, 71)[0])

        self.__setQss()
        self.__initLayout()

        # connect signal to slot
        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        """ initialize layout """
        self.widget.setFixedHeight(self.qWidget.height()+92)
        self.yesButton.setFixedHeight(35)
        self.cancelButton.setFixedHeight(35)
        self.hBoxLayout.setContentsMargins(0,10,0,10)
        self.contentLayout.addWidget(self.titleLabel)
        self.contentLayout.addWidget(self.contentLabel)
        self.hBoxLayout.addWidget(self.yesButton)
        self.hBoxLayout.addWidget(self.cancelButton)
        self.vBoxLayout.addLayout(self.contentLayout)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        
    def __onCancelButtonClicked(self):
        self.cancelSignal.emit()
        self.setResult(self.Rejected)
        self.close()

    def __onYesButtonClicked(self):
        self.setEnabled(False)
        self.yesSignal.emit()
        self.setResult(self.Accepted)
        self.close()

    def __setQss(self):
        """ set style sheet """
        self.windowMask.setObjectName('windowMask')
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        FluentStyleSheet.MESSAGE_DIALOG.apply(self)
