from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType, MessageBox, MessageDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QLineEdit
from ..models import StudentModel, Student 
from ..common import Function
from ..components import Dialog
from ..view.students.list_student_tab import ListStudent
from ..view.students.new_student_dialog import NewStudentDialog
from ..view.students.show_student_dialog import ShowStudentDialog

class StudentPresenter:
    
    HEADER_LABEL = ["Matricule", "Grade", "Nom", "Prénom(s)", "Genre",
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
        self.__init_combox_data()
        self.actions()
        self.fetchData()
    
    def __init_combox_data(self):
        companyStudents = self.model.fetch_items_by_id(self.promotion.id, group_by="company")
        sectionStudents = self.model.fetch_items_by_id(self.promotion.id, group_by="section")
        self.setComboxData(self.view.comboBoxCompany, companyStudents, "Compagnie", "company")
        self.setComboxData(self.view.comboBoxSection, sectionStudents, "Section", "section")
        
    def setComboxData(self, combox, data, label, key):
        nComboxData = []
        for item in data:
            val = item.get(key)
            companyLabel = f"{val}ère {label}" if val == 1 else f"{val}ème {label}"
            nComboxData.append(companyLabel)
        nComboxData.insert(0, label)
        combox.addItems(nComboxData)
        combox.setCurrentIndex(0)
        
    def actions(self):
        self.view.addAction.triggered.connect(lambda: self.addStudent())
        self.view.importAction.triggered.connect(lambda: self.importData())
        self.view.searchLineEdit.textChanged.connect(self.searchStudent)
        self.view.comboBoxCompany.currentTextChanged.connect(self.textChangedCombox)
        self.view.comboBoxSection.currentTextChanged.connect(self.textChangedCombox)
        self.view.tableView.contextMenuEvent = lambda event: self.mouseRightClick(event)
        
    def dataStudentFromDialog(self, dialog):
        lastname = dialog.lastnameEdit.lineEdit(0).text()
        firstname = dialog.firstnameEdit.lineEdit(0).text()
        matricule = dialog.matriculeEdit.lineEdit(0).text()
        level = dialog.gradeEdit.value()
        gender = dialog.genderEdit.value()
        return Student(
            promotion_id=self.promotion.id,
            lastname=lastname,
            firstname=firstname,
            gender=gender,
            level=level,
            matricule=matricule,
            company=matricule[0],
            section=matricule[1],
            number=matricule[2:4]
        )
            
        
    
    def addStudent(self):
        dialog = NewStudentDialog(self.view.parent)
        if dialog.exec():
            student = self.dataStudentFromDialog(dialog)
            if self.model.count_by(matricule=student.matricule) == 0:
                self.model.create(student)
                self.fetchData()
            else:
                self.func.errorSuccess("Matricule invalide", "Matricule exist déjà", self.view.parent)
                
        
    def textChangedCombox(self, text):
        print(text)
        
    def mouseRightClick(self, event):
        matricule_item = self.view.tableView.selectedItems()[0].text()
        action = MenuAction(self)
        menu = RoundMenu(parent=self.view)
        menu.addAction(Action(FluentIcon.FOLDER, 'Voir', triggered = lambda:action.show(matricule_item)))
        menu.addAction(Action(FluentIcon.EDIT, 'Modifier', triggered = lambda: action.update(matricule_item)))
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.SCROLL, 'Mouvement'))
        menu.addSeparator()
        menu.addAction(Action(FluentIcon.DELETE, 'Supprimer', triggered = lambda: action.delete(matricule_item)))
        menu.menuActions()[-2].setCheckable(True)
        menu.menuActions()[-2].setChecked(True)

        self.posCur = QCursor().pos()
        cur_x = self.posCur.x()
        cur_y = self.posCur.y()

        menu.exec(QPoint(cur_x, cur_y), aniType=MenuAnimationType.FADE_IN_DROP_DOWN)
        
    def fetchData(self):
        data = self.model.fetch_items_by_id(self.promotion.id, order="matricule ASC")
        self.view.tableView.setData(self.formatDataForTable(data))
        
    def formatDataForTable(self, data):
        listStudent = []
        for student in data:
            listStudent.append([
                student.matricule, student.level, student.lastname,
                student.firstname, student.gender
            ])
        return listStudent
        
    def searchStudent(self, text):
        data = self.model.search_with_id(self.promotion.id, matricule=text, firstname=text)
        self.view.tableView.setData(self.formatDataForTable(data))
    
    def importData(self):
        filename = self.func.importFile(self.view, "Importer base de données", "CSV File (*.csv)")
        if filename:
            with open(filename, "r") as data:
                listStudent = []
                for line in data:
                    items = line.strip().split(";")
                    matricule = items[0]
                    level = items[1]
                    '''FOR PROMOTION SANDRATRA
                    level = "EAP"
                    if matricule.find("11") == 0 or \
                        matricule.find("12") == 0 or \
                        matricule.find("21") == 0 or \
                        matricule.find("31") == 0:
                        level = "EIP" '''
                    name = items[2].split(" ")
                    lastname = name[0]
                    firstname = ' '.join([val for val in name[1:]]) if len(name) > 1 else ""
                    genre = items[3]
                    listStudent.append(Student(
                        promotion_id=self.promotion.id,
                        lastname=lastname,
                        firstname=firstname,
                        gender=genre,
                        level=level,
                        matricule=matricule,
                        company=matricule[0],
                        section=matricule[1],
                        number=matricule[2:4]
                    ))
                self.model.create_multiple(listStudent)
                self.fetchData()
                
class MenuAction:
    
    def __init__(self,presenter:Student) -> None:
        self.model = presenter.model
        self.view = presenter.view
        self.presenter = presenter
        
    def show(self, matricule):
        dialog = ShowStudentDialog(self.view)
        dialog.show()
        
    def delete(self, matricule):
        dialog = MessageBox(f"Supprimer", "Vous êtes sûr de vouloir supprimer?", self.view.parent.mainWindow)
        dialog.yesButton.setText("Oui")
        dialog.cancelButton.setText("Non")
        if dialog.exec():
            self.model.delete_by(promotion_id=self.presenter.promotion.id, matricule=matricule)
            self.fetchData()
            self.presenter.func.toastSuccess("Supprimé", "Suppression avec réussite", self.view.parent)
            
    def fetchData(self):
        text = self.view.searchLineEdit.text()
        if len(text) != 0:
            self.presenter.searchStudent(text)
        else:
            self.presenter.fetchData()
            
    def update(self, matricule):
        oldStudent = self.model.fetch_item_by_cols(promotion_id=self.presenter.promotion.id, matricule=matricule)
        dialog = NewStudentDialog(self.view.parent)
        dialog.lastnameEdit.lineEdit(0).setText(oldStudent.lastname)
        dialog.firstnameEdit.lineEdit(0).setText(oldStudent.firstname)
        dialog.matriculeEdit.lineEdit(0).setText(str(oldStudent.matricule))
        if oldStudent.gender == "F":
            dialog.genderEdit.combox.setCurrentIndex(1)
        if oldStudent.level == "EAP":
            dialog.gradeEdit.combox.setCurrentIndex(1)
            
        dialog.yesButton.setEnabled(True)
        dialog.yesButton.setText("Mettre à jour")
        if dialog.exec():
            student = self.presenter.dataStudentFromDialog(dialog)
            self.model.update_item(oldStudent.id, 
                              lastname=student.lastname, 
                              firstname=student.firstname,
                              gender=student.gender,
                              level=student.level,
                              matricule=student.matricule,
                              company=student.company,
                              section=student.section,
                              number=student.number)
            self.fetchData()
            self.presenter.func.toastSuccess("Mise à jour", "Mise à jour d'élève avec réussite!", self.view.parent)
       