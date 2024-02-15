from ..models import StudentModel, Student 
from ..common import Function
from ..view.students.list_student_tab import ListStudent

class StudentPresenter:
    
    HEADER_LABEL = ["ID", "Matricule", "Grade", "Nom", "Prénom(s)"]
    '''"Genre",
                    "Repos médical ou convalescence (Jour)", "Exant d'effort physique (Jour)",
                    "Permission (Jour)", "CODIS (Fois)", "Bomelenge (Fois)", "Autre Sanction disciplinaire (fois)",
                    "Absent non motivé (Jour)", "Lettre de félicitation", "Autre remarque positive (fois)"]
    '''
    def __init__(self, view:ListStudent, model: StudentModel):
        self.view = view
        self.model = model
        self.func = Function()
        self.view.tableView.setHorizontalHeaderLabels(self.HEADER_LABEL)
        self.view.tableView.setData([["0", "2723", "EAP", "RAHERINOMENJANAHARY", "Georginot Armelin"]])