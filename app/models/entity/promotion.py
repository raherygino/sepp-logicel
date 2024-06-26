# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Promotion(Entity):
    """Promotion information """
    id: int = 0
    name: str = ""
    rank: int = 0
    years: str = ""
    logo: str = ""