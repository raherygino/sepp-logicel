from .Controller import Controller
from ..models.Student import Student

class StudentController(Controller):

    def __init__(self, student: Student):
        if student == None:
            self.student = Student(None,None,None,None,None,None,None,
                                   None,None,None,None,None,None)
        else:
            self.student = student

    def create(self):
        self.student.create()

    def findById(self, id):
        return self.student.fetchById(id)

