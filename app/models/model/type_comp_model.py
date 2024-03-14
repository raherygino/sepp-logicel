from ..entity import TypeComportement
from .base_model import Model

class TypeComportementModel(Model):
    def __init__(self):
        super().__init__("type_comportements", TypeComportement())
        self.seed()
        
    def seed(self):
        data = ["Suspendu de progression", "Sanction", "Remarque positive"]
        for val in data:
            if len(self.fetch_items_by_cond(name=val)) == 0:
                self.create(TypeComportement(promotion_id=0, name=val))