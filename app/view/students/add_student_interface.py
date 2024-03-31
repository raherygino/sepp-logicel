from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QBoxLayout, QSizePolicy
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from qfluentwidgets import ComboBox, PrimaryPushButton, CommandBar, FluentIcon, Action, \
    ToolButton, PushButton, RoundMenu, SearchLineEdit, IndeterminateProgressBar, \
    TransparentDropDownPushButton, LineEdit, SmoothScrollArea, PixmapLabel, SubtitleLabel, StrongBodyLabel, \
        CheckBox, BodyLabel
from ...components import TableView, LineEditWithLabel, ComboxEditWithLabel
from ...common.config import OptionsConfigItem

class AddStudentInterface(QWidget):
    
    def __init__(self,  parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QVBoxLayout()
        self.scroll_area = SmoothScrollArea()
        self.scroll_area.setStyleSheet("SmoothScrollArea {border: none; background: rgba(255,255,255,0)}")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidget(self.__contentWidgets())
        self.scroll_area.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scroll_area)
        self.btnAdd = PrimaryPushButton("Ajouter", self)
        self.mainLayout.addWidget(self.btnAdd)
        self.setLayout(self.mainLayout)
        self.setObjectName("addStudentInterface")
        
    def __contentWidgets(self) -> QWidget:
        scrollable_widget = QWidget()
        scrollable_widget.setStyleSheet("QWidget {background: rgba(255,255,255,0)}")
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
        self.row1 = QHBoxLayout()
        self.titleStatus = SubtitleLabel("I - ETAT CIVIL")
        self.vBoxlayout.addWidget(self.titleStatus)
        self.leftCol = QVBoxLayout()
        self.leftCol.setAlignment(Qt.AlignTop)
        
        self.rightCol = QVBoxLayout()
        self.picture = PixmapLabel(self)
        self.picture.setPixmap(QPixmap("app/resource/images/user.png"))
        self.btnAddImage = PushButton(FluentIcon.PHOTO, "Ajouter une photo")
        
        self.addChild(self.rightCol, [self.picture, self.btnAddImage])
        self.addChild(self.row1, [self.leftCol, self.rightCol])
        
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
        
        self.row8 = QHBoxLayout()
        self.row8.setAlignment(Qt.AlignLeft)
        self.maritalStatus = ComboxEditWithLabel("Situation matrimoniale", ["Célibataire", "Marié(e) legitime", "Mari(é) selon coutume", "Divorcé(e)", "Veuf(ve)"])
        self.maritalStatus.combox.setFixedWidth(300)
        
        self.titleConjoint = StrongBodyLabel("CONJOINT(E)")
        
        self.row9 = QHBoxLayout()
        self.name_conjoint = LineEditWithLabel("Nom et prénoms")
        self.profession_conjoint = LineEditWithLabel("Profession")
        self.employer_conjoint = LineEditWithLabel("Employeur")
        self.locality = LineEditWithLabel("Localité")
        self.im_conjoint = LineEditWithLabel("IM (si fonctionnaire)")
        
        self.titleChild = StrongBodyLabel("ENFANT A CHARGE")
        self.tableChild = TableView(self)
        self.tableChild.setHorizontalHeaderLabels(["Nom et prénoms des enfants", "Sexe", "Date de naissance",  "Scolarité", ""])
        self.tableChild.setData([["dfsdfs","sdfsd","s", "dfd", ""]])
        self.tableChild.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        #self.tableChild.setFixedHeight(100)
        
        
        self.titleStudy = SubtitleLabel("II - ETUDES ET FORMATIONS  EFFECTUEES : (à Madagascar et à l'extérieur)")
        self.tableStudy = TableView(self)
        self.tableStudy.setHorizontalHeaderLabels(["Periode", "Filières / Disciplines ", "Etablissement",  "Diplôme/Certificat/Attestation", ""])
        self.tableStudy.setData([["-","-","-", "-", ""]])
        self.tableStudy.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        
        self.titleExp = SubtitleLabel("III - EXPERIENCES PROFESSIONNELLES")
        self.titleExp2 = StrongBodyLabel("a) Avant votre intégration au sein de la Police Nationale:")
        self.titleExp2.setContentsMargins(15,0,0,0)
        self.tableExp = TableView(self)
        self.tableExp.setHorizontalHeaderLabels(["PERIODE", "POSTE DE TRAVAIL", "ENTREPRISE EMPLOYEUR", ""])
        self.tableExp.setData([["-","-","-","-"]])
        self.tableExp.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        
        self.titleExp3 = StrongBodyLabel("b) Au sein de la Police Nationale, y compris les détachements et les missions  à l'extérieur:")
        self.titleExp3.setContentsMargins(15,0,0,0)
        self.tableExp2 = TableView(self)
        self.tableExp2.setHorizontalHeaderLabels(["PERIODE", "POSTE DE TRAVAIL", "DIRECTION/SERVICE", "REFERENCE DE LA DECISION D'AFFECTATION / MISSION", ""])
        self.tableExp2.setData([["-","-","-","", ""]])
        self.tableExp2.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        
        self.titleActivity = SubtitleLabel("IV - ACTIVITES ASSOCIATIVES")
        self.tableActivity = TableView(self)
        self.tableActivity.setHorizontalHeaderLabels(["PERIODE", "ASSOCIATION/ETABLISSEMENT", "RESPONSABILITE", ""])
        self.tableActivity.setData([["-","-","-", ""]])
        self.tableActivity.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        
        self.titleDict = SubtitleLabel("V - DICTINCTIONS HONORIFIQUES")
        self.tableDict = TableView(self)
        self.tableDict.setHorizontalHeaderLabels(["DICTINCTIONS HONORIFIQUES", "REFERENCES", "DATE D'OBTENTION", ""])
        self.tableDict.setData([["-","-","-", ""]])
        self.tableDict.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        
        self.titleInfo = SubtitleLabel("VI - CONNAISSANCES EN INFORMATIQUES")
        self.subTitleInfoOffice = StrongBodyLabel("1 - Bureautique")
        
        self.row10 = QHBoxLayout()
        self.row10.setAlignment(Qt.AlignLeft)
        self.row10.setContentsMargins(14,0,0,0)
        self.titleOffice = BodyLabel("a) Microsoft office")
        self.level = ["-","Usage simple", "Confirmé", "Expert"]
        self.comboBoxWord = ComboxEditWithLabel("Word")
        self.comboBoxWord.combox.addItems(self.level)
        self.comboBoxExcel = ComboxEditWithLabel('Excel')
        self.comboBoxExcel.combox.addItems(self.level)
        self.comboBoxPowerPoint = ComboxEditWithLabel('PowerPoint')
        self.comboBoxPowerPoint.combox.addItems(self.level)
        self.editVerOffice = LineEditWithLabel("Version")
        self.editVerOffice.lineEdit.setFixedWidth(100)
        self.editVerOffice.setAlignment(Qt.AlignLeft)
        
        self.row11 = QHBoxLayout()
        self.row11.setAlignment(Qt.AlignLeft)
        self.titleLevelOffice = BodyLabel("Niveau")
        self.titleLevelOffice.setContentsMargins(120, 0, 0, 0)
        self.titleOfficeExpert = BodyLabel("Si Expert")
        self.titleOfficeExpert.setContentsMargins(20, 0, 0, 0)
        self.checkBoxVbScript = CheckBox('VB Script', self)
        self.checkBoxMacros = CheckBox('Macros', self)
        
        self.row12 = QHBoxLayout()
        self.row12.setAlignment(Qt.AlignLeft)
        self.row12.setContentsMargins(14,0,0,0)
        self.titleOtherOffice = BodyLabel("b) Autres")
        self.comboBoxLibreOffice = ComboxEditWithLabel('Libre Office')
        self.comboBoxLibreOffice.combox.addItems(self.level)
        self.comboBoxOpenOffice = ComboxEditWithLabel('Open Office')
        self.comboBoxOpenOffice.combox.addItems(self.level)
        self.comboBoxAppleWorks = ComboxEditWithLabel('Apple Works')
        self.comboBoxAppleWorks.combox.addItems(self.level)
        
        self.subTitleInfoOS = StrongBodyLabel("2 - Système d'exploitation")
        self.row13 = QHBoxLayout()
        self.row13.setAlignment(Qt.AlignLeft)
        self.row13.setContentsMargins(14,0,0,0)
        self.comboBoxMsDos = ComboxEditWithLabel('MS-DOS')
        self.comboBoxMsDos.combox.addItems(self.level)
        self.comboBoxMac = ComboxEditWithLabel('MAC/OS X')
        self.comboBoxMac.combox.addItems(self.level)
        self.comboBoxWin = ComboxEditWithLabel('Windows')
        self.comboBoxWin.combox.addItems(self.level)
        self.comboBoxLinux = ComboxEditWithLabel('UNIX/Linux')
        self.comboBoxLinux.combox.addItems(self.level)
        
        self.subTitleInfoHardWare = StrongBodyLabel("3 - Hardware")
        self.row14 = QHBoxLayout()
        self.row14.setAlignment(Qt.AlignLeft)
        self.row14.setContentsMargins(14,0,0,0)
        self.comboBoxAssemblage = ComboxEditWithLabel('Assemblage')
        self.comboBoxAssemblage.combox.addItems(self.level)
        self.comboBoxConnect = ComboxEditWithLabel('Connectique')
        self.comboBoxConnect.combox.addItems(self.level)
        self.comboBoxMaintenance = ComboxEditWithLabel('Maintenance')
        self.comboBoxMaintenance.combox.addItems(self.level)
        
        self.subTitleInfoNetwork = StrongBodyLabel("4 - Réseaux")
        self.titleInternet = StrongBodyLabel("a) Internet")
        self.row15 = QHBoxLayout()
        self.row15.setAlignment(Qt.AlignLeft)
        self.row15.setContentsMargins(14,0,0,0)
        self.checkBoxWeb = CheckBox('Web', self)
        self.checkBoxMail = CheckBox('Corrier Electronique', self)
        self.checkBoxSocialMedia = CheckBox('Réseaux sociaux', self)
        
        self.titleTypeNetwork = StrongBodyLabel("b) Types réseaux")
        self.row16 = QHBoxLayout()
        self.row16.setAlignment(Qt.AlignLeft)
        self.row16.setContentsMargins(14,0,0,0)
        self.checkBoxPoste= CheckBox('LAN (Poste à poste)', self)
        self.checkBoxClientServer = CheckBox('LAN (Clients/Serveurs)', self)
        self.checkBoxSocialMAN = CheckBox('MAN', self)
        
        self.row17 = QHBoxLayout()
        self.row17.setAlignment(Qt.AlignLeft)
        self.row17.setContentsMargins(120,0,0,0)
        self.comboBoxLevel = ComboxEditWithLabel('Niveau')
        self.comboBoxLevel.combox.addItems(self.level)
        self.comboBoxLevel.combox.setFixedWidth(200)
        self.editNetworkTools = LineEditWithLabel("Outils utilisées")
        self.editNetworkTools.lineEdit.setFixedWidth(300)
        
        self.subTitleWeb = StrongBodyLabel("5 - Technologie du Web")
        self.row18 = QHBoxLayout()
        self.row18.setAlignment(Qt.AlignLeft)
        self.row18.setContentsMargins(14,0,0,0)
        self.comboBoxHtml = ComboxEditWithLabel('HTML')
        self.comboBoxHtml.combox.addItems(self.level)
        self.editScript = LineEditWithLabel('Script WEB (Langages web)')
        self.editScript.lineEdit.setFixedWidth(200)
        self.comboBoxLevelScript = ComboxEditWithLabel('Niveau script WEB')
        self.comboBoxLevelScript.combox.addItems(self.level)
        
        self.subTitleProgramming = StrongBodyLabel("6 - Programmation")
        self.row19 = QHBoxLayout()
        self.row19.setAlignment(Qt.AlignLeft)
        self.row19.setContentsMargins(14,0,0,0)
        self.comboBoxAlgo = ComboxEditWithLabel('a - Algorithme')
        self.comboBoxAlgo.combox.addItems(self.level)
        self.editLangageUsed = LineEditWithLabel('Langages utilisés')
        self.editExProjectAlgo = LineEditWithLabel('Exemples de projet réalisé')
        
        self.row19_2 = QHBoxLayout()
        self.row19_2.setAlignment(Qt.AlignLeft)
        self.row19_2.setContentsMargins(14,0,0,0)
        
        self.comboBoxProgrammingLang = ComboxEditWithLabel('b - Langage de programmation le plus connu')
        self.comboBoxProgrammingLang.combox.addItems(self.level)
        self.editLangageUsedProLang = LineEditWithLabel('Langages utilisés')
        self.editExProjectProLang = LineEditWithLabel('Exemples de projet réalisé')
        
        self.row19_3 = QHBoxLayout()
        self.row19_3.setAlignment(Qt.AlignLeft)
        self.row19_3.setContentsMargins(14,0,0,0)
        
        self.comboBoxObject = ComboxEditWithLabel('c - Conception orientée objet')
        self.comboBoxObject.combox.addItems(self.level)
        self.editLangageUsedObject = LineEditWithLabel('Langages utilisés')
        self.editExProjectObject = LineEditWithLabel('Exemples de projet réalisé')
        
        self.subTitleDatabase = StrongBodyLabel("7 - Base de données : Relationnelles")
        self.comboBoxLevelDb = ComboxEditWithLabel('Niveau')
        self.comboBoxLevelDb.combox.addItems(self.level)
        self.editLangageUsedDb = LineEditWithLabel('Langages utilisés')
        self.editExProjectDb = LineEditWithLabel('Exemples de projet réalisé')
        self.row20 = QHBoxLayout()
        self.row20.setAlignment(Qt.AlignLeft)
        self.row20.setContentsMargins(14,0,0,0)
        
        self.subTitleInfo = StrongBodyLabel("8 - Multimédia")
        self.comboBoxMultimedia = ComboxEditWithLabel('Infographie')
        self.comboBoxMultimedia.combox.addItems(self.level)
        self.comboBoxMultimedia.setContentsMargins(30,0,0,0)
        
        self.titleLang = SubtitleLabel("VII - CONNAISSANCES LINGUISTIQUES")
        self.tableLang = TableView(self)
        self.tableLang.setHorizontalHeaderLabels(["LANGUES", "ECRIS", "LU", "PARLE", "DIPLOMES CORRESPONDANTS"])
        self.tableLang.setData([["Français","","","",""], ["Anglais","","","",""]])
        self.tableLang.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.tableLang.setMinimumHeight(90)
        
        self.titlePremis = SubtitleLabel("VIII - APTITUDE EN CONDUITE DE VEHICULE : (Permis de conduire)")
        self.titleCat = BodyLabel("Catégorie:")
        self.row21 = QHBoxLayout()
        self.row21.setAlignment(Qt.AlignLeft)
        self.row21.setContentsMargins(14,0,0,0)
        self.checkboxA = CheckBox("A")
        self.checkboxA2 = CheckBox("A'")
        self.checkboxB = CheckBox("B")
        self.checkboxC = CheckBox("C")
        self.checkboxD = CheckBox("D")
        self.checkboxE = CheckBox("E")
        self.checkboxF = CheckBox("F")
    
        self.row22 = QHBoxLayout()
        self.row22.setAlignment(Qt.AlignLeft)
        self.row22.setContentsMargins(14,0,0,0)
        self.editDatePermis = LineEditWithLabel('Date de délivrance')
        self.comboxPermisAdmin = ComboxEditWithLabel('Détenez-vous un permis administravif?')
        self.comboxPermisAdmin.combox.addItems(["Oui", "Non"])
        self.comboxPermisAdmin.combox.setCurrentIndex(1)
        self.comboxDatePermisAdmin = LineEditWithLabel('Si oui, date de délivrance')
        
        self.titleSpeciality = SubtitleLabel("IX - APTITUDES SPECIALES")
        self.editSpeciality = LineEditWithLabel("Aptitudes")
        
        self.addChild(self.row2,   [self.im, self.grade, self.length, self.genre, self.blood])
        self.addChild(self.row3,   [self.birthday, self.birthplace])
        self.addChild(self.row4,   [self.nameFather,self.jobFather,self.nameMother, self.jobMother])
        self.addChild(self.row5,   [self.numberCin, self.dateCin,  self.placeCin])
        self.addChild(self.row6,   [self.regionOrigin, self.ethnie])
        self.addChild(self.row7,   [self.address, self.phone, self.email, self.contactEmergency])
        self.addChild(self.row8,   [self.maritalStatus])
        self.addChild(self.row9,   [self.name_conjoint, self.profession_conjoint, self.employer_conjoint, self.locality, self.im_conjoint])
        self.addChild(self.row10,  [self.comboBoxWord, self.comboBoxExcel, self.comboBoxPowerPoint, self.editVerOffice])
        self.addChild(self.row11,  [self.titleOfficeExpert, self.checkBoxVbScript, self.checkBoxMacros])
        self.addChild(self.row12,  [self.comboBoxLibreOffice, self.comboBoxOpenOffice, self.comboBoxAppleWorks])
        self.addChild(self.row13,  [self.comboBoxMsDos, self.comboBoxMac, self.comboBoxWin, self.comboBoxLinux])
        self.addChild(self.row14,  [self.comboBoxAssemblage, self.comboBoxConnect, self.comboBoxMaintenance])
        self.addChild(self.row15,  [self.titleInternet, self.checkBoxWeb, self.checkBoxMail, self.checkBoxSocialMedia])
        self.addChild(self.row16,  [self.titleTypeNetwork, self.checkBoxPoste, self.checkBoxClientServer, self.checkBoxSocialMAN])
        self.addChild(self.row17,  [self.comboBoxLevel, self.editNetworkTools])
        self.addChild(self.row18,  [self.comboBoxHtml, self.editScript, self.comboBoxLevelScript])
        self.addChild(self.row19 , [self.comboBoxAlgo, self.editLangageUsed, self.editExProjectAlgo])
        self.addChild(self.row19_2,[self.comboBoxProgrammingLang ,self.editLangageUsedProLang, self.editExProjectProLang])
        self.addChild(self.row19_3,[self.comboBoxObject, self.editLangageUsedObject, self.editExProjectObject])
        self.addChild(self.row20,  [self.comboBoxLevelDb, self.editLangageUsedDb, self.editExProjectDb])
        
        self.addChild(self.row21,  [self.titleCat ,self.checkboxA, self.checkboxA2, self.checkboxB, self.checkboxC, self.checkboxD, 
                                    self.checkboxE, self.checkboxF])
        self.addChild(self.row22,  [self.editDatePermis, self.comboxPermisAdmin, self.comboxDatePermisAdmin])
        
        self.addChild(self.leftCol,[self.row2, self.row3, self.row4])
        self.addChild(self.vBoxlayout, [ self.row1, self.row5, self.row6, self.row7, self.row8, self.titleConjoint, self.row9, 
                                        self.titleChild, self.tableChild, self.titleStudy, self.tableStudy, self.titleExp, self.titleExp2, 
                                        self.tableExp, self.titleExp3, self.tableExp2, self.titleActivity, self.tableActivity, self.titleDict, 
                                        self.tableDict, self.titleInfo, self.subTitleInfoOffice, self.titleOffice, self.row10,
                                        self.row11, self.titleOtherOffice, self.row12, self.subTitleInfoOS, self.row13, self.subTitleInfoHardWare,
                                        self.row14, self.subTitleInfoNetwork, self.row15, self.row16, self.row17, self.subTitleWeb,
                                        self.row18, self.subTitleProgramming, self.row19, self.row19_2, self.row19_3 , self.subTitleDatabase, self.row20,  self.subTitleInfo, 
                                        self.comboBoxMultimedia, self.titleLang, self.tableLang, self.titlePremis, 
                                        self.row21, self.row22, self.titleSpeciality, self.editSpeciality])
