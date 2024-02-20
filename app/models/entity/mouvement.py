# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Mouvement(Entity):
    id: int = 0
    idStudent: str = None
    promotion_id: int = 0
    type: str = None
    subType: str = None
    date: str = None
    day: str = None