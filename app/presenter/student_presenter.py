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
        data = self.model.search(matricule=text, firstname=text)
        self.view.tableView.setData(self.formatDataForTable(data))
        
        
