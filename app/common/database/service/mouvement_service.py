# coding:utf-8
from typing import List

from PyQt5.QtSql import QSqlDatabase

from ..dao import MouvementDao
from ..entity import Mouvement

from.service_base import ServiceBase


class MouvementService(ServiceBase):
    """ Song information service """

    def __init__(self, db: QSqlDatabase = None):
        super().__init__()
        self.mouvementDao = MouvementDao(db)

    def createTable(self) -> bool:
        return self.mouvementDao.createTable()
    
    def create(self, mouvement:Mouvement):
        return self.mouvementDao.create(mouvement)
    
    def listByStudentId(self, idStudent) -> List[Mouvement]:
        return self.mouvementDao.listByField("idStudent", idStudent)
    
    def deleteById(self, id:int):
        return self.mouvementDao.deleteById(id)

    