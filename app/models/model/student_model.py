from .model import Model
from ..entity import Student
from .model import Model

class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())