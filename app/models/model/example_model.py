from .model import Model
from ..entity import Example
from .base_model import Model

class ExampleModel(Model):
    def __init__(self):
        super().__init__("examples", Example())