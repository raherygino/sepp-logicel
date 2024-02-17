from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize, Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ImageLabel,PrimaryPushButton, PushButton, FluentIcon, BodyLabel
from ...components import TableView

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
        self.table.setHorizontalHeaderLabels(["Date", "Mouvement", "Nombre"])
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
        