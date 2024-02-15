from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType, MessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint
from ..models import StudentModel, Student 
from ..common import Function
from ..view.students.list_student_tab import ListStudent

class StudentPresenter:
    
    HEADER_LABEL = ["ID", "Matricule", "Grade", "Nom", "Prénom(s)", "Genre",
                    "Repos médical ou convalescence (Jour)", "Exant d'effort physique (Jour)",
                    "Permission (Jour)", "CODIS (Fois)", "Bomelenge (Fois)", 
                    "Autre Sanction disciplinaire (fois)",
                    "Absent non motivé (Jour)", "Lettre de félicitation", 
                    "Autre remarque positive (fois)"]
    
    def __init__(self, view:ListStudent, model: StudentModel, promotion):
        self.view = view
        self.model = model
        self.promotion = promotion
        self.func = Function()
        self.view.tableView.setHorizontalHeaderLabels(self.HEADER_LABEL)
        self.actions()
        self.fetchData()
        
    def actions(self):
        self.view.addAction.triggered.connect(lambda: print("ok"))
        self.view.importAction.triggered.connect(lambda: self.importData())
        self.view.searchLineEdit.textChanged.connect(self.searchStudent)
        self.view.tableView.contextMenuEvent = lambda event: self.mouseRightClick(event)
        
    def mouseRightClick(self, event):
        id_item = self.view.tableView.selectedItems()[0].text()
        action = MenuAction(self)
        menu = RoundMenu(parent=self.view)
        menu.addAction(Action(FluentIcon.FOLDER, 'Voir'))
        menu.addAction(Action(FluentIcon.EDIT, 'Modifier'))
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.SCROLL, 'Mouvement'))
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.delete(id_item)))
        menu.menuActions()[-2].setCheckable(True)
        menu.menuActions()[-2].setChecked(True)

        self.posCur = QCursor().pos()
        cur_x = self.posCur.x()
        cur_y = self.posCur.y()

        menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def importData(self):
        filename = self.func.importFile(self.view, "Importer base de données", "CSV File (*.csv)")
        if filename:
            with open(filename, "r") as data:
                listStudent = []
                for line in data:
                    items = line.strip().split(";")
                    matricule = items[0]
                    name = items[1].split(" ")
                    lastname = name[0]
                    firstname = ' '.join([val for val in name[1:]]) if len(name) > 1 else ""
                    genre = items[2]
                    listStudent.append(Student(
                        promotion_id=self.promotion.id,
                        lastname=lastname,
                        firstname=firstname,
                        gender=genre,
                        matricule=matricule,
                        company=matricule[0],
                        section=matricule[1],
                        number=matricule[2:4]
                    ))
                self.model.create_multiple(listStudent)
                self.fetchData()
                
    def fetchData(self):
        data = self.model.fetch_items_by_id(self.promotion.id)
        self.view.tableView.setData(self.formatDataForTable(data))
        
    def formatDataForTable(self, data):
        listStudent = []
        for student in data:
            listStudent.append([
                student.id, student.matricule, student.level, student.lastname,
                student.firstname, student.gender
            ])
        return listStudent
        
    def searchStudent(self, text):
        data = self.model.search_with_id(self.promotion.id, matricule=text, firstname=text)
        self.view.tableView.setData(self.formatDataForTable(data))
        
class MenuAction:
    
    def __init__(self,presenter) -> None:
        self.model = presenter.model
        self.view = presenter.view
        self.presenter = presenter
        
    def delete(self, id):
        dialog = MessageBox("Supprimer", "Vous êtes sûr de vouloir supprimer?", self.view.parent.mainWindow)
        dialog.yesButton.setText("Oui")
        dialog.cancelButton.setText("Non")
        if dialog.exec():
            self.model.delete_item(id)
            text = self.view.searchLineEdit.text()
            if len(text) != 0:
                self.presenter.searchStudent(text)
            else:
                self.presenter.fetchData()
            self.presenter.func.toastSuccess("Supprimé", "Suppression avec réussite", self.view.parent)
       