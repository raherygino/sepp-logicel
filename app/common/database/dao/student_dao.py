# coding:utf-8
from typing import List

from app.common.database.entity import Entity

from .dao_base import DaoBase
from ..entity import Student
import dataclasses


class StudentDao(DaoBase):
    """ Student information DAO """

    table = 'tbl_student'
    fields = [f'{field.name}' for field in dataclasses.fields(Student())]

    def createTable(self):
        return super().createTable(Student())
    
    
