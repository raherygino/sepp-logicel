from .Controller import Controller
from ..models.Student import Student

class StudentController(Controller):

    def __init__(self):
        self.student = Student(None,None,None,None,None,None,None,None,None,None,None,None,None)
        self.label = ['ID', 'Nom', 'prénom', 'Compagnie', 'Section', 'Numéro', 'Niveau']
        self.cols = ['id_student', 'lastname', 'firstname', 'company', 'section', 'number', 'level']
        super().__init__(self.student, self.cols)


