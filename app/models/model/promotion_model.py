from .model import Model
from ..entity import Promotion
from .model import Model

class PromotionModel(Model):
    def __init__(self):
        super().__init__("promotions", Promotion())