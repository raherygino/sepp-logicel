from .Controller import Controller
from ..models.Student import Student
from ..models.keys import *

class StudentController(Controller):

    def __init__(self):
        self.student = Student(None,None,None,None,None,None,None,None,None,None,None,None,None)
        self.label = STUDENT_TABLE_LABEL
        self.cols = STUDENT_TABLE_COLS
        super().__init__(self.student, self.cols)

    def seed(self, count:int):
        self.student.seeds(count)

