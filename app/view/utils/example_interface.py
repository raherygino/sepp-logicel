from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from qfluentwidgets import ComboBox, CommandBar, FluentIcon, Action, \
    ToolButton, PushButton, RoundMenu, SearchLineEdit, IndeterminateProgressBar, \
    TransparentDropDownPushButton, LineEdit, SmoothScrollArea, PixmapLabel
from ...components import TableView, LineEditWithLabel, ComboxEditWithLabel
from ...common.config import OptionsConfigItem

class ExampleInterface(QWidget):
    
    def __init__(self,  parent=None):
        super().__init__(parent=parent)
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setStyleSheet("SmoothScrollArea {border: none}")
        self.scroll_area.setWidget(self.__contentWidgets())
        self.scroll_area.setWidgetResizable(True)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.scroll_area)
        self.setLayout(self.mainLayout)
        self.setObjectName("exampleInterface")
        
    def __contentWidgets(self) -> QWidget:
        scrollable_widget = QWidget()
        self.vBoxlayout = QVBoxLayout()
        self.vBoxlayout.setAlignment(Qt.AlignTop)
        self.vBoxlayout.setContentsMargins(25,10,25,10)
        self.__content()
        scrollable_widget.setLayout(self.vBoxlayout)
        return scrollable_widget
    
    def addChild(self, parent, children):
        for child in children:
            if isinstance(child, QWidget):
                parent.addWidget(child)
            else:
                parent.addLayout(child)
            
    def __content(self):
        self.row = QHBoxLayout()
        #self.row.setAlignment(Qt.AlignTop)
        self.leftCol = QVBoxLayout()
        self.leftCol.setAlignment(Qt.AlignTop)
        
        self.rightCol = QVBoxLayout()
        self.picture = PixmapLabel(self)
        self.picture.setPixmap(QPixmap("app/resource/images/user.png"))
        self.btnAddImage = PushButton(FluentIcon.PHOTO, "Ajouter une photo")
        
        self.addChild(self.rightCol, [self.picture, self.btnAddImage])
        self.addChild(self.row, [self.leftCol, self.rightCol])
        
        self.name = LineEditWithLabel("Nom et prénoms")
        self.addChild(self.leftCol, [self.name])
        
        self.row2 = QHBoxLayout()
        self.im = LineEditWithLabel("IM")
        self.matricule = LineEditWithLabel("Matricule")
        self.grade = LineEditWithLabel("Grade")
        self.length = LineEditWithLabel("Taille")
        self.genre = ComboxEditWithLabel("Sexe", ["Masculin", "Féminin"])
        self.blood = LineEditWithLabel("Groupe Sanguin")
        
        self.row3 = QHBoxLayout()
        self.birthday = LineEditWithLabel("Date de naissance")
        self.birthplace = LineEditWithLabel("Lieu de naissance")
        
        self.row4 = QHBoxLayout()
        self.nameFather = LineEditWithLabel("Nom du père")
        self.jobFather = LineEditWithLabel("Profession")
        self.nameMother = LineEditWithLabel("Nom de la mère")
        self.jobMother = LineEditWithLabel("Profession")
        
        self.row5 = QHBoxLayout()
        self.numberCin = LineEditWithLabel("N° CIN")
        self.dateCin = LineEditWithLabel("Fait le")
        self.placeCin = LineEditWithLabel("Fait à")
        
        self.row6 = QHBoxLayout()
        self.regionOrigin = LineEditWithLabel("Region d'origine")
        self.ethnie = LineEditWithLabel("Ethnie")
        
        self.row7 = QHBoxLayout()
        self.address = LineEditWithLabel("Adresse")
        self.phone = LineEditWithLabel("Téléphone")
        self.email = LineEditWithLabel("Email")
        self.contactEmergency = LineEditWithLabel("Contact en cas d'urgence")
        
        self.addChild(self.row2,  [self.im, self.grade, self.length, self.genre, self.blood])
        self.addChild(self.row3,  [self.birthday, self.birthplace])
        self.addChild(self.row4,  [self.nameFather,self.jobFather,self.nameMother, self.jobMother])
        self.addChild(self.row5,  [self.numberCin, self.dateCin,  self.placeCin])
        self.addChild(self.row6,  [self.regionOrigin, self.ethnie])
        self.addChild(self.row7,  [self.address, self.phone, self.email, self.contactEmergency])
        
        self.addChild(self.leftCol, [self.row2, self.row3, self.row4])
        self.addChild(self.vBoxlayout, [self.row, self.row5, self.row6, self.row7])
    
    def __content2(self):
        self.hBoxLayout = QHBoxLayout()
        self.hBoxLayout.setAlignment(Qt.AlignTop)
        self.row = QHBoxLayout()
        self.leftCol = QVBoxLayout()
        self.leftCol.setAlignment(Qt.AlignTop)
        self.name = LineEditWithLabel("Nom et prénoms")
        self.im = LineEditWithLabel("IM")
        self.leftCol.addLayout(self.name)
        self.leftCol.addLayout(self.im)
        self.label = PixmapLabel(self)
        self.label.setPixmap(QPixmap("app/resource/images/user.png"))
        self.addChild(self.leftCol,self.row)
        self.addChild(self.leftCol,self.label)
        self.row.addLayout(self.leftCol)
        self.row.addWidget(self.label)
        self.vBoxlayout.addLayout(self.row)
        self.vBoxlayout.addLayout(self.hBoxLayout)
        