from ..entity import Comportement
from .base_model import Model

class ComportementModel(Model):
    def __init__(self):
        super().__init__("comportements", Comportement())