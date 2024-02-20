# coding:utf-8
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QPixmap, QDesktopServices
from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout

from qfluentwidgets import IconWidget, FluentIcon,BodyLabel, TextWrap, SingleDirectionScrollArea, TitleLabel, SubtitleLabel
from ..common.style_sheet import StyleSheet


class LinkCard(QFrame):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(250, 220)
        self.icon = icon
        self.iconWidget = IconWidget(icon, self)
        self.title = SubtitleLabel(self)
        self.title.setText(title)
        self.content = BodyLabel(self)
        self.content.setText(TextWrap.wrap(content, 28, False)[0])

        self.__initWidget()

    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)

        self.iconWidget.setFixedSize(54, 54)
        #self.urlWidget.setFixedSize(16, 16)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(24, 24, 0, 13)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(16)
        self.vBoxLayout.addWidget(self.title)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.content)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        #self.urlWidget.move(170, 192)

        self.title.setObjectName('title')
        self.content.setObjectName('content')


class LinkCardView(SingleDirectionScrollArea):
    """ Link card view """

    def __init__(self, parent=None):
        super().__init__(parent, Qt.Horizontal)
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.hBoxLayout.setContentsMargins(36, 0, 0, 0)
        self.hBoxLayout.setSpacing(12)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.view.setObjectName('view')
        StyleSheet.LINK_CARD.apply(self)

    def addCard(self, icon, title, content):
        """ add link card """
        card = LinkCard(icon, title, content, self.view)
        self.hBoxLayout.addWidget(card, 0, Qt.AlignLeft)
