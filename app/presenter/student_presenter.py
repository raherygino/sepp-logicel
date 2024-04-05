from ..models import StudentModel, Student, DatabaseWorker
from ..view.students import AddStudentInterface, ListStudentInterface, ImportDialog
from PyQt5.QtCore import QThread, QTimer
from ..common.constant import col
from ..common.functions import Function
from qfluentwidgets import MessageDialog

class StudentPresenter:
    
    def __init__(self, addView:AddStudentInterface, listView:ListStudentInterface, model: StudentModel):
        self.func = Function()
        self.addview = addView
        self.listView = listView
        self.mainView = self.listView.parent
        self.model = model
        self.promotion_id = 0
        self.timer = QTimer()
        self.__initTable()
        self.__actions()
        self.__workerThread()
        
    def __workerThread(self):
        
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.searchStudent)
        self.worker_thread = QThread()
        self.worker = DatabaseWorker(self.model.fetch_all(promotion_id=self.promotion_id))
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.handle_result)
        self.worker.finished.connect(self.worker_thread.quit)
        
    def __initTable(self):
        labels = ["Matricule", "Grade", "Nom et prénoms", "Sexe", "Date de naissance", "Lieu de naissance", "CIN", ""]
        self.listView.tableView.setHorizontalHeaderLabels(labels)
        
    def __actions(self):
        self.addview.btnAdd.clicked.connect(lambda: self.addStudent())
        self.listView.importAction.triggered.connect(self.importData)
        self.listView.deleteAction.triggered.connect(self.confirmDelete)
        self.listView.searchLineEdit.textChanged.connect(self.onQueryChanged)
        self.mainView.homeInterface.current_prom.connect(lambda value: self.setIdPromotion(value))
    
    def setIdPromotion(self, val):
        self.promotion_id = val
        self.fetchData()
        
    def update_progress(self, progress):
        self.listView.progressBar.setValue(int(progress))
        #self.progress_label.setText(f"{}%")
        
    def handle_result(self, data:list[Student]):
        self.listView.progressBar.setVisible(False)
        listData = []
        listData.clear()
        for student in data:
            listData.append([student.matricule, student.grade, student.name, student.genre, student.birthday, student.birthplace])
            
        self.listView.tableView.setData(listData)
        self.listView.progressBar.setValue(0)
        self.worker_thread.quit()
        
    def valueOf(self, **kwargs):
        keyEdit = "lineEdit"
        keyCombox = "combox"
        prefix = "self.addview."
        if keyEdit in kwargs:
            stringVal = f"{prefix}{kwargs.get(keyEdit)}.{keyEdit}.text()"
        if keyCombox in kwargs:
            stringVal = f"{prefix}{kwargs.get(keyCombox)}.{keyCombox}.currentText()"
        return eval(stringVal)
    
    def comboxData(self, keyword, label):
        students = self.model.fetch_all(promotion_id=self.promotion_id, group=keyword)
        dataVal = []
        dataLabel = []
        for i, student in enumerate(students):
            dataVal.append(student.get(keyword))
            dataLabel.append(f"{student.get(keyword)} {"ère" if i == 0 else "ème"} {label}")
        return {
            "data": dataVal,
            "label": dataLabel
        }   
    
    def fetchData(self):
        self.listView.progressBar.setVisible(True)
        self.companies = self.comboxData("company", "Companie")
        self.sections = self.comboxData("section", "Section")
        self.listView.comboBoxCompany.clear()
        self.listView.comboBoxCompany.addItems(self.companies.get("label"))
        self.listView.comboBoxSection.clear()
        self.listView.comboBoxSection.addItems(self.sections.get("label"))
        self.setData(self.model.fetch_all(promotion_id=self.promotion_id))
        
    def setData(self, data):
        self.worker.setData(data)
        self.worker_thread.start()
        
    
    def onQueryChanged(self, text):
        # Restart the timer whenever text is changed
        self.listView.progressBar.setVisible(True)
        self.timer.start()
        
    def searchStudent(self):
        self.timer.stop()
        text = self.listView.searchLineEdit.text()
        self.setData(self.model.search("promotion", self.promotion_id, name=text, matricule=text))
        
    def importData(self):
        
        filename = self.func.importFile(self.mainView, "Importer base de données", "CSV File (*.csv)")
        if filename:
            with open(filename, "r") as data:
                listStudent = []
                firstdata = []
                all_item = []
                keys = []
                for key in col.keys():
                    keys.append(key)
                for i, line in enumerate(data):
                    if i == 0:
                        firstdata = line.split(";")
                    else:
                        items = line.strip().split(";")
                        all_item.append(items)
                dialog = ImportDialog(firstdata, Student(), self.mainView)
                if dialog.exec():
                    valCombox = []
                    index_combox = []
                    for i, comb in enumerate(dialog.combox):
                        index = comb.currentIndex() - 1
                        if index != -1:
                            valCombox.append(keys[index])
                        else:
                            valCombox.append('-')
                        index_combox.append(i)
                    for item in all_item:
                        entity = {"promotion_id" : self.promotion_id}
                        for i, val_combox in enumerate(valCombox):
                            if val_combox != "-":
                                if i < len(item):
                                    val = item[index_combox[i]]
                                    entity[val_combox] = val
                                    if val_combox == "matricule":
                                        if len(val) == 4:
                                            entity['company'] = val[0]
                                            entity['section'] = val[1]
                                            entity['number'] = val[2:]
                        if len(entity.keys()) > 1:
                            listStudent.append(Student(**entity))
                    if len(listStudent) > 0:
                        self.model.create_multiple(listStudent)
                        self.fetchData()
        
    def addStudent(self):
        name = self.valueOf(lineEdit="name")
        im = self.valueOf(lineEdit="im")
        matricule = self.valueOf(lineEdit="matricule")
        grade = self.valueOf(lineEdit="grade")
        matricule = self.valueOf(lineEdit="matricule")
        genre = self.valueOf(combox="genre")
        height = self.valueOf(lineEdit="nHeight")
        blood = self.valueOf(lineEdit="blood")
        birthday = self.valueOf(lineEdit="birthday")
        birthplace = self.valueOf(lineEdit="birthplace")
        name_father = self.valueOf(lineEdit="nameFather")
        job_father = self.valueOf(lineEdit="jobFather")
        name_mother = self.valueOf(lineEdit="nameMother")
        job_mother = self.valueOf(lineEdit="jobMother")
        cin = self.valueOf(lineEdit="numberCin")
        date_cin = self.valueOf(lineEdit="dateCin")
        place_cin = self.valueOf(lineEdit="placeCin")
        region_origin = self.valueOf(lineEdit="regionOrigin")
        ethnie = self.valueOf(lineEdit="ethnie")
        address = self.valueOf(lineEdit="address")
        phone = self.valueOf(lineEdit="phone")
        email = self.valueOf(lineEdit="email")
        phone2 = self.valueOf(lineEdit="contactEmergency")
        
        student = Student(
            promotion_id= self.promotion_id,
            name=name, im=im, matricule=matricule,
            grade=grade, genre=genre, height=height,
            blood=blood, birthday=birthday, birthplace=birthplace,
            name_father=name_father, job_father=job_father,
            name_mother=name_mother, job_mother=job_mother, cin=cin,
            date_cin=date_cin, place_cin=place_cin, 
            region_origin=region_origin, ethnie=ethnie, address=address, 
            phone=phone, email=email, phone2=phone2
        )
        
        self.model.create(student)
        self.fetchData()
        
    def confirmDelete(self):
        dialog = MessageDialog("Supprimer", "Voulez-vous tous supprimer?", self.mainView)
        dialog.yesButton.clicked.connect(self.deleteAll)
        dialog.exec()
        
    def deleteAll(self):
        self.model.delete(promotion_id=self.promotion_id)
        self.fetchData()
        