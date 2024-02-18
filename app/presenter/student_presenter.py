from qfluentwidgets import RoundMenu, Action, FluentIcon, MenuAnimationType, MessageBox, Dialog
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QPoint, QThread, pyqtSignal
from PyQt5.QtWidgets import QLineEdit
from ..models import StudentModel, Student, MouvementModel, Mouvement
from ..common import Function
from ..components import TableView
from ..view.students.list_student_tab import ListStudent
from ..view.students.new_student_dialog import NewStudentDialog
from ..view.students.show_student_dialog import ShowStudentDialog
from ..view.students.new_movement_dialog import NewMouvementDialog


class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, data, model, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.data = data
        self.model = model
        self.listStudent = []

    def run(self):
        
        permission = NewMouvementDialog.typesMove[0]
        rm = NewMouvementDialog.typesMove[1]
        exant = NewMouvementDialog.subType[0][1]
        anm = NewMouvementDialog.typesMove[3]
        codis = NewMouvementDialog.subType[1][0]
        horsTour = NewMouvementDialog.subType[1][1]
        bemolenge = NewMouvementDialog.subType[1][2]
        pertEfPol = NewMouvementDialog.subType[1][3]
        sanc_disc = NewMouvementDialog.typesMove[2]
        other = NewMouvementDialog.subType[1][4]
        lettreFel = NewMouvementDialog.subType[2][0]
        remarkPos = NewMouvementDialog.typesMove[4]
        for i, student in enumerate(self.data):
            if i < 10:
                self.msleep(100)
            else:
                self.msleep(0)
            #rmVal = self.model.sum_by_with_id(student.id,"day",type=rm)
            '''exantVal = self.model.sum_by_with_id(student.id,"day", subType=exant)
            permissionVal = self.model.sum_by_with_id(student.id,"day",type=permission)
            anmVal = self.model.sum_by_with_id(student.id,"day",type=anm)
            codisVal = self.model.count_by_with_id(student.id, subType=codis)
            horsTourVal = self.model.sum_by_with_id(student.id,"day",subType=horsTour)
            bemolengeVal = self.model.count_by_with_id(student.id ,subType=bemolenge)
            pertEfPolVal = self.model.count_by_with_id(student.id, subType=pertEfPol)
            other_sanct = self.model.count_by_with_id(student.id, type=sanc_disc, subType=other)
            lettreFelVal = self.model.count_by_with_id(student.id, subType=lettreFel)
            remarkPosVal = self.model.count_by_with_id(student.id, type=remarkPos, subType=other)'''
            self.listStudent.append([
                student.matricule, student.level, student.lastname,
                student.firstname, student.gender,
                "","","","","",
                "","" , "","",
                "",""])
            progress = int((i + 1) / len(self.data) * 100)
            self.update_progress.emit(progress)
        #return listStudent
        
        # Update progress bar and emit signals
        '''for i, row in enumerate(self.data):
            # Simulate processing delay
            self.msleep(0)
            progress = int((i + 1) / len(self.data) * 100)
            self.update_progress.emit(progress)
            print(progress)'''

        self.finished.emit()


class StudentPresenter:
    
    HEADER_LABEL = ["Matricule", "Grade", "Nom", "Prénom(s)", "Genre",
                    "Repos médical ou convalescence (Jour)", "Exant d'effort physique (Jour)",
                    "Permission (Jour)", "CODIS (Fois)", "Bomelenge (Fois)", "Hours Tours",
                    "Perte Effet policier","Autre Sanction disciplinaire (fois)",
                    "Absent non motivé (Jour)", "Lettre de félicitation", 
                    "Autre remarque positive (fois)"]
    
    def __init__(self, view:ListStudent, model: StudentModel, promotion):
        self.view = view
        self.model = model
        self.modelMove = MouvementModel()
        self.promotion = promotion
        self.func = Function()
        self.view.tableView.setHorizontalHeaderLabels(self.HEADER_LABEL)
        self.__init_combox_data()
        self.actions()
        self.fetchData()
        '''self.thread = model.test_thread()
        self.thread.update_progress.connect(print)
        self.thread.finished.connect(lambda: print("ok"))
        self.thread.start()'''
    
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
        menu.addAction(Action(FluentIcon.SCROLL, 'Mouvement', triggered = lambda: action.mouvement(matricule_item)))
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
        #self.view.tableView.setData(self.formatDataForTable(data))
        
        self.worker_thread = WorkerThread(data, self.modelMove)
        self.worker_thread.update_progress.connect(self.update_progress_bar)
        self.worker_thread.finished.connect(self.worker_thread_finished)
        self.worker_thread.start()
        
    def update_progress_bar(self, value):
        self.view.progressBar.setValue(value)
        
    def worker_thread_finished(self):
        self.view.progressBar.setValue(0)
        self.view.tableView.setData(self.worker_thread.listStudent)
        
    def formatDataForTable(self, data):
        listStudent = []
        permission = NewMouvementDialog.typesMove[0]
        rm = NewMouvementDialog.typesMove[1]
        exant = NewMouvementDialog.subType[0][1]
        anm = NewMouvementDialog.typesMove[3]
        codis = NewMouvementDialog.subType[1][0]
        horsTour = NewMouvementDialog.subType[1][1]
        bemolenge = NewMouvementDialog.subType[1][2]
        pertEfPol = NewMouvementDialog.subType[1][3]
        sanc_disc = NewMouvementDialog.typesMove[2]
        other = NewMouvementDialog.subType[1][4]
        lettreFel = NewMouvementDialog.subType[2][0]
        remarkPos = NewMouvementDialog.typesMove[4]
        for student in data:
            rmVal = self.modelMove.sum_by_with_id(student.id,"day",type=rm)
            exantVal = self.modelMove.sum_by_with_id(student.id,"day", subType=exant)
            permissionVal = self.modelMove.sum_by_with_id(student.id,"day",type=permission)
            anmVal = self.modelMove.sum_by_with_id(student.id,"day",type=anm)
            codisVal = self.modelMove.count_by_with_id(student.id, subType=codis)
            horsTourVal = self.modelMove.sum_by_with_id(student.id,"day",subType=horsTour)
            bemolengeVal = self.modelMove.count_by_with_id(student.id ,subType=bemolenge)
            pertEfPolVal = self.modelMove.count_by_with_id(student.id, subType=pertEfPol)
            other_sanct = self.modelMove.count_by_with_id(student.id, type=sanc_disc, subType=other)
            lettreFelVal = self.modelMove.count_by_with_id(student.id, subType=lettreFel)
            remarkPosVal = self.modelMove.count_by_with_id(student.id, type=remarkPos, subType=other)
            listStudent.append([
                student.matricule, student.level, student.lastname,
                student.firstname, student.gender,
                rmVal,exantVal,permissionVal,codisVal,bemolengeVal,
                horsTourVal,pertEfPolVal , other_sanct,anmVal,
                lettreFelVal,remarkPosVal])
        return listStudent
        
    def searchStudent(self, text):
        data = self.model.search_with_id(self.promotion.id, matricule=text, firstname=text, lastname=text)
        #self.view.tableView.setData(self.formatDataForTable(data))
        self.worker_thread = WorkerThread(data, self.modelMove)
        self.worker_thread.update_progress.connect(self.update_progress_bar)
        self.worker_thread.finished.connect(self.worker_thread_finished)
        self.worker_thread.start()
    
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
        
    def dataStudent(self, matricule):
        return self.model.fetch_item_by_cols(promotion_id=self.presenter.promotion.id, matricule=matricule)
       
    def show(self, matricule):
        student = self.dataStudent(matricule)
        dataStudent = f'{student.level} {student.matricule}\n{student.lastname} {student.firstname}'
        mouvements = self.presenter.modelMove.fetch_items_by_id(student.id)
        dataMouvements = []
        for mouvement in mouvements:
            dataMouvements.append([
                mouvement.date,
                f'{mouvement.type} {mouvement.subType}',
                mouvement.day
            ])
        dialog = ShowStudentDialog(self.view.parent.mainWindow)
        dialog.label.setText(dataStudent)
        if len(dataMouvements) > 0:
            total = int(self.presenter.modelMove.sum_by_with_id(student.id, "day"))
            if total > 0:
                dataMouvements.append(["Total", "", total])
            dialog.ImageMessage.setVisible(False)
            dialog.message.setVisible(False)
            dialog.table.setVisible(True)
            dialog.table.setData(dataMouvements)
        else:
            dialog.ImageMessage.setVisible(True)
            dialog.message.setVisible(True)
            dialog.table.setVisible(False)
            
        dialog.exec()
        
    def mouvement(self, matricule):
        student = self.dataStudent(matricule)
        dialog = NewMouvementDialog(self.view.parent)
        dialog.subTitle.setText(f'{student.level} {student.lastname} {student.firstname}')
        if dialog.exec():
            mouvement = Mouvement(
                0,
                student.id,
                dialog.typeEdit.combox.text(),
                dialog.subTypeEdit.combox.text(),
                dialog.dateEdit.date.text(),
                dialog.dayMove.text())
            self.presenter.modelMove.create(mouvement)
            self.presenter.func.toastSuccess("Succès", "Ajout de mouvement de avec réussite", self.view.parent)
            self.fetchData()
         
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
       