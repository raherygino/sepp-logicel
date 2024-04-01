# coding:utf-8
from .base_entity import Entity
from dataclasses import dataclass

@dataclass
class Student(Entity):
    id: int = 0
    promotion_id : int = 0
    name: str = ""
    im: str = ""
    matricule: str = ""
    grade: str = ""
    height: int = 0
    genre: str = ""
    blood: str = ""
    birthday: str = ""
    birthplace: str = ""
    name_father: str = ""
    job_father: str = ""
    name_mother: str = ""
    job_mother: str = ""
    cin: str = ""
    date_cin: str = ""
    place_cin: str = ""
    region_origin: str = ""
    ethnie: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    phone2: str = ""
    