# coding:utf-8
from .entity import Entity
from dataclasses import dataclass

@dataclass
class Student(Entity):
    """ Student information """

    lastname: str = None
    firstname: str = None
    gender: str = None
    birthday: str = None
    birthplace: str = None
    address: str = None
    phone: str = None