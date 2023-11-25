# coding:utf-8
from .entity import Entity
from dataclasses import dataclass

@dataclass
class Student(Entity):
    """ Student information """

    lastname: str = None
    firstname: str = None
    gender: str = None
    level: str = None
    company: str = None
    section: str = None
    number: str = None
    matricule: str = None