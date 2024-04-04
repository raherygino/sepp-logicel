from PyQt5.QtWidgets import QHBoxLayout, QLineEdit
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, ComboBox
from ....common import col
from ....models import Student
import dataclasses

class ImportDialog(MessageBoxBase):
    def __init__(self, data:list[str], entity:Student, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('Importer', self)
        self.viewLayout.addWidget(self.titleLabel)
        label = ["Colonne"]
        for field in dataclasses.fields(entity):
            if field.name.find("id") == -1:
                if field.name in col.keys():
                    label.append(col[field.name])
        
        for item in data:
            if len(item.strip()) != 0:
                row = QHBoxLayout()
                lineEdit = LineEdit(self)
                lineEdit.setReadOnly(True)
                lineEdit.setText(item)
                combox = ComboBox(self)
                combox.addItems(label)
                row.addWidget(lineEdit)
                row.addWidget(combox)
                self.viewLayout.addLayout(row)
                
        self.combox = []
        for i in range(self.viewLayout.count()):
            item = self.viewLayout.itemAt(i)
            if item.layout():
                lay = item.layout()
                for i in range(lay.count()):
                    itm = lay.itemAt(i)
                    wdgt = itm.widget()
                    if wdgt:
                        if type(wdgt).__name__ == "ComboBox":
                            self.combox.append(wdgt)
                      
                    
