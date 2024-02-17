# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Mouvement(Entity):

    idStudent: str = None
    type: str = None
    subType: str = None
    date: str = None
    day: str = None