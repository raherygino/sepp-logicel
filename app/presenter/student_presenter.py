from ..models import StudentModel, Student, DatabaseWorker
from ..view.students import AddStudentInterface, ListStudentInterface
from PyQt5.QtCore import QThread

class StudentPresenter:
    
    def __init__(self, addView:AddStudentInterface, listView:ListStudentInterface, model: StudentModel):
        self.addview = addView
        self.listView = listView
        self.model = model
        self.__workerThread()
        self.__actions()
        
    def __workerThread(self):
        self.worker_thread = QThread()
        self.worker = DatabaseWorker(self.model.fetch_all())
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.update_progress)
        self.worker.result.connect(self.handle_result)
        self.worker.finished.connect(self.worker_thread.quit)
        
    def __actions(self):
        self.addview.btnAdd.clicked.connect(lambda: self.addStudent())
        self.listView.importAction.triggered.connect(self.fetchData)
        
    def update_progress(self, progress):
        self.listView.progressBar.setValue(int(progress))
        #self.progress_label.setText(f"{}%")
        
    
    def handle_result(self, data:list[Student]):
        self.listView.progressBar.setVisible(False)
        self.listView.tableView.setHorizontalHeaderLabels(['Nom et prénoms', 'Matricule'])
        listData = []
        listData.clear()
        for student in data:
            listData.append([student.name, student.matricule])
            
        self.listView.tableView.setData(listData)
        self.listView.progressBar.setValue(0)
        self.worker_thread.quit()
        
    def valueOf(self, **kwargs):
        keyEdit = "lineEdit"
        keyCombox = "combox"
        if keyEdit in kwargs:
            stringVal = f"self.addview.{kwargs.get(keyEdit)}.lineEdit.text()"
        if keyCombox in kwargs:
            stringVal = f"self.addview.{kwargs.get(keyCombox)}.combox.currentText()"
        return eval(stringVal)
    
    def fetchData(self):
        self.listView.progressBar.setVisible(True)
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
        
        '''student = Student(
            name=name, im=im, matricule=matricule,
            grade=grade, genre=genre, height=height,
            blood=blood, birthday=birthday, birthplace=birthplace,
            name_father=name_father, job_father=job_father,
            name_mother=name_mother, job_mother=job_mother, cin=cin,
            date_cin=date_cin, place_cin=place_cin, 
            region_origin=region_origin, ethnie=ethnie, address=address, 
            phone=phone, email=email, phone2=phone2
        )'''
        
        #self.model.create(student)
        #for i in range(300):
            #self.model.create(Student(name=f"Person {i}", matricule=f"{i+1}"))