from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QLinearGradient,QColor, QBrush
from PyQt5.QtCore import Qt, QRectF, QEasingCurve
from qfluentwidgets import BodyLabel, PixmapLabel, FluentIcon, isDarkTheme, ToolButton, TitleLabel, FlowLayout, SmoothScrollArea, ComboBox
from ...components.link_card2 import LinkCardView, LinkCard
from ...components.sample_card import SampleCardView
from ...common.style_sheet import StyleSheet
from ...common import resource

class HomeInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout()
        self.banner = QPixmap('app/resource/images/cover.jpg')
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(30, 20, 0, 0)
        self.setLayout(self.vBoxLayout)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.flowLayout = FlowLayout(needAni=True)
        self.flowLayout.setAnimation(250, QEasingCurve.OutQuad)
        self.flowLayout.setContentsMargins(0, 10, 30, 30)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(10)
        row = QHBoxLayout()
        
        self.logoPn = PixmapLabel(self)
        self.logoPn.setPixmap(QPixmap("app/resource/images/logo_pn.png"))
        self.logoPn.setFixedSize(180,180)
        
        title = TitleLabel('Ecole Nationale des Inspecteurs et Agents de Police', self)
        title.setAlignment(Qt.AlignCenter)
        
        self.logoEniap = PixmapLabel(self)
        self.logoEniap.setPixmap(QPixmap("app/resource/images/eniap.png"))
        self.logoEniap.setFixedSize(140,180)
        row.setContentsMargins(0,0,15,0)
        row.addWidget(self.logoPn)
        row.addWidget(title)
        row.addWidget(self.logoEniap)
        
        row2 = QHBoxLayout()
        row2.setSpacing(12)
        row2.setAlignment(Qt.AlignCenter)
        label = BodyLabel("Promotion")
        choicePromotion = ComboBox(self)
        choicePromotion.setFixedWidth(200)
        choicePromotion.addItems(["30ème promotion", "29ème promotion"])
        row2.addWidget(label)
        row2.addWidget(choicePromotion)
        #self.vBoxLayout.addWidget(title)
        self.vBoxLayout.setSpacing(25)
        self.vBoxLayout.addLayout(row)
        self.vBoxLayout.addLayout(row2)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        
        self.cardEffectif = LinkCard(FluentIcon.PEOPLE, 'Effectif', '1 220', self)
        self.cardEffectifEip = LinkCard(FluentIcon.EDUCATION, 'Effectif EIP', '1 000', self)
        self.cardEffectifEap = LinkCard(FluentIcon.EDUCATION, 'Effectif EAP', '220', self)
        self.cardEffectifWoman = LinkCard(FluentIcon.DICTIONARY, 'Effectif Feminin', '220', self)
        self.cardEffectifMan = LinkCard(FluentIcon.EDUCATION, 'Effectif Masculin', '220', self)
        self.cardAvgAge = LinkCard(FluentIcon.EDUCATION, 'Moyen d\'age', '25ans', self)
        self.cardAge = LinkCard(FluentIcon.EDUCATION, 'Age', 'Moins agé 23ans | plus agé 52ans', self)
        
        self.flowLayout.addWidget(self.cardEffectif)
        self.flowLayout.addWidget(self.cardEffectifEip)
        self.flowLayout.addWidget(self.cardEffectifEap)
        self.flowLayout.addWidget(self.cardEffectifMan)
        self.flowLayout.addWidget(self.cardEffectifWoman)
        self.flowLayout.addWidget(self.cardAvgAge)
        self.flowLayout.addWidget(self.cardAge)
        #print(self.flowLayout.takeAllWidgets())
        # z a QWidget to hold the layout
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