# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Student(Entity):
    """Student information """
    id: int = 0
    promotion_id: int = 0
    lastname: str = ""
    firstname: str = ""
    gender: str = ""
    level: str = ""
    company: int = 0
    section: int = 0
    number: int = 0
    matricule: int = 0