from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QLinearGradient,QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QEasingCurve
from qfluentwidgets import BodyLabel, PixmapLabel, isDarkTheme, FluentIcon, TitleLabel, FlowLayout, SmoothScrollArea, TransparentToolButton
from ...components.link_card2 import LinkCardView, LinkCard
from ...components.sample_card import SampleCardView
from ...common.style_sheet import StyleSheet

class HomeInterface(QWidget):
    """ Main interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout()
        self.banner = QPixmap(':/resource/images/header1.png')
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(30, 20, 0, 0)
        self.setLayout(self.vBoxLayout)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.flowLayout = FlowLayout(needAni=True)
        self.flowLayout.setAnimation(250, QEasingCurve.OutQuad)
        self.flowLayout.setContentsMargins(0, 10, 30, 30)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(10)
        title = TitleLabel('Liste des promotions', self)
        self.vBoxLayout.addWidget(title)

        
        #self.flowLayout.addWidget(self.cardNewEnv)
        #print(self.flowLayout.takeAllWidgets())
        # Create a QWidget to hold the layout
        widget = QWidget()
        widget.setLayout(self.flowLayout)
        widget.setObjectName("parentCard")

        # Create a QScrollArea and set the widget to be scrolled
        scroll_area = SmoothScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(widget)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: rgba(255, 255, 25, 0.0);}")
        widget.setStyleSheet("#parentCard { background-color: rgba(205, 25, 0, 0)}")

        StyleSheet.LINK_CARD.apply(self)
        # Set the main window layout
        self.vBoxLayout.addWidget(scroll_area)
        self.setObjectName("mainInterface")

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h-50, 50, 50))
        path.addRect(QRectF(w-50, 0, 50, 50))
        path.addRect(QRectF(w-50, h-50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            
        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))
