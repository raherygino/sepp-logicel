from ..models import StudentModel, Student, DatabaseWorker
from ..view.students import AddStudentInterface, ListStudentInterface
from PyQt5.QtCore import QThread

class StudentPresenter:
    
    def __init__(self, addView:AddStudentInterface, listView:ListStudentInterface, model: StudentModel):
        self.addview = addView
        self.listView = listView
        self.mainView = self.listView.parent
        self.model = model
        self.promotion_id = 0
        self.__initTable()
        self.__actions()
        self.__workerThread()
        self.fetchData()
        
    def __workerThread(self):
        self.worker_thread = QThread()
        self.worker = DatabaseWorker(self.model.fetch_by_condition(promotion_id=self.promotion_id))
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
        self.listView.importAction.triggered.connect(self.fetchData)
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
    
    def fetchData(self):
        self.listView.progressBar.setVisible(True)
        self.worker.setData(self.model.fetch_by_condition(promotion_id=self.promotion_id))
        self.worker_thread.start()
        
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
        '''for i in range(1200):
            self.model.create(Student(promotion_id= self.promotion_id, name=f"Person {i}", matricule=f"{i+1}"))'''