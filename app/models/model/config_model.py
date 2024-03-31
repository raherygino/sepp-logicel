
from ..entity.configuration import Configuration
from .base_model import Model

class ConfigModel(Model):
    def __init__(self):
        super().__init__("configuration", Configuration())