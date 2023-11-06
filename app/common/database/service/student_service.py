# coding:utf-8
from typing import List

from PyQt5.QtSql import QSqlDatabase

from ..dao import StudentDao
from ..entity import Student

from.service_base import ServiceBase


class StudentService(ServiceBase):
    """ Song information service """

    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.studentDao = StudentDao(db)

    def createTable(self) -> bool:
        return self.studentDao.createTable()
    
    def listAll(self) -> List[Student]:
        return self.studentDao.listAll()
    
    def create(self, student:Student):
        return self.studentDao.create(student)
    
    def deleteById(self, id:int):
        return self.studentDao.deleteById(id)
    
    def findById(self, id:int):
        return self.studentDao.listByIds([id])[0]
    
    def update(self, id:int, student:Student):
        return self.studentDao.update(id, student)
    
    def search(self, value:str):
        return self.studentDao.search(value)

    