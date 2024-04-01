from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import MessageBoxBase, SubtitleLabel, CompactSpinBox, PushButton, PixmapLabel, FluentIcon, BodyLabel
from ....components import LineEditWithLabel, SpinBoxEditWithLabel
from ....common.functions import Function

class NewPromotionDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.func = Function()
        self.row = QHBoxLayout()
        self.col_1 = QVBoxLayout()
        self.col_1.setAlignment(Qt.AlignCenter)
        
        self.logo = PixmapLabel(self)
        self.logoPath = ""
        self.placeholder = QPixmap("app/resource/images/placeholder.png")
        self.logo.setPixmap(self.placeholder)
        self.logo.setFixedSize(180,140)
        self.btnAddLogo = PushButton(FluentIcon.PHOTO, "Ajouter un logo")
        self.btnAddLogo.clicked.connect(lambda event: self.fetchLogo(event))
        self.col_1.addWidget(self.logo)
        self.col_1.addWidget(self.btnAddLogo)
        self.row.addLayout(self.col_1)
        
        self.col_2 = QVBoxLayout()
        self.col_2.setAlignment(Qt.AlignTop)
        
        self.titleLabel = SubtitleLabel('Promotion', self)
        
        self.rankcompactSpinBox = SpinBoxEditWithLabel("Rang")
        self.rankcompactSpinBox.spinbox.setAccelerated(True)
        self.rankcompactSpinBox.spinbox.textChanged.connect(self.__onChangeName)
        
        self.nameLineEdit = LineEditWithLabel('Nom de la promotion')
        self.nameLineEdit.lineEdit.setClearButtonEnabled(True)
        
        '''self.logoLineEdit = LineEditWithLabel("Logo")
        self.logoLineEdit.lineEdit.setPlaceholderText('Logo')
        self.logoLineEdit.lineEdit.setReadOnly(True)
        self.logoLineEdit.lineEdit.setClearButtonEnabled(True)
        self.logoLineEdit.lineEdit.mouseDoubleClickEvent = lambda event: self.fetchLogo(event)'''
        
        self.yearLineEdit = LineEditWithLabel("Année")
        self.yearLineEdit.lineEdit.setPlaceholderText('Année')
        self.yearLineEdit.lineEdit.setClearButtonEnabled(True)
        
        self.col_2.addLayout(self.rankcompactSpinBox)
        self.col_2.addLayout(self.nameLineEdit)
        self.col_2.addLayout(self.yearLineEdit)
        
        # add widget to view layout
        self.row.addLayout(self.col_2)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(self.row)

        # change the text of button
        self.yesButton.setText('Ajouter')
        self.cancelButton.setText('Annuler')
        self.yesButton.setEnabled(False)
        self.widget.setMinimumWidth(450)

        # self.hideYesButton()
    def __onChangeName(self, text):
        if int(text) != 0:
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)
            
    def fetchLogo(self, event):
        fileName = self.func.importFile(self, "Import image", "PNG File (*.png);;JPG File (*.jpg);;GIF File (*.gif)")
        if fileName:
            self.logoPath = fileName
            pixmap = QPixmap(fileName)
            self.logo.setPixmap(pixmap)
            self.logo.setFixedSize(140,140)
        else:
            self.logoPath = ""
            self.logo.setPixmap(self.placeholder)
            self.logo.setFixedSize(180,140)
