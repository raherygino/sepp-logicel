from ..entity.promotion import Promotion
from .base_model import Model

class PromotionModel(Model):
    def __init__(self):
        super().__init__("promotions", Promotion())