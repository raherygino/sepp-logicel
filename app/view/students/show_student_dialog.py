from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QSize, Qt
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ImageLabel, setTheme, Theme, BodyLabel
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
        self.table.setData([["12/02/2024", "Permission", "12jours"]])
        self.vBoxLayout.addWidget(self.table)
        
        self.viewLayout.addLayout(self.vBoxLayout)
        self.buttonLayout.setSpacing(8)
        self.buttonGroup.setFixedHeight(70)
        self.buttonLayout.setContentsMargins(8, 8, 8, 8)
        
        self.yesButton.setText("Exporter")
        self.cancelButton.setText("Fermer")
        
    def setLabelData(self, label, data, layout):
        title = SubtitleLabel(label, self)
        val = BodyLabel(data, self)
        layout.addWidget(title, 0, Qt.AlignTop)
        layout.addWidget(val, 0, Qt.AlignTop)
        