# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Promotion(Entity):
    """Promotion information """
    id: int = 0
    name: str = None
    rank: str = None
    years: str = None