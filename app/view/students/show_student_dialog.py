from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame
from PyQt5.QtCore import QSize, Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ImageLabel,\
    PrimaryPushButton, PushButton, FluentIcon, BodyLabel, Dialog
from ...components import TableView
'''
class ShowStudentDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.setSpacing(7)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
    
        self.ImageLabel = ImageLabel(self)
        self.ImageLabel.setImage("app/resource/images/user.png")
        self.ImageLabel.setFixedSize(QSize(100,100))
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.vBoxLayout.addWidget(self.ImageLabel, 0, Qt.AlignCenter)
        self.ImageLabel.setAlignment(Qt.AlignCenter)
        
        self.label = BodyLabel("EAP 2723\nRAHERINOMENJANAHARY Georginot Armelin", self)
        self.label.setFixedWidth(450)
        self.vBoxLayout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.table = TableView(self)
        self.table.setHorizontalHeaderLabels(["Date", "Mouvement", "Nombre de jour"])
        self.vBoxLayout.addWidget(self.table)
        
        self.viewLayout.addLayout(self.vBoxLayout)
        self.buttonLayout.setSpacing(8)
        self.buttonGroup.setFixedHeight(50)
        self.buttonLayout.setContentsMargins(8, 4, 8, 4)
        
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.yesButton = PrimaryPushButton('OK', self, FluentIcon.ACCEPT)
        self.yesButton.clicked.connect(self.accept)
        self.buttonLayout.addWidget(self.yesButton)
        
        self.pushButton2 = PushButton('Exporter', self, FluentIcon.SHARE)
        self.buttonLayout.addWidget(self.pushButton2)
        
        self.buttonLayout.setAlignment(Qt.AlignRight)
        
    def setLabelData(self, label, data, layout):
        title = SubtitleLabel(label, self)
        val = BodyLabel(data, self)
        layout.addWidget(title, 0, Qt.AlignTop)
        layout.addWidget(val, 0, Qt.AlignTop)
'''       

class ShowStudentDialog(Dialog):
    def __init__(self, parent=None):
        super().__init__("", "", parent)
        self.setTitleBarVisible(False)
        self.contentLabel.setVisible(False)
        self.titleLabel.setVisible(False)
        self.ImageLabel = ImageLabel(self)
        self.ImageLabel.setImage("app/resource/images/user.png")
        self.ImageLabel.setFixedSize(QSize(100,100))
        self.ImageLabel.setObjectName(u"ImageLabel")
        self.textLayout.addWidget(self.ImageLabel, 0, Qt.AlignCenter)
        self.ImageLabel.setAlignment(Qt.AlignCenter)
        
        self.label = BodyLabel("EAP 2723\nRAHERINOMENJANAHARY Georginot Armelin", self)
        self.label.setFixedWidth(450)
        self.textLayout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.title = SubtitleLabel("Mouvement", self)
        self.title.setAlignment(Qt.AlignCenter)
        

        self.ImageMessage = ImageLabel(self)
        self.ImageMessage.setImage("app/resource/images/default-file-icon.png")
        self.ImageMessage.setFixedSize(QSize(100,100))
        self.message = BodyLabel("Aucune mouvement", self)
        self.message.setAlignment(Qt.AlignCenter)
        self.textLayout.addWidget(self.line)
        self.textLayout.addWidget(self.title)
        self.textLayout.addWidget(self.ImageMessage, 0, Qt.AlignCenter)
        self.textLayout.addWidget(self.message)
        
        self.table = TableView(self)
        self.table.setHorizontalHeaderLabels(["Date", "Mouvement", "Jours"])
        self.table.setMinimumHeight(280)
        self.textLayout.addWidget(self.table)
        
        
        self.buttonLayout.setSpacing(8)
        self.buttonGroup.setFixedHeight(50)
        self.buttonLayout.setContentsMargins(8, 4, 8, 4)
        
        self.yesButton.setVisible(False)
        self.cancelButton.setVisible(False)
        
        self.yesButton = PrimaryPushButton('OK', self, FluentIcon.ACCEPT)
        self.yesButton.clicked.connect(self.accept)
        self.buttonLayout.addWidget(self.yesButton)
        
        self.exportButton = PushButton('Exporter', self, FluentIcon.SHARE)
        self.buttonLayout.addWidget(self.exportButton)
        
        self.buttonLayout.setAlignment(Qt.AlignRight)
        
        