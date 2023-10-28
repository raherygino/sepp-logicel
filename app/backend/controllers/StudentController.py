from .Controller import Controller
from ..models.Student import Student

class StudentController(Controller):

    def __init__(self, student: Student):
        self.student = student

    def create(self):
        self.student.create()

