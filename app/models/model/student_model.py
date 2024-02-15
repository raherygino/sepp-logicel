from ..entity import Student
from .base_model import Model

class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())