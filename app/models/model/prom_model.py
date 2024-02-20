from ..entity.promotion import Promotion
from .base_model import Model
from .student_model import StudentModel
from .move_model import MouvementModel

class PromotionModel(Model):
    def __init__(self):
        super().__init__("promotions", Promotion())
        self.model_student = StudentModel()
        self.move_model = MouvementModel()
        
    def delete_item(self, item_id):
        self.model_student.delete_with_cond(promotion_id=item_id)
        self.move_model.delete_with_cond(promotion_id=item_id)
        return super().delete_item(item_id)
    
    def delete_all_student(self, item_id):
        self.model_student.delete_with_cond(promotion_id=item_id)
        self.move_model.delete_with_cond(promotion_id=item_id)