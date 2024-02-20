from ..entity import Student
from .base_model import Model
from .move_model import MouvementModel

class StudentModel(Model):
    def __init__(self):
        super().__init__("students", Student())
        self.move_model = MouvementModel()
    
    def delete_item(self, item_id):
        self.move_model.delete_with_cond(idStudent=item_id)
        return super().delete_item(item_id)