from ..entity import Mouvement
from .base_model import Model

class MouvementModel(Model):
    def __init__(self):
        super().__init__("mouvements", Mouvement())