from ..models import StudentModel, Student 
from ..common import Function
from ..view import StudentInterface

class StudentPresenter:

    def __init__(self, view:StudentInterface, model: StudentModel):
        self.view = view
        self.model = model
        self.func = Function()