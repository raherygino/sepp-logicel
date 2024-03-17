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
    birthday: str = ""
    birthplace: str = ""
    city_origin: str = ""
    region_origin: str = ""
    city: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    father_name: str = ""
    mother_name: str = ""
    diplome_max: str = ""
    speciality: str = ""
    level: str = ""
    company: int = 0
    section: int = 0
    number: int = 0
    matricule: int = 0