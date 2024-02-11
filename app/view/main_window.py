# coding: utf-8
from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase

from qfluentwidgets import NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow, SplashScreen
from qfluentwidgets import FluentIcon as FIF

from .utils.gallery_interface import GalleryInterface
from .utils.setting_interface import SettingInterface
from .students.students_interface import StudentInterface

from .home.home_interface import HomeInterface

from ..common.config import SUPPORT_URL, Lang
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common.Translate import Translate
from ..common import resource
from qfluentwidgets import isDarkTheme
#from pynput.mouse import Listener

from app.common.database.db_initializer import DBInitializer as DB
from app.common.database.service.student_service import StudentService
from app.common.database.entity.student import Student

class MainWindow(FluentWindow):
    
    def __init__(self):
        super().__init__()
        self.trans = Translate(Lang().current).text
        self.initWindow()
        #Initilize DATABASE 
        self.db = DB
        self.db.init()
        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.studentInterface = StudentInterface(self)
    
        
        self.readData("all")   
        '''
        self.widgetsInterface = WidgetsInterface(self)
        self.tableViewInterface = TableViewInterface(self)
        self.blankInterface = BlankInterface(self)
        '''
        self.settingInterface = SettingInterface(self)
        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()
        
        self.splashScreen.finish()

    def initLayout(self):
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def readData(self, name):
        f = open("app/resource/data/"+name+".csv", "r")
        lines = f.readlines()
        count = 0
        newFile = open("app/resource/data/"+name+"_formated.csv", "w")
        database = QSqlDatabase.database(self.db.CONNECTION_NAME, True)
        service = StudentService(database)
        for line in lines:
            count += 1
            data = line.strip().split(";")
            name = data[1].split(" ")
            lastname = name[0]
            firstname =  ' '.join([f'{i}' for i in name[1:]])
            company = data[0][0]
            section = data[0][1]
            level = "EAP"
            if company in ["1", "2", "3"] and section == "1":
                level = "EIP"
            elif company == "1" and section == "2":
                level = "EIP"
    
            #student = Student(lastname, firstname, data[2], level, company, section, data[0][2:3], data[0])
            #service.create(student)
            '''
            student = {
                "level": level,
                "company": company,
                "section": section,
                "numero": f"{data[0][2]}{data[0][3]}",
                "matricule": data[0],
                "lastname": lastname,
                "firstname": firstname,
                "gender": data[2]
            }
            #print(student)
            newFile.write(str(student)+"\n") '''
     

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, "Home")
        self.addSubInterface(self.studentInterface, FIF.PEOPLE, "Elèves")
        '''
        self.addSubInterface(self.widgetsInterface, FIF.GAME, t.widgets)
        self.addSubInterface(self.tableViewInterface, FIF.LAYOUT, t.table_view)
        self.addSubInterface(self.blankInterface, FIF.DOCUMENT, t.blank)
        '''
        self.navigationInterface.addSeparator()
        pos = NavigationItemPosition.SCROLL
        
        # add custom widget to bottom
        '''
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('Georginot', 'app/resource/images/user.png'),
            onClick=self.onSupport,
            position=NavigationItemPosition.BOTTOM
        ) '''
        
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)
        

    def initWindow(self):
        self.resize(960, 670)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon('app/resource/images/logo-eniap.png'))
        self.setWindowTitle(self.trans['app_name'])
        
        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(220, 220))
        self.splashScreen.raise_()
        

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        
        w = MessageBox(
            'Profile',
            'You want to see my profile?',
            self
        )
        w.yesButton.setText('Yes')
        w.cancelButton.setText('No')
        if w.exec():
            QDesktopServices.openUrl(QUrl(SUPPORT_URL))
        
    def closeEvent(self, event):
        
        exitDialog = MessageBox(
            'Quitter', 'Voulez vous quitter vraiment?',
            self
        )
        exitDialog.yesButton.setText('Oui')
        exitDialog.cancelButton.setText('Non')
        if exitDialog.exec():
            event.accept()
        else:
            event.ignore()

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)
