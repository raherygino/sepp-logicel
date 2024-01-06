# coding:utf-8
from typing import List

from PyQt5.QtSql import QSqlDatabase

from ..dao import StudentDao,MouvementDao
from ..entity import Student

from.service_base import ServiceBase


class StudentService(ServiceBase):
    """ Song information service """

    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.studentDao = StudentDao(db)
        self.moveDao = MouvementDao(db)

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
    
    def countTypeMove(self, idStudent, type):
        countType = len(self.moveDao.listByConditions(idStudent = idStudent, type = type))
        if countType == 0:
            return ""
        else:
            return countType
    
    def countSubTypeMove(self, idStudent,subType):
        countSubType = len(self.moveDao.listByConditions(idStudent = idStudent, subType = subType))
        if countSubType == 0:
            return ""
        else:
            return countSubType
    
    def sumOfDayTypeMove(self, idStudent, type):
        return self.moveDao.sumColumn("day", idStudent=idStudent, type=type)
    
    def sumOfDaySubTypeMove(self, idStudent, subType):
        return self.moveDao.sumColumn("day", idStudent=idStudent, subType=subType)

    