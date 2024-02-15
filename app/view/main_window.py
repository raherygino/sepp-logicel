# coding: utf-8
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout

from qfluentwidgets import ( NavigationItemPosition, FluentWindow,
                            SplashScreen, TitleLabel)
from qfluentwidgets import FluentIcon as FIF

from .setting_interface import SettingInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource
from .home.home_interface import HomeInterface
from ..models.model.prom_model import PromotionModel
from ..presenter.prom_presenter import PromotionPresenter
from ..view import StudentInterface
from ..models import StudentModel
from ..presenter import StudentPresenter

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = TitleLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.studentInterface = StudentInterface(self)
        self.settingInterface = SettingInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)
        self.connectSignalToSlot()

        promModel = PromotionModel()
        studentModel = StudentModel()
        
        PromotionPresenter(self.homeInterface, promModel, self)
        StudentPresenter(self.studentInterface, studentModel)

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.addSubInterface(self.studentInterface, FIF.PEOPLE, "Students")
        self.navigationInterface.addSeparator()

        # add custom widget to bottom
        self.navigationInterface.addItem(
            routeKey='price',
            icon=Icon.PRICE,
            text=t.price,
            onClick=self.onSupport,
            selectable=False,
            tooltip=t.price,
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())