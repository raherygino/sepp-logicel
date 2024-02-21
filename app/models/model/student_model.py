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
    
    def delete_by_matricule(self, promotion_id, matricule):
        student = self.fetch_items_by_cond(promotion_id=promotion_id, matricule=matricule)[0]
        self.move_model.delete_with_cond(idStudent=student.id)
        return super().delete_by(promotion_id=promotion_id, matricule=matricule)