# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Comportement(Entity):
    id: int = 0
    promotion_id: int = 0
    name: str = ""
    abrv: str = ""
    comp_type: str = 0