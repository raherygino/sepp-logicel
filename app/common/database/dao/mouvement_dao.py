# coding:utf-8
from typing import List

from app.common.database.entity import Entity

from .dao_base import DaoBase
from ..entity import Mouvement
import dataclasses


class MouvementDao(DaoBase):
    """ Student information DAO """

    table = 'tbl_mouvement'
    fields = [f'{field.name}' for field in dataclasses.fields(Mouvement())]

    def createTable(self):
        return super().createTable(Mouvement())
    
    
