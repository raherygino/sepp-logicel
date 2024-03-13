# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class SubComportement(Entity):
    id: int = 0
    comportemen_comportement : int = 0
    name: str = ""
    abrv: str = ""